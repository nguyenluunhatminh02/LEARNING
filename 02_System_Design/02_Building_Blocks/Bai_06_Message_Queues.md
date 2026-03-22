# Bài 06: Message Queues & Event-Driven Architecture

## 🎯 Mục tiêu
- Hiểu Message Queue, khi nào cần dùng
- Kafka, RabbitMQ, SQS
- Event-driven vs Request-driven architecture
- Pub/Sub pattern, Event Sourcing

---

## 1. Tại sao cần Message Queue?

```
❌ Synchronous (tight coupling):
  User → [Order Service] → [Payment Service] → [Email Service] → [Inventory]
  Nếu Payment chậm → tất cả chờ. Nếu Email down → order fail!

✅ Asynchronous (loose coupling):
  User → [Order Service] → [Message Queue] → Payment Service
                                            → Email Service
                                            → Inventory Service
  Order Service respond ngay. Các service xử lý độc lập.
```

### Lợi ích
- **Decoupling**: Services không phụ thuộc nhau
- **Buffering**: Queue hấp thụ traffic spikes
- **Reliability**: Message persist, retry khi fail
- **Scalability**: Scale consumers độc lập

---

## 2. Message Queue Patterns

### 2.1 Point-to-Point (Queue)
```
Producer → [Queue] → Consumer
                   (1 message → 1 consumer)

Use case: Task processing, order processing
```

### 2.2 Pub/Sub (Topic)
```
Publisher → [Topic] → Subscriber 1 (Email)
                   → Subscriber 2 (Analytics)
                   → Subscriber 3 (Notification)
                   (1 message → N subscribers)

Use case: Event broadcasting, notifications
```

### 2.3 Fan-out
```
Service → [Exchange/Router] → Queue 1 (filter: type=ORDER)
                            → Queue 2 (filter: type=PAYMENT)
                            → Queue 3 (all messages)
```

---

## 3. Kafka — Distributed Event Streaming

```
┌──────────────────────────────────────────┐
│           Topic: "orders"                │
│  ┌──────────┬──────────┬──────────┐     │
│  │Partition 0│Partition 1│Partition 2│    │
│  │[0][1][2]  │[0][1]    │[0][1][2] │    │
│  └──────────┴──────────┴──────────┘     │
└──────────────────────────────────────────┘

Producer → Topic → Partition (by key hash) → Consumer Group
```

```python
# Kafka Producer
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode()
)

producer.send('orders', key=b'user_123', value={
    'order_id': 'ORD001',
    'items': [{'id': 1, 'qty': 2}],
    'total': 150.00
})

# Kafka Consumer
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'orders',
    group_id='payment-service',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode())
)

for message in consumer:
    process_order(message.value)
```

### Kafka Key Concepts
- **Topic**: Category cho messages
- **Partition**: Unit of parallelism (ordered within partition)
- **Consumer Group**: Mỗi partition chỉ 1 consumer trong group đọc
- **Offset**: Vị trí đọc của consumer (có thể replay)
- **Retention**: Giữ data N ngày (default 7 ngày)

---

## 4. RabbitMQ vs Kafka vs SQS

| | RabbitMQ | Kafka | AWS SQS |
|---|---|---|---|
| Model | Message Queue | Event Log | Message Queue |
| Ordering | Per-queue | **Per-partition** | Best-effort (FIFO available) |
| Throughput | ~50K msg/s | **~1M msg/s** | ~3K msg/s |
| Replay | ❌ (consumed = gone) | **✅** (offset-based) | ❌ |
| Routing | **Advanced** (exchange types) | Topic-based | Simple |
| Best for | Task queues, RPC | **Event streaming, logs** | Cloud-native, simple queue |

---

## 5. Delivery Guarantees

```
At-most-once:  Fire and forget      → Có thể mất message
At-least-once: Retry until ACK      → Có thể duplicate ⭐ Phổ biến
Exactly-once:  Dedup + Transaction  → Khó, performance thấp

→ Thực tế: At-least-once + Idempotent consumer
```

```python
# Idempotent consumer — xử lý duplicate
def process_payment(message):
    idempotency_key = message['order_id']
    
    # Check if already processed
    if redis.sismember('processed_orders', idempotency_key):
        return  # Skip duplicate
    
    # Process
    charge_customer(message)
    
    # Mark as processed
    redis.sadd('processed_orders', idempotency_key)
```

---

## 6. Event-Driven Architecture

### Event Sourcing
```
Thay vì lưu state hiện tại, lưu TẤT CẢ events:

Event Store:
  1. OrderCreated { id: 1, items: [...], total: 100 }
  2. OrderPaid    { id: 1, amount: 100 }
  3. OrderShipped { id: 1, tracking: "ABC" }
  4. OrderDelivered { id: 1 }

State tại bất kỳ thời điểm = replay events đến thời điểm đó
→ Full audit trail, có thể time travel
```

### CQRS (Command Query Responsibility Segregation)
```
Command (Write) → Event Store → Event Bus → Read Model (Query)

Write DB: Normalized, optimized for writes
Read DB:  Denormalized, optimized for reads (có thể dùng Elasticsearch)
```

---

## 📝 Bài tập

1. Setup Kafka cluster (Docker Compose) với 3 brokers, tạo topic, produce/consume
2. Implement order processing pipeline: Order → Payment → Notification
3. Implement idempotent consumer xử lý duplicate messages
4. So sánh: RabbitMQ vs Kafka cho use case email notification

---

## 📚 Tài liệu
- *Designing Data-Intensive Applications* — Martin Kleppmann (Ch.11)
- *Kafka: The Definitive Guide* — Narkhede, Shapira, Palino
- [Confluent Kafka Tutorials](https://developer.confluent.io/)
