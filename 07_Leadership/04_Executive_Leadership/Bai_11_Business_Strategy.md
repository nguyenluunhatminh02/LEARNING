# Bài 11: Business & Strategy for Technical Leaders

## 🎯 Mục tiêu
- P&L understanding & budget management
- Fundraising & investor communication
- Build vs buy at strategic level
- Vendor management & negotiation

## 📖 Câu chuyện đời thường
> Bạn là chủ một doanh nghiệp nhỏ. **P&L** giống sổ thu chi gia đình: thu bao nhiêu (revenue), chi bao nhiêu (cost), còn lại bao nhiêu (profit). **Build vs Buy** giống: tự nấu cơm (tốn thời gian, kiểm soát chất lượng) hay đặt cơm hộp (nhanh, đắt, phụ thuộc người khác). **Fundraising** giống vay ngân hàng mở rộng: phải chứng minh "sẽ kiếm được gấp 10 số vay". **Vendor negotiation** giống mặc cả ở chợ: biết giá thị trường, có phương án thay thế, và sẵn sàng rời đi nếu không hợp lý.

---

## 1. P&L (Profit & Loss) for CTOs

```
CTO cần hiểu tài chính vì:
  - Budget decisions (hire vs tool vs service)
  - ROI arguments for engineering investment
  - Board communication
  - Company strategy alignment

Simplified P&L:
┌─────────────────────────────────────────────┐
│ Revenue                          $10,000,000│
│ - Cost of Goods Sold (COGS)      -$3,000,000│
│   (hosting, API costs, support)             │
│ ─────────────────────────────────────────── │
│ Gross Profit                      $7,000,000│
│ Gross Margin                           70%  │
│                                             │
│ - Engineering salaries           -$4,000,000│
│ - Other OpEx                     -$2,000,000│
│ ─────────────────────────────────────────── │
│ Operating Profit (EBITDA)         $1,000,000│
│ Operating Margin                       10%  │
└─────────────────────────────────────────────┘

Engineering as % of Revenue:
  Early stage startup:  40-60% (building the product)
  Growth stage:         25-35% (scaling)
  Mature:               15-25% (maintenance + new features)
  
CTO questions to answer:
  "What's our cost per user/transaction?"
  "How does engineering spending translate to revenue?"
  "Where can we reduce COGS?" (optimize cloud spend)
```

---

## 2. Budget Management

```
Engineering Budget Components:
  1. People (70-80%): Salaries, benefits, contractors
  2. Infrastructure (10-15%): Cloud, hosting, databases
  3. Tools (5-10%): SaaS tools, licenses
  4. Other (5%): Training, conferences, equipment

Cloud Cost Optimization (often biggest variable cost):
  Strategy 1: Right-sizing
    → Most instances are over-provisioned
    → Monitor actual usage → downsize
    → Savings: 20-40%
  
  Strategy 2: Reserved Instances / Savings Plans
    → Commit for 1-3 years → 30-70% discount
    → For predictable base load
  
  Strategy 3: Spot Instances
    → For fault-tolerant workloads (batch processing)
    → Savings: 60-90%
  
  Strategy 4: Architecture optimization
    → Cache more → fewer DB queries → smaller DB needed
    → Serverless for sporadic workloads
    → CDN for static content
  
  Monthly cloud review:
    Track: cost per service, cost per user, month-over-month trend
    Alert: if any service cost increases > 20% unexpectedly

Headcount Planning:
  Team size → Capacity → What we can deliver
  "If we hire 3 more engineers, we can ship Feature X 
   2 months earlier, capturing $500K in revenue.
   Cost: $450K/year (3 × $150K). ROI: positive in month 3."
```

---

## 3. Working with Board & Investors

```
What Board/Investors Care About:
  1. Revenue growth & profitability path
  2. Product-market fit evidence
  3. Team quality & retention
  4. Technical moat / competitive advantage
  5. Risk (security, scaling, single points of failure)

CTO Board Presentation Structure:
  1. ENGINEERING HIGHLIGHTS (2 min)
     "Shipped X, Y, Z. Impact: +15% revenue, -30% latency."
  
  2. TEAM UPDATE (1 min)
     "Team: 25 engineers (hired 3, attrition 0). 
      Hiring plan: 5 more in Q2."
  
  3. TECHNICAL STRATEGY (3 min)
     "We're investing in X because Y.
      Expected impact: Z by Q3."
  
  4. RISKS & MITIGATIONS (2 min)
     "Key risk: scaling for projected growth.
      Mitigation: migration to K8s (on track, 70% complete)."
  
  5. ASKS (1 min)
     "Need: budget approval for security audit ($50K)."

Board Communication Rules:
  ✅ Business language, not tech jargon
  ✅ Data and metrics, not opinions
  ✅ Forward-looking (strategy), not just backward (what we did)
  ✅ Be honest about risks (surprised board = unhappy board)
```

---

## 4. Strategic Technical Decisions

```
Technology Strategy Framework:

1. CORE vs CONTEXT (Geoffrey Moore)
   Core: Things that differentiate your product
     → Invest heavily, build in-house, best engineers
   Context: Everything else
     → Buy, outsource, use commodity solutions
   
   Example (Uber):
     Core: Matching algorithm, routing, pricing
     Context: Payment processing, email, monitoring

2. TECHNICAL MOAT
   What makes your technology hard to replicate?
   - Proprietary data (trained on unique data)
   - Network effects (more users → better product)
   - Performance at scale (years of optimization)
   - Integrations (ecosystem lock-in)
   
   CTO job: Build and protect the technical moat

3. TECHNOLOGY RADAR
   Track emerging technologies:
   ADOPT:   Ready for production use (stable, proven)
   TRIAL:   Worth trying on non-critical projects
   ASSESS:  Worth exploring, not ready for adoption
   HOLD:    Don't start new work with this technology

4. PLATFORM STRATEGY
   "Should we build a platform?"
   
   Rule of Three: Build a platform when 3+ consumers need it.
   Before 3: copy-paste is fine.
   
   Platform investment timeline:
   Year 1: Build for 1 consumer (learn the problem)
   Year 2: Generalize for 3 consumers (find patterns)
   Year 3: Self-service platform (scale without platform team)
```

---

## 5. Vendor Management

```
Vendor Selection:
  1. Requirements document (must-have vs nice-to-have)
  2. RFP (Request for Proposal) to 3+ vendors
  3. POC (Proof of Concept) with top 2
  4. Reference checks (talk to their customers)
  5. Contract negotiation

Negotiation Tips:
  - Always negotiate (initial price is never final)
  - Multi-year commitment = leverage for discount
  - Compete vendors against each other
  - Negotiate exit clause (data portability, migration support)
  - Cap price increases (max 5%/year)
  - Performance SLAs with penalties

Vendor Risk Management:
  - Avoid single vendor dependency for critical services
  - Abstract vendor integrations (adapter pattern)
  - Test failover scenarios
  - Annual vendor review (cost, performance, alternatives)
  
  Vendor lock-in avoidance:
  → Use standard protocols (SQL, REST, gRPC) not vendor-specific
  → Keep data in formats YOU control
  → Architecture: abstract infrastructure from business logic
```

---

## 📝 Bài tập

1. Create cloud cost optimization plan (audit current spending)
2. Build engineering budget proposal cho next quarter
3. Prepare CTO board presentation (mock)
4. Evaluate 1 vendor relationship: cost, value, alternatives

---

## 📚 Tài liệu
- *High Output Management* — Andy Grove
- *The Hard Thing About Hard Things* — Ben Horowitz
- *An Elegant Puzzle* — Will Larson (org scaling)
