# Bài 10: Product Thinking for Engineers

## 🎯 Mục tiêu
- Product-market fit & validation
- Metrics-driven development
- A/B testing & experimentation
- User research cho technical leadership

---

## 1. Product Thinking

```
CTO/Staff Engineer needs to understand WHY they build, not just HOW.

Product Thinking = 
  Understanding the PROBLEM before jumping to SOLUTION

Bad: "Let's build a recommendation engine using collaborative filtering!"
Good: "Users can't find relevant products. Let's validate whether 
       recommendations would increase purchase rate."

Framework:
  1. WHO is the user? (persona, segment)
  2. WHAT problem do they have? (pain point)
  3. HOW do we solve it? (solution — this is where eng starts)
  4. HOW do we KNOW it works? (metrics, validation)

Product Discovery:
  Idea → Validate desirability (do users want it?)
       → Validate feasibility (can we build it?)
       → Validate viability (does business model work?)
       → Build MVP → Measure → Iterate
```

---

## 2. Metrics-Driven Development

```
North Star Metric = THE metric that matters most
  Spotify: Time spent listening
  Airbnb: Nights booked
  Slack: Messages sent per team/week
  Your product: ___ (define this with PM/CEO)

Metric Hierarchy:
  North Star → Primary Metrics → Input Metrics

  Example (E-commerce):
  North Star: Monthly Revenue
    ← Primary: Conversion Rate, Average Order Value, Traffic
      ← Input: Page load time, Search relevance, Checkout completion

Engineering Impact on Metrics:
  p99 latency 2s → 200ms  = +12% conversion rate
  Search relevance +20%    = +8% orders
  Checkout 5 steps → 2     = -30% abandonment

Always ask: "How does this engineering work impact user metrics?"

Guardrail Metrics (don't sacrifice these for growth):
  - Error rate (quality)
  - Page load time (performance)
  - Customer support tickets (user experience)
  - Churn rate (retention)
```

---

## 3. A/B Testing & Experimentation

```python
# A/B Testing = Scientific method for product decisions
# Control (A): Existing experience
# Treatment (B): New experience
# Measure: Which performs better on target metric?

# Technical Architecture
class ExperimentService:
    def get_variant(self, experiment_name: str, user_id: str) -> str:
        """Deterministic assignment: same user always gets same variant"""
        # Hash user_id to get consistent assignment
        hash_val = int(hashlib.sha256(
            f"{experiment_name}:{user_id}".encode()
        ).hexdigest(), 16)
        
        experiment = self.get_experiment(experiment_name)
        # 50/50 split by default
        if hash_val % 100 < experiment.traffic_percentage:
            return "treatment"
        return "control"
    
    def log_event(self, experiment_name: str, user_id: str, 
                  event: str, value: float = None):
        """Track user actions for statistical analysis"""
        self.events_store.append({
            "experiment": experiment_name,
            "user_id": user_id,
            "variant": self.get_variant(experiment_name, user_id),
            "event": event,
            "value": value,
            "timestamp": time.time()
        })

# Statistical Significance
# Need enough sample size to be confident
# p-value < 0.05 = 95% confident result isn't random
# Minimum detectable effect: decide BEFORE running test
# Duration: typically 1-4 weeks (full business cycle)

# Common Pitfalls:
# ❌ Peeking at results early → inflated false positive rate
# ❌ Stopping test when result looks good → confirmation bias
# ❌ Testing too many things at once → unclear what caused effect
# ❌ Ignoring segment differences → average hides insights
```

---

## 4. Build vs Buy Decisions

```
For CTO: One of the most important decisions

BUILD when:
  ✅ Core to your product differentiation
  ✅ Existing solutions don't meet specific needs
  ✅ You have the expertise and team capacity
  ✅ Long-term ownership cost < ongoing vendor cost
  Example: Spotify building their own recommendation engine

BUY when:
  ✅ Commodity capability (auth, payments, email)
  ✅ Time-to-market is critical
  ✅ Vendor has deeper expertise
  ✅ Maintenance burden not worth owning
  Example: Using Stripe instead of building payment processing

Evaluation Framework:
┌────────────────────┬──────────────┬──────────────┐
│ Factor             │ Build        │ Buy          │
├────────────────────┼──────────────┼──────────────┤
│ Time to market     │ Months       │ Days/Weeks   │
│ Customization      │ Full control │ Limited      │
│ Ongoing cost       │ Team time    │ License fee  │
│ Maintenance        │ You own it   │ Vendor does  │
│ Risk               │ May fail     │ Vendor risk  │
│ Data ownership     │ Full         │ Depends      │
│ Integration effort │ Native       │ May be hard  │
└────────────────────┴──────────────┴──────────────┘

Total Cost of Ownership (3-year view):
  Build: Dev cost + maintenance + infrastructure + opportunity cost
  Buy: License + integration + customization + migration risk
```

---

## 5. Technical Product Roadmap

```
Engineering-Informed Roadmap:

Quarter Plan Template:
┌─────────────────────────────────────────────────────────┐
│ Q1 2024 — Engineering Roadmap                           │
│                                                          │
│ THEME: Performance & Scale                               │
│                                                          │
│ 🎯 BUSINESS GOALS:                                      │
│    - Support 10x user growth                             │
│    - Reduce churn by improving speed                     │
│                                                          │
│ 🔧 ENGINEERING INITIATIVES:                              │
│    1. Caching layer (Redis) — reduce DB load 60%        │
│       Business impact: p99 latency 2s → 200ms           │
│       Effort: 3 engineers × 6 weeks                     │
│                                                          │
│    2. Search rewrite (Elasticsearch)                     │
│       Business impact: Search relevance +40%             │
│       Effort: 2 engineers × 8 weeks                     │
│                                                          │
│    3. Auto-scaling infrastructure                        │
│       Business impact: Handle 10x traffic without manual │
│       Effort: 1 engineer × 4 weeks                      │
│                                                          │
│ 🔄 TECH DEBT (20% allocation):                          │
│    - Migrate to K8s (reduce deploy time 45min → 5min)   │
│    - Fix flaky tests (CI reliability 80% → 99%)         │
│                                                          │
│ 📊 SUCCESS METRICS:                                     │
│    - p99 latency < 200ms                                │
│    - Zero downtime during 5x traffic spike              │
│    - Deploy frequency: weekly → daily                    │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 Bài tập

1. Define North Star metric + metric hierarchy cho product
2. Design A/B test: hypothesis, metrics, sample size, duration
3. Evaluate a build vs buy decision: full cost analysis
4. Write 1-quarter engineering roadmap tied to business goals

---

## 📚 Tài liệu
- *Inspired* — Marty Cagan
- *Lean Analytics* — Alistair Croll
- *Trustworthy Online Controlled Experiments* — Kohavi et al.
