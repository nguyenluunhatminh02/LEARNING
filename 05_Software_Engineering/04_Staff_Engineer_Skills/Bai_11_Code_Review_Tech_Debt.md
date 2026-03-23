# Bài 11: Code Review & Technical Debt Management

## 🎯 Mục tiêu
- Code review best practices (reviewer + author)
- Technical debt identification & management
- Refactoring strategy

## 📖 Câu chuyện đời thường
> **Code Review** giống kiểm tra bài luận cho bạn: không phải phê phán mà là giúp bạn viết tốt hơn. "Câu này có thể rõ hơn", "bạn quên kết luận" — cách góp ý xây dựng. **Technical Debt** giống nợ thẻ tín dụng: bạn code nhanh để ship kịp deadline ("vay nợ"), nhưng nếu không trả (refactor), lãi chồng chất — mỗi tính năng mới tốn gấp đôi thời gian. **Refactoring** giống dọn nhà: không thay đổi chức năng (nhà vẫn để ở) mà sắp xếp lại cho gọn gàng, dễ tìm hơn.

---

## 1. Code Review Best Practices

### Reviewer Guidelines
```
WHAT to review (by priority):
1. Correctness   — Does it do what it should? Edge cases?
2. Security      — Injection, auth bypass, data exposure?
3. Design        — Right abstraction level? Follows team patterns?
4. Performance   — N+1 queries? Unnecessary allocations?
5. Readability   — Clear naming? Would you understand in 6 months?
6. Tests         — Meaningful tests? Not just happy path?

HOW to review:
- Start with understanding the WHY (read PR description first)
- Review tests first → understand expected behavior
- Look at big picture (architecture) before details (style)
- Be specific: "Consider using a set here for O(1) lookup" 
  not "this could be better"
- Ask questions, don't command: "What happens if user_id is None?"
- Approve with suggestions: "LGTM, consider X for next PR"
```

### Author Guidelines
```
Make reviews EASY:
- Small PRs (< 400 lines) → faster review, better feedback
- Clear description: what, why, how to test
- Self-review trước khi request review
- Split refactor PRs from feature PRs
  → 1 PR refactor code + 1 PR add feature

Stacked PRs for large changes:
  PR1: Add new table migration
  PR2: Add repository layer (depends on PR1)
  PR3: Add API endpoint (depends on PR2)
  PR4: Add UI (depends on PR3)
  Each is small, reviewable, deployable
```

---

## 2. Technical Debt Identification

```
Types of Tech Debt:

DELIBERATE:
  "We know this is a shortcut, ship now, fix later"
  → Track in backlog, schedule repayment

ACCIDENTAL:
  "We didn't know better at the time"
  → Discovered during code review or incidents

BIT ROT:
  "Was good code, but requirements changed"
  → Periodic architecture review needed

OUTDATED DEPENDENCIES:
  "Security vulnerabilities in old versions"
  → Automated: Dependabot / Renovate

Signs of High Debt:
┌─────────────────────────────────────────────────────┐
│ • "Don't touch that file" — fear of changes         │
│ • Bug fixes create new bugs                         │
│ • Simple features take weeks                        │
│ • New team members take months to be productive     │
│ • No one understands how module X works             │
│ • Copy-paste patterns everywhere                    │
│ • Tests are flaky or missing                        │
│ • Deployment is manual or scary                     │
└─────────────────────────────────────────────────────┘
```

---

## 3. Tech Debt Management Framework

```python
# Tech Debt Quadrant (Martin Fowler)
#
#              Deliberate          |    Inadvertent
# ─────────────────────────────────┼───────────────────────
# Reckless   "No time for design" | "What's layering?"
#            → High risk           | → Education needed
# ─────────────────────────────────┼───────────────────────
# Prudent    "Ship now, refactor  | "Now we know how we
#             next sprint"         |  should have done it"
#            → Acceptable          | → Normal evolution

# Debt Scoring System
debt_items = [
    {"name": "Legacy auth module", "impact": 8, "effort": 5, "risk": 9,
     "priority": (8 * 9) / 5},  # = 14.4 → HIGH
    
    {"name": "Unused API v1", "impact": 3, "effort": 2, "risk": 2,
     "priority": (3 * 2) / 2},  # = 3.0 → LOW
    
    {"name": "No DB indexes on search", "impact": 7, "effort": 1, "risk": 6,
     "priority": (7 * 6) / 1},  # = 42.0 → CRITICAL
]
# Priority = (Impact × Risk) / Effort
# High score → fix first
```

### The 20% Rule
```
Sprint Allocation Strategy:
┌──────────────────────────────────────┐
│ 70% — New features (business value)  │
│ 20% — Tech debt repayment            │
│ 10% — Innovation / exploration       │
└──────────────────────────────────────┘

Techniques:
- Boy Scout Rule: Leave code better than you found it
- Refactor alongside feature work (same file → improve it)
- "Tech debt sprint" every quarter for larger items
- Track debt reduction metrics: deployment freq, MTTR
```

---

## 4. Refactoring Strategy

```python
# Safe Refactoring Process:
# 1. ENSURE tests exist (write them first if missing)
# 2. Make small, incremental changes
# 3. Run tests after each change
# 4. Never refactor AND add features in same PR

# Strangler Fig Pattern (for large rewrites)
class PaymentService:
    def __init__(self):
        self.legacy = LegacyPaymentProcessor()
        self.new = NewPaymentProcessor()
    
    def process(self, payment):
        if self._use_new_system(payment):
            return self.new.process(payment)
        return self.legacy.process(payment)
    
    def _use_new_system(self, payment):
        # Gradually route more traffic to new system
        # 10% → 50% → 90% → 100% → remove legacy
        return payment.amount < 1000  # Start with low-risk

# Branch by Abstraction
# Step 1: Create interface
# Step 2: Old implementation behind interface
# Step 3: New implementation behind interface
# Step 4: Switch from old → new
# Step 5: Remove old implementation
```

---

## 📝 Bài tập

1. Review 5 PRs using the review checklist above
2. Audit project: list top 10 tech debt items, score & prioritize
3. Practice: refactor a legacy module using Strangler Fig
4. Propose 20% rule to team, track impact over 1 quarter

---

## 📚 Tài liệu
- *Refactoring* — Martin Fowler
- *Working Effectively with Legacy Code* — Michael Feathers
- *The Staff Engineer's Path* — Tanya Reilly (Chapter on tech debt)
