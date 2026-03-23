# Bài 09: Engineering Metrics & Developer Productivity

## 🎯 Mục tiêu
- DORA metrics & software delivery performance
- SPACE framework for developer productivity
- Developer experience (DevEx)
- Making investment cases for engineering tools

## 📖 Câu chuyện đời thường
> Bạn quản lý một nhà máy và cần biết: sản xuất nhanh hay chậm? chất lượng ra sao? **DORA metrics** giống 4 chỉ số chính của nhà máy: tần suất xuất hàng (deployment frequency), thời gian từ đơn đến giao (lead time), tỷ lệ hàng lỗi (change failure rate), thời gian sửa lỗi (MTTR). **DevEx** giống đầu tư máy móc tốt cho công nhân: máy cũ kẹt liên tục, công nhân bực bội và chậm. Mua máy mới đắt nhưng năng suất tăng 3x — đó là **investment case**: chi tiền tool để tiết kiệm thời gian người.

---

## 1. DORA Metrics

```
(DevOps Research & Assessment — validated by 7 years of research)

4 Key Metrics:
┌──────────────────────────┬────────────┬────────────┬────────────┐
│ Metric                   │ Elite      │ High       │ Low        │
├──────────────────────────┼────────────┼────────────┼────────────┤
│ Deployment Frequency     │ On-demand  │ Weekly     │ Monthly+   │
│ (How often you deploy)   │ (multiple/ │            │            │
│                          │  day)      │            │            │
├──────────────────────────┼────────────┼────────────┼────────────┤
│ Lead Time for Changes    │ < 1 hour   │ < 1 week   │ > 1 month  │
│ (Commit → production)    │            │            │            │
├──────────────────────────┼────────────┼────────────┼────────────┤
│ Change Failure Rate      │ 0-15%      │ 16-30%     │ > 45%      │
│ (% deploys causing       │            │            │            │
│  incidents)              │            │            │            │
├──────────────────────────┼────────────┼────────────┼────────────┤
│ Mean Time to Recover     │ < 1 hour   │ < 1 day    │ > 1 week   │
│ (Incident → resolution)  │            │            │            │
└──────────────────────────┴────────────┴────────────┴────────────┘

Key Insight: Speed AND stability go TOGETHER
  Elite teams deploy more often AND have fewer failures.
  Shipping small changes frequently = less risk per change.

How to measure:
  Deployment Frequency: Count deployments per day/week
  Lead Time: Timestamp from commit → deployed to prod
  Change Failure Rate: Incidents / Deployments
  MTTR: Incident start → service restored

Where to get data:
  GitHub (commits, PRs), CI/CD (deploys), PagerDuty (incidents)
```

---

## 2. SPACE Framework

```
(Microsoft Research — holistic developer productivity)

S — Satisfaction & Well-being
  "Are developers happy and sustainable?"
  Measure: Survey (1-5 satisfaction), work-life balance questions
  
P — Performance
  "What outcomes does the team deliver?"
  Measure: Customer impact, reliability, quality metrics

A — Activity
  "What do developers do?" (proxy metrics, handle with care)
  Measure: PRs merged, deployments, code reviews completed
  ⚠️ WARNING: Never use activity as productivity!
  Lines of code ≠ productivity. PRs/day ≠ productivity.

C — Communication & Collaboration
  "How well does the team communicate?"
  Measure: PR review time, knowledge sharing, meeting effectiveness

E — Efficiency & Flow
  "Can developers get work done without interruptions?"
  Measure: Time-in-flow, wait times, blocked tasks

Best practice: Measure across MULTIPLE dimensions.
  Activity alone → Goodhart's Law ("when a measure becomes a target,
  it ceases to be a good measure")
```

---

## 3. Developer Experience (DevEx)

```
DevEx = How easy/pleasant is it to be productive?

Three Dimensions (DX Research):
  1. FEEDBACK LOOPS — How fast do I know if my code works?
     Build time: < 1 min (local), < 10 min (CI)
     Test time: < 30s (unit), < 10 min (full suite)
     Review time: < 4 hours for first review
     Deploy time: < 15 min (commit → production)

  2. COGNITIVE LOAD — How much do I need to remember?
     Documentation: Can I find answers easily?
     Tooling: Do tools handle complexity for me?
     Architecture: Is the system understandable?
     Onboarding: Can new member be productive in 2 weeks?

  3. FLOW STATE — Can I focus for extended periods?
     Interruptions: < 2 per focus block
     Context switching: Minimize multi-project work
     Meeting load: < 30% of week in meetings
     Tools work: No fighting broken CI, flaky tests

DevEx Improvements (highest ROI):
┌────────────────────────────┬──────────┬─────────────────┐
│ Improvement                │ Effort   │ Impact          │
├────────────────────────────┼──────────┼─────────────────┤
│ Fix flaky tests            │ Medium   │ HIGH (everyone) │
│ Speed up CI from 30→10min  │ Medium   │ HIGH (every PR) │
│ Better error messages      │ Low      │ Medium          │
│ Local dev environment      │ High     │ HIGH (daily)    │
│ Self-service infrastructure│ High     │ HIGH (unblocks) │
│ Documentation improvement  │ Low      │ Medium          │
│ PR template/checklist      │ Low      │ Low-Medium      │
└────────────────────────────┴──────────┴─────────────────┘
```

---

## 4. Making Investment Cases

```
How to justify engineering tool/infrastructure investment:

STEP 1: Quantify the problem
  "CI takes 30 minutes. We run 50 CI builds/day.
   50 × 30min = 25 hours of developer waiting time/day.
   With 20 engineers at $75/hr, that's $1,875/day = $487K/year."

STEP 2: Propose solution with expected improvement
  "Upgrading CI to parallel execution: estimated 30min → 10min.
   Saves 16.7 hours/day = $325K/year in developer time."

STEP 3: Cost of solution
  "Better CI runners: $2K/month = $24K/year."

STEP 4: ROI
  "Investment: $24K/year. Savings: $325K/year. ROI: 13.5x."

Common Engineering Investments:
  Build systems: Fast builds → faster iteration
  Testing infra: Reliable tests → fewer incidents
  Dev environments: Easy setup → faster onboarding
  Documentation: Self-service → less knowledge bottleneck
  Monitoring/Observability: Faster debugging → lower MTTR
  
Present to executives:
  ❌ "We need to upgrade our CI infrastructure"
  ✅ "We can ship features 40% faster with a $24K investment.
      Here's the data showing $325K in developer time savings."
```

---

## 5. Engineering Dashboard

```
CTO Dashboard: Track monthly

Delivery:
  📊 Deployment frequency: ___ /week (target: daily)
  📊 Lead time: ___ hours (target: < 4 hours)
  📊 Change failure rate: ___% (target: < 15%)
  📊 MTTR: ___ hours (target: < 1 hour)

Quality:
  📊 Bug escape rate: ___ bugs found in prod / sprint
  📊 Test coverage: ___% (trend, not absolute number)
  📊 Flaky test rate: ___% (target: < 1%)

Productivity:
  📊 PR review time: ___ hours (target: < 4 hours)
  📊 Developer satisfaction: ___/5 (quarterly survey)
  📊 Onboarding time to first PR: ___ days (target: < 5)

Health:
  📊 On-call pages: ___ /week (target: < 2)
  📊 Team NPS (Net Promoter Score): ___
  📊 Attrition rate: ___% (target: < 10%/year)
```

---

## 📝 Bài tập

1. Measure DORA metrics cho team hiện tại
2. Run developer satisfaction survey using SPACE dimensions
3. Identify top 3 DevEx bottlenecks, prioritize improvements
4. Build business case for 1 engineering tool investment

---

## 📚 Tài liệu
- *Accelerate* — Nicole Forsgren, Jez Humble, Gene Kim
- [SPACE Framework paper](https://queue.acm.org/detail.cfm?id=3454124)
- [DORA State of DevOps Report](https://dora.dev/)
