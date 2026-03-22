# Bài 05: Event-Driven Architecture

## 🎯 Mục tiêu
- Event Sourcing, CQRS
- Choreography vs Orchestration
- Outbox pattern, idempotency

---

## 1. Event Sourcing

```
Thay vì lưu state hiện tại → lưu TẤT CẢ events

Traditional: orders table → {id:1, status:"shipped", total:100}
Event Sourcing: events table →
  1. OrderCreated  {id:1, items:[...], total:100}
  2. PaymentReceived {id:1, amount:100}
  3. OrderConfirmed {id:1}
  4. OrderShipped {id:1, tracking:"ABC"}

Rebuild state: replay events 1→4
Time travel: replay events 1→2 → state at that point
```

```python
class Order:
    def __init__(self):
        self.status = None
        self.events = []
    
    def apply(self, event):
        handler = getattr(self, f"_on_{event.type}", None)
        if handler:
            handler(event)
        self.events.append(event)
    
    def _on_order_created(self, event):
        self.id = event.data["id"]
        self.items = event.data["items"]
        self.status = "pending"
    
    def _on_order_confirmed(self, event):
        self.status = "confirmed"
    
    @staticmethod
    def from_events(events):
        order = Order()
        for event in events:
            order.apply(event)
        return order
```

---

## 2. CQRS (Command Query Responsibility Segregation)

```
Command (Write):
  API → Command Handler → Domain Model → Event Store
                                        → Publish Event

Query (Read):
  Event → Projector → Read Model (denormalized)
  API → Query Handler → Read Model → Response

Write DB: Event Store (append-only, normalized)
Read DB: Materialized views (Elasticsearch, Redis, PostgreSQL views)
```

---

## 3. Saga Patterns

### Choreography (Event-driven)
```
OrderService publishes OrderCreated
  → PaymentService listens → charges → publishes PaymentCompleted
    → InventoryService listens → reserves → publishes StockReserved
      → ShippingService listens → ships → publishes OrderShipped

Compensation (on failure):
  PaymentFailed event
    → OrderService listens → cancels order
    → InventoryService listens → releases stock
```

### Orchestration (Central coordinator)
```python
class OrderSagaOrchestrator:
    def execute(self, order):
        self.state = "STARTED"
        
        try:
            payment = self.payment_service.charge(order.total)
            self.state = "PAYMENT_DONE"
            
            inventory = self.inventory_service.reserve(order.items)
            self.state = "INVENTORY_RESERVED"
            
            self.shipping_service.schedule(order)
            self.state = "COMPLETED"
        except InventoryError:
            self.payment_service.refund(payment.id)  # compensate
            self.state = "COMPENSATED"
        except PaymentError:
            self.state = "FAILED"
```

---

## 4. Outbox Pattern (Reliable Event Publishing)

```
Problem: DB write + event publish → dual write problem
  DB commit success + event publish fails → inconsistency

Solution: Outbox table in same DB transaction

BEGIN;
  INSERT INTO orders (...) VALUES (...);
  INSERT INTO outbox (event_type, payload) VALUES ('OrderCreated', '{...}');
COMMIT;

-- Background worker polls outbox → publishes to Kafka → marks as sent
```

---

## 5. Idempotent Event Consumers

```python
def handle_payment_completed(event):
    # Dedup by event_id
    if db.exists("SELECT 1 FROM processed_events WHERE event_id = %s", event.id):
        return  # already processed
    
    db.begin()
    update_order_status(event.order_id, "paid")
    db.insert("INSERT INTO processed_events (event_id) VALUES (%s)", event.id)
    db.commit()
```

---

## 📝 Bài tập

1. Implement Event Sourcing cho Order aggregate
2. Build Saga (choreography) cho Order → Payment → Shipping
3. Implement Outbox pattern với PostgreSQL + background worker
4. CQRS: separate write model (PostgreSQL) and read model (Elasticsearch)

---

## 📚 Tài liệu
- *Building Event-Driven Microservices* — Adam Bellemare
- *Microservices Patterns* — Chris Richardson (Ch.4-5)
