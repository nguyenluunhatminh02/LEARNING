# Bài 15: Cloud, Kubernetes & CI/CD

## 🎯 Mục tiêu
- Cloud fundamentals (AWS/GCP/Azure)
- Kubernetes orchestration
- CI/CD pipeline
- Infrastructure as Code (Terraform)

---

## 1. Cloud Computing Models

```
On-Premise:  Bạn quản lý TẤT CẢ (hardware → OS → app)
IaaS:        Cloud cho hardware (EC2, VMs) — bạn quản lý OS + app
PaaS:        Cloud cho platform (Heroku, App Engine) — bạn chỉ deploy code
FaaS:        Serverless (Lambda, Cloud Functions) — bạn chỉ viết function
SaaS:        Cloud cho app (Gmail, Slack) — bạn chỉ dùng
```

### AWS Core Services

```
Compute:
  EC2          — Virtual machines
  Lambda       — Serverless functions
  ECS/EKS      — Container orchestration
  Fargate      — Serverless containers

Storage:
  S3           — Object storage (images, videos, backups)
  EBS          — Block storage (EC2 disk)
  EFS          — Network file system

Database:
  RDS          — Managed PostgreSQL/MySQL
  DynamoDB     — Managed NoSQL (key-value)
  ElastiCache  — Managed Redis/Memcached
  Aurora       — High-performance MySQL/PostgreSQL

Networking:
  VPC          — Virtual private network
  ALB/NLB      — Load balancers
  CloudFront   — CDN
  Route 53     — DNS

Messaging:
  SQS          — Message queue
  SNS          — Pub/Sub notifications
  Kinesis      — Real-time streaming (like Kafka)
```

---

## 2. Docker & Containerization

```dockerfile
# Dockerfile — package application
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml — multi-container setup
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
  
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - pgdata:/var/lib/postgresql/data
  
  cache:
    image: redis:7-alpine

volumes:
  pgdata:
```

---

## 3. Kubernetes (K8s)

```
K8s = Container Orchestration Platform

Pod         → smallest unit (1+ containers)
Deployment  → manage Pods (scaling, rolling update)
Service     → stable network endpoint for Pods
Ingress     → HTTP routing (external → services)
ConfigMap   → configuration
Secret      → sensitive data (encrypted)
```

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
      - name: order-service
        image: myregistry/order-service:v1.2.3
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: "250m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### K8s Deployment Strategies
```
Rolling Update (default):
  v1 v1 v1 → v1 v1 v2 → v1 v2 v2 → v2 v2 v2
  Zero-downtime, gradual

Blue-Green:
  [Blue: v1] ← traffic
  [Green: v2] (ready, tested)
  Switch traffic: Blue → Green
  Rollback: Green → Blue
  ✅ Instant rollback

Canary:
  v1 (90% traffic) + v2 (10% traffic)
  Monitor v2 metrics → gradually increase %
  ✅ Safe rollout, catch issues early
```

---

## 4. CI/CD Pipeline

```
Code Push → Build → Test → Deploy

┌──────┐   ┌───────┐   ┌──────┐   ┌─────────┐   ┌────────┐
│ Git  │──→│ Build │──→│ Test │──→│ Staging │──→│  Prod  │
│ Push │   │ Image │   │ Unit │   │ Deploy  │   │ Deploy │
└──────┘   └───────┘   │ Intg │   │ E2E Test│   │ Canary │
                        │ Lint │   └─────────┘   └────────┘
                        └──────┘
```

```yaml
# GitHub Actions CI/CD
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v --cov=src
      - run: ruff check src/

  build-and-push:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: myregistry/app:${{ github.sha }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - run: |
          kubectl set image deployment/app \
            app=myregistry/app:${{ github.sha }}
          kubectl rollout status deployment/app
```

---

## 5. Infrastructure as Code (Terraform)

```hcl
# main.tf — AWS infrastructure
provider "aws" {
  region = "ap-southeast-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.medium"
  
  tags = {
    Name = "web-server"
  }
}

resource "aws_rds_instance" "db" {
  engine         = "postgres"
  engine_version = "16"
  instance_class = "db.t3.medium"
  allocated_storage = 50
  
  db_name  = "myapp"
  username = "admin"
  password = var.db_password  # from tfvars or secrets
}

resource "aws_elasticache_cluster" "cache" {
  cluster_id      = "redis-cache"
  engine          = "redis"
  node_type       = "cache.t3.medium"
  num_cache_nodes = 1
}

# terraform plan   → preview changes
# terraform apply  → create/update infrastructure
# terraform destroy → tear down
```

---

## 📝 Bài tập

1. Dockerize ứng dụng FastAPI + PostgreSQL + Redis
2. Deploy lên K8s (Minikube) với Deployment + Service + HPA
3. Setup GitHub Actions CI/CD: test → build → deploy
4. Viết Terraform config cho: VPC + EC2 + RDS + ElastiCache

---

## 📚 Tài liệu
- *Kubernetes in Action* — Marko Lukša
- *The DevOps Handbook* — Gene Kim
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Terraform Tutorials](https://developer.hashicorp.com/terraform/tutorials)
