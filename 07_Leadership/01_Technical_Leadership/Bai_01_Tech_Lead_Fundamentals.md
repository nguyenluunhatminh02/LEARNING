# Bài 01: Tech Lead Fundamentals

## 🎯 Mục tiêu
- Tech Lead role & responsibilities
- Influence without authority
- Technical mentoring & sponsorship
- Balancing coding vs leading

---

## 1. Tech Lead Role Definition

```
Tech Lead ≠ Boss
Tech Lead = Technical multiplier + team enabler

Responsibilities:
┌─────────────────────────────────────────────────────────┐
│ TECHNICAL                                                │
│ • Set technical direction for the team                   │
│ • Make key architecture decisions (or facilitate them)   │
│ • Code review — maintain quality bar                     │
│ • Unblock team members on technical problems             │
│ • Prototype high-risk/uncertain features                 │
│                                                          │
│ PROCESS                                                  │
│ • Break features into tasks, estimate effort             │
│ • Define done criteria, ensure testability               │
│ • Identify technical risks early                         │
│ • Communicate technical constraints to PM/stakeholders   │
│                                                          │
│ PEOPLE                                                   │
│ • Mentor junior/mid engineers                            │
│ • Pair programming on complex problems                   │
│ • Create safe environment for questions                  │
│ • Advocate for team's technical needs                    │
└─────────────────────────────────────────────────────────┘

Time allocation (varies by team size):
  Small team (3-5):  50% coding, 30% review/unblock, 20% planning
  Large team (6-10): 30% coding, 30% review/unblock, 40% planning/comms
```

---

## 2. Influence Without Authority

```
Tech Lead thường KHÔNG phải manager → how to lead without power?

Techniques:
1. BUILD TRUST — Deliver quality code, be reliable, follow through
2. LISTEN FIRST — Understand concerns before proposing solutions
3. DATA-DRIVEN — "Metrics show X" > "I think we should..."
4. PROPOSE, DON'T IMPOSE — "What if we tried X?" > "We must do X"
5. GIVE CREDIT — "Team A's approach inspired this solution"
6. ADMIT MISTAKES — "I was wrong about X, here's what I learned"

Decision-Making Framework:
  Reversible (two-way door):
    → Make decision, move fast, adjust later
    → "Let's try this approach for 2 weeks"
  
  Irreversible (one-way door):
    → Consult team, gather data, build consensus
    → "Let's discuss in design review before committing"
  
  Disagreement:
    → "I disagree but I'll commit. Let's set a review date."
    → Never: "I told you so" — instead: "Here's what we learned"
```

---

## 3. Technical Mentoring

```
Levels of Support:

TELLING (junior, urgent):
  "Here's exactly how to fix this. Change line 42 to..."
  → Fast but low learning

TEACHING (junior, normal):
  "This is called the N+1 problem. It means..."
  → Transfer knowledge, explain WHY

COACHING (mid-level):
  "What do you think is causing the slowness? What would you try?"
  → Guide their thinking, don't give answers

DELEGATING (senior):
  "I trust you with this decision. Loop me in if you need a sounding board"
  → Empower, stay available

Mentoring practices:
- Pair programming: work together on complex features
- Design review: let them present, guide with questions
- Progressive responsibility: simple → complex → critical path
- Regular 1:1 technical discussions: "What are you learning?"
- Writing: encourage blog posts, documentation, ADRs

Sponsorship (beyond mentoring):
  Mentoring = "Here's what I think"
  Sponsorship = "I'll advocate for you in rooms you're not in"
  → Nominate for high-visibility projects
  → Recommend for promotions
  → Give credit publicly
```

---

## 4. Balancing Coding vs Leading

```
The Trap: "I can code this faster myself"
  → True short-term, destructive long-term
  → Your job: make TEAM faster, not yourself

What to code:
  ✅ Prototypes / spikes (explore uncertain areas)
  ✅ Critical path infrastructure (shared by many)
  ✅ Code reviews (most impactful "coding" activity)
  ✅ Pair programming (teach while building)
  
What NOT to code (delegate):
  ❌ Feature work on the critical path (you'll become bottleneck)
  ❌ Everything (you'll lose context and credibility)
  ❌ Production bug fixes (unless you're the only one who can)

Signs you're doing too much:
  - Team waits for your review/input
  - You're the only one who touches certain code
  - No one else can explain the architecture
  - Your PRs are the biggest ones

Signs you're doing too little:
  - You can't review code effectively (lost context)
  - Team doesn't trust your technical judgment
  - Architecture decisions feel disconnected
  - You become "the meeting person"

Healthy balance:
  Keep hands in code enough to stay credible
  Delegate enough to develop others and scale
```

---

## 5. Common Tech Lead Anti-patterns

```
❌ Hero Mode: "Only I can fix this"
  → Creates single point of failure
  Fix: Document everything, pair program, delegate

❌ Code Gatekeeper: All PRs must go through me
  → Bottleneck, disempowering
  Fix: Establish coding standards, trust reviewers, review selectively

❌ Architecture Astronaut: Over-engineer everything
  → Slows team, premature abstraction
  Fix: YAGNI, start simple, refactor when needed

❌ Conflict Avoider: Never push back on bad ideas
  → Technical debt accumulates, team loses direction
  Fix: Disagree constructively, with data

❌ Meeting Monster: Calendar full, no coding time
  → Lose technical context, can't help team
  Fix: Block calendar for focused work, say no to non-essential meetings

❌ Perfectionist: Nothing ships until it's perfect
  → Velocity drops, team gets frustrated
  Fix: "Ship it, iterate" — define MVP criteria clearly
```

---

## 📝 Bài tập

1. Self-assess: What % of time coding vs leading vs meetings?
2. Identify 3 things you do that should be delegated
3. Set up mentoring relationship with 1 junior engineer
4. Practice influence: propose 1 improvement without using authority

---

## 📚 Tài liệu
- *The Staff Engineer's Path* — Tanya Reilly
- *The Manager's Path* — Camille Fournier (Chapters 3-4)
- *Team Topologies* — Matthew Skelton & Manuel Pais
