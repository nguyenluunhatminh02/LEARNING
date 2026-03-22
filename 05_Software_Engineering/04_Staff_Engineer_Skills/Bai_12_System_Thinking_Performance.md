# Bài 12: System Thinking & Performance Engineering

## 🎯 Mục tiêu
- Performance profiling & optimization
- Capacity planning
- Reliability engineering (SLO/SLI/SLA)
- System thinking cho Staff Engineer

---

## 1. Performance Profiling

```python
# CPU Profiling
import cProfile
import pstats

def profile_function(func):
    profiler = cProfile.Profile()
    profiler.enable()
    result = func()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 bottlenecks
    return result

# Memory Profiling
from memory_profiler import profile

@profile
def process_large_dataset():
    data = load_data()          # 500MB
    filtered = filter(data)      # 200MB  ← peak?
    result = aggregate(filtered) # 50MB
    return result

# Async Profiling — find slow I/O
import time
from functools import wraps

def trace_async(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        if elapsed > 0.1:  # Log slow calls
            logger.warning(f"Slow call: {func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper

# Performance Checklist:
# 1. Profile first, optimize second (never guess)
# 2. Find THE bottleneck (usually 1 thing causes 80% of slowness)
# 3. Measure before AND after optimization
# 4. Set performance budgets (p99 < 200ms)
```

---

## 2. Common Performance Patterns

```python
# N+1 Query Problem
# BAD: 1 query for orders + N queries for users
orders = db.query("SELECT * FROM orders LIMIT 100")
for order in orders:
    user = db.query(f"SELECT * FROM users WHERE id = %s", (order.user_id,))
# → 101 queries!

# GOOD: Eager loading
orders = db.query("""
    SELECT o.*, u.name as user_name 
    FROM orders o JOIN users u ON o.user_id = u.id
    LIMIT 100
""")
# → 1 query

# Connection Pooling
from sqlalchemy import create_engine
engine = create_engine(
    DATABASE_URL,
    pool_size=20,          # Persistent connections
    max_overflow=10,       # Extra under load
    pool_recycle=3600,     # Refresh every hour
    pool_pre_ping=True,    # Health check
)

# Caching Strategy
# Cache-Aside Pattern:
async def get_user(user_id: str):
    cached = await redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)
    user = await db.get_user(user_id)
    await redis.setex(f"user:{user_id}", 300, json.dumps(user))  # TTL 5min
    return user
```

---

## 3. Capacity Planning

```
Step 1: Define current baseline
  - Current RPS: 5,000
  - Current p99 latency: 150ms
  - Current CPU utilization: 40%
  - Current DB connections: 60/100

Step 2: Project growth
  - Expected growth: 3x in 12 months
  - Peak: 5x normal (Black Friday, campaigns)
  - Target: 15,000 RPS normal, 75,000 peak

Step 3: Load test to find limits
  - At what RPS does latency degrade?
  - At what point does error rate spike?
  - Which component fails first? (DB? App? Cache?)

Step 4: Plan scaling
  ┌─────────────────────────────────────────────────────┐
  │ Component    │ Current │ Need   │ Action            │
  ├──────────────┼─────────┼────────┼───────────────────┤
  │ App servers  │ 4       │ 12     │ Auto-scale group  │
  │ Database     │ 1 write │ 1W+3R  │ Read replicas     │
  │ Redis cache  │ 1 node  │ Cluster│ Redis Cluster 6   │
  │ DB pool      │ 100     │ 300    │ PgBouncer         │
  └──────────────┴─────────┴────────┴───────────────────┘

Step 5: Budget
  - Cost per 1000 RPS = $X/month
  - ROI: each user generates $Y → justify scaling cost
```

---

## 4. Reliability Engineering (SLO/SLI/SLA)

```
SLI (Service Level Indicator) — What you measure
  - Availability: % of successful requests
  - Latency: p99 response time
  - Throughput: requests/second at acceptable latency
  - Error rate: % of 5xx responses

SLO (Service Level Objective) — Internal target
  - Availability: 99.9% (43min downtime/month)
  - Latency p99: < 200ms
  - Error rate: < 0.1%

SLA (Service Level Agreement) — Promise to customers
  - Usually less aggressive than SLO
  - SLA: 99.5% → SLO: 99.9% → gives buffer
  - Breach → financial penalties / credits

Error Budget:
  SLO = 99.9% → Error budget = 0.1% = 43 min/month
  If budget consumed → freeze deployments, focus on reliability
  If budget remaining → deploy faster, take more risks

Error Budget Policy:
  > 50% remaining → Normal development velocity
  30-50% remaining → Extra caution, require extra review
  < 30% remaining → Only reliability improvements
  0% remaining → Feature freeze until next month
```

---

## 5. System Thinking cho Staff Engineer

```
Staff Engineer = person who sees THE WHOLE SYSTEM

Responsibilities:
1. TECHNICAL VISION — Where should architecture go in 2-3 years?
2. CROSS-TEAM IMPACT — How does team A's change affect team B?
3. FORCE MULTIPLIER — Make 10 engineers 2x productive > do 2x work yourself
4. RISK IDENTIFICATION — See problems before they become incidents

Thinking Patterns:
┌─────────────────────────────────────────────────────┐
│ First-order: "This change makes our service faster"  │
│ Second-order: "But increases load on downstream DB"  │
│ Third-order: "Which affects team B's SLO"            │
│ → Solution: Add caching layer between services       │
└─────────────────────────────────────────────────────┘

Build vs Buy Decision Matrix:
  BUILD when: Core differentiation, exact fit needed, team has expertise
  BUY when: Commodity feature, time pressure, not core business
  
Time allocation (typical Staff Engineer):
  30% — Coding / architecture work
  30% — Technical mentoring / code review
  20% — Cross-team coordination, RFCs, ADRs
  20% — Technical strategy, documentation, hiring
```

---

## 📝 Bài tập

1. Profile 1 slow endpoint: find bottleneck, optimize, measure improvement
2. Create capacity plan cho system hiện tại (project 12 months)
3. Define SLI/SLO cho 3 critical services
4. Write technical vision document cho team (2-year horizon)

---

## 📚 Tài liệu
- *The Staff Engineer's Path* — Tanya Reilly
- *Staff Engineer: Leadership beyond the management track* — Will Larson
- *Site Reliability Engineering* — Google
- *Systems Performance* — Brendan Gregg
