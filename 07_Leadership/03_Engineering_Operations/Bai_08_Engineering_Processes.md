# Bài 08: Engineering Processes

## 🎯 Mục tiêu
- Sprint management that works
- On-call & incident response
- Blameless postmortems
- Change management

---

## 1. Sprint Management

```
Sprint ≠ Deadline factory
Sprint = Time-boxed iteration for learning & delivery

Healthy Sprint Pattern:
  Day 1 (Monday):   Sprint planning (1-2 hours)
  Daily (10 min):    Standup: blockers only, not status
  Mid-sprint:        Check progress, adjust if needed
  Last day:          Demo + Retrospective

Sprint Planning Checklist:
  □ Review last sprint velocity (avg story points completed)
  □ Don't commit more than avg velocity
  □ Leave 20% buffer for bugs, reviews, unexpected work
  □ Each story has clear acceptance criteria
  □ Stories are small enough to finish in 1-3 days
  □ Dependencies identified and owners assigned

Common Sprint Problems:
  Problem: Carry-over stories every sprint
  Cause: Over-commitment or stories too large
  Fix: Reduce commitment, break stories smaller

  Problem: Constant interruptions
  Cause: No buffer, no escalation process
  Fix: 20% buffer, rotate "interrupt handler" role

  Problem: All stories finish on last day
  Cause: Stories too big, no WIP limits
  Fix: WIP limit (max 2 stories in progress per person)
```

---

## 2. On-Call Best Practices

```
On-Call Goals:
  - Detect issues before users do
  - Respond quickly (within SLA)
  - Minimize user impact
  - Learn from every incident

On-Call Structure:
  Primary:   Responds to pages, investigates
  Secondary: Backup if primary unavailable, escalation
  Rotation:  Weekly, equal distribution across team
  Handoff:   Written summary of ongoing issues

Rules for Healthy On-Call:
┌─────────────────────────────────────────────────────────┐
│ 1. Max 25% of time on-call → fair rotation              │
│ 2. Comp time for overnight pages                        │
│ 3. Runbooks for every alert → know what to do            │
│ 4. Auto-escalation after 15min no response              │
│ 5. On-call doesn't mean 24/7 coding → protect rest      │
│ 6. If too many alerts → FIX THE SYSTEM, not burn people │
│ 7. New hires shadow on-call before being primary        │
│ 8. Track: pages/week, MTTA, MTTR → improve over time   │
└─────────────────────────────────────────────────────────┘

Alert Quality:
  Good alert: Actionable, clear what to do
  Bad alert: Noisy, wakes you up but no action needed
  
  Rule: Every alert that wakes someone up gets reviewed
  If no action taken → fix or remove the alert
  Target: < 2 pages per on-call shift (low noise)
```

---

## 3. Incident Response

```
Severity Levels:
  SEV1: Service down, data loss, security breach
    → All hands, 15min response, exec communication
  SEV2: Major feature broken, significant degradation
    → On-call team, 30min response
  SEV3: Minor feature issue, workaround exists
    → Next business day
  SEV4: Cosmetic, low-impact
    → Normal backlog priority

Incident Response Process:
  1. ALERT → On-call paged
  
  2. ACKNOWLEDGE (< 5 min)
     "I'm looking into the payment processing alert"
  
  3. TRIAGE (< 15 min)
     Determine severity, assemble team if needed
     Communication: #incident-xxx Slack channel
  
  4. MITIGATE
     Goal: RESTORE SERVICE, not find root cause
     Options: rollback, feature flag off, scale up, failover
     "Can we revert the last deployment?"
  
  5. COMMUNICATE
     Template: "What's happening → Impact → What we're doing → ETA"
     Update every 30 min
     Stakeholders: engineering, support, execs (severity-dependent)
  
  6. RESOLVE
     Service restored, monitoring confirms stability
     "All clear" communication
  
  7. POSTMORTEM
     Schedule within 48 hours while memory is fresh
```

---

## 4. Blameless Postmortems

```
Purpose: LEARN, not blame. Improve the SYSTEM, not punish people.

Postmortem Template:
┌─────────────────────────────────────────────────────────┐
│ INCIDENT SUMMARY                                         │
│ Date: 2024-01-15 | Duration: 45 min | Severity: SEV2   │
│ Impact: 5000 users unable to checkout for 45 minutes     │
│                                                          │
│ TIMELINE (UTC)                                           │
│ 14:00 — Deploy v2.3.1 (new payment flow)                │
│ 14:05 — Error rate spike to 15% (PagerDuty alert)       │
│ 14:08 — On-call acknowledges, begins investigation       │
│ 14:15 — Root cause: new payment API timeout (5s → 30s)  │
│ 14:20 — Decision: rollback to v2.3.0                     │
│ 14:35 — Rollback complete, error rate normal             │
│ 14:45 — All clear declared                               │
│                                                          │
│ ROOT CAUSE                                               │
│ New payment integration had 30s timeout (up from 5s).    │
│ Under load, connections pooled up, exhausting DB pool.   │
│                                                          │
│ WHAT WENT WELL                                           │
│ ✅ Alert fired within 5 minutes                          │
│ ✅ On-call responded quickly                             │
│ ✅ Rollback process worked smoothly                      │
│                                                          │
│ WHAT WENT WRONG                                          │
│ ❌ No load testing before deploy                         │
│ ❌ Timeout change not in review checklist                │
│ ❌ No circuit breaker on payment calls                   │
│                                                          │
│ ACTION ITEMS                                             │
│ 1. Add load test stage to CI/CD — @alice — 2024-01-22  │
│ 2. Implement circuit breaker — @bob — 2024-01-29       │
│ 3. Add timeout validation to review checklist — @carol  │
│ 4. Create runbook for payment service degradation       │
│                                                          │
│ LESSONS LEARNED                                          │
│ Timeout changes are high-risk. Treat like schema changes │
│ with explicit review and load testing.                   │
└─────────────────────────────────────────────────────────┘

Blameless Culture Rules:
  - "The system allowed this to happen" not "X caused this"
  - Ask "what" and "how", never "who"
  - Anyone can call a postmortem — no judgment
  - Publish postmortems openly (normalizes learning from failure)
  - Track action item completion (don't write & forget)
```

---

## 5. Change Management

```
Change = Risk. Manage it.

Change Types:
  Standard:   Low risk, pre-approved (e.g., config update)
  Normal:     Medium risk, needs review (e.g., new feature deploy)
  Emergency:  High risk, urgent (e.g., security patch, incident fix)

Pre-Change Checklist:
  □ What's changing? (specific, not vague)
  □ What could go wrong? (risk assessment)
  □ How do we rollback? (< 5 minutes?)
  □ Who is monitoring? (during and after)
  □ When to deploy? (not Friday 5pm!)
  □ Who to notify? (downstream teams, support)

Deploy Calendar:
  ✅ Tuesday-Thursday: normal deploys
  ❌ Friday: no non-urgent deploys (weekend support risk)
  ❌ Before holidays: no major changes
  🔄 Monday: catch-up deploys from weekend planning
```

---

## 📝 Bài tập

1. Audit current on-call: pages/week, MTTA, MTTR, alert quality
2. Run a blameless postmortem cho recent incident
3. Create incident response runbook cho top 3 failure scenarios
4. Implement deploy checklist for your team

---

## 📚 Tài liệu
- *Incident Management for Operations* — Rob Schnepp
- *Site Reliability Engineering* — Google
- *Accelerate* — Nicole Forsgren (DORA metrics)
