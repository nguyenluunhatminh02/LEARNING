# Bài 02: Technical Communication

## 🎯 Mục tiêu
- Writing effective RFCs & design docs
- Presenting to executives (non-technical audience)
- Stakeholder management
- Written communication best practices

## 📖 Câu chuyện đời thường
> Bạn là bác sĩ giải thích bệnh cho bệnh nhân. Nếu nói thuật ngữ chuyên môn — bệnh nhân không hiểu. Nếu nói "phổi bị nhiễm khuẩn, cần uống thuốc 7 ngày" — hiểu ngay. Đó là kỹ năng **trình bày cho người không kỹ thuật**. **RFC** giống bản đề xuất phương án điều trị: vấn đề, các lựa chọn, khuyến nghị — gửi cho hội đồng góp ý trước khi làm. **Stakeholder management** là biết bệnh nhân (user), gia đình (PM), bảo hiểm (finance) cần nghe gì khác nhau.

---

## 1. Writing Design Documents / RFCs

```markdown
# Design Doc Template

## Title: [Feature/System Name]
## Author: [Name] | Date: [Date] | Status: [Draft/In Review/Approved]
## Reviewers: @person1, @person2, @person3

### 1. Context & Problem Statement
WHY are we doing this? What problem does this solve?
- Business impact: "Users abandoning checkout at 30% rate"
- Technical need: "Current system can't handle projected load"
Include data/metrics when possible.

### 2. Goals & Non-Goals
Goals:
- Reduce checkout abandonment to < 15%
- Handle 10x current traffic

Non-Goals (explicitly state what you're NOT solving):
- Mobile app redesign (separate project)
- Payment provider migration

### 3. Proposed Solution
High-level architecture, diagrams, key decisions explained.
Explain the WHY behind each choice.

### 4. Alternatives Considered
What else did you evaluate? Why was it rejected?
This builds trust and shows thorough analysis.

### 5. Technical Design
API contracts, data models, sequence diagrams.
Enough detail to implement, not so much that it becomes code.

### 6. Migration / Rollout Plan
How to get from current state to new state.
Phased approach, feature flags, backward compatibility.

### 7. Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

### 8. Open Questions
Things not yet decided — invite discussion.

### 9. Timeline
Rough estimate by phase/milestone.
```

---

## 2. Presenting to Executives

```
Executive Communication Rules:

1. LEAD WITH IMPACT (not technical details)
   ❌ "We need to migrate from PostgreSQL to CockroachDB for 
       multi-region active-active replication"
   ✅ "We can reduce downtime from 4 hours/year to near-zero,
       which prevents ~$2M in lost revenue"

2. PYRAMID STRUCTURE (conclusion first)
   ❌ "We investigated 3 options, analyzed trade-offs, ...
       and we recommend Option B"
   ✅ "We recommend Option B (save $500K/year). Here's why..."

3. THREE KEY POINTS (max)
   Executives retain 3 things. If you have 10 points, 
   group into 3 themes.

4. ANSWER SO WHAT?
   Every technical fact needs a business translation:
   "Response time improved from 2s to 200ms"
   → "Users convert 15% more, adding ~$100K MRR"

5. PREPARE FOR QUESTIONS
   "What if this fails?" → Have mitigation plan ready
   "How much will it cost?" → TCO comparison
   "When will it be done?" → Timeline with milestones
   "Why not do the simpler thing?" → Trade-off explanation
```

### The 1-3-1 Framework
```
For any proposal or update:

1 — ONE situation/context (1 sentence)
  "Our API latency exceeds SLA for 5% of users."

3 — THREE options (pros/cons each)
  A: Add caching layer ($, 2 weeks, 70% improvement)
  B: Optimize DB queries (free, 4 weeks, 50% improvement)
  C: Scale horizontally ($$, 1 week, 90% improvement)

1 — ONE recommendation
  "I recommend C: fastest to implement, biggest impact.
   Then follow up with B to reduce ongoing costs."
```

---

## 3. Stakeholder Management

```
Stakeholder Map:
┌─────────────────────────────────────────────────────────┐
│                     HIGH INFLUENCE                       │
│                                                          │
│  MANAGE CLOSELY          │  KEEP SATISFIED               │
│  (CEO, VP Eng, Product)  │  (Board, Legal, Finance)      │
│  Regular updates,        │  Inform on schedule,           │
│  involve in decisions    │  address concerns proactively  │
│                          │                                │
│ ─────────────────────────┼──────────────────────────────  │
│                          │                                │
│  KEEP INFORMED           │  MONITOR                      │
│  (Dependent teams,       │  (Other departments,           │
│   downstream consumers)  │   external partners)           │
│  Status updates,         │  Minimal communication,        │
│  heads-up on changes     │  respond to inquiries          │
│                          │                                │
│                     LOW INFLUENCE                         │
└─────────────────────────────────────────────────────────┘

Communication Cadence:
  High-power stakeholders: Weekly 1:1 or updates
  Medium: Bi-weekly summary email
  Low: Monthly newsletter or status page

Managing Up (to your manager/VP):
  - No surprises: Escalate risks early
  - Come with solutions: "We have a problem. I recommend X."
  - Keep them informed: They need to advocate for your team
  - Understand their pressures: What does THEIR boss care about?
```

---

## 4. Written Communication

```
Engineering Writing Best Practices:

EMAILS / SLACK MESSAGES:
  - First line = action needed: "Need your approval by Friday"
  - Bold key decisions/questions
  - Use bullet points, not paragraphs
  - One topic per message

STATUS UPDATES:
  Format: Traffic light (Green/Yellow/Red)
  🟢 On track: [what's going well]
  🟡 At risk: [potential issues, mitigation plan]
  🔴 Blocked: [what's needed to unblock]
  
  ❌ BAD: "We're making progress on the migration"
  ✅ GOOD: "Migration 70% complete (14/20 services). 
     On track for March deadline. 
     Risk: Payment service needs extra week for PCI compliance."

INCIDENT COMMUNICATION:
  Template: "What happened → Impact → What we're doing → ETA"
  Update every 30 minutes during active incident.
  "Payment processing is down since 14:00 UTC. 
   ~2000 users affected. 
   Root cause identified: DB connection pool exhaustion.
   Fix deploying now. ETA: 30 minutes."

DOCUMENTATION:
  - Write for someone joining in 6 months
  - Include WHY, not just HOW
  - Keep next to code (docs/ folder, READMEs)
  - Review and update quarterly
```

---

## 📝 Bài tập

1. Write a design doc for a feature using the template above
2. Practice the 1-3-1 framework: present a technical proposal
3. Map your stakeholders, create communication cadence
4. Rewrite a technical email for an executive audience

---

## 📚 Tài liệu
- *The Pyramid Principle* — Barbara Minto
- *Writing Without Bullshit* — Josh Bernoff
- *Staff Engineer* — Will Larson (Chapter on communication)
