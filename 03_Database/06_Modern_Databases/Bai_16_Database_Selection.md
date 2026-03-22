# Bài 16: Database Selection & Polyglot Persistence — Kỹ năng #1 của CTO

## 🎯 Mục tiêu
- Framework chọn database đúng cho từng bài toán
- Polyglot persistence — dùng nhiều DB trong 1 hệ thống
- Trade-offs & decision matrix
- Real-world case studies

---

## 1. Tại sao chọn Database là quyết định quan trọng nhất?

```
Chọn sai database → hệ quả:
  ❌ Re-architecture sau 2 năm → tốn $$$, mất 6 tháng
  ❌ Performance problems không giải quyết được bằng optimize
  ❌ Team phải học technology mới giữa chừng
  ❌ Data migration pain, potential data loss

CTO/Staff phải trả lời:
  "Tại sao chọn PostgreSQL thay vì MongoDB cho service này?"
  → Không phải "vì quen dùng" mà phải có REASONING rõ ràng
```

---

## 2. Decision Framework — 7 câu hỏi

```
Trước khi chọn database, trả lời 7 câu hỏi:

Q1: Data model là gì?
    → Relational (tables, JOINs) → PostgreSQL, MySQL
    → Document (nested JSON) → MongoDB
    → Key-Value (simple lookup) → Redis, DynamoDB
    → Wide-Column (time-series) → Cassandra, ScyllaDB
    → Graph (relationships) → Neo4j, Neptune
    → Search (full-text) → Elasticsearch
    → Vector (embeddings) → pgvector, Pinecone

Q2: Read/Write ratio?
    → Read-heavy (100:1) → PostgreSQL + Redis cache
    → Write-heavy (1:100) → Cassandra, time-series DB
    → Balanced → PostgreSQL, MongoDB

Q3: Consistency requirement?
    → Strong consistency (banking) → PostgreSQL, CockroachDB
    → Eventual consistency OK (social feed) → Cassandra, MongoDB
    → Tunable → CockroachDB, MongoDB

Q4: Scale requirement?
    → Single server OK (<1TB) → PostgreSQL
    → Horizontal scale needed → CockroachDB, Cassandra, MongoDB
    → Global distribution → Spanner, CockroachDB

Q5: Query patterns?
    → Ad-hoc queries, complex JOINs → PostgreSQL
    → Known queries, denormalized → MongoDB, Cassandra
    → Full-text search → Elasticsearch
    → Graph traversal → Neo4j
    → Real-time aggregation → ClickHouse, Druid

Q6: Operational complexity tolerance?
    → Managed service preferred → RDS, Atlas, Aiven
    → Team có DBA experience → Self-managed
    → Startup, ít người → Managed + simple stack

Q7: Budget & team expertise?
    → Team biết SQL → PostgreSQL (safe default)
    → Cloud-native → DynamoDB/Firestore (serverless)
    → Enterprise budget → Oracle, Spanner
```

---

## 3. The "PostgreSQL First" Strategy

```
Rule of thumb cho MOST startups và mid-size companies:

"Start with PostgreSQL, add specialized DBs when needed"

PostgreSQL handles:
  ✅ Relational data (ACID, JOINs, constraints)
  ✅ JSON data (JSONB — almost as good as MongoDB)
  ✅ Full-text search (tsvector — good enough for most)
  ✅ Key-value (HSTORE extension)
  ✅ Time-series (TimescaleDB extension)
  ✅ Vector search (pgvector extension)
  ✅ Geospatial (PostGIS extension)
  ✅ Graph queries (recursive CTE, Apache AGE extension)
  ✅ Pub/sub (LISTEN/NOTIFY)

Khi nào THÊM specialized DB:
  → Redis: khi cần sub-millisecond cache, rate limiting
  → Elasticsearch: khi PostgreSQL full-text search không đủ (>10M docs phức tạp)
  → Kafka: khi cần event streaming, CDC
  → ClickHouse: khi analytics queries quá chậm trên PostgreSQL
  → Neo4j: khi có graph queries phức tạp (>3 hops)
```

### Ví dụ: E-commerce platform evolution
```
Giai đoạn 1 (0-100K users): 
  PostgreSQL only
  → Products, orders, users, search tất cả trong PG

Giai đoạn 2 (100K-1M users):
  PostgreSQL + Redis
  → Redis: session cache, product cache, rate limiting

Giai đoạn 3 (1M-10M users):
  PostgreSQL + Redis + Elasticsearch
  → ES: product search với facets, autocomplete

Giai đoạn 4 (10M+ users):
  PostgreSQL + Redis + Elasticsearch + Kafka + ClickHouse
  → Kafka: order events, inventory sync
  → ClickHouse: analytics dashboard
```

---

## 4. Database Decision Matrix

```
┌─────────────┬──────────┬──────────┬────────┬──────────┬───────────┐
│ Use Case    │ Primary  │ Cache    │ Search │ Analytics│ Streaming │
├─────────────┼──────────┼──────────┼────────┼──────────┼───────────┤
│ E-commerce  │ PG       │ Redis    │ ES     │ CH       │ Kafka     │
│ Social      │ PG       │ Redis    │ ES     │ CH       │ Kafka     │
│ Chat/Msg    │ Cassandra│ Redis    │ ES     │ CH       │ Kafka     │
│ IoT         │ TS-DB    │ Redis    │ -      │ CH       │ Kafka     │
│ FinTech     │ PG/CRDB  │ Redis    │ -      │ PG       │ Kafka     │
│ CMS/Blog    │ PG       │ Redis    │ ES     │ -        │ -         │
│ Gaming      │ PG       │ Redis    │ -      │ CH       │ Kafka     │
│ AI/ML App   │ PG+pgv   │ Redis    │ -      │ -        │ -         │
└─────────────┴──────────┴──────────┴────────┴──────────┴───────────┘

PG = PostgreSQL, ES = Elasticsearch, CH = ClickHouse
CRDB = CockroachDB, TS-DB = TimescaleDB, pgv = pgvector
```

---

## 5. Polyglot Persistence Pattern

```
                    ┌──────────────────────────┐
                    │     API Gateway           │
                    └──────────┬───────────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                     │
    ┌─────▼─────┐      ┌──────▼──────┐      ┌──────▼──────┐
    │ User Svc  │      │ Product Svc │      │ Order Svc   │
    │ (PG)      │      │ (PG + ES)   │      │ (PG + Kafka)│
    └─────┬─────┘      └──────┬──────┘      └──────┬──────┘
          │                    │                     │
    ┌─────▼─────┐      ┌──────▼──────┐      ┌──────▼──────┐
    │PostgreSQL │      │PostgreSQL   │      │PostgreSQL   │
    │(users)    │      │(products)   │      │(orders)     │
    └───────────┘      │Elasticsearch│      │Kafka        │
                       │(search)     │      │(events)     │
                       └─────────────┘      └─────────────┘

Rules:
1. Mỗi service OWN data của mình (không share DB)
2. Primary source of truth = 1 DB per service
3. Sync data giữa DBs qua events/CDC (not direct queries)
4. Accept eventual consistency between services
```

---

## 6. Anti-patterns — Sai lầm thường gặp

```
❌ Anti-pattern 1: "MongoDB for everything"
   → Khi cần JOINs phức tạp, transactions → nightmare
   → Fix: Dùng PostgreSQL cho core data

❌ Anti-pattern 2: "Premature optimization — sharding từ đầu"
   → 10K users không cần sharding
   → Fix: Scale vertically first, shard khi THỰC SỰ cần

❌ Anti-pattern 3: "Redis as primary database"
   → Redis mất data nếu crash (even with persistence)
   → Fix: Redis là CACHE, PostgreSQL là source of truth

❌ Anti-pattern 4: "Shared database between microservices"
   → Tight coupling, schema changes break other services
   → Fix: Each service owns its DB, communicate via APIs/events

❌ Anti-pattern 5: "Choosing tech because it's trendy"
   → "Let's use Cassandra" when PostgreSQL works fine
   → Fix: Boring technology is usually the right choice

❌ Anti-pattern 6: "Not planning for data migration"
   → Stuck with wrong DB because migration too expensive
   → Fix: Abstract data layer, plan migration path from day 1
```

---

## 7. CTO Decision Template

```markdown
## Database Decision Record

**Service:** Order Management Service
**Date:** 2024-01-15
**Decision maker:** [Your name]

### Context
- Expected 50K orders/day, growing 3x/year
- Need strong consistency (money involved)
- Complex queries: reports, analytics, search
- Team has strong PostgreSQL experience

### Options Considered
| Option | Pros | Cons |
|--------|------|------|
| PostgreSQL | ACID, team experience, extensions | Single-node limit |
| MongoDB | Flexible schema | Weak transactions, team learning |
| CockroachDB | Distributed ACID | Operational complexity, cost |

### Decision
PostgreSQL with read replicas

### Reasoning
- Strong consistency required → eliminates MongoDB
- Current scale (<1TB) fits single PostgreSQL
- Team expertise reduces operational risk
- Read replicas handle analytics queries
- Migration path to CockroachDB if scale demands

### Review date
Re-evaluate in 12 months or when orders > 500K/day
```

---

## 8. Real-World Case Studies

### Uber: PostgreSQL → MySQL → Schemaless (Custom)
```
Problem: PostgreSQL MVCC bloat with high write volume
Solution: Built custom storage on MySQL (simpler replication)
Lesson: Đôi khi generic DB không fit extreme workloads
         Nhưng 99% companies KHÔNG phải Uber
```

### Discord: Cassandra → ScyllaDB
```
Problem: Cassandra GC pauses, latency spikes
Solution: ScyllaDB (C++ rewrite of Cassandra, no GC)
Lesson: Same data model nhưng different implementation
```

### Shopify: MySQL + Redis + Kafka + Elasticsearch
```
Architecture:
  MySQL: orders, products (sharded by shop_id)
  Redis: sessions, caching, job queues
  Elasticsearch: product search
  Kafka: event streaming, CDC
Lesson: Classic polyglot persistence done right
```

---

## 📝 Bài tập

1. Viết Database Decision Record cho 3 scenarios: (a) Chat app, (b) IoT platform, (c) FinTech payment
2. Design polyglot persistence cho food delivery platform
3. Đánh giá hệ thống hiện tại của bạn: đúng DB choice chưa?
4. Lập migration plan: từ MongoDB sang PostgreSQL cho e-commerce

---

## 📚 Tài liệu
- *Designing Data-Intensive Applications* — Martin Kleppmann (Ch.2-3) ⭐
- *Database Internals* — Alex Petrov (Ch.1)
- [DB-Engines Ranking](https://db-engines.com/en/ranking)
- *Architecture Decision Records* — Michael Nygard
