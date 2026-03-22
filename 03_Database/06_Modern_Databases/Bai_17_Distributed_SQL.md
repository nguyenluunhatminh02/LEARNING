# Bài 17: Distributed SQL (NewSQL) — CockroachDB, Spanner, TiDB

## 🎯 Mục tiêu
- Hiểu tại sao cần Distributed SQL
- Architecture: CockroachDB, Google Spanner, TiDB
- CAP Theorem trong thực tế
- Khi nào dùng, khi nào KHÔNG dùng

---

## 1. Vấn đề mà NewSQL giải quyết

```
Traditional SQL (PostgreSQL, MySQL):
  ✅ ACID transactions, powerful queries
  ❌ Scale = vertical only (bigger machine)
  ❌ Single point of failure (without HA setup)

Traditional NoSQL (Cassandra, MongoDB):
  ✅ Horizontal scale, distributed
  ❌ Weak/no transactions
  ❌ Limited query capabilities

NewSQL = Best of both worlds:
  ✅ SQL interface + ACID transactions
  ✅ Horizontal scaling (add nodes)
  ✅ Distributed, fault-tolerant
  ✅ Geo-replication

Tưởng tượng: "PostgreSQL nhưng chạy trên 100 nodes trên toàn cầu"
```

---

## 2. CAP Theorem — Hiểu đúng

```
CAP: Chỉ có thể chọn 2 trong 3:
  C — Consistency: Mọi node đọc cùng data mới nhất
  A — Availability: Mọi request đều nhận response
  P — Partition tolerance: Hoạt động khi mạng giữa nodes bị đứt

Thực tế: Network partition LUÔN xảy ra → phải chọn P
  → CP: Consistency + Partition tolerance (từ chối request khi partition)
  → AP: Availability + Partition tolerance (trả data cũ khi partition)

CP databases: PostgreSQL, CockroachDB, Spanner, etcd
AP databases: Cassandra, DynamoDB, Couchbase

★ PACELC (mở rộng CAP):
  "Khi có Partition → chọn A hay C?"
  "Else (bình thường) → chọn Latency hay Consistency?"

  CockroachDB: PC/EC (always consistent, higher latency)
  Cassandra:   PA/EL (always available, lower latency)
  MongoDB:     PA/EC (tunable)
```

### Consistency Models — Phổ trên thực tế
```
Strong                                                    Weak
  |                                                         |
  ▼                                                         ▼
Linearizable → Sequential → Causal → Eventual
  (Spanner)    (CockroachDB) (MongoDB)  (Cassandra)

Linearizable: Mọi operation xảy ra tại 1 thời điểm chính xác
  "Sau khi write thành công, mọi read đều thấy giá trị mới"
  → Cần cho: banking, inventory, leader election

Sequential: Operations trong 1 process theo đúng thứ tự
  → Cần cho: order processing, audit logs

Causal: Nếu A gây ra B, mọi người thấy A trước B
  → Cần cho: social media comments (reply after post)

Eventual: Cuối cùng tất cả nodes sẽ agree
  → OK cho: product catalog, user preferences, analytics
```

---

## 3. Google Spanner

```
Spanner = Globally distributed SQL database by Google

Key innovation: TrueTime API
  GPS + atomic clocks → global clock với bounded uncertainty
  "Thời gian trên server A và server B sai lệch < 7ms"

How it works:
  Mỗi transaction gán timestamp → global ordering
  Wait out uncertainty period → guarantee linearizability

Architecture:
  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
  │  Zone US-1  │  │  Zone EU-1  │  │  Zone AP-1  │
  │  Spanserver │  │  Spanserver │  │  Spanserver │
  │  [Paxos]    │←→│  [Paxos]    │←→│  [Paxos]    │
  └─────────────┘  └─────────────┘  └─────────────┘

  Data chia thành splits (tablets)
  Mỗi split replicated qua Paxos (consensus algorithm)
  Reads: local replica (stale) hoặc leader (strong)
  Writes: qua Paxos consensus → majority agree

Use case:
  Google: AdWords, Gmail, Google Play (billions of users)
  Banking: Global transactions across regions
  
Limitation:
  Cloud Spanner only (Google Cloud) → vendor lock-in
  Expensive ($0.90/node/hour = ~$650/month per node minimum)
```

---

## 4. CockroachDB

```
CockroachDB = Open-source inspired by Spanner
  "Spanner cho mọi người" — không cần TrueTime (dùng hybrid-logical clock)

Architecture:
  ┌─────────────────────────────────────────────────┐
  │                 SQL Layer                         │
  │  (PostgreSQL-compatible wire protocol)           │
  ├─────────────────────────────────────────────────┤
  │            Distribution Layer                     │
  │  Ranges → Raft consensus → replicas              │
  ├─────────────────────────────────────────────────┤
  │              Storage Layer                        │
  │  Pebble (LSM-Tree key-value store)               │
  └─────────────────────────────────────────────────┘

Key concepts:
  Ranges: Data chia thành 512MB ranges
  Raft: Mỗi range = 1 Raft group (3 replicas default)
  Leaseholder: 1 replica xử lý reads (minimize latency)
  Transaction: Serializable isolation (strong guarantee)
```

### CockroachDB — Hands-on
```sql
-- Tạo cluster (Docker)
-- docker run cockroachdb/cockroach start-single-node --insecure

-- SQL gần như PostgreSQL
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email STRING UNIQUE NOT NULL,
    name STRING NOT NULL,
    region STRING NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Geo-partitioning: data gần user
ALTER TABLE users PARTITION BY LIST (region) (
    PARTITION us VALUES IN ('us-east', 'us-west'),
    PARTITION eu VALUES IN ('eu-west', 'eu-central'),
    PARTITION ap VALUES IN ('ap-southeast', 'ap-northeast')
);

-- Pin partitions to specific nodes
ALTER PARTITION us OF TABLE users
    CONFIGURE ZONE USING constraints = '[+region=us]';
ALTER PARTITION eu OF TABLE users  
    CONFIGURE ZONE USING constraints = '[+region=eu]';

-- Data ở US → stored on US nodes → low latency cho US users
-- Data ở EU → stored on EU nodes → GDPR compliance (data stays in EU!)

-- Multi-region transaction: vẫn ACID!
BEGIN;
INSERT INTO users (email, name, region) VALUES ('alice@eu.com', 'Alice', 'eu-west');
INSERT INTO orders (user_id, total) VALUES (..., 100); -- order on US node
COMMIT; -- Distributed transaction qua Raft consensus
```

### Khi nào dùng CockroachDB?
```
✅ Cần ACID + horizontal scale
✅ Multi-region deployment (geo-distributed)
✅ Strong consistency bắt buộc (financial, inventory)
✅ Team muốn PostgreSQL compatibility
✅ Automated failover (no manual HA setup)

❌ Single-region, data < 500GB → PostgreSQL đủ rồi
❌ Read-heavy analytics → ClickHouse tốt hơn
❌ Budget limited → CockroachDB licensing cost
❌ Need PostgreSQL extensions (PostGIS, pgvector) → không support
```

---

## 5. TiDB

```
TiDB = MySQL-compatible distributed SQL (by PingCAP, China)

Architecture (HTAP — Hybrid Transactional/Analytical):
  ┌──────────────────────────────────┐
  │          TiDB Server             │ ← SQL layer (MySQL protocol)
  └──────────┬──────────┬────────────┘
             │          │
  ┌──────────▼────┐ ┌───▼───────────┐
  │    TiKV       │ │   TiFlash     │ ← Column store (analytics)
  │  (Row store)  │ │  (OLAP)       │
  │  Raft + RocksDB│ │  Raft + Delta │
  └───────────────┘ └───────────────┘
             │
  ┌──────────▼────┐
  │      PD       │ ← Placement Driver (scheduling, timestamp)
  └───────────────┘

HTAP = 1 database cho cả OLTP + OLAP:
  OLTP queries → TiKV (row-based, fast point lookups)
  OLAP queries → TiFlash (columnar, fast aggregation)
  Auto-detect query type → route to correct engine!
```

```sql
-- MySQL compatible
CREATE TABLE orders (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    total DECIMAL(10,2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- OLTP: fast point query → routed to TiKV
SELECT * FROM orders WHERE id = 12345;

-- OLAP: analytics → routed to TiFlash
SELECT DATE(created_at) AS date, SUM(total) AS revenue
FROM orders
WHERE created_at > '2024-01-01'
GROUP BY DATE(created_at);
```

---

## 6. So sánh NewSQL

| | CockroachDB | Spanner | TiDB | YugabyteDB |
|---|---|---|---|---|
| Compatibility | PostgreSQL | Custom SQL | MySQL | PostgreSQL |
| Consensus | Raft | Paxos | Raft | Raft |
| Clock | Hybrid-logical | TrueTime | TSO (centralized) | Hybrid-logical |
| HTAP | No | No | **Yes** (TiFlash) | No |
| Open-source | BSL → Apache | No (Cloud only) | Apache 2.0 | Apache 2.0 |
| Managed | CockroachDB Cloud | Cloud Spanner | TiDB Cloud | Yugabyte Cloud |
| Best for | Global ACID | Google-scale | HTAP, MySQL shops | PG compatibility |

---

## 7. Consensus Algorithms — Tại sao quan trọng

```
Distributed DB cần nodes AGREE on data → Consensus

Paxos (Spanner):
  Original consensus algorithm (Lamport, 1989)
  Complex, hard to implement
  Variants: Multi-Paxos, Fast Paxos

Raft (CockroachDB, TiDB):
  Simplified Paxos (2014)
  Leader-based: Leader nhận writes → replicate to followers
  
  Term 1: [Leader A] → [Follower B] → [Follower C]
  Leader A dies:
  Term 2: [Dead A] → [Leader B] → [Follower C]  (B elected)

  Write flow:
  1. Client → Leader: "INSERT ..."
  2. Leader → append to log → send to followers
  3. Majority (2/3) ACK → "committed"
  4. Leader → Client: "OK"
  5. Follower C nhận late → catch up eventually

  → Tolerates: (N-1)/2 node failures
  → 3 nodes → 1 failure OK
  → 5 nodes → 2 failures OK
```

---

## 8. Migration Path: PostgreSQL → Distributed SQL

```
Phase 1: PostgreSQL (single node)
  Good for: 0 → ~500GB, ~10K TPS

Phase 2: PostgreSQL + Read Replicas
  Good for: ~500GB → 2TB, ~50K TPS (reads)
  
Phase 3: PostgreSQL + Citus (sharding extension)
  Good for: ~2TB → 10TB, distributed queries
  Advantage: Still PostgreSQL, minimal code changes

Phase 4: CockroachDB (if need global distribution)
  Good for: >10TB, multi-region, global consistency
  Migration: pg_dump → cockroach import (most SQL compatible)

★ Key insight: Hầu hết companies KHÔNG BAO GIỜ cần Phase 4
  PostgreSQL + Citus handles 95% of scale requirements
  Only move to CockroachDB if truly need multi-region ACID
```

---

## 📝 Bài tập

1. So sánh chi tiết: CockroachDB vs PostgreSQL + Citus cho e-commerce 10M users
2. Implement basic Raft consensus bằng Python (leader election + log replication)
3. Setup CockroachDB 3-node cluster (Docker), test failover
4. Viết decision record: khi nào từ PostgreSQL migrate sang CockroachDB?

---

## 📚 Tài liệu
- *Designing Data-Intensive Applications* — Kleppmann (Ch.5, 7, 9) ⭐
- [CockroachDB Architecture](https://www.cockroachlabs.com/docs/stable/architecture/overview.html)
- [Raft Consensus Visualization](https://thesecretlivesofdata.com/raft/)
- [Spanner Paper](https://research.google/pubs/pub39966/) — Google Research
- *Database Internals* — Alex Petrov (Ch.12-14)
