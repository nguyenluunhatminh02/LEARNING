# Bài 07: Project & Program Management

## 🎯 Mục tiêu
- Software estimation techniques
- Project planning & risk management
- Managing scope & stakeholder expectations
- Agile at scale

---

## 1. Software Estimation

```
Estimation is HARD. Be honest about uncertainty.

Techniques:
1. T-SHIRT SIZING (strategic planning)
   XS (< 1 day) | S (1-3 days) | M (1-2 weeks) | L (2-4 weeks) | XL (1+ month)
   → Good for roadmap planning, bad for sprint commitment

2. STORY POINTS (relative estimation)
   Compare to known reference: "Auth feature was 5 points.
   This is about twice as complex → 8 points."
   Fibonacci: 1, 2, 3, 5, 8, 13, 21
   → Good for sprint planning, needs calibration

3. THREE-POINT ESTIMATE (when precision matters)
   Optimistic (O): Everything goes perfectly → 3 days
   Likely (M):     Normal amount of surprises → 7 days
   Pessimistic (P): Murphy's Law → 15 days
   Expected = (O + 4M + P) / 6 = (3 + 28 + 15) / 6 ≈ 8 days

Why estimates fail:
  - Planning fallacy: humans are optimistic by nature
  - Unknown unknowns: can't estimate what you can't predict
  - Dependencies: waiting for other teams
  - Context switching: meetings, incidents, reviews
  - Scope creep: "while we're at it, can you also..."

Estimation Tips:
  ✅ Add buffer: Multiply by 1.5-2x for unknowns
  ✅ Timeboxed spikes: "I'll spend 2 days investigating, then estimate"
  ✅ Break into small pieces: Easier to estimate 10 small tasks
  ✅ Historical data: "Similar features took X days"
  ✅ Estimate as a team: Planning poker reduces individual bias
  ✅ Ranges, not points: "5-8 days" better than "6 days"
```

---

## 2. Project Planning

```
Project Planning Framework:

PHASE 1: SCOPE (Week 1)
  - Define success criteria (measurable)
  - List requirements (must-have vs nice-to-have)
  - Identify dependencies & risks
  - Get stakeholder sign-off on scope

PHASE 2: DESIGN (Week 1-2)
  - Technical design doc / RFC
  - API contracts & data models
  - Review with team & stakeholders

PHASE 3: BREAKDOWN (Week 2)
  - Epics → Stories → Tasks
  - Estimate each task
  - Identify critical path
  - Assign owners

PHASE 4: SCHEDULE (Week 2)
  - Milestones with dates
  - Buffer (20% of total estimate)
  - Dependencies mapped
  - Risk mitigation planned

PHASE 5: EXECUTE
  - Track weekly: on track / at risk / blocked
  - Re-estimate when scope changes
  - Communicate status proactively

Critical Path:
  Longest sequence of dependent tasks
  Any delay on critical path → delays entire project
  Focus attention on critical path tasks
```

---

## 3. Risk Management

```
Risk = Probability × Impact

Risk Register:
┌──────────────────┬──────┬────────┬──────────────────────┐
│ Risk             │ Prob │ Impact │ Mitigation           │
├──────────────────┼──────┼────────┼──────────────────────┤
│ API provider     │ Med  │ High   │ Abstract integration,│
│ changes contract │      │        │ contract tests       │
├──────────────────┼──────┼────────┼──────────────────────┤
│ Key person leaves│ Low  │ High   │ Knowledge sharing,   │
│                  │      │        │ documentation        │
├──────────────────┼──────┼────────┼──────────────────────┤
│ Performance      │ Med  │ Med    │ Load test in staging │
│ doesn't meet SLA │      │        │ before launch        │
├──────────────────┼──────┼────────┼──────────────────────┤
│ Scope creep      │ High │ Med    │ Change request       │
│                  │      │        │ process, say NO      │
└──────────────────┴──────┴────────┴──────────────────────┘

Risk Responses:
  AVOID:    Change plan to eliminate risk
  MITIGATE: Reduce probability or impact
  TRANSFER: Insurance, outsource, SLA with vendor
  ACCEPT:   Low probability + low impact → acknowledge & move on
```

---

## 4. Scope Management

```
Scope Creep = #1 project killer

Prevention:
  1. Written scope document: signed off by stakeholders
  2. Change request process:
     "New request → Estimate impact → Stakeholder decides 
      (add scope = push deadline OR cut something else)"
  3. MoSCoW prioritization:
     Must have: Ship won't sail without it
     Should have: Important but workaround exists
     Could have: Nice to have if time permits
     Won't have: Explicitly out of scope (this round)

Handling "Can you also add...":
  "Great idea! Let me estimate the impact. 
   Adding this would push delivery by 1 week. 
   Should we delay, or replace another feature?"
  
  → Never "no" outright — show trade-offs
  → Never "yes" without acknowledging impact
  
  CTO tip: Protect scope aggressively.
  Every "quick addition" adds testing, docs, maintenance forever.
```

---

## 5. Scaling Agile

```
Small team (1 team): Scrum/Kanban works well
Multiple teams (3-10): Need coordination mechanism

Coordination Patterns:
1. SCRUM OF SCRUMS
   Representatives from each team meet weekly
   Share: progress, blockers, cross-team dependencies
   Simple, low overhead

2. SHAPE UP (Basecamp)
   6-week cycles: shaped work → build → cooldown
   No backlogs, no sprints, no story points
   Appetite-based: "We'll spend 2 weeks on this, max"
   Good for product teams

3. QUARTERLY PLANNING
   Every quarter: priorities set at org level
   Teams self-organize into the work
   Mid-quarter check: adjust if needed
   
   Planning inputs (from each team):
   - What we'll deliver (committed)
   - What we might deliver (stretch)
   - Risks and dependencies
   - Capacity constraints

Don't over-process:
  More process = more overhead = less building
  Add process only when pain emerges
  Remove process that doesn't add value
```

---

## 📝 Bài tập

1. Estimate a real project using three-point estimation
2. Create a project plan with milestones, critical path, risk register
3. Practice scope negotiation: "add feature X" → propose trade-offs
4. Run a planning poker session with your team

---

## 📚 Tài liệu
- *Software Estimation Without Guessing* — George Dinwiddie
- *Shape Up* — Ryan Singer (Basecamp)
- *An Elegant Puzzle* — Will Larson (team scaling)
