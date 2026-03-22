# Bài 09: Infrastructure & Observability

## 🎯 Mục tiêu
- Infrastructure as Code (IaC) với Terraform
- Monitoring, Logging, Tracing (3 trụ cột observability)
- Alerting & Incident Response

---

## 1. Infrastructure as Code (IaC)

```hcl
# Terraform — Declarative infrastructure
resource "aws_ecs_service" "app" {
  name            = "my-app"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = 3

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = 8000
  }
}

resource "aws_rds_instance" "db" {
  engine         = "postgres"
  instance_class = "db.r6g.large"
  multi_az       = true
  storage_encrypted = true
}

# Benefits:
# - Version controlled infrastructure
# - Reproducible environments
# - Auto-scaling, self-healing
# - terraform plan → review changes before apply
```

---

## 2. Three Pillars of Observability

### 2.1. Metrics (Prometheus + Grafana)
```python
from prometheus_client import Counter, Histogram, start_http_server

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency', ['endpoint'])

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.url.path).observe(duration)
    return response

# RED Metrics:
# Rate    — requests/second
# Errors  — error rate %
# Duration — p50, p95, p99 latency
```

### 2.2. Logging (Structured Logs)
```python
import structlog

logger = structlog.get_logger()

# BAD: logger.info(f"User {user_id} placed order {order_id}")
# GOOD: structured, searchable
logger.info("order_placed",
    user_id=user_id,
    order_id=order_id,
    total=order.total,
    items_count=len(order.items))

# → {"event": "order_placed", "user_id": "u123", "order_id": "o456", ...}
# Searchable in ELK / Loki / CloudWatch
```

### 2.3. Distributed Tracing (OpenTelemetry)
```python
from opentelemetry import trace
tracer = trace.get_tracer(__name__)

async def process_order(order):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order.id)
        
        with tracer.start_as_current_span("validate"):
            validate(order)
        
        with tracer.start_as_current_span("charge_payment"):
            charge(order)  # → trace propagated to payment service
        
        with tracer.start_as_current_span("send_notification"):
            notify(order)  # → trace propagated to notification service

# Jaeger/Zipkin/Tempo: visualize request flow across services
# Find: which service is slow? where did the error occur?
```

---

## 3. Alerting & Incident Response

```yaml
# Alert rules (Prometheus)
groups:
  - name: app-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels: { severity: critical }
        annotations: { summary: "Error rate > 5% for 5 minutes" }

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        labels: { severity: warning }
```

### Incident Response Framework
```
SEV1 (Critical): Service down, data loss → All hands, 15min response
SEV2 (Major):    Major feature broken → On-call team, 30min response
SEV3 (Minor):    Degraded performance → Next business day

Process:
1. DETECT   — Alert fires, PagerDuty pages on-call
2. TRIAGE   — Assess severity, assign incident commander
3. MITIGATE — Rollback, feature flag off, scale up
4. RESOLVE  — Root cause fix
5. POSTMORTEM — Blameless review, action items, prevent recurrence
```

---

## 📝 Bài tập

1. Setup Prometheus + Grafana dashboard cho ứng dụng
2. Implement structured logging với correlation ID across services
3. Viết Terraform cho basic AWS infrastructure (VPC + ECS + RDS)
4. Create incident response runbook cho team

---

## 📚 Tài liệu
- *Observability Engineering* — Charity Majors
- *Terraform Up & Running* — Yevgeniy Brikman
- [OpenTelemetry Docs](https://opentelemetry.io/docs/)

## 🔗 Liên kết chéo
- → **AI Bài 29: Model Deployment** — ML-specific monitoring (drift, accuracy)
- → **SE Bài 08: CI/CD** — monitoring integration trong deployment pipeline
- → **System Design Bài 05: Load Balancing** — infrastructure monitoring
- → **Security Bài 08: Incident Response** — alerting và incident detection
