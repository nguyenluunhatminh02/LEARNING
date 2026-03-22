# Bài 14: Reliability, Scalability & Observability

## 🎯 Mục tiêu
- Scalability patterns (horizontal, vertical)
- High availability & fault tolerance
- Observability: logging, metrics, tracing
- SLI/SLO/SLA

---

## 1. Scalability

### Vertical vs Horizontal

```
Vertical Scaling (Scale Up):
  1 server: 4 CPU → 64 CPU, 8GB RAM → 256GB RAM
  ✅ Simple, no code change
  ❌ Limit: hardware ceiling
  ❌ Single point of failure

Horizontal Scaling (Scale Out):
  1 server → 10 servers behind load balancer
  ✅ No hardware limit
  ✅ Fault tolerant
  ❌ Complex: stateless design, distributed data
```

### Stateless vs Stateful Services

```
Stateless (scalable ✅):
  Server không giữ user state
  State stored in: Redis, DB, JWT token
  → Bất kỳ server nào cũng handle được request

Stateful (hard to scale ❌):
  Server giữ session trong memory
  → User phải hit cùng server (sticky session)
  → Scaling = migrating state

Rule: Make services STATELESS, store state externally
```

---

## 2. High Availability

### Availability Numbers

```
99%    → 3.65 days downtime/year     (bad)
99.9%  → 8.76 hours downtime/year   (okay)
99.99% → 52.6 minutes downtime/year (good)
99.999% → 5.26 minutes downtime/year (excellent)
```

### Redundancy Patterns

```
Active-Active:
  [Server A] ← traffic → [Server B]
  Cả hai đều xử lý requests
  ✅ Full capacity, instant failover
  ❌ Data sync complexity

Active-Passive:
  [Server A] ← traffic    [Server B] (standby)
  B chỉ activate khi A fail
  ✅ Simple
  ❌ Wasted resource, failover delay

Multi-Region:
  [Region US] ↔ [Region EU] ↔ [Region Asia]
  User → nearest region (GeoDNS)
  Data replicated across regions
```

### Failure Handling

```
Single server MTBF (Mean Time Between Failures): ~3 years
1000 servers → expect ~1 failure/day

Strategies:
1. Redundancy: N+1 hoặc N+2 servers
2. Health checks: detect failures quickly
3. Auto-healing: K8s restart failed pods
4. Graceful degradation: disable non-critical features
5. Chaos engineering: intentionally inject failures (Netflix Chaos Monkey)
```

---

## 3. Observability — Three Pillars

### 3.1 Logging
```python
import logging
import json

# Structured logging (JSON) — dễ parse, search
logger = logging.getLogger(__name__)

def process_order(order_id, user_id):
    logger.info(json.dumps({
        "event": "order_processing",
        "order_id": order_id,
        "user_id": user_id,
        "stage": "started"
    }))
    
    try:
        result = charge_payment(order_id)
        logger.info(json.dumps({
            "event": "order_processing",
            "order_id": order_id,
            "stage": "payment_completed",
            "amount": result.amount
        }))
    except Exception as e:
        logger.error(json.dumps({
            "event": "order_processing",
            "order_id": order_id,
            "stage": "payment_failed",
            "error": str(e)
        }))
        raise
```

```
Log Aggregation Stack:
  App → Fluentd/Filebeat → Elasticsearch → Kibana (ELK)
  App → Promtail → Loki → Grafana
```

### 3.2 Metrics
```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

# Counter: luôn tăng (total requests, errors)
request_count = Counter('http_requests_total', 'Total requests', ['method', 'endpoint', 'status'])

# Histogram: distribution (response time)
request_duration = Histogram('http_request_duration_seconds', 'Request duration',
                              buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0])

# Gauge: giá trị hiện tại (active connections, queue size)
active_connections = Gauge('active_connections', 'Active WebSocket connections')

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    request_duration.observe(duration)
    
    return response
```

```
4 Golden Signals (Google SRE):
1. Latency:    Response time (p50, p95, p99)
2. Traffic:    Requests per second
3. Errors:     Error rate (5xx / total)
4. Saturation: CPU, memory, disk usage

RED Method (microservices):
  Rate, Errors, Duration

USE Method (infrastructure):
  Utilization, Saturation, Errors
```

### 3.3 Distributed Tracing
```
User request spans multiple services:

Request ID: abc-123
├── API Gateway (5ms)
│   ├── Auth Service (2ms)
│   └── Order Service (50ms)
│       ├── Inventory Service (10ms)
│       ├── Payment Service (30ms)
│       │   └── Bank API (25ms)  ← bottleneck!
│       └── DB Query (5ms)

Trace = collection of spans across services
→ Identify bottlenecks, debug slow requests
```

```python
# OpenTelemetry (standard)
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

async def process_order(order):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order.id)
        
        with tracer.start_as_current_span("check_inventory"):
            await inventory_service.check(order.items)
        
        with tracer.start_as_current_span("process_payment"):
            await payment_service.charge(order.total)

# Tools: Jaeger, Zipkin, Datadog, AWS X-Ray
```

---

## 4. SLI / SLO / SLA

```
SLI (Service Level Indicator):
  Metric đo lường → "p99 latency là 200ms"

SLO (Service Level Objective):
  Target cho SLI → "p99 latency < 500ms, 99.9% time"

SLA (Service Level Agreement):
  Contract với customer → "99.99% uptime, nếu không → refund"

Example:
  SLI: Error rate = 0.05%
  SLO: Error rate < 0.1%
  SLA: Error rate < 1%, penalty: 10% credit nếu exceed

Error Budget:
  SLO=99.9% → Error budget = 0.1% = 43.8 min/month
  Dùng budget cho: deployments, experiments, maintenance
  Budget hết → freeze deployments, focus on reliability
```

---

## 5. Alerting Strategy

```
Page (wake people up):
  - Service DOWN
  - Error rate > 5%
  - p99 latency > 5s
  - Data loss risk

Ticket (fix during work hours):
  - Error rate > 1%
  - Disk usage > 80%
  - Certificate expiring in 7 days

Log only:
  - Error rate > 0.1%
  - Gradual latency increase

Rule: Alert on symptoms (user impact), not causes
```

---

## 📝 Bài tập

1. Setup Prometheus + Grafana monitoring cho FastAPI app
2. Implement distributed tracing với OpenTelemetry
3. Define SLI/SLO cho e-commerce: checkout, search, product page
4. Setup ELK stack (Elasticsearch + Logstash + Kibana) cho centralized logging

---

## 📚 Tài liệu
- *Site Reliability Engineering* — Google SRE Book
- *Observability Engineering* — Charity Majors
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
