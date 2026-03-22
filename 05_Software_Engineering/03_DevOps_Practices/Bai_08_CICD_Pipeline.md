# Bài 08: CI/CD Pipeline Design

## 🎯 Mục tiêu
- CI/CD stages & best practices
- Deployment strategies (Blue-Green, Canary, Rolling)
- Feature flags

---

## 1. CI/CD Pipeline Stages

```
Code Push → Build → Lint → Test → Security Scan → Build Image → Deploy Staging → E2E Test → Deploy Prod

Stage 1: BUILD     — Compile, install deps, build artifacts
Stage 2: LINT      — Code style, static analysis (ruff, eslint)
Stage 3: TEST      — Unit tests + coverage check (>80%)
Stage 4: SECURITY  — SAST (semgrep), dependency audit (safety, npm audit)
Stage 5: BUILD IMG — Docker image, push to registry
Stage 6: STAGING   — Deploy to staging environment
Stage 7: E2E       — End-to-end tests on staging
Stage 8: PROD      — Deploy to production (canary/rolling)
```

---

## 2. Deployment Strategies

```
Rolling Update:
  [v1 v1 v1] → [v2 v1 v1] → [v2 v2 v1] → [v2 v2 v2]
  Zero-downtime, gradual

Blue-Green:
  [Blue: v1] ← 100% traffic
  [Green: v2] deployed, tested
  Switch: [Green: v2] ← 100% traffic
  Rollback: switch back to Blue

Canary:
  [v1] ← 95% traffic
  [v2] ← 5% traffic (canary)
  Monitor errors, latency → gradually increase v2 %
  If bad → route 100% back to v1
```

---

## 3. Feature Flags

```python
# Decouple deployment from release
# Deploy code anytime, enable feature when ready

class FeatureFlags:
    def __init__(self, store):
        self.store = store  # Redis, LaunchDarkly, etc.
    
    def is_enabled(self, flag_name, user_id=None):
        flag = self.store.get(flag_name)
        if not flag: return False
        if flag.get("percentage"):
            return hash(user_id) % 100 < flag["percentage"]
        return flag.get("enabled", False)

# Usage
if feature_flags.is_enabled("new_checkout", user.id):
    return new_checkout_flow(cart)
else:
    return old_checkout_flow(cart)

# Benefits:
# - Ship incomplete features behind flag
# - A/B testing
# - Gradual rollout (1% → 10% → 50% → 100%)
# - Kill switch for broken features
```

---

## 4. Pipeline Configuration

```yaml
# GitHub Actions
name: CI/CD
on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - run: ruff check src/
      - run: pytest tests/ -v --cov=src --cov-fail-under=80

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip-audit -r requirements.txt
      - uses: returntocorp/semgrep-action@v1

  deploy:
    needs: [lint-and-test, security]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: docker build -t app:${{ github.sha }} .
      - run: docker push registry/app:${{ github.sha }}
      - run: kubectl set image deployment/app app=registry/app:${{ github.sha }}
```

---

## 📝 Bài tập

1. Setup full CI/CD pipeline (lint → test → security → deploy)
2. Implement canary deployment với K8s
3. Build feature flag system với Redis
4. Measure: deployment frequency, lead time, MTTR (DORA metrics)

---

## 📚 Tài liệu
- *Continuous Delivery* — Jez Humble
- *Accelerate* — Nicole Forsgren (DORA metrics)
- [GitHub Actions Docs](https://docs.github.com/en/actions)

## 🔗 Liên kết chéo
- → **AI Bài 28-29: MLOps & Model Deployment** — CI/CD cho ML pipelines
- → **SE Bài 09: Observability** — monitoring sau deployment
- → **Security Bài 05-06: SAST/DAST** — security scanning trong CI pipeline
- → **Leadership Bài 06: Engineering Metrics** — DORA metrics tracking
