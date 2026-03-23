# Bài 02: SQL Intermediate — JOINs, Subqueries, Set Operations

## 🎯 Mục tiêu
- Master tất cả loại JOINs
- Subqueries (scalar, correlated, EXISTS)
- GROUP BY advanced, HAVING
- Set operations: UNION, INTERSECT, EXCEPT

## 📖 Câu chuyện đời thường
> Bạn có 2 danh sách: "Nhân viên" và "Phòng ban". **INNER JOIN** là ghép tên nhân viên với phòng ban của họ — ai chưa có phòng thì bỏ qua. **LEFT JOIN** là liệt kê TẤT CẢ nhân viên, ai chưa có phòng thì ghi "chưa xác định". **Subquery** giống như bạn hỏi: "Tìm nhân viên có lương cao hơn trung bình" — trước tiên phải tính trung bình (đó là subquery), rồi mới so sánh. **GROUP BY** giống như xếp nhân viên thành nhóm theo phòng ban rồi đếm: "Phòng kỹ thuật 10 người, phòng kinh doanh 8 người". **HAVING** là lọc tiếp: "chỉ hiển phòng có trên 5 người".

---

## 1. JOINs

### Sample Data
```sql
-- users: (1,'Alice'), (2,'Bob'), (3,'Charlie')
-- posts: (1,1,'Post A'), (2,1,'Post B'), (3,2,'Post C')
-- post_tags: (1,1), (1,2), (2,1), (3,3)
-- tags: (1,'python'), (2,'sql'), (3,'go'), (4,'rust')
```

### INNER JOIN
```sql
-- Chỉ lấy rows match ở CẢ HAI bảng
SELECT u.username, p.title
FROM users u
INNER JOIN posts p ON u.id = p.user_id;

-- Result:
-- Alice  | Post A
-- Alice  | Post B
-- Bob    | Post C
-- (Charlie không có posts → bị loại)
```

### LEFT JOIN (LEFT OUTER JOIN)
```sql
-- Lấy TẤT CẢ từ bảng trái, match từ bảng phải (NULL nếu không match)
SELECT u.username, p.title
FROM users u
LEFT JOIN posts p ON u.id = p.user_id;

-- Result:
-- Alice   | Post A
-- Alice   | Post B
-- Bob     | Post C
-- Charlie | NULL      ← Charlie vẫn xuất hiện
```

### RIGHT JOIN
```sql
-- Ngược của LEFT JOIN: lấy TẤT CẢ từ bảng phải
SELECT u.username, p.title
FROM users u
RIGHT JOIN posts p ON u.id = p.user_id;
-- Ít dùng, thường đổi thành LEFT JOIN cho dễ đọc
```

### FULL OUTER JOIN
```sql
-- Lấy TẤT CẢ từ CẢ HAI bảng
SELECT u.username, p.title
FROM users u
FULL OUTER JOIN posts p ON u.id = p.user_id;
-- Rows không match ở bên nào → NULL
```

### CROSS JOIN
```sql
-- Cartesian product: mỗi row bảng A × mỗi row bảng B
SELECT u.username, t.name
FROM users u
CROSS JOIN tags t;
-- 3 users × 4 tags = 12 rows
```

### SELF JOIN
```sql
-- Join bảng với chính nó
-- Ví dụ: tìm employees có cùng manager
SELECT e1.name AS employee, e2.name AS colleague
FROM employees e1
JOIN employees e2 ON e1.manager_id = e2.manager_id
WHERE e1.id != e2.id;
```

### Multi-table JOIN
```sql
-- Posts với tên user và tags
SELECT p.title, u.username, ARRAY_AGG(t.name) AS tags
FROM posts p
JOIN users u ON p.user_id = u.id
JOIN post_tags pt ON p.id = pt.post_id
JOIN tags t ON pt.tag_id = t.id
GROUP BY p.id, p.title, u.username;

-- Result:
-- Post A | Alice | {python, sql}
-- Post B | Alice | {python}
-- Post C | Bob   | {go}
```

---

## 2. Subqueries

### Scalar Subquery (trả về 1 value)
```sql
-- Users có nhiều posts hơn trung bình
SELECT username, 
       (SELECT COUNT(*) FROM posts WHERE user_id = u.id) AS post_count
FROM users u
WHERE (SELECT COUNT(*) FROM posts WHERE user_id = u.id) > 
      (SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM posts GROUP BY user_id) sub);
```

### Subquery trong WHERE
```sql
-- Users chưa có post nào
SELECT * FROM users 
WHERE id NOT IN (SELECT DISTINCT user_id FROM posts);

-- Posts từ users active
SELECT * FROM posts
WHERE user_id IN (SELECT id FROM users WHERE is_active = TRUE);
```

### EXISTS (efficient hơn IN cho large datasets)
```sql
-- Users có ít nhất 1 post published
SELECT u.*
FROM users u
WHERE EXISTS (
    SELECT 1 FROM posts p 
    WHERE p.user_id = u.id AND p.status = 'published'
);

-- Users KHÔNG có post nào
SELECT u.*
FROM users u
WHERE NOT EXISTS (
    SELECT 1 FROM posts p WHERE p.user_id = u.id
);
```

### Correlated Subquery
```sql
-- Post có view_count cao nhất của mỗi user
SELECT *
FROM posts p1
WHERE view_count = (
    SELECT MAX(view_count) 
    FROM posts p2 
    WHERE p2.user_id = p1.user_id
);
```

### Subquery trong FROM (Derived Table)
```sql
SELECT ranked.username, ranked.total_views
FROM (
    SELECT u.username, SUM(p.view_count) AS total_views,
           RANK() OVER (ORDER BY SUM(p.view_count) DESC) AS rank
    FROM users u
    JOIN posts p ON u.id = p.user_id
    GROUP BY u.id, u.username
) ranked
WHERE ranked.rank <= 3;
```

---

## 3. GROUP BY Advanced

```sql
-- Doanh thu theo tháng, theo category
SELECT 
    DATE_TRUNC('month', o.created_at) AS month,
    c.name AS category,
    COUNT(DISTINCT o.id) AS order_count,
    SUM(oi.quantity * oi.price) AS revenue,
    AVG(oi.quantity * oi.price) AS avg_order_value
FROM orders o
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id
JOIN categories c ON p.category_id = c.id
WHERE o.status = 'completed'
GROUP BY month, c.name
HAVING SUM(oi.quantity * oi.price) > 1000
ORDER BY month DESC, revenue DESC;
```

### GROUPING SETS, ROLLUP, CUBE
```sql
-- ROLLUP: hierarchical grouping
SELECT 
    EXTRACT(YEAR FROM created_at) AS year,
    EXTRACT(MONTH FROM created_at) AS month,
    SUM(amount) AS total
FROM orders
GROUP BY ROLLUP (year, month);
-- Returns: (year, month), (year, NULL), (NULL, NULL) ← grand total

-- CUBE: all possible combinations
GROUP BY CUBE (category, region);
-- Returns: (cat, region), (cat, NULL), (NULL, region), (NULL, NULL)

-- GROUPING SETS: specific combinations
GROUP BY GROUPING SETS ((category, region), (category), (region), ());
```

---

## 4. Set Operations

```sql
-- UNION: kết hợp results, loại duplicate
SELECT email FROM users
UNION
SELECT email FROM newsletter_subscribers;

-- UNION ALL: giữ duplicates (nhanh hơn)
SELECT email FROM users
UNION ALL
SELECT email FROM newsletter_subscribers;

-- INTERSECT: rows xuất hiện trong CẢ HAI queries
SELECT email FROM users
INTERSECT
SELECT email FROM newsletter_subscribers;

-- EXCEPT: rows trong query 1 NHƯNG KHÔNG trong query 2
SELECT email FROM users
EXCEPT
SELECT email FROM newsletter_subscribers;
-- → Users chưa subscribe newsletter
```

---

## 5. Useful SQL Patterns

### CASE WHEN
```sql
SELECT username,
    CASE 
        WHEN post_count > 100 THEN 'Power User'
        WHEN post_count > 10 THEN 'Active'
        WHEN post_count > 0 THEN 'Beginner'
        ELSE 'Lurker'
    END AS user_tier
FROM (
    SELECT u.username, COUNT(p.id) AS post_count
    FROM users u
    LEFT JOIN posts p ON u.id = p.user_id
    GROUP BY u.id, u.username
) stats;
```

### LATERAL JOIN (for each row, run subquery)
```sql
-- Top 3 posts gần đây nhất của mỗi user
SELECT u.username, latest.title, latest.created_at
FROM users u
CROSS JOIN LATERAL (
    SELECT title, created_at
    FROM posts
    WHERE user_id = u.id
    ORDER BY created_at DESC
    LIMIT 3
) latest;
```

### String Functions
```sql
SELECT 
    UPPER(name),
    LOWER(name),
    TRIM(name),
    LENGTH(name),
    SUBSTRING(name FROM 1 FOR 3),
    CONCAT(first_name, ' ', last_name),
    REPLACE(email, '@gmail.com', '@newdomain.com'),
    SPLIT_PART('a.b.c', '.', 2)  -- 'b'
FROM users;
```

---

## 📝 Bài tập

1. E-commerce: Lấy top 10 sản phẩm bán chạy nhất kèm tên category
2. Tìm users đã mua hàng nhưng chưa viết review nào
3. Doanh thu theo tháng với ROLLUP (month, grand total)
4. Tìm categories có doanh thu > trung bình tất cả categories

---

## 📚 Tài liệu
- *SQL Performance Explained* — Markus Winand
- [PostgreSQL Window Functions](https://www.postgresql.org/docs/current/tutorial-window.html)
- [Mode Analytics SQL Tutorial](https://mode.com/sql-tutorial)
