# Bài 01: Database Basics & SQL Fundamentals

## 🎯 Mục tiêu
- Hiểu relational database model
- DDL, DML, DCL commands
- CRUD operations
- Data types, constraints

---

## 1. Database là gì?

```
Database = Tập hợp dữ liệu có tổ chức
DBMS = Database Management System (phần mềm quản lý)

Relational Database:
  Data lưu trong TABLES (bảng)
  Tables có ROWS (bản ghi) và COLUMNS (trường)
  Tables liên kết qua FOREIGN KEYS

Popular RDBMS:
  PostgreSQL  — ⭐ Feature-rich, open-source, production-grade
  MySQL       — Phổ biến, web applications
  SQLite      — Embedded, mobile apps, testing
  SQL Server  — Microsoft ecosystem
  Oracle      — Enterprise
```

---

## 2. Data Types (PostgreSQL)

```sql
-- Numeric
INTEGER          -- -2B to 2B
BIGINT           -- larger integers
NUMERIC(10,2)    -- exact decimal (money: 12345678.99)
REAL / FLOAT     -- approximate decimal

-- String
VARCHAR(255)     -- variable-length string (max 255)
TEXT             -- unlimited length string
CHAR(10)         -- fixed-length (padded with spaces)

-- Date/Time
DATE             -- 2024-01-15
TIME             -- 14:30:00
TIMESTAMP        -- 2024-01-15 14:30:00
TIMESTAMPTZ      -- with timezone ⭐ (luôn dùng cái này)

-- Boolean
BOOLEAN          -- TRUE/FALSE/NULL

-- Other
UUID             -- universally unique identifier ⭐
JSONB            -- binary JSON (indexable, queryable)
ARRAY            -- PostgreSQL arrays
BYTEA            -- binary data
```

---

## 3. DDL — Data Definition Language

```sql
-- Tạo bảng
CREATE TABLE users (
    id          BIGSERIAL PRIMARY KEY,       -- auto-increment
    email       VARCHAR(255) UNIQUE NOT NULL,
    username    VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name   VARCHAR(100),
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE posts (
    id          BIGSERIAL PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title       VARCHAR(255) NOT NULL,
    content     TEXT,
    status      VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft','published','archived')),
    view_count  INTEGER DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE tags (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- Many-to-many relationship
CREATE TABLE post_tags (
    post_id BIGINT REFERENCES posts(id) ON DELETE CASCADE,
    tag_id  INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);

-- Modify table
ALTER TABLE users ADD COLUMN bio TEXT;
ALTER TABLE users ALTER COLUMN username TYPE VARCHAR(100);
ALTER TABLE users DROP COLUMN bio;

-- Delete table
DROP TABLE IF EXISTS post_tags;
TRUNCATE TABLE posts;  -- Xóa tất cả rows (nhanh hơn DELETE)
```

### Constraints
```sql
PRIMARY KEY     -- unique + not null, 1 per table
UNIQUE          -- no duplicate values
NOT NULL        -- cannot be NULL
FOREIGN KEY     -- reference to another table
CHECK           -- custom validation
DEFAULT         -- default value

-- Composite unique constraint
ALTER TABLE users ADD CONSTRAINT uq_email_username 
    UNIQUE (email, username);
```

---

## 4. DML — Data Manipulation Language

### INSERT
```sql
-- Single row
INSERT INTO users (email, username, password_hash, full_name)
VALUES ('alice@email.com', 'alice', 'hashed_pw_123', 'Alice Nguyen');

-- Multiple rows
INSERT INTO tags (name) VALUES 
    ('python'), ('sql'), ('database'), ('backend');

-- Insert with returning
INSERT INTO posts (user_id, title, content, status)
VALUES (1, 'Learn SQL', 'SQL is powerful...', 'published')
RETURNING id, created_at;

-- Insert from select
INSERT INTO archived_posts (id, title, content)
SELECT id, title, content FROM posts WHERE status = 'archived';

-- Upsert (Insert or Update)
INSERT INTO users (email, username, password_hash)
VALUES ('alice@email.com', 'alice_new', 'new_hash')
ON CONFLICT (email) 
DO UPDATE SET username = EXCLUDED.username, updated_at = NOW();
```

### SELECT
```sql
-- Basic
SELECT * FROM users;
SELECT id, email, full_name FROM users WHERE is_active = TRUE;

-- Filtering
SELECT * FROM posts 
WHERE status = 'published' 
  AND created_at > '2024-01-01'
  AND title LIKE '%SQL%'
  AND view_count BETWEEN 100 AND 1000
  AND user_id IN (1, 2, 3);

-- Sorting & Pagination
SELECT * FROM posts
ORDER BY created_at DESC, view_count DESC
LIMIT 20 OFFSET 40;  -- Page 3 (20 items per page)

-- Aggregate
SELECT 
    user_id,
    COUNT(*) AS post_count,
    SUM(view_count) AS total_views,
    AVG(view_count) AS avg_views,
    MAX(view_count) AS max_views
FROM posts
WHERE status = 'published'
GROUP BY user_id
HAVING COUNT(*) > 5
ORDER BY total_views DESC;

-- DISTINCT
SELECT DISTINCT status FROM posts;
SELECT COUNT(DISTINCT user_id) FROM posts;
```

### UPDATE
```sql
UPDATE users 
SET full_name = 'Alice Tran', updated_at = NOW()
WHERE id = 1;

-- Update with subquery
UPDATE posts 
SET status = 'archived'
WHERE created_at < NOW() - INTERVAL '1 year'
  AND status = 'published';

-- Update with JOIN (PostgreSQL syntax)
UPDATE posts p
SET view_count = view_count + 1
FROM users u
WHERE p.user_id = u.id AND u.username = 'alice';
```

### DELETE
```sql
DELETE FROM posts WHERE id = 5;
DELETE FROM posts WHERE status = 'draft' AND created_at < '2023-01-01';

-- Soft delete (preferred in production)
-- Thay vì DELETE, dùng flag:
UPDATE posts SET deleted_at = NOW() WHERE id = 5;
-- Query: SELECT * FROM posts WHERE deleted_at IS NULL;
```

---

## 5. NULL Handling

```sql
-- NULL = unknown, không phải 0 hay empty string
-- NULL = NULL → FALSE (không thể so sánh NULL)

SELECT * FROM users WHERE full_name IS NULL;
SELECT * FROM users WHERE full_name IS NOT NULL;

-- COALESCE: trả về giá trị đầu tiên NOT NULL
SELECT COALESCE(full_name, username, 'Anonymous') AS display_name
FROM users;

-- NULLIF: trả về NULL nếu 2 giá trị bằng nhau
SELECT NULLIF(view_count, 0);  -- tránh division by zero
SELECT total / NULLIF(count, 0) AS average;
```

---

## 6. Practice — Setup

```bash
# Docker PostgreSQL
docker run -d --name postgres \
  -e POSTGRES_DB=learning \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secret \
  -p 5432:5432 \
  postgres:16

# Connect
psql -h localhost -U admin -d learning
# Hoặc dùng DBeaver/pgAdmin (GUI)
```

---

## 📝 Bài tập

1. Tạo schema cho hệ thống e-commerce: users, products, categories, orders, order_items
2. Insert sample data (10 users, 50 products, 30 orders)
3. Viết queries: top 5 sản phẩm bán chạy, doanh thu theo tháng
4. Implement soft delete cho orders table

---

## 📚 Tài liệu
- [PostgreSQL Official Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- *Learning SQL* — Alan Beaulieu
- [SQLBolt Interactive Tutorial](https://sqlbolt.com/)
