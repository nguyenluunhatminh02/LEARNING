# Bài 05: Indexing Deep Dive

## 🎯 Mục tiêu
- Hiểu tất cả loại index trong PostgreSQL
- Composite index, covering index
- Khi nào INDEX giúp, khi nào không
- Partial index, expression index

---

## 1. Tại sao cần Index?

```
Không index:
  SELECT * FROM users WHERE email = 'alice@email.com';
  → Seq Scan: đọc TẤT CẢ rows → O(N) → 1M rows = 1M comparisons

Có index on email:
  → Index Scan: B-Tree lookup → O(log N) → 1M rows = ~20 comparisons
  → 50,000x nhanh hơn!
```

---

## 2. Index Types

### B-Tree Index ⭐ (default)
```sql
CREATE INDEX idx_users_email ON users(email);

-- Hỗ trợ operators: =, <, >, <=, >=, BETWEEN, IN, IS NULL
-- Dùng cho: hầu hết trường hợp
-- ❌ Không hỗ trợ: LIKE '%abc' (prefix wildcard)
```

### Hash Index
```sql
CREATE INDEX idx_users_email_hash ON users USING hash(email);

-- Chỉ hỗ trợ: = (equality)
-- Nhỏ hơn B-Tree, nhanh hơn cho equality lookup
-- ❌ Không hỗ trợ: range queries, ORDER BY
```

### GIN (Generalized Inverted Index)
```sql
-- Full-text search
CREATE INDEX idx_posts_search ON posts USING gin(to_tsvector('english', title || ' ' || content));

SELECT * FROM posts 
WHERE to_tsvector('english', title || ' ' || content) @@ to_tsquery('database & optimization');

-- JSONB indexing
CREATE INDEX idx_data_gin ON products USING gin(metadata);

SELECT * FROM products WHERE metadata @> '{"color": "red"}';

-- Array indexing
CREATE INDEX idx_tags_gin ON posts USING gin(tags);

SELECT * FROM posts WHERE tags @> ARRAY['python', 'sql'];
```

### GiST (Generalized Search Tree)
```sql
-- Geometric / spatial data
CREATE INDEX idx_locations_gist ON stores USING gist(location);

-- Range types
CREATE INDEX idx_booking_range ON bookings USING gist(
    tstzrange(check_in, check_out)
);

-- Find overlapping bookings
SELECT * FROM bookings 
WHERE tstzrange(check_in, check_out) && 
      tstzrange('2024-03-01', '2024-03-05');
```

### BRIN (Block Range Index)
```sql
-- Cho data physically sorted (time-series, logs)
CREATE INDEX idx_logs_created ON logs USING brin(created_at);

-- Cực nhỏ: 1 entry per 128 pages (thay vì 1 entry per row)
-- Perfect cho: append-only tables (logs, events, time-series)
-- ❌ Không tốt nếu data insert random order
```

---

## 3. Composite Index (Multi-column)

```sql
CREATE INDEX idx_posts_user_status ON posts(user_id, status);

-- ✅ WHERE user_id = 1 AND status = 'published'    (cả 2 columns)
-- ✅ WHERE user_id = 1                               (leftmost prefix)
-- ❌ WHERE status = 'published'                       (không dùng được!)

-- Rule: Leftmost prefix phải có trong WHERE clause
-- ORDER matters: (A, B, C) dùng được cho A, AB, ABC — KHÔNG cho B, C, BC

-- Thứ tự columns:
-- 1. Equality conditions trước (=)
-- 2. Range conditions sau (<, >, BETWEEN)
-- 3. Columns dùng cho ORDER BY cuối

CREATE INDEX idx_orders_status_date ON orders(status, created_at DESC);
-- ✅ WHERE status = 'pending' ORDER BY created_at DESC → index-only sort
```

---

## 4. Covering Index (INCLUDE)

```sql
-- Problem: Index Scan → vẫn phải đọc table để lấy data columns
-- Solution: INCLUDE columns trong index → Index Only Scan

CREATE INDEX idx_posts_user_covering 
ON posts(user_id) 
INCLUDE (title, created_at);

-- Query này dùng Index Only Scan (không cần đọc table):
SELECT title, created_at FROM posts WHERE user_id = 1;
-- Tất cả data đã nằm trong index!
```

---

## 5. Partial Index

```sql
-- Index chỉ cho subset of rows → nhỏ hơn, nhanh hơn

CREATE INDEX idx_orders_pending 
ON orders(created_at) 
WHERE status = 'pending';

-- Chỉ index orders pending (5% of total)
-- Size: 20x nhỏ hơn full index
-- ✅ SELECT * FROM orders WHERE status = 'pending' ORDER BY created_at
```

---

## 6. Expression Index

```sql
-- Index trên biểu thức / function
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- ✅ WHERE LOWER(email) = 'alice@email.com'

CREATE INDEX idx_orders_month ON orders(DATE_TRUNC('month', created_at));

-- ✅ WHERE DATE_TRUNC('month', created_at) = '2024-01-01'
```

---

## 7. Index Anti-patterns

```sql
-- ❌ Over-indexing: mỗi INSERT/UPDATE phải update TẤT CẢ indexes
-- Rule: chỉ tạo index cho queries thực sự chạy thường xuyên

-- ❌ Index on low-cardinality column
CREATE INDEX idx_users_gender ON users(gender);  -- Chỉ M/F/Other
-- 3 distinct values / 1M rows = seq scan có thể nhanh hơn!

-- ❌ Function trên indexed column
WHERE UPPER(email) = 'ALICE@EMAIL.COM'  -- ❌ không dùng idx_email
WHERE email = LOWER('ALICE@EMAIL.COM')  -- ✅ dùng được index

-- ❌ Implicit type casting
WHERE id = '123'  -- id là INTEGER, '123' là TEXT → cast → skip index

-- ❌ OR conditions
WHERE email = 'a@b.com' OR phone = '123'  -- Cần 2 separate indexes

-- ✅ Monitor unused indexes
SELECT indexrelname, idx_scan 
FROM pg_stat_user_indexes 
WHERE idx_scan = 0 
ORDER BY pg_relation_size(indexrelid) DESC;
-- idx_scan = 0 → index chưa bao giờ dùng → DROP
```

---

## 8. Index Maintenance

```sql
-- Check index size
SELECT 
    indexname,
    pg_size_pretty(pg_relation_size(indexname::regclass)) AS size
FROM pg_indexes 
WHERE tablename = 'orders'
ORDER BY pg_relation_size(indexname::regclass) DESC;

-- Rebuild bloated index (concurrently — không lock table)
REINDEX INDEX CONCURRENTLY idx_orders_status;

-- Check index usage
SELECT 
    relname AS table,
    indexrelname AS index,
    idx_scan AS scans,
    idx_tup_read AS tuples_read,
    idx_tup_fetch AS tuples_fetched
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

---

## 📝 Bài tập

1. Tạo indexes tối ưu cho e-commerce queries: search products, filter by price/category, order history
2. So sánh performance trước/sau index bằng EXPLAIN ANALYZE
3. Tạo GIN index cho full-text search trên products
4. Tìm và DROP unused indexes trong database

---

## 📚 Tài liệu
- [Use The Index, Luke](https://use-the-index-luke.com/) ⭐
- *SQL Performance Explained* — Markus Winand
- [PostgreSQL Index Types](https://www.postgresql.org/docs/current/indexes-types.html)

## 🔗 Liên kết chéo
- → **System Design Bài 08: Database Scaling** — index strategies cho sharded databases
- → **DB Bài 06: Query Optimization** — sử dụng indexes trong query plan
- → **SE Bài 06: API Design** — database design ảnh hưởng API performance
