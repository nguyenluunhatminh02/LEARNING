# Bài 06: Query Optimization

## 🎯 Mục tiêu
- Đọc EXPLAIN ANALYZE như expert
- Chiến lược tối ưu query
- Common performance pitfalls
- PostgreSQL tuning parameters

---

## 1. EXPLAIN ANALYZE Mastery

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.username, COUNT(p.id) AS post_count
FROM users u
JOIN posts p ON u.id = p.user_id
WHERE p.status = 'published' AND p.created_at > '2024-01-01'
GROUP BY u.id
ORDER BY post_count DESC
LIMIT 10;
```

### Các loại Scan/Join

```
SCAN TYPES (đọc data):
  Seq Scan           → đọc toàn bộ table (O(N))
  Index Scan         → B-Tree lookup → fetch row (O(log N))
  Index Only Scan    → đọc CHỈ từ index, skip table (fastest)
  Bitmap Index Scan  → index → bitmap → table (medium selectivity)

JOIN TYPES:
  Nested Loop   → cho mỗi row A, scan B → O(N×M) → tốt khi B nhỏ
  Hash Join     → build hash(B), probe A → O(N+M) → tốt khi B fit RAM
  Merge Join    → cả 2 sorted → merge → O(N+M) → tốt khi đã sorted

SORT:
  Sort: top-N heapsort → LIMIT nhỏ (fast)
  Sort: quicksort → general
  Sort: external merge → data > work_mem → chậm (dùng disk)
```

### Red Flags trong Query Plan
```
❌ Seq Scan on large table (>10K rows) → cần index
❌ Nested Loop on 2 large tables → force hash join hoặc thêm index
❌ Sort: external merge Disk → tăng work_mem
❌ Rows Removed by Filter: 99999 → index cover điều kiện này
❌ estimated rows vs actual rows sai lệch lớn → ANALYZE table
❌ Buffers: read >> shared hit → buffer pool nhỏ
```

---

## 2. Optimization Strategies

### Strategy 1: Add the Right Index
```sql
-- Before: Seq Scan (500ms)
EXPLAIN ANALYZE SELECT * FROM orders WHERE status = 'pending' AND created_at > '2024-01-01';

-- Add composite index
CREATE INDEX idx_orders_status_date ON orders(status, created_at);

-- After: Index Scan (2ms)
```

### Strategy 2: Rewrite Query
```sql
-- ❌ Slow: subquery executed per row
SELECT *, (SELECT COUNT(*) FROM posts WHERE user_id = u.id) AS cnt
FROM users u;

-- ✅ Fast: single join + aggregate
SELECT u.*, COALESCE(p.cnt, 0) AS cnt
FROM users u
LEFT JOIN (SELECT user_id, COUNT(*) AS cnt FROM posts GROUP BY user_id) p
ON u.id = p.user_id;
```

### Strategy 3: Avoid N+1 Queries
```python
# ❌ N+1 problem (101 queries for 100 users)
users = db.query("SELECT * FROM users LIMIT 100")
for user in users:
    posts = db.query("SELECT * FROM posts WHERE user_id = %s", user.id)

# ✅ 2 queries total
users = db.query("SELECT * FROM users LIMIT 100")
user_ids = [u.id for u in users]
posts = db.query("SELECT * FROM posts WHERE user_id = ANY(%s)", user_ids)
```

### Strategy 4: Pagination — Cursor vs Offset
```sql
-- ❌ Offset pagination (chậm cho page lớn)
SELECT * FROM posts ORDER BY created_at DESC LIMIT 20 OFFSET 100000;
-- DB phải đọc 100,020 rows rồi skip 100,000!

-- ✅ Cursor pagination  
SELECT * FROM posts 
WHERE created_at < '2024-01-15T10:30:00'  -- cursor from previous page
ORDER BY created_at DESC 
LIMIT 20;
-- Chỉ đọc 20 rows (nếu có index trên created_at)
```

### Strategy 5: Materialized View
```sql
-- Query phức tạp chạy thường xuyên → pre-compute
CREATE MATERIALIZED VIEW mv_user_stats AS
SELECT 
    u.id, u.username,
    COUNT(p.id) AS post_count,
    SUM(p.view_count) AS total_views,
    MAX(p.created_at) AS last_post_at
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id;

CREATE UNIQUE INDEX ON mv_user_stats(id);

-- Refresh (manual)
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_user_stats;
-- Schedule: cron job mỗi 5-15 phút
```

---

## 3. PostgreSQL Tuning

```sql
-- Memory
shared_buffers = '4GB'        -- 25% of RAM (buffer pool)
work_mem = '256MB'             -- per-operation sort/hash memory
effective_cache_size = '12GB'  -- 75% of RAM (OS + PG cache estimate)
maintenance_work_mem = '1GB'   -- for VACUUM, CREATE INDEX

-- Planner
random_page_cost = 1.1         -- SSD (default 4.0 for HDD)
effective_io_concurrency = 200 -- SSD

-- WAL
wal_buffers = '64MB'
checkpoint_completion_target = 0.9

-- Autovacuum (quan trọng!)
autovacuum_max_workers = 3
autovacuum_naptime = '1min'
```

---

## 4. Monitoring Slow Queries

```sql
-- Enable pg_stat_statements
CREATE EXTENSION pg_stat_statements;

-- Top 10 slowest queries
SELECT 
    calls,
    ROUND(total_exec_time::numeric, 2) AS total_ms,
    ROUND(mean_exec_time::numeric, 2) AS avg_ms,
    ROUND(max_exec_time::numeric, 2) AS max_ms,
    query
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Log slow queries
-- postgresql.conf:
-- log_min_duration_statement = 1000  -- log queries > 1s
```

---

## 📝 Bài tập

1. Tìm 5 slow queries trong app, optimize bằng index + rewrite
2. Convert offset pagination → cursor pagination
3. Tạo materialized view cho dashboard analytics
4. Tune PostgreSQL cho server 16GB RAM, SSD

---

## 📚 Tài liệu
- *SQL Performance Explained* — Markus Winand
- [pgMustard EXPLAIN Visualizer](https://www.pgmustard.com/)
- [PostgreSQL Wiki: Performance Tips](https://wiki.postgresql.org/wiki/Performance_Optimization)
