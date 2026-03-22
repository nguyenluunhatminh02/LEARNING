# Bài 10: Security Program Leadership

## 🎯 Mục tiêu
- Building security culture trong engineering team
- DevSecOps implementation
- Security program management (CTO perspective)
- Vendor & third-party risk management

---

## 1. Security Culture

```
Security là trách nhiệm của MỌI NGƯỜI, không chỉ security team

Building Security Culture:
┌─────────────────────────────────────────────────────────┐
│ 1. TRAINING                                              │
│    - Security onboarding cho new engineers               │
│    - Quarterly secure coding workshops                   │
│    - CTF competitions (gamification)                     │
│    - Threat modeling exercises per team                   │
│                                                          │
│ 2. PROCESS                                               │
│    - Security review as part of design docs              │
│    - Security checklist in PR template                   │
│    - Automated scanning in CI/CD (no extra effort)       │
│    - Bug bounty program (external researchers)           │
│                                                          │
│ 3. INCENTIVES                                            │
│    - Celebrate security improvements                     │
│    - "Security champion" per team (dedicated time)       │
│    - Blameless incident postmortems                      │
│    - Include security in performance evaluations         │
│                                                          │
│ 4. COMMUNICATION                                         │
│    - Monthly security newsletter (learnings, tips)       │
│    - Security office hours (ask questions)               │
│    - Share incident learnings (anonymized)               │
└─────────────────────────────────────────────────────────┘

Security Champion Program:
  - 1 engineer per team volunteers as security champion
  - 20% time dedicated to security
  - Responsibilities: threat model reviews, security test reviews,
    team security training, liaison with security team
  - Benefits: career growth, specialized knowledge, influence
```

---

## 2. DevSecOps Pipeline

```
Traditional:  Dev → QA → Security Review → Ops → Deploy
              (Security is bottleneck, found late = expensive)

DevSecOps:    Security integrated at EVERY stage

┌─────────────────────────────────────────────────────────────┐
│ PLAN     │ Threat modeling, security requirements            │
│ CODE     │ IDE security plugins, pre-commit hooks            │
│ BUILD    │ SAST (semgrep), dependency scanning               │
│ TEST     │ DAST (OWASP ZAP), security unit tests            │
│ RELEASE  │ Image scanning, SBOM, artifact signing            │
│ DEPLOY   │ IaC security (checkov), policy-as-code            │
│ OPERATE  │ WAF, monitoring, anomaly detection                │
│ MONITOR  │ SIEM, incident response, threat intelligence      │
└─────────────────────────────────────────────────────────────┘

Shift Left = Find security issues early (cheaper to fix)
  - Design phase: $1 to fix
  - Development: $10
  - Testing: $100
  - Production: $10,000+ (breach)
```

```yaml
# Automated Security in CI/CD
stages:
  pre-commit:
    - detect-secrets       # No hardcoded secrets
    - ruff/eslint          # Code quality
  
  build:
    - semgrep              # SAST (code patterns)
    - bandit               # Python-specific security
    - pip-audit            # Dependency CVEs
  
  test:
    - security unit tests  # Auth, authz, input validation
    - OWASP ZAP (DAST)    # Dynamic testing against running app
  
  release:
    - trivy                # Container image scanning
    - syft                 # SBOM generation
    - cosign               # Image signing
  
  deploy:
    - checkov              # IaC security (Terraform)
    - OPA/Gatekeeper       # K8s policy enforcement
  
  runtime:
    - falco                # Container runtime security
    - GuardDuty            # Cloud threat detection
```

---

## 3. Security Program Management

```
CTO's Security Responsibilities:
1. SET STRATEGY     — What risks are acceptable? What's the security roadmap?
2. ALLOCATE BUDGET  — Security team, tools, training, bug bounty
3. RISK MANAGEMENT  — Accept, mitigate, transfer (insurance), avoid
4. COMPLIANCE       — Ensure regulatory requirements are met
5. INCIDENT PREP    — Team and process ready for breaches
6. BOARD REPORTING  — Communicate security posture to leadership

Security Program Maturity Model:
Level 1 — Reactive:    Fix vulnerabilities when found
Level 2 — Managed:     Regular scanning, basic policies
Level 3 — Defined:     Threat modeling, security design reviews
Level 4 — Measured:    Metrics tracked, continuous improvement
Level 5 — Optimized:   Predictive, automated, security-first culture

Key Security Metrics (for CTO dashboard):
┌─────────────────────────────────────────────────────────┐
│ MTTR (Mean Time to Remediate vulnerabilities)           │
│   Critical: < 24 hours | High: < 7 days | Medium: < 30 │
│                                                          │
│ Vulnerability Density: CVEs per 1000 lines of code      │
│                                                          │
│ Patch Coverage: % of systems on latest security patches │
│                                                          │
│ Security Training Completion: % of engineers trained    │
│                                                          │
│ Mean Time to Detect (MTTD): When attack started →       │
│   when we noticed → reducing this is critical           │
│                                                          │
│ Scan Coverage: % of repos with automated security scan  │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Third-Party Risk Management

```
Every vendor/SaaS/library = potential attack vector

Vendor Assessment Checklist:
□ SOC 2 Type II report available?
□ Penetration test results shared?
□ Data encryption (at rest + in transit)?
□ Data residency (where is data stored)?
□ Incident response SLA?
□ Data deletion upon contract termination?
□ Sub-processor list (who else processes data)?
□ Insurance coverage?

Risk Tiers:
  Tier 1 (Critical): Accesses sensitive data, core infrastructure
    → Full security assessment, annual review, SLA with penalties
    → Examples: Cloud provider, payment processor, auth provider
  
  Tier 2 (Important): Accesses some data, not core
    → Questionnaire + SOC2 review, bi-annual check
    → Examples: Analytics, monitoring, CI/CD platform
  
  Tier 3 (Low): No sensitive data access
    → Basic review, check Terms of Service
    → Examples: Documentation tools, design tools

Open Source Risk:
  - Check: maintainer activity, issue response time, security history
  - Prefer: widely used, actively maintained, reputable maintainers
  - Monitor: CVE databases, GitHub security advisories
```

---

## 5. Building the Security Team

```
Security Team Structure (scales with company size):

Startup (< 50 eng): 
  No dedicated security → 1 security-focused engineer
  Focus: Automated scanning, basic security practices

Growth (50-200 eng):
  1-3 security engineers
  Focus: AppSec program, DevSecOps, incident response

Scale (200-500 eng):
  5-10 security team
  Roles: AppSec, InfraSec, Detection & Response, GRC (Governance)
  Security champions program

Enterprise (500+ eng):
  CISO reports to CTO/CEO
  Dedicated teams: AppSec, Cloud Security, SOC, Red Team, GRC
  Bug bounty program, security research

Hiring priority order:
1. Security Engineer (generalist, sets up foundations)
2. AppSec Engineer (code review, secure development)
3. Detection & Response (monitoring, incident response)
4. GRC Analyst (compliance, risk management)
```

---

## 📝 Bài tập

1. Design DevSecOps pipeline cho organization
2. Create security champion program proposal
3. Build CTO security dashboard (define metrics, set targets)
4. Conduct vendor risk assessment cho 3 critical vendors

---

## 📚 Tài liệu
- *Building a Cybersecurity Program* — NIST CSF
- *The Phoenix Project* — Gene Kim (DevOps culture, applies to DevSecOps)
- *Security Engineering* — Ross Anderson
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
