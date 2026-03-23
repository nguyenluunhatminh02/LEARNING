# Bài 06: Team Health & Culture

## 🎯 Mục tiêu
- Psychological safety
- Team dynamics & Tuckman's stages
- Remote/hybrid leadership
- Preventing burnout

## 📖 Câu chuyện đời thường
> **Psychological safety** giống lớp học nơi học sinh dám giơ tay hỏi "em không hiểu" mà không sợ bị chê cười. Nếu ai cũng sợ sai, không ai dám thử cái mới. **Tuckman's stages**: Forming (lớp mới, ai cũng lịch sự) → Storming (bắt đầu va chạm) → Norming (tìm ra cách làm việc chung) → Performing (phối hợp ăn ý). Đừng hoảng khi đội xung đột — đó là bước tự nhiên. **Burnout** giống chạy marathon không nghỉ: ai cũng có giới hạn. Quản lý tốt biết khi nào đội cần nghỉ, giống huấn luyện viên biết khi nào cầu thủ cần thay người.

---

## 1. Psychological Safety

```
(Google's Project Aristotle: #1 factor for high-performing teams)

Definition: Team members feel safe to take risks, 
speak up, disagree, and make mistakes without fear.

Signs of Psychological Safety:
  ✅ People ask "dumb" questions freely
  ✅ Mistakes are discussed openly (learning, not blame)
  ✅ Junior members voice opinions
  ✅ Bad news is shared early
  ✅ People say "I don't know"

Signs of LOW Psychological Safety:
  ❌ Silence in meetings (people think but don't speak)
  ❌ Same 2-3 people always talk
  ❌ Issues discovered late (people afraid to raise concerns)
  ❌ "Cover your ass" culture
  ❌ Blame after incidents

Building Psychological Safety:
┌─────────────────────────────────────────────────────────┐
│ 1. MODEL VULNERABILITY                                   │
│    "I made a mistake on the deployment. Here's what I    │
│     learned..." → Leaders go first                       │
│                                                          │
│ 2. RESPOND TO MISTAKES WITH CURIOSITY                    │
│    "Interesting! What can we learn from this?"           │
│    NEVER: "Who did this?" or "How could you?"            │
│                                                          │
│ 3. INVITE INPUT                                          │
│    "I want to hear from everyone. @quiet_person,         │
│     what's your perspective?"                            │
│                                                          │
│ 4. THANK DISAGREEMENT                                    │
│    "Thanks for pushing back on this. Let me reconsider." │
│                                                          │
│ 5. BLAMELESS POSTMORTEMS                                 │
│    Focus: What happened? Why? How to prevent?            │
│    NOT: Whose fault is it?                               │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Team Dynamics — Tuckman's Model

```
FORMING (New team, new members)
  Behavior: Polite, cautious, testing boundaries
  Need: Clear goals, roles, expectations
  Leader role: Directive — set structure, make introductions
  Duration: 2-4 weeks

STORMING (Conflicts emerge)
  Behavior: Disagreements, power struggles, frustration
  Need: Conflict resolution, clear decision-making process
  Leader role: Coach — facilitate disagreements, normalize conflict
  Duration: 2-8 weeks
  Key: THIS IS NORMAL. Don't avoid it — work through it.

NORMING (Finding rhythm)
  Behavior: Trust builds, processes established, collaboration
  Need: Reinforce good patterns, refine processes
  Leader role: Facilitator — empower, delegate more
  Duration: Ongoing

PERFORMING (High performance)
  Behavior: Self-organizing, high trust, high output
  Need: Challenge, growth opportunities, autonomy
  Leader role: Servant leader — remove obstacles, stay out of the way
  Duration: Until team change

ADJOURNING (Team changes, project ends)
  Behavior: Reflection, celebration or mourning
  Need: Recognition, knowledge transfer, closure
  Leader role: Celebrate wins, capture learnings

Note: Any team change (new member, lost member, new project) 
resets to Forming. This is normal — move through stages faster each time.
```

---

## 3. Remote & Hybrid Leadership

```
Challenges:
  - Isolation: no hallway conversations
  - Communication gaps: async misunderstandings
  - Visibility: out of sight, out of mind
  - Timezone differences: can't meet synchronously

Solutions:
┌─────────────────────────────────────────────────────────┐
│ COMMUNICATION                                            │
│ • Default to writing (decisions, context in docs)        │
│ • Over-communicate: repeat important messages 3x         │
│ • Video ON for 1:1s (build relationship)                 │
│ • Async-first: don't require synchronous for everything  │
│                                                          │
│ CONNECTION                                               │
│ • Virtual coffee chats (random pairings, non-work)       │
│ • Team social time (games, show & tell, lunch chat)      │
│ • In-person offsites (quarterly if possible)             │
│ • Celebrate wins publicly (Slack shoutouts)              │
│                                                          │
│ STRUCTURE                                                │
│ • Core hours overlap (e.g., 10am-2pm UTC)                │
│ • Recorded meetings (for different timezones)            │
│ • Written standups (async, not synchronous meetings)     │
│ • Decision log (written, accessible to all)              │
│                                                          │
│ TRUST                                                    │
│ • Judge output, not hours online                         │
│ • No surveillance tools (destroys trust)                 │
│ • Trust by default, verify through results               │
│ • Explicit expectations: response time, availability     │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Preventing Burnout

```
Burnout Signs:
  Physical: Exhaustion, sleep problems, frequent illness
  Emotional: Cynicism, detachment, irritability
  Mental: Reduced creativity, difficulty concentrating
  Professional: Lower quality work, missed deadlines

Causes in Engineering:
  - Unrealistic deadlines → constant pressure
  - On-call without support → sleep disruption
  - No autonomy → micromanagement
  - Unclear priorities → everything is urgent
  - No growth → boredom (bore-out is real)
  - Toxic culture → emotional drain

Prevention (Manager Level):
  1. SUSTAINABLE PACE
     No hero culture: "Working weekends isn't impressive, 
     it means we planned badly"
     Track overtime: if consistent → fix workload
  
  2. CLEAR PRIORITIES
     "These 3 things matter this sprint. Everything else can wait."
     Saying NO to protect the team is your job.
  
  3. ON-CALL HEALTH
     Fair rotation, secondary backup
     Comp time after heavy on-call
     Invest in reducing alerts (fix noisy alerts)
  
  4. GROWTH OPPORTUNITIES
     Boring work → burnout. Mix routine with challenging work.
     Conference attendance, 20% time, learning days
  
  5. CHECK IN REGULARLY
     "How's your energy level this week? (1-5)"
     Watch for: withdrawal, quality drop, cynicism
  
  6. MODEL HEALTHY BEHAVIOR
     Take your own vacation. Don't send emails at midnight.
     "I'm signing off at 6pm" → permission for team to do same.
```

---

## 5. Team Rituals & Culture

```
Effective Team Rituals:
  Daily standup (async or 15min sync): What's blocking you?
  Weekly team sync (30min): Wins, learnings, upcoming work
  Bi-weekly retro (45min): What to keep/stop/start?
  Monthly demo day: Show what we built (celebrate!)
  Quarterly planning: Align on goals and priorities

Retro Format (Start/Stop/Continue):
  START: "Let's start writing ADRs for architecture decisions"
  STOP:  "Let's stop having meetings that could be emails"
  CONTINUE: "Keep doing mob programming for complex features"
  
  Rule: Every retro produces 1-3 ACTION ITEMS with owners
  Follow up: Check previous action items at next retro

Culture is what you DO, not what you SAY:
  You say "quality matters" but ship without tests? Culture = speed over quality
  You say "work-life balance" but reward overtime? Culture = hustle
  Actions > Words. Always.
```

---

## 📝 Bài tập

1. Assess team psychological safety (anonymous survey, 5 questions)
2. Identify your team's Tuckman stage, adjust leadership style
3. Implement 2 remote-friendly rituals from the list
4. Have a 1:1 conversation about workload/burnout with each team member

---

## 📚 Tài liệu
- *The Five Dysfunctions of a Team* — Patrick Lencioni
- *Drive* — Daniel Pink (motivation: autonomy, mastery, purpose)
- *Turn the Ship Around* — L. David Marquet
- *Project Aristotle* — Google re:Work
