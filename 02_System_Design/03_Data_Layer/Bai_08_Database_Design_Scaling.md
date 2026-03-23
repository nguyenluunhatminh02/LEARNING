# Bài 08: Database Design & Scaling

## 🎯 Mục tiêu
- SQL vs NoSQL trade-offs
- Database replication & sharding
- CAP theorem thực tế
- Connection pooling, query optimization

## 📖 Câu chuyện đời thường
> Bạn quản lý một chuỗi thư viện. **SQL** giống thư viện truyền thống: mỗi cuốn sách được ghi vào phiếu mượn, có quy tắc chặt chẽ (schema). **NoSQL** giống kho lưu trữ linh hoạt: sách, băng đĩa, bản đồ đều cho vào được. **Replication** là photo nhiều bản catalogue để mỗi chi nhánh có một bản (nếu một bản mất vẫn còn bản khác). **Sharding** là chia catalogue thành tập: A-M ở chi nhánh 1, N-Z ở chi nhánh 2 — mỗi nơi chỉ giữ một phần. **CAP theorem** nói: khi mạng lưới hỏng (điện thoại giữa các chi nhánh mất), bạn phải chọn: hoặc tất cả chi nhánh có data giống nhau (consistency) hoặc vẫn phục vụ khách dù data có thể hơi cũ (availability).

---

## 1. SQL vs NoSQL

### Khi nào dùng SQL?
```
✅ ACID transactions (banking, order)
✅ Complex JOINs, aggregations
✅ Structured data, clear schema
✅ Strong consistency required
→ PostgreSQL, MySQL
```

### Khi nào dùng NoSQL?
```
✅ Flexible schema (user profiles, product catalog)
✅ High write throughput
✅ Horizontal scaling dễ
✅ Low-latency reads (pre-computed views)

Document DB → MongoDB (flexible JSON docs)
Key-Value   → Redis (cache, sessions)
Wide-Column → Cassandra (time-series, IoT, logs)
Graph DB    → Neo4j (social networks, recommendations)
```

---

## 2. CAP Theorem

```
Trong distributed system, chỉ chọn được 2/3:
  C (Consistency)  — Mọi read đều trả data mới nhất
  A (Availability) — Mọi request đều nhận response
  P (Partition tolerance) — Hệ thống vẫn chạy khi network split

P luôn phải có → thực tế chọn CP hoặc AP:
  CP: PostgreSQL, MongoDB → consistent nhưng có thể unavailable
  AP: Cassandra, DynamoDB → available nhưng có thể stale data
```

### PACELC (mở rộng CAP)
```
If Partition → choose A or C
Else (normal) → choose Latency or Consistency

PostgreSQL: PC/EC (consistent mọi lúc)
Cassandra:  PA/EL (available + low latency, eventual consistency)
MongoDB:    PA/EC (tunable)
```

---

## 3. Database Replication

### Master-Slave (Primary-Replica)
```
Writes → [Master] → replication → [Slave 1] ← Reads
                                → [Slave 2] ← Reads
                                → [Slave 3] ← Reads

✅ Scale reads (thêm slaves)
❌ Write vẫn bottleneck (1 master)
❌ Replication lag → stale reads
```

### Multi-Master
```
[Master 1] ↔ [Master 2]
  ↑ Write     ↑ Write

✅ Write availability cao
❌ Conflict resolution phức tạp
❌ Split-brain risk
```

### Synchronous vs Asynchronous Replication
```
Sync:  Master wait slave ACK → strong consistency, slower writes
Async: Master không wait    → faster writes, possible data loss
Semi-sync: Wait 1 slave ACK → balance
```

---

## 4. Database Sharding

```
User ID 1-1M    → Shard 1
User ID 1M-2M   → Shard 2
User ID 2M-3M   → Shard 3

Mỗi shard = independent database
→ Scale writes + reads horizontally
```

### Sharding Strategies

```python
# 1. Range-based
shard = user_id // 1_000_000  # Shard by ID range
# ❌ Hotspot: shard chứa celebrities có load cao

# 2. Hash-based
shard = hash(user_id) % num_shards  # Distribute đều
# ❌ Thêm shard → phải rehash tất cả (dùng consistent hashing)

# 3. Directory-based
shard = lookup_table[user_id]  # Lookup service quyết định
# ✅ Flexible nhưng lookup = bottleneck
```

### Consistent Hashing
```
Ring: 0 ─────────── 2^32
     │  Shard A    │  Shard B    │  Shard C    │

hash(key) → position trên ring → đi clockwise → gặp shard đầu tiên

Thêm shard D → chỉ cần migrate 1/N data (không phải tất cả)
Virtual nodes: mỗi shard có nhiều positions → distribute đều hơn
```

---

## 5. Connection Pooling

```python
# ❌ Mỗi request = new connection (chậm, tốn resource)
def handle_request():
    conn = psycopg2.connect(...)  # ~50ms to establish
    cursor = conn.cursor()
    cursor.execute("SELECT ...")
    conn.close()

# ✅ Connection Pool (reuse connections)
from psycopg2 import pool

connection_pool = pool.ThreadedConnectionPool(
    minconn=5,
    maxconn=20,  # Max 20 connections
    host='localhost', dbname='mydb'
)

def handle_request():
    conn = connection_pool.getconn()  # ~0ms, reuse existing
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT ...")
    finally:
        connection_pool.putconn(conn)  # Return to pool
```

---

## 6. Practical Design Decisions

```
Hệ thống nhỏ (<1M users):
  → PostgreSQL single instance + read replicas
  
Hệ thống trung bình (1-10M users):
  → PostgreSQL + Redis cache + read replicas + connection pooling

Hệ thống lớn (>10M users):
  → Sharded PostgreSQL + Redis cluster + message queue
  → Hoặc: DynamoDB/Cassandra cho write-heavy

Read-heavy (90% reads):
  → Read replicas + aggressive caching

Write-heavy:
  → Sharding + write-back cache + async processing
```

---

## 📝 Bài tập

1. Thiết kế database schema cho Twitter (users, tweets, follows, likes)
2. Implement consistent hashing bằng Python
3. Setup PostgreSQL master-slave replication (Docker)
4. Benchmark: PostgreSQL với/không connection pool

---

## 📚 Tài liệu
- *Designing Data-Intensive Applications* — Martin Kleppmann (Ch.5-6)
- *Database Internals* — Alex Petrov
- [Use The Index, Luke](https://use-the-index-luke.com/)

## 🔗 Liên kết chéo
- → **DB Bài 05: Indexing Deep Dive** — chi tiết B-Tree, Hash, GIN/GiST indexes
- → **DB Bài 07-08: Replication & Sharding** — implement cụ thể các pattern
- → **DSA Bài 12: System Algorithms** — Consistent Hashing, Bloom Filter cho distributed DB
- → **AI Bài 28: ML Pipeline** — data storage cho ML feature stores
