# Bài 20: Schema Migration & Evolution — Zero-Downtime Changes

## 🎯 Mục tiêu
- Schema migration strategies
- Zero-downtime migrations
- Migration tools: Flyway, Alembic, golang-migrate
- Backward/forward compatible changes

## 📖 Câu chuyện đời thường
> Bạn cần sửa lại hệ thống điện trong nhà (**schema migration**) nhưng gia đình vẫn đang sống trong đó (**zero-downtime**). Bạn không thể cắt điện 3 ngày! Thay vào đó: bước 1 lắp thêm đường dây mới chạy song song. Bước 2 chuyển thiết bị sang dây mới. Bước 3 tháo dây cũ. **Backward compatible** = thiết bị cũ vẫn chạy được với dây mới. Migration tools (Flyway, Alembic) giống như bản vẽ sửa điện có đánh số từ bước 1 đến bước 10 — ai làm cũng làm giống nhau, và có thể quay lại bước trước nếu sai (rollback).

---

## 1. Tại sao Schema Migration khó?

```
Production database:
  - 500GB data, 10K requests/second
  - 24/7 uptime required
  - "ALTER TABLE ADD COLUMN" → có thể LOCK table hàng giờ!

Thực tế đau thương:
  1. Dev thêm column → deploy → table lock 30 phút → downtime
  2. Rename column → app crash vì old code reads old column name
  3. Drop column → old app instances still query it → 500 errors
  4. Add NOT NULL constraint → existing rows violate → migration fails

CTO/Staff Engineer phải biết:
  → Migration là operation NGUY HIỂM NHẤT trong production
  → Mọi migration phải backward compatible
  → Test on staging với production-size data TRƯỚC
```

---

## 2. Migration Tools

### Flyway (Java/JVM, database-focused)
```sql
-- V1__create_users_table.sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- V2__add_phone_to_users.sql
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- V3__create_orders_table.sql
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    total DECIMAL(10,2),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

```
Flyway tracks migrations in schema_version table:
| version | description           | installed_on        | success |
| 1       | create users table    | 2024-01-15 10:00:00 | true    |
| 2       | add phone to users    | 2024-01-20 14:00:00 | true    |
| 3       | create orders table   | 2024-02-01 09:00:00 | true    |

→ Next deploy: only run V4+ (skip already-applied)
```

### Alembic (Python/SQLAlchemy)
```python
# alembic revision --autogenerate -m "add phone to users"

"""add phone to users"""
revision = 'abc123'
down_revision = 'def456'

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))

def downgrade():
    op.drop_column('users', 'phone')
```

```bash
# Apply migrations
alembic upgrade head

# Rollback 1 step
alembic downgrade -1

# Show current version
alembic current
```

### golang-migrate
```sql
-- 001_create_users.up.sql
CREATE TABLE users (id BIGSERIAL PRIMARY KEY, email VARCHAR(255) UNIQUE);

-- 001_create_users.down.sql
DROP TABLE users;
```

---

## 3. Zero-Downtime Migration Patterns

### Pattern 1: Expand-Migrate-Contract (3 deploys)

```
Mục tiêu: Rename column "name" → "full_name"

❌ WRONG (1 deploy — DOWNTIME):
  ALTER TABLE users RENAME COLUMN name TO full_name;
  → Old app instances crash (still reading "name")

✅ CORRECT (3 deploys):

Deploy 1 — EXPAND (add new column):
  ALTER TABLE users ADD COLUMN full_name VARCHAR(100);
  UPDATE users SET full_name = name;  -- backfill
  -- Trigger: keep both columns in sync
  CREATE TRIGGER sync_name BEFORE INSERT OR UPDATE ON users
  FOR EACH ROW EXECUTE FUNCTION sync_name_columns();
  
  App: write to BOTH columns, read from "name"

Deploy 2 — MIGRATE (switch reads):
  App: write to BOTH columns, read from "full_name"
  
Deploy 3 — CONTRACT (remove old column):
  DROP TRIGGER sync_name ON users;
  ALTER TABLE users DROP COLUMN name;
  App: only use "full_name"

Timeline: 3 deploys over 1-2 weeks
  → Zero downtime!
  → Rollback possible at any step!
```

### Pattern 2: Adding NOT NULL column

```
❌ WRONG:
  ALTER TABLE users ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'user';
  → PostgreSQL 11+ handles this fast (metadata-only for DEFAULT)
  → But older versions: REWRITES ENTIRE TABLE → lock!

✅ SAFE (works everywhere):
  Step 1: Add nullable column
    ALTER TABLE users ADD COLUMN role VARCHAR(20);
    
  Step 2: Backfill in batches (NO lock)
    UPDATE users SET role = 'user' WHERE role IS NULL AND id BETWEEN 1 AND 10000;
    UPDATE users SET role = 'user' WHERE role IS NULL AND id BETWEEN 10001 AND 20000;
    -- ... batch by batch, with sleep between batches
    
  Step 3: Set default for new rows
    ALTER TABLE users ALTER COLUMN role SET DEFAULT 'user';
    
  Step 4: Add NOT NULL constraint
    ALTER TABLE users ADD CONSTRAINT users_role_not_null CHECK (role IS NOT NULL) NOT VALID;
    ALTER TABLE users VALIDATE CONSTRAINT users_role_not_null;
    -- NOT VALID: add constraint without checking existing rows (fast)
    -- VALIDATE: check existing rows (slow but doesn't block writes)
```

### Pattern 3: Adding Index without Downtime

```sql
-- ❌ WRONG (blocks writes during build):
CREATE INDEX idx_orders_user ON orders(user_id);

-- ✅ CORRECT:
CREATE INDEX CONCURRENTLY idx_orders_user ON orders(user_id);
-- Builds index without blocking writes
-- Takes longer but zero downtime
-- If fails: DROP and retry (partial index may exist)
```

### Pattern 4: Large Table Migration

```python
# Migrate 100M rows: change data format in batches

import time

BATCH_SIZE = 5000
last_id = 0

while True:
    result = db.execute("""
        UPDATE users 
        SET phone_normalized = normalize_phone(phone)
        WHERE id > %s AND phone_normalized IS NULL
        ORDER BY id
        LIMIT %s
        RETURNING id
    """, [last_id, BATCH_SIZE])
    
    if result.rowcount == 0:
        break
    
    last_id = result.fetchall()[-1][0]
    time.sleep(0.1)  # Throttle: don't overload DB
    print(f"Migrated up to id {last_id}")
```

---

## 4. Dangerous Operations — Cheat Sheet

```
Operation                         | Risk    | Safe Alternative
----------------------------------|---------|----------------------------------
ALTER TABLE ADD COLUMN (nullable) | 🟢 Safe | Just do it
ALTER TABLE ADD COLUMN NOT NULL   | 🟡 Warn | Add nullable → backfill → constraint
ALTER TABLE DROP COLUMN           | 🔴 HIGH | Deploy code first → then drop column
ALTER TABLE RENAME COLUMN         | 🔴 HIGH | Expand-Migrate-Contract pattern
ALTER TABLE ALTER TYPE             | 🔴 HIGH | Add new column → migrate → drop old
CREATE INDEX                      | 🟡 Warn | CREATE INDEX CONCURRENTLY
DROP TABLE                        | 🔴 HIGH | Rename first → wait → drop later
ADD FOREIGN KEY                   | 🟡 Warn | ADD NOT VALID → VALIDATE separately
ADD CHECK CONSTRAINT              | 🟡 Warn | NOT VALID → VALIDATE
TRUNCATE TABLE                    | 🔴 HIGH | DELETE in batches
```

---

## 5. Schema Versioning Best Practices

```
1. Một chiều: migrations chỉ FORWARD (không dùng down migrations in production)
   Why? Down migration có thể mất data
   Rollback = viết migration mới đảo ngược

2. Idempotent: migration chạy lại không lỗi
   IF NOT EXISTS, ADD IF NOT EXISTS

3. Small & focused: 1 migration = 1 thay đổi nhỏ
   ❌ 1 migration: create 5 tables + 10 indexes + alter 3 tables
   ✅ 5 migrations: each does 1 thing

4. Review trước production:
   DBA review tất cả migrations
   Test trên staging với production-size data
   Estimate lock time và impact

5. Monitoring:
   Alert nếu migration > 5 minutes
   Monitor: lock_timeout, statement_timeout
   Ready to cancel (pg_cancel_backend)

6. Naming convention:
   V001_20240115_create_users_table.sql
   V002_20240120_add_phone_to_users.sql
   → Sequential + timestamp + description
```

---

## 6. Advanced: Online Schema Change Tools

```
Khi ALTER TABLE lock quá lâu → dùng online schema change tools:

pg_osc (PostgreSQL Online Schema Change):
  1. Create shadow table with new schema
  2. Copy data in batches
  3. Replay changes via trigger
  4. Atomic swap tables
  → Zero downtime for ANY schema change

gh-ost (GitHub, MySQL):
  1. Create ghost table with new schema
  2. Copy data using binlog streaming
  3. Cut-over: atomic rename
  → Used by GitHub for all MySQL migrations

pt-online-schema-change (Percona, MySQL):
  Similar to gh-ost, trigger-based
```

```bash
# pg_osc example
pg_osc perform \
  --dbname mydb \
  --table users \
  --alter "ADD COLUMN avatar_url TEXT, DROP COLUMN legacy_field" \
  --batch-count 5000
```

---

## 7. Database Branching (Modern Approach)

```
Neon, PlanetScale: Database branching (like git branches)

Main branch: production data
  └── dev branch: copy-on-write clone
      → Make schema changes
      → Test with real data
      → Merge to main (apply migration)

Benefits:
  ✅ Test migrations on production-size data
  ✅ Instant clone (copy-on-write, no copy data)
  ✅ Preview environments with real data
  ❌ Vendor-specific, cloud-only
```

---

## 📝 Bài tập

1. Viết expand-migrate-contract cho rename column (3 Alembic migrations)
2. Migrate 1M rows: batch update with throttling
3. Tạo governance checklist: "migration review process"
4. Practice: add NOT NULL column to table có 10M rows without downtime

---

## 📚 Tài liệu
- *Refactoring Databases* — Scott Ambler
- [Strong Migrations gem (Ruby)](https://github.com/ankane/strong_migrations) — patterns apply to all languages
- [pg_osc](https://github.com/shayonj/pg_osc) — PostgreSQL online schema change
- [gh-ost](https://github.com/github/gh-ost) — GitHub's MySQL schema change tool
- [PlanetScale Branching](https://planetscale.com/docs/concepts/branching)
