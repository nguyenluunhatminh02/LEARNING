# Bài 13: Microservices Architecture

## 🎯 Mục tiêu
- Monolith vs Microservices trade-offs
- Service communication patterns
- Service discovery, circuit breaker
- Data management trong microservices

## 📖 Câu chuyện đời thường
> **Monolith** giống như một nhà hàng nhỏ: 1 bếp, 1 đầu bếp làm hết từ khai vị đến tráng miệng. Đơn giản nhưng khi đông khách, 1 người không xuể nổi. **Microservices** giống food court: quầy phở, quầy sữđi, quầy nước — mỗi quầy chuyên một món, hoạt động độc lập. Nếu quầy nước hỏng, khách vẫn ăn phở được. **Circuit Breaker** giống cầu dao điện: khi quầy nước liên tục hỏng, bạn tạm ngắt kết nối ("đừng gọi nước nữa, chờ họ sửa xong") thay vì để khách chờ mãi. **Service Discovery** giống bảng chỉ dẫn trong food court: quầy phở ở số 3, quầy nước ở số 7.

---

## 1. Monolith vs Microservices

```
Monolith:
┌────────────────────────────────────┐
│  [User Module] [Order] [Payment]  │
│  [Inventory] [Notification]        │
│  ─────── Shared Database ──────── │
└────────────────────────────────────┘
Single deployment unit

Microservices:
┌──────┐ ┌──────┐ ┌────────┐ ┌───────┐ ┌────────┐
│ User │ │Order │ │Payment │ │Invent.│ │Notif.  │
│  DB  │ │  DB  │ │   DB   │ │  DB   │ │  DB    │
└──────┘ └──────┘ └────────┘ └───────┘ └────────┘
Independent deployment, own database
```

### Khi nào dùng gì?

| | Monolith | Microservices |
|---|---|---|
| Team size | <10 developers | >20 developers |
| Complexity | Simple-medium | High complexity |
| Deploy | Simple (1 unit) | Complex (nhiều services) |
| Scaling | Scale toàn bộ | Scale từng service |
| Database | Shared, easy JOINs | Distributed, no JOINs |
| Latency | In-process calls (ns) | Network calls (ms) |
| **Start with** | ✅ Always start here | Migrate khi cần |

**Rule: Monolith first → Extract microservices khi team & complexity grow**

---

## 2. Service Communication

### Synchronous — REST / gRPC
```
Order Service → HTTP/gRPC → Payment Service
  + Simple, immediate response
  - Coupling: nếu Payment down → Order fail
  - Cascade failure risk
```

### Asynchronous — Message Queue ⭐
```
Order Service → Kafka/RabbitMQ → Payment Service
  + Decoupled, resilient
  + Buffer traffic spikes
  - Eventual consistency
  - Complex debugging
```

### Khi nào dùng gì?
```
Sync:  Cần response ngay (user-facing, queries)
Async: Fire-and-forget, long processing, event notification
```

---

## 3. Service Discovery

```
Problem: Service A cần gọi Service B, nhưng B có nhiều instances
         IP/port thay đổi liên tục (auto-scaling, failures)

Solution 1: Client-Side Discovery
  Service A → [Service Registry] → get B's addresses
  Service A → B (instance 2)
  Tools: Consul, Eureka

Solution 2: Server-Side Discovery
  Service A → [Load Balancer] → B (instance 2)
  LB queries registry automatically
  Tools: AWS ALB + ECS, Kubernetes Services

Solution 3: DNS-based
  Service A → DNS lookup "payment.service.local" → IP:Port
  Tools: Consul DNS, CoreDNS (K8s)
```

```yaml
# Kubernetes Service Discovery (built-in)
apiVersion: v1
kind: Service
metadata:
  name: payment-service
spec:
  selector:
    app: payment
  ports:
    - port: 80
      targetPort: 8080

# Other services call: http://payment-service:80
# K8s DNS auto-resolves to healthy pod IPs
```

---

## 4. Resilience Patterns

### Circuit Breaker
```
                    ┌─────────────┐
  CLOSED ──────────→│   OPEN      │
  (normal)    N     │ (fail fast) │
  failures    │     └──────┬──────┘
  threshold   │            │ timeout
              │     ┌──────▼──────┐
              └─────│ HALF-OPEN   │
                    │ (test 1 req)│
                    └─────────────┘
                    success → CLOSED
                    fail → OPEN
```

```python
import time

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=30):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        self.last_failure_time = None
    
    def call(self, func, *args):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit is OPEN — fail fast")
        
        try:
            result = func(*args)
            if self.state == 'HALF_OPEN':
                self.state = 'CLOSED'
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = 'OPEN'
            raise e
```

### Retry with Exponential Backoff
```python
import time, random

def retry_with_backoff(func, max_retries=3, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            time.sleep(delay)
            # Attempt 0: ~1s, Attempt 1: ~2s, Attempt 2: ~4s
```

### Bulkhead Pattern
```
Isolate failures: separate thread pools per dependency

Thread Pool A (Payment): 20 threads
Thread Pool B (Email):   10 threads
Thread Pool C (Search):  30 threads

Payment slow → Pool A exhausted → Pool B,C unaffected
```

---

## 5. Data Management

### Database per Service
```
Order Service → Order DB (PostgreSQL)
Payment Service → Payment DB (PostgreSQL)
Product Service → Product DB (MongoDB)
Search Service → Elasticsearch

❌ No cross-service JOINs
→ Use API composition hoặc event-driven data sync
```

### API Composition
```python
# API Gateway aggregates data from multiple services
async def get_order_details(order_id):
    order = await order_service.get(order_id)
    user = await user_service.get(order.user_id)
    payment = await payment_service.get(order.payment_id)
    
    return {
        "order": order,
        "user": user,
        "payment": payment
    }
```

### Event-Driven Data Sync (CQRS)
```
Order Service publishes "OrderCreated" event
→ Search Service consumes → updates Elasticsearch index
→ Analytics Service consumes → updates dashboards
→ Notification Service consumes → sends email

Each service maintains its own read-optimized view
```

---

## 6. Strangler Fig Pattern (Migration)

```
Monolith → Microservices migration (gradual):

Phase 1: [API Gateway] → [Monolith]
Phase 2: [API Gateway] → /users → [User Service]
                       → /* → [Monolith]
Phase 3: [API Gateway] → /users → [User Service]
                       → /orders → [Order Service]
                       → /* → [Monolith]
Phase N: [API Gateway] → all routes → [Microservices]
         Monolith decommissioned ✅
```

---

## 📝 Bài tập

1. Decompose monolith e-commerce thành microservices (vẽ diagram)
2. Implement Circuit Breaker + Retry pattern
3. Setup service discovery với Docker Compose + Consul
4. Implement Saga pattern cho Order → Payment → Inventory

---

## 📚 Tài liệu
- *Building Microservices* — Sam Newman
- *Microservices Patterns* — Chris Richardson
- [microservices.io](https://microservices.io/patterns/)
