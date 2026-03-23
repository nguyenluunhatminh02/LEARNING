# Bài 19: CDC, Event Sourcing & Streaming — Data in Motion

## 🎯 Mục tiêu
- Change Data Capture (CDC) — Debezium
- Event Sourcing pattern
- Apache Kafka as data backbone
- CQRS (Command Query Responsibility Segregation)

## 📖 Câu chuyện đời thường
> Bạn có một sổ tài khoản ngân hàng (database). **CDC** giống như dịch vụ thông báo SMS mỗi lần có giao dịch: khi số dư thay đổi, hệ thống tự động gửi thông báo cho các app khác (analytics, search, cache). **Event Sourcing** giống sổ cái kế toán: thay vì chỉ ghi "số dư: 10 triệu", bạn ghi mọi giao dịch: "+5tr, -2tr, +7tr" — bất cứ lúc nào cũng tính lại được, và biết chính xác chuyện gì đã xảy ra. **CQRS** giống như tách quầy gửi tiền và quầy tra cứu: quầy gửi (write) cần chính xác, quầy tra (read) cần nhanh — 2 quầy tối ưu khác nhau.

---

## 1. Tại sao cần CDC?

```
Vấn đề thực tế:

Bạn có PostgreSQL (source of truth) và muốn:
  → Elasticsearch (search index) luôn sync
  → Redis cache invalidate khi data thay đổi
  → Data Warehouse nhận data mới
  → Microservice khác biết khi order tạo mới

Cách truyền thống (BAD):
  ❌ Dual write: app viết vào PG + ES → inconsistent khi 1 fails
  ❌ Polling: "SELECT * WHERE updated_at > ?" mỗi 5s → wasteful, delay
  ❌ Trigger + queue: PG trigger → insert queue table → consumer → complex

Cách đúng → CDC:
  ✅ Đọc transaction log (WAL) → stream changes ra ngoài
  ✅ Guaranteed delivery (not miss changes)
  ✅ Low latency (near real-time)
  ✅ No impact on source DB performance
```

---

## 2. Debezium — CDC Platform

```
Debezium = Distributed CDC platform built on Kafka Connect

PostgreSQL WAL → Debezium → Kafka → Consumers (ES, Redis, DW)

  ┌──────────┐    ┌──────────┐    ┌─────────┐    ┌──────────────┐
  │PostgreSQL│──→ │ Debezium │──→ │  Kafka  │──→ │Elasticsearch │
  │  (WAL)   │    │ Connector│    │  Topic  │──→ │Redis Cache   │
  │          │    │          │    │         │──→ │Data Warehouse│
  └──────────┘    └──────────┘    └─────────┘    └──────────────┘

Mỗi thay đổi trong PG → event trên Kafka topic:
  INSERT → {"op": "c", "after": {"id": 1, "name": "Alice"}}
  UPDATE → {"op": "u", "before": {...}, "after": {...}}
  DELETE → {"op": "d", "before": {"id": 1, "name": "Alice"}}
```

### Setup Debezium
```json
// Register Debezium PostgreSQL connector
// POST http://localhost:8083/connectors
{
  "name": "pg-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "database.hostname": "postgres",
    "database.port": "5432",
    "database.user": "debezium",
    "database.password": "secret",
    "database.dbname": "mydb",
    "database.server.name": "myserver",
    "table.include.list": "public.orders,public.products",
    "plugin.name": "pgoutput",
    "slot.name": "debezium_slot",
    "publication.name": "dbz_publication"
  }
}
```

### Consumer: Kafka → Elasticsearch
```python
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

consumer = KafkaConsumer(
    'myserver.public.products',  # topic = server.schema.table
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='es-sync-group'
)

es = Elasticsearch("http://localhost:9200")

for message in consumer:
    payload = message.value['payload']
    op = payload['op']
    
    if op in ('c', 'u'):  # create or update
        doc = payload['after']
        es.index(index='products', id=doc['id'], body=doc)
    elif op == 'd':  # delete
        doc = payload['before']
        es.delete(index='products', id=doc['id'], ignore=[404])
```

---

## 3. Apache Kafka — Hiểu sâu hơn "just messaging"

```
Kafka KHÔNG CHỈ là message queue. Kafka là DISTRIBUTED COMMIT LOG.

┌──────────────────────────────────────────────────────────┐
│ Topic: "orders"                                           │
│                                                           │
│ Partition 0: [msg0] [msg1] [msg2] [msg3] [msg4] ...     │
│ Partition 1: [msg0] [msg1] [msg2] [msg3] ...            │
│ Partition 2: [msg0] [msg1] [msg2] ...                   │
│                                                           │
│ Ordering: guaranteed WITHIN partition                     │
│ Retention: configurable (7 days default, can be forever) │
│ Replay: consumers can re-read from any offset            │
└──────────────────────────────────────────────────────────┘

Key properties:
  ✅ Durable: data persisted to disk, replicated
  ✅ Ordered: within partition
  ✅ Replayable: consumer can go back in time
  ✅ Scalable: add partitions/brokers
  ✅ Multi-consumer: multiple groups read independently
```

### Kafka as Database?
```
"Kafka is the new database of record" — Martin Kleppmann

Log compaction: keep only LATEST value per key
  Key: user_1 → {name: "Alice"}
  Key: user_1 → {name: "Alice Nguyen"}  (overwrites previous)
  Key: user_2 → {name: "Bob"}

After compaction:
  Key: user_1 → {name: "Alice Nguyen"}  (latest only)
  Key: user_2 → {name: "Bob"}

→ Kafka topic = materialized view of current state!
→ Used by: Uber (trip data), LinkedIn (profile updates)

Kafka Streams / ksqlDB: real-time processing
  CREATE STREAM orders_stream AS
  SELECT user_id, SUM(total) AS total_spent
  FROM orders
  GROUP BY user_id
  EMIT CHANGES;
```

---

## 4. Event Sourcing

```
Traditional: Store CURRENT STATE
  users table: {id: 1, balance: 150}

Event Sourcing: Store ALL EVENTS
  events table:
    {type: "AccountCreated", user_id: 1, balance: 0, timestamp: T1}
    {type: "Deposited",      user_id: 1, amount: 200, timestamp: T2}
    {type: "Withdrawn",      user_id: 1, amount: 50,  timestamp: T3}
  
  Current state = replay all events:
    0 (created) + 200 (deposit) - 50 (withdrawal) = 150

Advantages:
  ✅ Full audit trail (ai làm gì, lúc nào)
  ✅ Time travel: rebuild state at any point in time
  ✅ Debug: replay events to reproduce bugs
  ✅ Analytics: historical data preserved forever
  ✅ Undo: reverse events

Disadvantages:
  ❌ Complexity: query current state = replay or use snapshot
  ❌ Event schema evolution (versioning events)
  ❌ Eventually consistent views
  ❌ Storage: events grow forever
```

### Event Sourcing Implementation
```python
# Event Store
class EventStore:
    def __init__(self):
        self.events = []  # Thực tế: dùng PostgreSQL hoặc EventStoreDB
    
    def append(self, aggregate_id, event_type, data):
        event = {
            "aggregate_id": aggregate_id,
            "event_type": event_type,
            "data": data,
            "timestamp": datetime.utcnow(),
            "version": self._next_version(aggregate_id)
        }
        self.events.append(event)
        return event
    
    def get_events(self, aggregate_id):
        return [e for e in self.events if e["aggregate_id"] == aggregate_id]

# Aggregate: rebuild state from events
class BankAccount:
    def __init__(self, account_id, event_store):
        self.account_id = account_id
        self.balance = 0
        self.store = event_store
        self._replay_events()
    
    def _replay_events(self):
        for event in self.store.get_events(self.account_id):
            self._apply(event)
    
    def _apply(self, event):
        if event["event_type"] == "Deposited":
            self.balance += event["data"]["amount"]
        elif event["event_type"] == "Withdrawn":
            self.balance -= event["data"]["amount"]
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        event = self.store.append(self.account_id, "Deposited", {"amount": amount})
        self._apply(event)
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        event = self.store.append(self.account_id, "Withdrawn", {"amount": amount})
        self._apply(event)

# Snapshot: optimize replay performance
# Mỗi 100 events → save snapshot {balance: 150, version: 100}
# Rebuild: load snapshot → replay events since version 100
```

---

## 5. CQRS — Command Query Responsibility Segregation

```
Traditional: 1 model cho cả READ và WRITE

CQRS: Tách READ model và WRITE model

  ┌──────────┐    Commands     ┌──────────────┐
  │          │───────────────→ │ Write Model  │
  │  Client  │                 │ (PostgreSQL) │
  │          │    Queries      │     │        │
  │          │←────────────── ┌▼─────▼────────┐
  └──────────┘                │ Read Model    │
                              │(Elasticsearch)│
                              │(Redis Cache)  │
                              │(Denormalized) │
                              └───────────────┘

Write Model (Commands):
  - Normalized, strong consistency
  - Handles business rules, validation
  - PostgreSQL with ACID

Read Model (Queries):
  - Denormalized, optimized for reads
  - Multiple read stores for different queries
  - Eventually consistent (synced via events/CDC)

Example: E-commerce
  Write: INSERT INTO orders → PostgreSQL
  Event: "OrderCreated" → Kafka
  Read projections:
    → Elasticsearch: order search
    → Redis: user's recent orders cache
    → ClickHouse: analytics dashboard
```

### CQRS + Event Sourcing
```
              Commands          Events           Read Models
  ┌────────┐           ┌─────────────┐          ┌───────────┐
  │ Client │──────────→│ Event Store │─────────→│ View 1    │ (PG denormalized)
  │        │           │ (immutable  │─────────→│ View 2    │ (Elasticsearch)
  │        │←──queries─│  append-only)│─────────→│ View 3    │ (Redis)
  └────────┘           └─────────────┘          └───────────┘

  Write: append event to event store
  Projectors: consume events → update read models
  Query: read from optimized read model

★ Khi nào dùng CQRS + Event Sourcing?
  ✅ Financial systems (audit trail bắt buộc)
  ✅ Complex domain with many read patterns
  ✅ High read:write ratio (100:1)
  ❌ Simple CRUD apps → overkill
  ❌ Small team → too much complexity
```

---

## 6. Practical: Outbox Pattern

```
Problem: "Lưu vào DB + publish event" — làm sao đảm bảo cả 2?

❌ Bad:
  BEGIN;
  INSERT INTO orders (...);
  COMMIT;
  kafka.publish("OrderCreated");  # ← Fails? Event lost!

❌ Also bad:
  kafka.publish("OrderCreated");  # ← Succeeds
  BEGIN;
  INSERT INTO orders (...);       # ← Fails? Ghost event!

✅ Outbox Pattern:
  BEGIN;
  INSERT INTO orders (...);
  INSERT INTO outbox (event_type, payload) VALUES ('OrderCreated', '{...}');
  COMMIT;  # Both in same transaction → atomic!

  # Separate process: poll outbox → publish to Kafka → mark as sent
  # Or: CDC on outbox table → Debezium → Kafka (better!)

  ┌──────────┐  same tx  ┌──────────┐  CDC   ┌───────┐
  │ orders   │←─────────→│ outbox   │──────→ │ Kafka │
  └──────────┘           └──────────┘        └───────┘
```

```sql
-- Outbox table
CREATE TABLE outbox (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(50) NOT NULL,  -- 'Order', 'User'
    aggregate_id VARCHAR(50) NOT NULL,
    event_type VARCHAR(50) NOT NULL,      -- 'OrderCreated'
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    published_at TIMESTAMPTZ             -- NULL = not yet published
);

-- In application:
BEGIN;
INSERT INTO orders (user_id, total) VALUES (1, 100) RETURNING id;
INSERT INTO outbox (aggregate_type, aggregate_id, event_type, payload)
VALUES ('Order', '123', 'OrderCreated', '{"order_id": 123, "total": 100}');
COMMIT;

-- Publisher (poll-based):
-- SELECT * FROM outbox WHERE published_at IS NULL ORDER BY created_at LIMIT 100;
-- Publish to Kafka → UPDATE outbox SET published_at = NOW() WHERE id = ?;
```

---

## 7. Khi nào dùng gì?

```
Simple sync (PG → ES):
  → CDC (Debezium) — most common, reliable

Audit trail required:
  → Event Sourcing — full history

Microservice communication:
  → Kafka events — async, decoupled

Multiple read patterns:
  → CQRS — separate read/write models

Reliable "save + publish":
  → Outbox Pattern — transactional guarantee
```

---

## 📝 Bài tập

1. Setup Debezium: PostgreSQL → Kafka → Elasticsearch pipeline
2. Implement Event Sourcing cho banking account (deposit/withdraw)
3. Implement Outbox Pattern cho order service
4. Design CQRS architecture cho e-commerce: write model + 3 read models

---

## 📚 Tài liệu
- *Designing Data-Intensive Applications* — Kleppmann (Ch.11-12) ⭐
- [Debezium Documentation](https://debezium.io/documentation/)
- *Building Event-Driven Microservices* — Adam Bellemare
- [Event Sourcing pattern — Microsoft](https://learn.microsoft.com/en-us/azure/architecture/patterns/event-sourcing)
- *Kafka: The Definitive Guide* — 2nd Edition
