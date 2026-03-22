# Bài 04: Hiring & Team Building

## 🎯 Mục tiêu
- Design effective interview process
- Hiring bar & evaluation criteria
- Diversity & inclusion in hiring
- Onboarding for success

---

## 1. Interview Process Design

```
Goal: Predict on-the-job performance → reduce false positives & negatives

Structured Interview Process:
┌───────────────────────────────────────────────────────────┐
│ Stage 1: RESUME SCREEN (10 min)                           │
│   Focus: relevant experience, projects, progression       │
│   Anti-bias: blind review (remove name, school, photo)    │
│                                                           │
│ Stage 2: PHONE SCREEN (30 min)                            │
│   Technical conversation, problem-solving approach        │
│   "Tell me about a challenging system you built"          │
│   Evaluate: communication, depth of knowledge             │
│                                                           │
│ Stage 3: TECHNICAL INTERVIEW (60 min × 2)                 │
│   a) Coding: Real-world problem, not leetcode trick       │
│   b) System design: Architecture discussion               │
│   Evaluate: problem-solving, code quality, trade-offs     │
│                                                           │
│ Stage 4: BEHAVIORAL / VALUES (45 min)                     │
│   Structured behavioral questions (STAR format)           │
│   "Tell me about a time you disagreed with your team"     │
│   Evaluate: collaboration, growth mindset, communication  │
│                                                           │
│ Stage 5: TEAM FIT / REVERSE INTERVIEW (30 min)            │
│   Candidate asks questions, meet future teammates         │
│   This is also selling — make candidate want to join      │
│                                                           │
│ Stage 6: DEBRIEF (30 min)                                 │
│   All interviewers discuss independently first            │
│   Then share scores → discuss → hire/no-hire decision     │
└───────────────────────────────────────────────────────────┘
```

---

## 2. Evaluation Criteria

```
Scoring Rubric (1-4 per criterion):
  4 — Strong hire: Exceeds bar significantly
  3 — Hire: Meets bar
  2 — Lean no: Below bar
  1 — Strong no: Significantly below bar

Criteria for Software Engineers:
┌────────────────────────┬──────────────────────────────────┐
│ Technical Skills       │ Problem solving, code quality,    │
│                        │ system design, testing            │
│ Communication          │ Explains thinking clearly,        │
│                        │ asks good questions               │
│ Collaboration          │ Gives/receives feedback,          │
│                        │ works well with others            │
│ Growth Mindset         │ Learns from mistakes,             │
│                        │ adapts to new information         │
│ Impact/Ownership       │ Drives results, takes initiative, │
│                        │ considers broader impact          │
└────────────────────────┴──────────────────────────────────┘

Hiring Bar by Level:
  Junior:  Can they learn quickly? Are fundamentals solid?
  Mid:     Can they deliver independently? Good code quality?
  Senior:  Can they own complex features? Mentor others?
  Staff:   Can they drive technical direction? Influence org?

Red flags:
  - Can't explain their own project's architecture
  - Blames others for failures (no accountability)
  - No questions about the team/product (not curious)
  - Can't handle ambiguity (needs everything specified)
```

---

## 3. Diversity & Inclusive Hiring

```
Why Diversity Matters (beyond ethics):
  - Diverse teams make better decisions (different perspectives)
  - Correlation with better financial performance
  - Better product for diverse user base
  - Larger talent pool

Reducing Bias:
  1. Job descriptions: Remove gendered language
     ❌ "ninja", "rockstar", "crush it"
     ✅ "build", "collaborate", "design"
     Tool: textio.com — analyzes job posting bias

  2. Sourcing: Diversify pipeline
     → Post on diverse job boards
     → Employee referrals (but watch for homogeneity)
     → University partnerships beyond top-10 schools

  3. Screening: Structured rubric  
     → Same questions for every candidate
     → Score before discussing with others
     → Remove identifying info from resume review

  4. Interview panel: Diverse interviewers
     → Not all same background/gender/level
     → Train interviewers on bias awareness

  5. Evaluation: Calibrate regularly
     → Review hiring data: conversion rates by demographics
     → Are we applying bar consistently?
```

---

## 4. Onboarding

```
Goal: New hire productive in 30 days, confident in 90 days

Week 1: ORIENTATION
  Day 1: Setup (laptop, accounts, tools, Slack channels)
  Day 2: Architecture overview (big picture)
  Day 3: Codebase walkthrough with buddy
  Day 4-5: First small PR (typo fix, doc update, small bug)
  → Psychological win: ship code in first week

Week 2-4: RAMP UP
  Week 2: Paired programming on a feature
  Week 3: Independent small feature (with review support)
  Week 4: First on-call shadow (observe, not primary)
  → Regular 1:1 with manager + buddy

Day 30 CHECK-IN: "What's confusing? What's missing?"

Month 2-3: INDEPENDENT
  Own a medium feature end-to-end
  Participate in design reviews
  Start doing code reviews
  On-call rotation (with senior backup)

Day 90 CHECK-IN: "What would improve onboarding?"

Onboarding Buddy:
  - NOT the manager (different relationship)
  - Same or slightly higher level
  - Available for "dumb questions" (no judgment)
  - Meets daily for first 2 weeks, then weekly
```

---

## 5. Building the Right Team

```
Team Composition (ideal 5-8 people):
  - Mix of levels: 1 senior/staff + 2-3 mid + 1-2 junior
  - T-shaped skills: deep in 1 area, broad across others
  - Cognitive diversity: different thinking styles, backgrounds

Conway's Law:
  "Organizations design systems that mirror their 
   communication structures"
  → Design teams around the architecture you want
  → Team owns a service? Service will have clear boundaries
  → Two teams share a service? Service will have unclear ownership

Signs of a Healthy Team:
  ✅ Members genuinely help each other
  ✅ Healthy debate in design reviews
  ✅ Knowledge is shared (no silos)
  ✅ People volunteer for hard problems
  ✅ Failures are learning opportunities

Signs of Trouble:
  ❌ One person is always the hero
  ❌ People afraid to ask questions
  ❌ Blaming culture after incidents
  ❌ Knowledge hoarding ("only I know this")
  ❌ Consistently working overtime
```

---

## 📝 Bài tập

1. Design interview process cho team: questions, rubric, scorecard
2. Review 5 job descriptions for bias, rewrite one
3. Create 30-60-90 onboarding plan cho your team
4. Assess team composition: what skills are missing?

---

## 📚 Tài liệu
- *Who* — Geoff Smart & Randy Street (hiring)
- *The Making of a Manager* — Julie Zhuo (Chapter on hiring)
- *Thinking, Fast and Slow* — Daniel Kahneman (on bias)
