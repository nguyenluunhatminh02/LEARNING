# Bài 08: Security Architecture & Threat Modeling

## 🎯 Mục tiêu
- Threat modeling methodologies (STRIDE)
- Security design review process
- Attack trees & risk assessment
- Defense in depth architecture

---

## 1. Threat Modeling với STRIDE

```
STRIDE = 6 loại threat:
  S — Spoofing      : Giả mạo identity (fake login, stolen token)
  T — Tampering      : Sửa đổi data (modify request, alter DB)
  R — Repudiation    : Phủ nhận hành động (no audit trail)
  I — Info Disclosure: Lộ thông tin (data breach, verbose errors)
  D — Denial of Service: Làm sập hệ thống (DDoS, resource exhaustion)
  E — Elevation of Privilege: Leo thang quyền (user → admin)

Process:
1. DIAGRAM   — Draw system architecture (data flow diagram)
2. IDENTIFY  — For each component/flow, apply STRIDE
3. RATE      — Assess risk (likelihood × impact)
4. MITIGATE  — Design countermeasures
5. VALIDATE  — Verify mitigations work
```

---

## 2. Threat Modeling Example: E-Commerce

```
Data Flow Diagram:
  [Browser] → HTTPS → [API Gateway] → [Order Service] → [DB]
                            ↓
                    [Payment Service] → [Stripe API]
                            ↓
                    [Notification Service] → [Email/SMS]

STRIDE Analysis for Order Flow:
┌─────────────────┬─────────────────────┬──────────────────────────┐
│ Threat          │ Attack              │ Mitigation               │
├─────────────────┼─────────────────────┼──────────────────────────┤
│ Spoofing        │ Stolen JWT token    │ Short-lived tokens, MFA  │
│                 │ Fake API requests   │ mTLS between services    │
├─────────────────┼─────────────────────┼──────────────────────────┤
│ Tampering       │ Modify order amount │ Server-side price calc   │
│                 │ Replay payment      │ Idempotency keys         │
├─────────────────┼─────────────────────┼──────────────────────────┤
│ Repudiation     │ User denies order   │ Audit logs, signed txns  │
│                 │ Admin denies change │ Immutable audit trail    │
├─────────────────┼─────────────────────┼──────────────────────────┤
│ Info Disclosure │ DB breach           │ Encryption at rest       │
│                 │ PII in logs         │ Log sanitization         │
│                 │ Error stack traces  │ Generic error messages   │
├─────────────────┼─────────────────────┼──────────────────────────┤
│ DoS             │ Order spam          │ Rate limiting            │
│                 │ Large file upload   │ Size limits, validation  │
├─────────────────┼─────────────────────┼──────────────────────────┤
│ Elevation       │ User → admin        │ RBAC, server-side checks │
│                 │ IDOR: view others'  │ Ownership verification   │
│                 │ orders              │                          │
└─────────────────┴─────────────────────┴──────────────────────────┘
```

---

## 3. Risk Assessment Matrix

```
Risk = Likelihood × Impact

Likelihood (1-5):
  1 — Rare: Requires insider + advanced skills
  2 — Unlikely: Possible but difficult
  3 — Possible: Known attack vector exists
  4 — Likely: Easy to exploit, tools available
  5 — Almost certain: Script kiddie level

Impact (1-5):
  1 — Negligible: No data loss, minor inconvenience
  2 — Minor: Limited data exposure, recoverable
  3 — Moderate: Significant data loss, service degradation
  4 — Major: Large-scale breach, extended downtime
  5 — Critical: Complete compromise, regulatory violation

Risk Matrix:
           Impact →
           1    2    3    4    5
  L  1  │ Low  Low  Low  Med  Med
  i  2  │ Low  Low  Med  Med  High
  k  3  │ Low  Med  Med  High High
  e  4  │ Med  Med  High High Crit
  l  5  │ Med  High High Crit Crit
  y

Priority:
  Critical → Fix immediately (hours)
  High     → Fix this sprint
  Medium   → Fix this quarter
  Low      → Accept or fix when convenient
```

---

## 4. Security Design Review

```markdown
# Security Design Review Checklist

## Authentication & Authorization
□ How are users authenticated? (OAuth, JWT, sessions?)
□ How are services authenticated? (mTLS, API keys?)
□ Is authorization checked on every endpoint?
□ Are admin functions properly protected?

## Data Protection
□ What sensitive data is stored? (PII, credentials, financial)
□ Is data encrypted at rest and in transit?
□ How are encryption keys managed and rotated?
□ What's the data retention and deletion policy?

## Input Validation
□ Are all inputs validated (type, length, format)?
□ Is output encoding applied (XSS prevention)?
□ Are file uploads restricted and validated?

## Error Handling
□ Do errors expose internal details? (stack traces, DB queries)
□ Are errors logged with correlation IDs?
□ Are error rates monitored and alerted?

## Logging & Monitoring
□ Are security events logged? (login, access denied, admin actions)
□ Are logs tamper-proof? (immutable storage)
□ Is there alerting for suspicious patterns?

## Dependencies
□ Are dependencies scanned for vulnerabilities?
□ Are versions pinned and regularly updated?
□ Is there an SBOM?

## Infrastructure
□ Is network segmented properly?
□ Are secrets managed securely? (not in code/env)
□ Are backups encrypted and tested?
```

---

## 5. Defense in Depth

```
Layer 1: PERIMETER
  → CDN, WAF, DDoS protection, rate limiting

Layer 2: NETWORK
  → VPC segmentation, firewalls, network policies
  → mTLS, zero trust

Layer 3: APPLICATION
  → Input validation, output encoding, CSRF tokens
  → Authentication, authorization, session management

Layer 4: DATA
  → Encryption (at rest, in transit)
  → Access controls, column-level encryption
  → Backup encryption

Layer 5: MONITORING
  → Audit logs, anomaly detection
  → Incident response, alerting

Principle: If one layer fails, next layer catches it
  WAF bypassed? → App validates input
  Auth bypassed? → DB has row-level security
  DB breached? → Data is encrypted
```

---

## 📝 Bài tập

1. Threat model cho system của bạn: draw DFD + STRIDE analysis
2. Build attack tree cho "steal user credentials" scenario
3. Conduct security design review cho 1 new feature
4. Create risk register: list top 10 risks, assess, prioritize

---

## 📚 Tài liệu
- *Threat Modeling: Designing for Security* — Adam Shostack
- *Designing Secure Software* — Loren Kohnfelder
- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
