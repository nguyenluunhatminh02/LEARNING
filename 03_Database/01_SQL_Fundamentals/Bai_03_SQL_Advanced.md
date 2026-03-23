# Bài 03: SQL Advanced — Window Functions, CTE, EXPLAIN

## 🎯 Mục tiêu
- Window Functions (ROW_NUMBER, RANK, LAG, LEAD, SUM OVER)
- CTE (Common Table Expressions) & Recursive CTE
- EXPLAIN ANALYZE — đọc query plan

## 📖 Câu chuyện đời thường
> Bạn là giáo viên và cần xếp hạng học sinh trong lớp. **ROW_NUMBER** = đánh số thứ tự riêng cho từng lớp: lớp A có hạng 1-30, lớp B có hạng 1-30 (không trộn lẫn). **RANK** = xếp hạng cho phép đồng hạng: 2 người cung điểm thì cùng hạng 1, người tiếp theo là hạng 3. **LAG/LEAD** giống so sánh điểm tháng này với tháng trước: "bạn A tháng này 8 điểm, tháng trước 7 điểm → tiến bộ!". **EXPLAIN ANALYZE** giống như đặt camera theo dõi cách database tìm dữ liệu — để biết nó đang mất thời gian ở đâu và cải thiện.

---

## 1. Window Functions

```sql
-- Window Function = tính toán trên "window" (nhóm rows) 
-- KHÔNG collapse rows như GROUP BY

-- Syntax:
-- function() OVER (PARTITION BY col ORDER BY col ROWS BETWEEN ... AND ...)
```

### ROW_NUMBER, RANK, DENSE_RANK
```sql
SELECT 
    username, 
    post_count,
    ROW_NUMBER() OVER (ORDER BY post_count DESC) AS row_num,
    RANK()       OVER (ORDER BY post_count DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY post_count DESC) AS dense_rank
FROM user_stats;

-- post_count  row_num  rank  dense_rank
-- 100         1        1     1
-- 100         2        1     1          ← RANK: tie = same rank
-- 80          3        3     2          ← DENSE_RANK: no gap
-- 70          4        4     3
```

### Top-N per group
```sql
-- Top 3 bài viết nhiều views nhất của MỖI user
SELECT * FROM (
    SELECT 
        p.*,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY view_count DESC) AS rn
    FROM posts p
    WHERE status = 'published'
) ranked
WHERE rn <= 3;
```

### LAG, LEAD (access previous/next row)
```sql
-- So sánh doanh thu với tháng trước
SELECT 
    month,
    revenue,
    LAG(revenue, 1) OVER (ORDER BY month) AS prev_month_revenue,
    revenue - LAG(revenue, 1) OVER (ORDER BY month) AS growth,
    ROUND(
        (revenue - LAG(revenue, 1) OVER (ORDER BY month)) * 100.0 
        / LAG(revenue, 1) OVER (ORDER BY month), 2
    ) AS growth_pct
FROM monthly_revenue;

-- month    revenue   prev_month   growth   growth_pct
-- 2024-01  10000     NULL         NULL     NULL
-- 2024-02  12000     10000        2000     20.00
-- 2024-03  11000     12000        -1000    -8.33
```

### Running Total (SUM OVER)
```sql
-- Cumulative revenue
SELECT 
    date,
    daily_revenue,
    SUM(daily_revenue) OVER (ORDER BY date) AS cumulative_revenue,
    SUM(daily_revenue) OVER (
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS rolling_7day_revenue,
    AVG(daily_revenue) OVER (
        ORDER BY date 
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS moving_avg_7day
FROM daily_stats;
```

### FIRST_VALUE, LAST_VALUE, NTH_VALUE
```sql
SELECT 
    user_id,
    order_date,
    amount,
    FIRST_VALUE(amount) OVER (PARTITION BY user_id ORDER BY order_date) AS first_order,
    LAST_VALUE(amount) OVER (
        PARTITION BY user_id ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_order
FROM orders;
```

### NTILE (divide into buckets)
```sql
-- Chia users thành 4 nhóm theo spending
SELECT 
    user_id,
    total_spending,
    NTILE(4) OVER (ORDER BY total_spending DESC) AS quartile
FROM user_spending;
-- quartile 1 = top 25% spenders
```

---

## 2. CTE (Common Table Expressions)

```sql
-- WITH clause — tạo temporary named result set
-- Dễ đọc hơn subquery, có thể reuse

WITH active_users AS (
    SELECT id, username, email
    FROM users
    WHERE is_active = TRUE AND created_at > '2024-01-01'
),
user_posts AS (
    SELECT user_id, COUNT(*) AS post_count, SUM(view_count) AS total_views
    FROM posts
    WHERE status = 'published'
    GROUP BY user_id
)
SELECT 
    au.username,
    au.email,
    COALESCE(up.post_count, 0) AS post_count,
    COALESCE(up.total_views, 0) AS total_views
FROM active_users au
LEFT JOIN user_posts up ON au.id = up.user_id
ORDER BY total_views DESC;
```

### Recursive CTE
```sql
-- Org chart: tìm tất cả subordinates của manager
-- employees: (id, name, manager_id)

WITH RECURSIVE org_tree AS (
    -- Base case: top-level manager
    SELECT id, name, manager_id, 0 AS depth, name AS path
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: employees reporting to people already in tree
    SELECT e.id, e.name, e.manager_id, 
           ot.depth + 1,
           ot.path || ' > ' || e.name
    FROM employees e
    JOIN org_tree ot ON e.manager_id = ot.id
)
SELECT * FROM org_tree ORDER BY path;

-- Result:
-- CEO (depth 0)
--   CEO > VP Engineering (depth 1)
--     CEO > VP Engineering > Senior Dev (depth 2)
--       CEO > VP Engineering > Senior Dev > Junior Dev (depth 3)
```

```sql
-- Recursive: Generate date series
WITH RECURSIVE dates AS (
    SELECT DATE '2024-01-01' AS d
    UNION ALL
    SELECT d + INTERVAL '1 day'
    FROM dates
    WHERE d < DATE '2024-12-31'
)
SELECT d, EXTRACT(DOW FROM d) AS day_of_week
FROM dates;

-- Hoặc dùng generate_series (PostgreSQL built-in):
SELECT generate_series('2024-01-01'::date, '2024-12-31'::date, '1 day'::interval) AS d;
```

---

## 3. EXPLAIN ANALYZE — Query Plan

```sql
EXPLAIN ANALYZE
SELECT u.username, COUNT(p.id) AS post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.is_active = TRUE
GROUP BY u.id, u.username
ORDER BY post_count DESC
LIMIT 10;
```

### Đọc Query Plan
```
Limit  (cost=152.73..152.76 rows=10 width=44) (actual time=2.1..2.1 rows=10 loops=1)
  -> Sort  (cost=152.73..155.23 rows=1000 width=44) (actual time=2.0..2.1 rows=10 loops=1)
        Sort Key: (count(p.id)) DESC
        Sort Method: top-N heapsort  Memory: 25kB
        -> Hash Left Join  (cost=29.50..135.50 rows=1000 width=44) (actual time=0.5..1.8 rows=1000 loops=1)
              Hash Cond: (u.id = p.user_id)
              -> Seq Scan on users u  (cost=0.00..22.50 rows=1000 width=36) (actual time=0.01..0.1 rows=500 loops=1)
                    Filter: (is_active = true)
                    Rows Removed by Filter: 500
              -> Hash  (cost=17.00..17.00 rows=1000 width=8) (actual time=0.3..0.3 rows=1000 loops=1)
                    -> Seq Scan on posts p  (cost=0.00..17.00 rows=1000 width=8) (actual time=0.01..0.1 rows=1000 loops=1)
Planning Time: 0.2 ms
Execution Time: 2.2 ms
```

### Key Terms
```
Seq Scan:     Đọc toàn bộ bảng (slow cho bảng lớn)
Index Scan:   Đọc qua index (fast)
Index Only Scan: Đọc CHỈ từ index (fastest)
Bitmap Scan:  Index → bitmap → table (medium selectivity)
Hash Join:    Build hash table cho 1 bảng, probe từ bảng kia
Nested Loop:  Cho mỗi row bảng A, scan bảng B
Merge Join:   Cả 2 sorted → merge

cost=start..total: estimated cost
actual time: ms thực tế
rows: số rows processed
loops: lặp bao nhiêu lần
```

### Đọc & Tối ưu
```
❌ Seq Scan on large table → cần INDEX
❌ Nested Loop on large tables → consider Hash/Merge Join
❌ Rows Removed by Filter >> rows returned → index phù hợp
❌ Sort Method: external merge Disk → tăng work_mem

✅ Index Scan / Index Only Scan
✅ actual rows ≈ estimated rows (statistics chính xác)
✅ Execution time < 100ms cho common queries
```

---

## 4. Advanced SQL Patterns

### Pivoting (CROSSTAB)
```sql
-- Revenue by month as columns
SELECT 
    product_name,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 1 THEN amount ELSE 0 END) AS jan,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 2 THEN amount ELSE 0 END) AS feb,
    SUM(CASE WHEN EXTRACT(MONTH FROM order_date) = 3 THEN amount ELSE 0 END) AS mar
FROM order_items oi
JOIN products p ON oi.product_id = p.id
GROUP BY product_name;
```

### Gap and Island Problem
```sql
-- Tìm consecutive login days
WITH login_dates AS (
    SELECT user_id, login_date,
        login_date - INTERVAL '1 day' * ROW_NUMBER() OVER (
            PARTITION BY user_id ORDER BY login_date
        ) AS grp
    FROM user_logins
)
SELECT user_id, 
    MIN(login_date) AS streak_start,
    MAX(login_date) AS streak_end,
    COUNT(*) AS streak_length
FROM login_dates
GROUP BY user_id, grp
HAVING COUNT(*) >= 7  -- Streaks of 7+ days
ORDER BY streak_length DESC;
```

---

## 📝 Bài tập

1. Top 3 sản phẩm bán chạy nhất MỖI category (Window Function)
2. Tính growth rate doanh thu month-over-month (LAG)
3. Recursive CTE: tìm tất cả subcategories từ root category
4. EXPLAIN ANALYZE: tối ưu query chậm bằng cách thêm index

---

## 📚 Tài liệu
- *SQL Performance Explained* — Markus Winand
- [PostgreSQL EXPLAIN Visualizer](https://explain.dalibo.com/)
- [Window Functions Tutorial](https://www.postgresql.org/docs/current/tutorial-window.html)
