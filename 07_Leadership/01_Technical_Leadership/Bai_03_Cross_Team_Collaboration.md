# Bài 03: Cross-Team Collaboration

## 🎯 Mục tiêu
- Managing cross-team dependencies
- Organizational alignment
- Conflict resolution
- Building consensus at scale

---

## 1. Cross-Team Dependencies

```
Dependencies kill velocity. Minimize, manage, or eliminate.

Types:
1. BLOCKING: Team A can't start until Team B finishes
   → Most dangerous, creates delays
2. SHARED: Both teams need same resource/component
   → Requires coordination and ownership clarity
3. KNOWLEDGE: Team A needs info/expertise from Team B
   → Can often be async (documentation, design docs)

Management Strategies:
┌─────────────────────────────────────────────────────────┐
│ ELIMINATE                                                │
│ → Self-contained teams (own their full stack)            │
│ → Clear API contracts (teams are independent consumers)  │
│ → Platform teams (provide self-service tools)            │
│                                                          │
│ MINIMIZE                                                 │
│ → Plan dependencies in sprint planning                   │
│ → Use dependency tracker (spreadsheet or tool)           │
│ → Build interfaces/contracts early, implement later      │
│                                                          │
│ MANAGE                                                   │
│ → Cross-team sync meeting (weekly, 30min max)            │
│ → Shared Slack channel for blocked items                 │
│ → Escalation path: Direct → Manager → Director           │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Team Topologies

```
4 Team Types (Team Topologies by Skelton & Pais):

1. STREAM-ALIGNED TEAM
   → Owns a business domain end-to-end (order team, user team)
   → Most teams should be this type
   → Independent: build, deploy, operate their services

2. PLATFORM TEAM
   → Provides self-service infrastructure
   → Examples: CI/CD platform, developer tools, cloud infrastructure
   → Reduces cognitive load on stream-aligned teams

3. ENABLING TEAM
   → Helps other teams adopt new technologies
   → Examples: Security champions, ML platform team
   → Temporary engagement: teach, then move on

4. COMPLICATED SUBSYSTEM TEAM
   → Owns technically complex component
   → Examples: ML model training, video encoding
   → Deep expertise, used by other teams via API

Interaction Modes:
  Collaboration: Work together (temporary, expensive)
  X-as-a-Service: Use via API/interface (scalable)
  Facilitating: Help team adopt something (enabling team)
```

---

## 3. Conflict Resolution

```
Healthy Conflict = Productive debate about IDEAS
Unhealthy Conflict = Personal attacks, territorial battles

Framework for Technical Disagreements:

STEP 1: UNDERSTAND both positions
  "Help me understand why you prefer approach A."
  Listen without interrupting. Repeat back: "So you're saying..."

STEP 2: FIND COMMON GROUND
  "We both agree the system needs to scale. 
   We disagree on HOW to scale it."

STEP 3: USE DATA
  "Let's benchmark both approaches. Whoever's approach 
   performs better under load test, we go with that."

STEP 4: TIME-BOX
  "Let's spend 1 hour prototyping each. Compare results."

STEP 5: DECIDE & COMMIT
  If no consensus → escalate to decision-maker
  Decision-maker decides → everyone commits
  "I disagree but I'll fully commit to making this work."

Common Conflict Sources in Engineering:
  - Architecture debates (monolith vs microservices)
  - Technology choices (language, framework, database)
  - Ownership boundaries (who owns this service?)
  - Priority disagreements (features vs tech debt)
  - Code style/approach differences

For each: ask "Is this a one-way door?" 
  Yes → thorough analysis needed
  No → decide quickly, iterate
```

---

## 4. Building Consensus at Scale

```
Consensus ≠ Everyone agrees
Consensus = Everyone can accept and commit

Consensus-Building Techniques:

1. PROPOSAL DOC (async, scalable)
   Write RFC → Share for comments (1 week) → Address concerns
   → Schedule decision meeting (if needed)
   Most decisions can be made async via docs

2. DECISION MATRIX
   List options, criteria, scores:
   "Based on these 5 criteria, Option B scores highest.
    Does anyone have a criterion we missed?"

3. RACI CHART (for large decisions)
   R — Responsible: Does the work
   A — Accountable: Makes the call (ONE person)
   C — Consulted: Provides input before decision
   I — Informed: Told after decision
   
   Clearn RACI prevents: "Wait, I thought I had a say?"

4. ADVISORY PROCESS
   Decision-maker MUST seek advice from:
   - People affected by the decision
   - People with relevant expertise
   But decision-maker makes the final call
   → Faster than consensus, more inclusive than autocracy

5. DISAGREE AND COMMIT (Amazon principle)
   "I've heard everyone's input. I'm going with Option B.
    I know some prefer A. Let's commit fully to B and
    evaluate results in 3 months."
```

---

## 5. Working with Product & Design

```
Engineer-PM Partnership:
  PM: WHAT to build & WHY (market, users, business goals)
  Engineer: HOW to build & feasibility (tech constraints, estimates)
  
  Healthy dynamic:
  PM: "Users need faster search results"
  Eng: "We can achieve sub-100ms with caching (2 weeks) or 
       full rewrite (2 months). Caching gets us 80% there."
  PM: "Let's go with caching. We'll validate if 80% is enough."

  Anti-patterns:
  ❌ PM dictates technical solution: "Use ElasticSearch"
  ❌ Engineer ignores business: "Let me rewrite everything first"
  ❌ No pushback: silently accepting impossible deadlines
  
  Healthy pushback:
  "I want to make this work, but this timeline requires cutting X.
   Here are three options with different scope/timeline trade-offs."
```

---

## 📝 Bài tập

1. Map all cross-team dependencies of your team
2. Define RACI for 3 upcoming decisions
3. Practice conflict resolution: facilitate a technical debate
4. Write a proposal doc, share for async feedback, make a decision

---

## 📚 Tài liệu
- *Team Topologies* — Matthew Skelton & Manuel Pais
- *An Elegant Puzzle* — Will Larson
- *Crucial Conversations* — Patterson, Grenny, McMillan
