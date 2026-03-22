# Bài 09: Distributed Systems Fundamentals

## 🎯 Mục tiêu
- Hiểu challenges of distributed systems
- Consensus algorithms (Raft, Paxos)
- Distributed transactions (2PC, Saga)
- Consistency models

---

## 1. Challenges of Distributed Systems

```
Fallacies of Distributed Computing (Peter Deutsch):
1. Network is reliable           → Packets drop, timeout
2. Latency is zero               → Cross-DC: 50-100ms
3. Bandwidth is infinite          → Bottlenecks exist
4. Network is secure              → Always assume insecure
5. Topology doesn't change        → Servers added/removed
6. There is one administrator     → Multiple teams
7. Transport cost is zero         → Serialization, network I/O
8. Network is homogeneous         → Different OS, versions
```

### Failure Modes
```
Crash failure:     Node stops responding (easy to detect)
Byzantine failure: Node sends wrong/conflicting data (hardest)
Network partition: Nodes can't communicate with each other
Slow node:        Response extremely slow (is it dead or slow?)
```

---

## 2. Consistency Models

### Strong Consistency
```
Write X=5 → immediately all reads return X=5
→ Linearizability: giống single-server behavior
→ Expensive: require coordination (quorum writes)
Use: Banking, inventory count
```

### Eventual Consistency
```
Write X=5 → some reads may return old value for a while
→ Eventually all reads return X=5 (convergence time ~ms to ~seconds)
Use: Social media likes, view counts, DNS
```

### Causal Consistency
```
If A causes B, then everyone sees A before B
But concurrent events can be seen in different order
Use: Comments thread (reply must appear after parent)
```

---

## 3. Consensus — Raft Algorithm

```
Raft: Leader-based consensus cho replicated state machines

Nodes: Leader (1) + Followers (N)

1. Leader Election:
   - Follower timeout → becomes Candidate
   - Candidate requests votes from all nodes
   - Majority vote → becomes Leader
   - Leader sends heartbeats to maintain authority

2. Log Replication:
   Client → Leader: "SET x=5"
   Leader → append to log → replicate to Followers
   Majority ACK → Leader commits → notify Followers to commit
   Leader responds to Client: "OK"
```

```
Term 1: [Leader A] ── heartbeat → [Follower B, C, D, E]
                                   
A dies...

Term 2: [Candidate C] → requests votes → B,D,E vote YES
         C becomes Leader
```

### Quorum
```
N=5 nodes, Quorum = N/2 + 1 = 3

Write: succeed khi ≥3 nodes ACK
Read:  read từ ≥3 nodes → guaranteed to see latest write

Tolerate: (N-1)/2 = 2 failures
→ 5 nodes tolerate 2 failures
→ 3 nodes tolerate 1 failure
```

---

## 4. Distributed Transactions

### 2PC (Two-Phase Commit)
```
Phase 1 — Prepare:
  Coordinator → all participants: "Can you commit?"
  Participants: lock resources, write to WAL, reply YES/NO

Phase 2 — Commit/Abort:
  If ALL yes → Coordinator: "COMMIT"  → all commit
  If ANY no  → Coordinator: "ABORT"   → all rollback

❌ Problems:
  - Blocking: participants hold locks waiting for coordinator
  - Single point of failure: coordinator crash → stuck
  - Not partition tolerant
```

### Saga Pattern ⭐ (Preferred for microservices)
```
Saga = sequence of local transactions + compensating actions

Order Saga:
  T1: Create Order (pending)
  T2: Reserve Inventory
  T3: Process Payment
  T4: Confirm Order

If T3 fails:
  C2: Release Inventory (compensate T2)
  C1: Cancel Order (compensate T1)
```

```python
# Choreography-based Saga (event-driven)
# Mỗi service listen event và trigger next step

class OrderService:
    def create_order(self, order):
        db.save(order, status="PENDING")
        event_bus.publish("OrderCreated", order)

class InventoryService:
    def on_order_created(self, event):
        if reserve_stock(event.items):
            event_bus.publish("StockReserved", event)
        else:
            event_bus.publish("StockReservationFailed", event)

class PaymentService:
    def on_stock_reserved(self, event):
        if charge(event.total):
            event_bus.publish("PaymentCompleted", event)
        else:
            event_bus.publish("PaymentFailed", event)

# Compensating actions
class InventoryService:
    def on_payment_failed(self, event):
        release_stock(event.items)  # Compensate
```

```python
# Orchestrator-based Saga (centralized coordinator)
class OrderSaga:
    def execute(self, order):
        try:
            order_id = order_service.create(order)
            inventory_service.reserve(order.items)
            payment_service.charge(order.total)
            order_service.confirm(order_id)
        except PaymentError:
            inventory_service.release(order.items)
            order_service.cancel(order_id)
        except InventoryError:
            order_service.cancel(order_id)
```

---

## 5. Clocks & Ordering

```
Physical clocks: NTP sync, nhưng clock skew ~ms
→ Không tin tưởng cho ordering events

Logical clocks:
  Lamport Clock: counter tăng mỗi event
  Vector Clock: [A:3, B:2, C:1] → detect concurrent events

→ Dùng Lamport/Vector clocks cho event ordering
→ Hybrid Logical Clock (HLC): combine physical + logical
```

---

## 6. Idempotency in Distributed Systems

```python
# Network failure → client retry → duplicate request
# Solution: Idempotency key

def transfer_money(request):
    idempotency_key = request.headers['Idempotency-Key']
    
    # Check if already processed
    existing = db.query(
        "SELECT * FROM transactions WHERE idempotency_key = %s",
        idempotency_key
    )
    if existing:
        return existing.result  # Return cached result
    
    # Process and store result
    result = execute_transfer(request)
    db.insert("INSERT INTO transactions (idempotency_key, result) VALUES (%s, %s)",
              idempotency_key, result)
    return result
```

---

## 📝 Bài tập

1. Implement Raft leader election simulator bằng Python
2. Implement Saga pattern cho Order → Payment → Shipping
3. Giải thích: tại sao 2PC không phù hợp cho microservices?
4. Implement Vector Clock bằng Python, test concurrent events

---

## 📚 Tài liệu
- *Designing Data-Intensive Applications* — Martin Kleppmann (Ch.8-9)
- [The Raft Consensus Algorithm](https://raft.github.io/)
- *Distributed Systems* — Maarten van Steen
