# 🚀 Capstone Projects — End-to-End

> Mỗi project kết hợp kiến thức từ nhiều track, mô phỏng công việc thực tế ở level Senior → Staff → CTO.

---

## Project 1: Full-Stack ML Platform (3-4 tuần)

**Track liên quan:** AI (Bài 20-29), System Design (Bài 05-08), Database (Bài 05-09), Software Engineering (Bài 08-10), Security (Bài 02-04)

### Mô tả
Xây dựng hệ thống ML end-to-end: từ data ingestion → training → serving → monitoring.

### Yêu cầu
1. **Data Pipeline**: Ingest data từ API/CSV → clean → store trong PostgreSQL + Redis cache
2. **Model Training**: Train model classification/regression, track experiments với MLflow
3. **Model Serving**: REST API (FastAPI) + gRPC endpoint, Dockerized
4. **Monitoring**: Prometheus metrics, Grafana dashboard, data drift detection
5. **CI/CD**: GitHub Actions pipeline: test → build → deploy → smoke test
6. **Security**: JWT authentication, input validation, rate limiting

### Tech Stack
```
Backend:    FastAPI, SQLAlchemy, Celery
ML:         scikit-learn/PyTorch, MLflow, DVC
Infra:      Docker, docker-compose, Nginx
Database:   PostgreSQL, Redis
Monitoring: Prometheus, Grafana
CI/CD:      GitHub Actions
```

### Deliverables
- [ ] GitHub repo với README, architecture diagram
- [ ] Docker-compose one-command deployment
- [ ] API docs (Swagger/OpenAPI)
- [ ] Monitoring dashboard screenshot
- [ ] Load test results (locust/k6)
- [ ] Bài viết: "Lessons Learned" (500+ từ)

---

## Project 2: Distributed System Design & Implementation (3-4 tuần)

**Track liên quan:** System Design (Bài 01-10), Database (Bài 07-12), DSA (Bài 11-12), Security (Bài 05-07)

### Mô tả
Thiết kế và implement URL Shortener hoặc Message Queue system với full production concerns.

### Option A: URL Shortener (Distributed)
1. **Design Doc**: System design document với capacity estimation, API design, database schema
2. **Core Service**: Base62 encoding, collision handling, TTL support
3. **Database**: Sharded writes (consistent hashing), read replicas, caching layer (Redis)
4. **Analytics**: Click tracking pipeline → time-series aggregation
5. **Rate Limiting**: Token bucket per API key
6. **Scalability**: Load balancer, horizontal scaling demo

### Option B: Message Queue
1. **Design Doc**: Pub/sub vs point-to-point, at-least-once delivery guarantees
2. **Broker**: Topic-based routing, consumer groups, offset management
3. **Storage**: WAL (Write-Ahead Log) cho durability
4. **Client SDK**: Producer/Consumer Python library
5. **Monitoring**: Lag metrics, throughput dashboard

### Tech Stack
```
Language:   Python / Go
Database:   PostgreSQL + Redis
Network:    gRPC / WebSocket
Testing:    pytest, chaos testing (random node failure)
Deploy:     Docker Compose (3+ nodes)
```

### Deliverables
- [ ] System Design Doc (problem → constraints → API → schema → architecture)
- [ ] Working prototype (multi-node)
- [ ] Benchmark: throughput, latency p50/p95/p99
- [ ] Chaos test results (node failure recovery)
- [ ] Trade-off analysis document

---

## Project 3: Production API Platform (2-3 tuần)

**Track liên quan:** Software Engineering (Bài 01-09), Database (Bài 01-06), Security (Bài 01-06), System Design (Bài 05-06)

### Mô tả
Xây dựng production-ready REST/GraphQL API cho E-commerce hoặc SaaS platform.

### Yêu cầu
1. **Architecture**: Clean Architecture / Hexagonal Architecture
2. **API Design**: RESTful + GraphQL, versioning, pagination, filtering
3. **Database**: PostgreSQL với migrations, indexing strategy, query optimization
4. **Auth**: OAuth2 + JWT, RBAC (Role-Based Access Control), refresh tokens
5. **Testing**: Unit (90%+ coverage), integration, contract, E2E
6. **Observability**: Structured logging (JSON), distributed tracing (OpenTelemetry), metrics
7. **Documentation**: OpenAPI spec, ADR (Architecture Decision Records)

### Tech Stack
```
Backend:      FastAPI / NestJS / Spring Boot
Database:     PostgreSQL, Redis
Auth:         OAuth2, JWT
Testing:      pytest / Jest, Testcontainers
Observability: OpenTelemetry, ELK/Loki
API Doc:      Swagger/Redoc
```

### Deliverables
- [ ] Clean codebase với proper layering
- [ ] 50+ tests (unit + integration + E2E)
- [ ] Performance: handle 1000 RPS (load test proof)
- [ ] Security audit checklist (OWASP Top 10)
- [ ] Architecture Decision Records (3+ ADRs)

---

## Project 4: Data-Intensive Application (2-3 tuần)

**Track liên quan:** Database (Bài 07-15), System Design (Bài 09-12), DSA (Bài 06, 12)

### Mô tả
Thiết kế và xây dựng hệ thống xử lý dữ liệu lớn: real-time analytics dashboard hoặc recommendation engine.

### Option A: Real-Time Analytics Dashboard
1. **Ingestion**: Kafka/Redis Streams nhận events (clickstream, purchases)
2. **Processing**: Stream processing — sliding window aggregation
3. **Storage**: TimescaleDB/ClickHouse cho time-series, Redis cho hot data
4. **Query**: Pre-computed materialized views + ad-hoc query support
5. **Dashboard**: WebSocket real-time updates

### Option B: Recommendation Engine
1. **Data**: Collaborative filtering + content-based (hybrid)
2. **Feature Store**: User/item features, real-time feature computation
3. **Model**: Matrix factorization / Neural CF, A/B testing framework
4. **Serving**: Low-latency retrieval (< 50ms p99)
5. **Evaluation**: Offline (NDCG, MAP) + Online (CTR, conversion)

### Deliverables
- [ ] Data flow diagram + schema design
- [ ] Working pipeline: ingest → process → store → query
- [ ] Latency benchmarks
- [ ] Scalability analysis (what happens at 10x, 100x load?)

---

## Project 5: Technical Leadership Simulation (2 tuần)

**Track liên quan:** Leadership (Bài 01-12), Software Engineering (Bài 10-12), Security (Bài 08-10)

### Mô tả
Mô phỏng vai trò Tech Lead / Engineering Manager qua documentation và planning exercises.

### Yêu cầu
1. **RFC/Design Doc**: Viết 2 RFC cho feature phức tạp (migration, new service)
   - Problem statement, proposed solution, alternatives, risks, timeline
2. **Team Roadmap**: Lập quarterly roadmap cho team 5-8 người
   - OKRs, task breakdown, dependency mapping, risk mitigation
3. **Incident Response**: 
   - Viết incident postmortem cho 2 scenarios (database outage, security breach)
   - Tạo runbook template
4. **Architecture Review**:
   - Review kiến trúc của 1 open-source project (ví dụ: Kafka, Redis, Kubernetes)
   - Viết analysis document: strengths, weaknesses, trade-offs
5. **Interview Plan**:
   - Thiết kế quy trình phỏng vấn cho Senior Engineer position
   - 3 technical questions + rubric + evaluation criteria
6. **Budget Proposal**:
   - Cloud cost estimation cho project (AWS/GCP calculator)
   - Build vs Buy analysis cho 1 component

### Deliverables
- [ ] 2 RFC documents (2000+ từ mỗi cái)
- [ ] Quarterly roadmap spreadsheet/doc
- [ ] 2 incident postmortems
- [ ] Architecture review document
- [ ] Interview plan + rubric
- [ ] Budget/cost analysis

---

## Project 6: Security-First Application (2 tuần)

**Track liên quan:** Security (Bài 01-10), Software Engineering (Bài 06-07), System Design (Bài 14-15)

### Mô tả
Xây dựng ứng dụng với security là priority #1, sau đó tự pentest.

### Yêu cầu
1. **Secure API**: Implement OWASP Top 10 mitigations
2. **Auth System**: Multi-factor authentication, session management, password hashing (Argon2)
3. **Data Protection**: Encryption at rest (AES-256) + in transit (TLS), PII handling
4. **Security Testing**: 
   - SAST scan (Bandit/Semgrep)
   - DAST scan (OWASP ZAP)
   - Dependency audit (pip-audit / npm audit)
5. **Threat Model**: STRIDE analysis cho toàn bộ hệ thống
6. **Compliance**: GDPR checklist implementation (consent, right to delete, data export)

### Deliverables
- [ ] Secure application code
- [ ] STRIDE threat model document
- [ ] Security scan reports (SAST + DAST)
- [ ] Penetration test findings (self-assessment)
- [ ] GDPR compliance checklist

---

## 📋 Thứ tự thực hiện đề xuất

| Thứ tự | Project | Level | Thời gian |
|--------|---------|-------|-----------|
| 1 | Project 3: Production API | Senior | 2-3 tuần |
| 2 | Project 1: ML Platform | Senior+ | 3-4 tuần |
| 3 | Project 4: Data-Intensive | Staff | 2-3 tuần |
| 4 | Project 2: Distributed System | Staff | 3-4 tuần |
| 5 | Project 6: Security-First | Staff | 2 tuần |
| 6 | Project 5: Leadership Sim | Lead/Manager | 2 tuần |

> **Tổng:** ~14-19 tuần cho toàn bộ 6 projects.
> Có thể làm song song Project 5 (documentation) với bất kỳ project nào khác.

---

## 🎯 Đánh giá Portfolio

Sau khi hoàn thành ≥ 4/6 projects, bạn sẽ có portfolio chứng minh:
- ✅ Thiết kế hệ thống phức tạp (System Design)
- ✅ Implement production-quality code (Software Engineering)
- ✅ Quản lý data pipeline end-to-end (AI/ML + Database)
- ✅ Security mindset bài bản (Security)
- ✅ Leadership và communication skills (Leadership)
- ✅ Trade-off analysis và decision-making (Staff/CTO thinking)
