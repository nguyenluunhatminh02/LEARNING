# Bài 08: MVCC & Concurrency Control

## 🎯 Mục tiêu
- MVCC (Multi-Version Concurrency Control)
- PostgreSQL MVCC implementation
- VACUUM & bloat
- Lock types

---

## 1. MVCC — Multi-Version Concurrency Control

```
Problem: Readers block writers, writers block readers → low concurrency
Solution: MVCC — keep multiple versions of each row

Rule: Readers NEVER block writers, writers NEVER block readers!

Mỗi row có hidden columns:
  xmin: Transaction ID that inserted this row
  xmax: Transaction ID that deleted/updated this row (0 = still valid)

INSERT id=1 (xid=100):
  → (xmin=100, xmax=0, id=1, name='Alice')

UPDATE name='Bob' (xid=200):
  → (xmin=100, xmax=200, id=1, name='Alice')  ← old version (dead)
  → (xmin=200, xmax=0,   id=1, name='Bob')    ← new version (live)

DELETE (xid=300):
  → (xmin=200, xmax=300, id=1, name='Bob')    ← marked as dead
```

### Snapshot Isolation
```
Transaction 500 starts:
  → Takes snapshot: "I can see rows where xmin < 500 AND committed"
  → Cannot see rows with xmin ≥ 500 (future transactions)
  → Cannot see rows with xmax < 500 AND committed (deleted)

Tx 500 reads table:
  (xmin=100, xmax=200) → xmax committed & < 500 → INVISIBLE (deleted)
  (xmin=200, xmax=0)   → xmin committed & < 500 → VISIBLE ✅
  (xmin=501, xmax=0)   → xmin > 500 → INVISIBLE (future)
```

---

## 2. VACUUM — Cleanup Dead Tuples

```
MVCC creates dead tuples (old versions)
Without VACUUM → table grows forever (bloat)

VACUUM does:
1. Mark dead tuples as reusable space
2. Update visibility map
3. Update free space map
4. Freeze old transaction IDs (prevent wraparound)

VACUUM FULL:
  Rewrites entire table → reclaims disk space
  ❌ LOCKS TABLE (exclusive access required)
  → Dùng pg_repack thay thế (online, no lock)
```

```sql
-- Check dead tuples
SELECT 
    relname AS table,
    n_dead_tup AS dead_tuples,
    n_live_tup AS live_tuples,
    ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
    last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Autovacuum config
autovacuum = on
autovacuum_vacuum_threshold = 50         -- min dead tuples before vacuum
autovacuum_vacuum_scale_factor = 0.1     -- vacuum when 10% dead tuples
autovacuum_analyze_threshold = 50
autovacuum_analyze_scale_factor = 0.05
```

### Table Bloat
```sql
-- Check bloat ratio
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(tablename::regclass)) AS total_size,
    pg_size_pretty(pg_relation_size(tablename::regclass)) AS table_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename::regclass) DESC;

-- Fix bloat without locking (pg_repack extension)
-- pg_repack --table=orders --jobs=4 mydb
```

---

## 3. Lock Types

### Table-Level Locks
```
ACCESS SHARE          → SELECT (weakest, compatible with most)
ROW SHARE             → SELECT FOR UPDATE
ROW EXCLUSIVE         → INSERT, UPDATE, DELETE
SHARE                 → CREATE INDEX (blocks writes)
EXCLUSIVE             → VACUUM FULL, some ALTER TABLE
ACCESS EXCLUSIVE      → DROP TABLE, ALTER TABLE (strongest, blocks all)

Compatibility matrix:
  SELECT + SELECT = OK ✅
  SELECT + INSERT = OK ✅ (MVCC!)
  INSERT + INSERT = OK ✅ (different rows)
  UPDATE same row = WAIT (row-level lock)
  DDL + anything = WAIT
```

### Row-Level Locks
```sql
-- FOR UPDATE: exclusive lock on selected rows
SELECT * FROM products WHERE id = 1 FOR UPDATE;

-- FOR SHARE: shared lock (others can read, not modify)
SELECT * FROM products WHERE id = 1 FOR SHARE;

-- FOR UPDATE SKIP LOCKED: job queue pattern
-- Worker 1 and Worker 2 both try to get tasks:
BEGIN;
SELECT * FROM tasks 
WHERE status = 'pending' 
ORDER BY created_at 
LIMIT 1 
FOR UPDATE SKIP LOCKED;
-- Each worker gets a DIFFERENT task (no contention!)
UPDATE tasks SET status = 'processing' WHERE id = ?;
COMMIT;
```

---

## 4. Transaction ID Wraparound

```
PostgreSQL uses 32-bit transaction IDs → 4 billion
After 2 billion transactions → wraparound risk

If not vacuumed:
  Old data with txid=100 → after wraparound, 100 looks "future"
  → Data DISAPPEARS!

Prevention: VACUUM freezes old txids
  → Replace xmin with FrozenTransactionId
  → Autovacuum does this automatically
  → Monitor: age(datfrozenxid) should be < 1 billion

-- Check
SELECT datname, age(datfrozenxid) FROM pg_database ORDER BY age DESC;
-- If age > 1 billion → URGENT: manual VACUUM FREEZE
```

---

## 5. Connection Pooling (PgBouncer)

```
Problem: PostgreSQL fork process per connection (~10MB each)
  500 connections = 5GB RAM just for connections!
  Connection setup = ~50ms

Solution: Connection pool
  Application → PgBouncer (100 connections) → PostgreSQL (20 connections)

PgBouncer modes:
  Session:     1 client = 1 server conn (until disconnect)
  Transaction: 1 client = 1 server conn (per transaction) ⭐
  Statement:   1 client = 1 server conn (per statement) — risky
```

```ini
# pgbouncer.ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
min_pool_size = 5
```

---

## 📝 Bài tập

1. Demo MVCC: 2 concurrent transactions, show xmin/xmax
2. Monitor dead tuples, trigger VACUUM, observe cleanup
3. Implement job queue bằng FOR UPDATE SKIP LOCKED
4. Setup PgBouncer với transaction pooling mode

---

## 📚 Tài liệu
- *PostgreSQL 14 Internals* — Egor Rogov
- [PostgreSQL MVCC Explained](https://www.interdb.jp/pg/pgsql05.html)
- [PgBouncer Documentation](https://www.pgbouncer.org/)
