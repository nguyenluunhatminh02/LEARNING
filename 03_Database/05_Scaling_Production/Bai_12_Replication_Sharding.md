# Bài 12: Replication & Sharding

## 🎯 Mục tiêu
- Replication strategies
- Sharding strategies & consistent hashing
- PostgreSQL replication setup
- Vitess, Citus for sharding

## 📖 Câu chuyện đời thường
> Bạn có một cuốn sách công thức nấu ăn tuyệt vời. **Replication** = photo thêm 3 bản đặt ở 3 nhà khác nhau: nếu 1 nhà cháy, vẫn còn 2 bản (fault tolerance). Nhiều người có thể đọc cùng lúc (read scaling). **Sharding** = chia sách thành 3 tập: Món Việt (shard 1), Món Nhật (shard 2), Món Âu (shard 3). Mỗi tập nhỏ hơn, tra nhanh hơn. **Consistent Hashing** là cách quyết định "món này thuộc tập nào" mà khi thêm tập mới, không cần chuyển hết công thức — chỉ chuyển một phần nhỏ.

---

## 1. Replication

### Streaming Replication (PostgreSQL)
```
Primary (writes) → WAL stream → Standby 1 (reads)
                              → Standby 2 (reads)

Synchronous:  Primary waits for standby ACK → no data loss, slower
Asynchronous: Primary doesn't wait → faster, possible data loss
```

```sql
-- Primary: postgresql.conf
wal_level = replica
max_wal_senders = 5
synchronous_standby_names = 'standby1'

-- Standby: standby.signal file + primary_conninfo
primary_conninfo = 'host=primary port=5432 user=replicator'

-- Check replication lag
SELECT client_addr, state, 
       pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes
FROM pg_stat_replication;
```

### Logical Replication
```sql
-- Replicate specific tables (not entire database)
-- Primary
CREATE PUBLICATION my_pub FOR TABLE users, orders;

-- Subscriber
CREATE SUBSCRIPTION my_sub
CONNECTION 'host=primary port=5432 dbname=mydb'
PUBLICATION my_pub;

-- Use cases: 
-- - Replicate subset of data
-- - Cross-version replication
-- - Data migration with zero downtime
```

---

## 2. Sharding Strategies

### Hash-based Sharding
```python
shard_id = hash(user_id) % num_shards

# user_id=123 → shard 1
# user_id=456 → shard 2
# ✅ Even distribution
# ❌ Adding shards → rehash everything → massive data migration
```

### Consistent Hashing (preferred)
```
Hash ring (0 → 2^32):

     Shard A (pos 1000)
    /
   /    Shard B (pos 5000)
  |    /
  |   /    Shard C (pos 9000)
   \  |   /
    \ |  /
     ring

hash(key) → position → walk clockwise → first shard

Adding Shard D (pos 3000):
  Only keys between A(1000) and D(3000) migrate from B to D
  → Minimal data movement (~1/N keys)

Virtual nodes: each shard → multiple positions on ring
  → Better distribution
```

### Range-based Sharding
```
users A-M → Shard 1
users N-Z → Shard 2

dates 2024-01 to 2024-06 → Shard 1
dates 2024-07 to 2024-12 → Shard 2

✅ Range queries efficient (within shard)
❌ Hotspots (popular ranges overloaded)
```

### Sharding Challenges
```
Cross-shard queries:  JOIN across shards → very expensive
Cross-shard transactions: 2PC needed → complex
Resharding:  Adding/removing shards → data migration
Global ordering: No single auto-increment across shards
```

---

## 3. Tools

```
Citus (PostgreSQL extension):
  - Distributed PostgreSQL
  - Transparent sharding
  - Distributed queries, JOINs

Vitess (MySQL):
  - YouTube's sharding middleware
  - Connection pooling + query routing

ProxySQL / PgPool:
  - Query routing to correct shard
  - Read/write splitting
```

---

## 📝 Bài tập

1. Implement consistent hashing bằng Python
2. Setup PostgreSQL streaming replication (Docker Compose)
3. Design sharding strategy cho user_id-based system
4. Monitor replication lag

---

## 📚 Tài liệu
- *Designing Data-Intensive Applications* — Kleppmann (Ch.5-6)
- [Citus Documentation](https://docs.citusdata.com/)
