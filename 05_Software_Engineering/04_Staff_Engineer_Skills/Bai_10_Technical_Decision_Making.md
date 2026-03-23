# Bài 10: Technical Decision Making

## 🎯 Mục tiêu
- Architecture Decision Records (ADR)
- Trade-off analysis frameworks
- RFC process & technical proposals

## 📖 Câu chuyện đời thường
> Bạn mua nhà — quyết định lớn nhất đời. Bạn không chọn bừa mà ghi lại: "Tại sao chọn Quận 7? Vì gần công ty, trường học. Tại sao không chọn Quận 2? Giá đất cao hơn 30%" — đó là **ADR** (Architecture Decision Record). **Trade-off analysis** là cân nhắc: nhà lớn thì đắt, nhà nhỏ thì chật, xa trung tâm thì rẻ nhưng tốn thời gian. **RFC** giống việc bạn gửi bản phân tích cho cả gia đình góp ý trước khi quyết định. Staff Engineer cũng vậy: quyết định kiến trúc ảnh hưởng nhiều năm, cần ghi chép và cân nhắc kỹ.

---

## 1. Architecture Decision Records (ADR)

```markdown
# ADR-001: Chọn Message Queue cho Event-Driven Architecture

## Status: Accepted
## Date: 2024-01-15

## Context
Hệ thống order processing cần async communication giữa 5 microservices.
Current volume: 10K events/sec, projected: 100K events/sec trong 12 tháng.

## Options Considered

### Option A: RabbitMQ
- Pros: Mature, flexible routing, good for task queues
- Cons: Single-node throughput limited, harder to scale horizontally

### Option B: Apache Kafka
- Pros: High throughput (millions msg/sec), built-in replay, ordering guarantees
- Cons: Higher operational complexity, overkill for low volume

### Option C: AWS SQS/SNS
- Pros: Fully managed, no ops burden, scales automatically  
- Cons: Vendor lock-in, limited ordering, no replay

## Decision
**Kafka** — because projected growth needs high throughput, event replay
is critical for our event-sourcing architecture, and team has Kafka experience.

## Consequences
- Need Kafka ops expertise (or use managed Confluent Cloud)
- Schema registry required for event evolution
- Consumer group management adds complexity
```

### ADR Practices
```
Khi nào viết ADR:
- Chọn database, message queue, framework
- Thay đổi architecture pattern
- Thay đổi deployment strategy
- Bất kỳ decision nào ảnh hưởng > 1 team

Lưu ở đâu:
docs/adr/001-message-queue-choice.md
docs/adr/002-auth-strategy.md
Version controlled cùng codebase → decision history

Key: ADR ghi lại WHY, không chỉ WHAT
```

---

## 2. Trade-off Analysis Framework

```
STEP 1: Define constraints & requirements
  - Functional: What must the system do?
  - Non-functional: Latency, throughput, availability, cost
  - Constraints: Team size, timeline, existing tech stack

STEP 2: Identify options (minimum 3)
  - Build vs Buy vs Open Source
  - Option A / B / C

STEP 3: Evaluate against criteria (score 1-5)
  ┌──────────────────┬─────────┬────────┬─────────┐
  │ Criterion        │ Kafka   │ Rabbit │ SQS     │
  ├──────────────────┼─────────┼────────┼─────────┤
  │ Throughput       │ ★★★★★  │ ★★★   │ ★★★★   │
  │ Ops complexity   │ ★★     │ ★★★   │ ★★★★★  │
  │ Event replay     │ ★★★★★  │ ★     │ ★       │
  │ Team familiarity │ ★★★★   │ ★★    │ ★★★    │
  │ Cost (3yr)       │ ★★★    │ ★★★★  │ ★★     │
  └──────────────────┴─────────┴────────┴─────────┘

STEP 4: Make decision & document (ADR)

STEP 5: Define success metrics & review date
  - Review in 6 months: Are we hitting 50K events/sec?
```

---

## 3. RFC Process (Request for Comments)

```markdown
# RFC: Migrate from Monolith to Microservices

## Author: Nguyen Van A | Date: 2024-02-01
## Reviewers: @team-lead, @architect, @devops-lead
## Status: Under Review

## 1. Problem Statement
Monolith deployment takes 45min, any change requires full redeploy.
Team velocity decreased 40% in last quarter.

## 2. Proposed Solution
Extract 3 bounded contexts into separate services:
- User Service (team A)
- Order Service (team B)  
- Payment Service (team C)

## 3. Design
[Architecture diagram]
[API contracts]
[Data ownership boundaries]

## 4. Migration Plan
Phase 1 (Q1): Strangler Fig pattern — extract User Service
Phase 2 (Q2): Extract Order Service
Phase 3 (Q3): Extract Payment Service

## 5. Risks & Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Distributed transactions | High | Saga pattern |
| Service discovery | Medium | K8s + Istio |
| Data consistency | High | Event sourcing + CDC |

## 6. Alternatives Considered
- Modular monolith (rejected: doesn't solve deployment coupling)
- Serverless (rejected: cold start latency unacceptable)

## 7. Success Criteria
- Deploy time < 5min per service
- Team velocity +30% in 6 months
- p99 latency < 200ms
```

---

## 4. Two-Way Door vs One-Way Door Decisions

```
ONE-WAY DOOR (hard to reverse):
  → Database choice, programming language, cloud provider
  → Require: thorough analysis, ADR, team consensus
  → Timeline: take time to decide right

TWO-WAY DOOR (easy to reverse):
  → Library choice, API field naming, UI layout
  → Approach: decide quickly, iterate
  → "Disagree and commit" — don't block on consensus

Staff Engineer skill: identify WHICH TYPE early
  → Prevent over-analysis on two-way doors
  → Ensure rigor on one-way doors
```

---

## 📝 Bài tập

1. Viết ADR cho 1 technical decision trong project hiện tại
2. Thực hành trade-off analysis: chọn database cho e-commerce platform
3. Viết RFC cho 1 system change proposal
4. Classify 10 recent decisions: one-way or two-way door?

---

## 📚 Tài liệu
- *Fundamentals of Software Architecture* — Mark Richards, Neal Ford
- *The Staff Engineer's Path* — Tanya Reilly
- [ADR GitHub Template](https://adr.github.io/)
