# Bài 12: CTO & VP Engineering Skills

## 🎯 Mục tiêu
- Organization design & scaling
- Technical strategy & vision
- CTO vs VP Engineering roles
- Scaling engineering organizations

## 📖 Câu chuyện đời thường
> **CTO** giống kiến trúc sư trưởng: nhìn xa, chọn công nghệ, vẽ tầm nhìn "tòa nhà 5 năm nữa sẽ ra sao". **VP Engineering** giống chỉ huy công trường: đảm bảo xây xong đúng hạn, đội ngũ khỏe, quy trình trơn tru. **Org design** giống thiết kế sơ đồ công ty: 10 người thì 1 đội là đủ, 100 người cần chia nhiều đội nhỏ, mỗi đội có trưởng nhóm. **Scaling** giống mở chuỗi cửa hàng: không thể quản lý 50 cửa hàng giống 1 cửa hàng — cần hệ thống, quy trình, và con người tự vận hành.

---

## 1. CTO vs VP Engineering

```
CTO = OUTWARD-facing technical leader
  - Technology vision & strategy
  - Product architecture direction
  - External: customers, partners, conferences
  - Innovation: R&D, tech radar
  - Board communication
  - "What should we build and why?"

VP Engineering = INWARD-facing engineering leader
  - Engineering execution & delivery
  - Team management & organization
  - Process, tooling, developer productivity
  - Hiring, retention, career development
  - "How do we build it efficiently with a great team?"

At small companies: CTO does both roles
At scale: Both roles needed, working as partners

Career Path:
  IC Track:    Senior → Staff → Principal → Distinguished Fellow
  Mgmt Track:  TL → EM → Sr EM → Director → VP Eng → CTO

  Staff/Principal: Deep technical impact, architecture influence
  Director: Manages managers, runs organization (50-100 people)
  VP Engineering: Runs all of engineering (100-500+ people)
  CTO: Sets technical direction for the entire company
```

---

## 2. Organization Design

```
Conway's Law (use it intentionally):
  "Organizations produce systems mirroring their communication structures"
  → Design org around the architecture you WANT

Team Structures:

Small (10-20 engineers):
  2-3 cross-functional teams
  Each team: 4-6 engineers + PM + Designer
  CTO directly involved in architecture
  
  Team 1: Core Product
  Team 2: Growth & Engagement
  Team 3: Infrastructure & Platform

Medium (50-100 engineers):
  3-4 departments, each with multiple teams
  Engineering Managers manage teams
  Directors manage departments
  
  Product Engineering (3-4 teams, stream-aligned)
  Platform Engineering (2 teams, enabling)
  Data & ML (1-2 teams)
  SRE/DevOps (1 team)

Large (200+ engineers):
  Multiple departments, VPs/Directors
  Architecture review board
  Technical fellows / distinguished engineers
  
  Product Area 1 (Director + 4-5 teams)
  Product Area 2 (Director + 4-5 teams)
  Platform (Director + 3-4 teams)
  Data/ML (Director + 2-3 teams)
  Security (Manager + team)
  SRE (Director + 2-3 teams)

Span of Control:
  IC teams: 5-8 engineers per team
  EM: manages 1-2 teams (5-10 ICs)
  Director: manages 3-5 EMs (25-50 ICs)
  VP: manages 3-6 Directors (100-300 ICs)
```

---

## 3. Scaling Engineering Organizations

```
Scaling Challenges at Each Stage:

10 → 30 Engineers:
  Challenge: Knowledge sharing, losing startup speed
  Solution: 
    - Documentation culture
    - First engineering managers
    - Basic processes (PR review, on-call)
    - Team charters & ownership

30 → 100 Engineers:
  Challenge: Communication overhead, coordination
  Solution:
    - Clear team boundaries & ownership
    - Platform team (internal tooling)
    - Engineering ladder (career levels)
    - Architecture review process
    - On-call rotation per team

100 → 300 Engineers:
  Challenge: Alignment, consistency, culture dilution
  Solution:
    - Engineering principles (written values)
    - Technical strategy document
    - Inner source / shared libraries
    - Developer experience team
    - Quarterly planning at org level

300+ Engineers:
  Challenge: Innovation speed, bureaucracy
  Solution:
    - Autonomous teams with clear boundaries
    - Internal APIs & contracts
    - Architecture governance (advisory, not blocking)
    - Engineering blog / tech talks (maintain culture)
    - Regular re-org based on product needs

Scaling Rule of Thumb:
  Every 3x in team size → need to rethink processes
  What works at 10 won't work at 30
  What works at 30 won't work at 100
```

---

## 4. Technical Strategy Document

```markdown
# Technical Strategy 2024-2026

## 1. Vision
"Build a world-class, scalable platform that can serve 
10M users with sub-100ms response time, while maintaining 
weekly release velocity."

## 2. Current State Assessment
- Architecture: Modular monolith, 3 microservices
- Scale: 500K users, 2K RPS
- Team: 45 engineers across 6 teams
- Tech stack: Python/FastAPI, PostgreSQL, Redis, K8s

## 3. Target State (2026)
- Architecture: 12 microservices, event-driven
- Scale: 10M users, 50K RPS
- Team: 100 engineers across 15 teams
- New capabilities: ML recommendations, real-time analytics

## 4. Strategic Pillars

Pillar 1: SCALABILITY
  - Migrate to event-driven architecture
  - Database sharding for user data
  - CDN for global low-latency access

Pillar 2: DEVELOPER PRODUCTIVITY
  - Self-service infrastructure platform
  - CI/CD < 10 minutes end-to-end
  - Comprehensive testing framework

Pillar 3: DATA & AI
  - Data platform for ML pipeline
  - Real-time analytics infrastructure
  - Recommendation engine

Pillar 4: RELIABILITY
  - Multi-region deployment
  - 99.99% availability SLO
  - Automated incident response

## 5. Technology Radar
  ADOPT:  Kubernetes, PostgreSQL, Redis, gRPC
  TRIAL:  Kafka, ClickHouse, OpenTelemetry
  ASSESS: WebAssembly, edge computing
  HOLD:   MongoDB (migrate existing to PostgreSQL)

## 6. Investment Allocation
  60% — New features (directly revenue-generating)
  20% — Platform & infrastructure (scalability)
  10% — Tech debt (reliability & maintainability)
  10% — Innovation (R&D, experiments)
```

---

## 5. Executive Decision Framework

```
CTO Decision-Making:

STRATEGIC (1-way door, long-term):
  Cloud provider, primary language, core architecture
  → Thorough analysis, ADR, team input, board alignment
  → Timeline: weeks to decide

TACTICAL (2-way door, medium-term):
  Tool choices, process changes, team structure
  → Data-driven, RFC process, quick iteration
  → Timeline: days to decide

OPERATIONAL (day-to-day):
  Bug prioritization, sprint scope, code approach
  → Delegate to teams, provide guidelines
  → Timeline: hours or less

Delegation Matrix (as CTO):
  ALWAYS DELEGATE:
    Sprint planning, code reviews, feature implementation
    Hiring decisions (except senior leadership)
  
  DELEGATE WITH OVERSIGHT:
    Architecture decisions (review ADRs)
    Tool selection (approve if above $X)
    Process changes (ensure alignment)
  
  KEEP:
    Technical strategy & vision
    Senior hiring (VP, Director)
    Key vendor/partnership decisions
    Board communication
    Cultural & values decisions

Time Allocation (CTO):
  30% — Strategy & planning
  25% — People (1:1s, hiring, coaching)
  20% — Cross-functional (product, sales, board)
  15% — Technical (architecture reviews, staying current)
  10% — External (conferences, community, recruiting)
```

---

## 📝 Bài tập

1. Design org chart cho 50-person engineering team
2. Write 2-year technical strategy document
3. Create technology radar cho your stack
4. Practice: present technical strategy to mock board

---

## 📚 Tài liệu
- *An Elegant Puzzle* — Will Larson
- *The Manager's Path* — Camille Fournier
- *High Output Management* — Andy Grove
- *Scaling Up Excellence* — Sutton & Rao
- *Staff Engineer* — Will Larson
