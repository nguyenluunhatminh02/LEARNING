# Bài 05: Network & Cloud Security

## 🎯 Mục tiêu
- Network security fundamentals (VPC, firewalls)
- Cloud security architecture
- Zero Trust model
- DDoS protection

---

## 1. VPC & Network Segmentation

```
AWS VPC Architecture (secure):

┌──────────────────── VPC (10.0.0.0/16) ────────────────────┐
│                                                             │
│  ┌─── Public Subnet (10.0.1.0/24) ───┐                    │
│  │  ALB (Load Balancer)               │                    │
│  │  NAT Gateway                       │                    │
│  │  Bastion Host (SSH jump box)       │                    │
│  └────────────────────────────────────┘                    │
│         │                                                   │
│  ┌─── Private Subnet (10.0.2.0/24) ──┐                    │
│  │  App Servers (ECS/EKS)             │  ← No public IP   │
│  │  Internal API services             │                    │
│  └────────────────────────────────────┘                    │
│         │                                                   │
│  ┌─── Data Subnet (10.0.3.0/24) ─────┐                    │
│  │  RDS (Database)                    │  ← Most restricted │
│  │  ElastiCache (Redis)              │                    │
│  │  Only accessible from App subnet  │                    │
│  └────────────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘

Security Groups (stateful firewall):
  ALB SG:     Inbound 443 from 0.0.0.0/0 (internet)
  App SG:     Inbound 8000 from ALB SG only
  DB SG:      Inbound 5432 from App SG only
  → Defense in depth: even if app is compromised, DB has its own firewall
```

---

## 2. WAF (Web Application Firewall)

```
AWS WAF Rules:
1. Rate limiting     — Max 2000 requests/5min per IP
2. Geo blocking      — Block countries where you have no users
3. SQL injection     — Pattern matching on query params, body
4. XSS detection     — Block suspicious script patterns
5. Bot protection    — CAPTCHA for suspicious traffic patterns
6. IP reputation     — Block known malicious IPs

Layer defense:
  Internet → CloudFront (CDN + Edge caching)
    → WAF (filter malicious traffic)
    → ALB (load balancing)
    → App (application logic)
    → DB (data storage)
```

---

## 3. Zero Trust Architecture

```
Traditional (Castle & Moat):
  "Trust everything inside the network"
  ❌ Once attacker is inside → full access

Zero Trust:
  "Never trust, always verify"
  ✅ Every request is authenticated & authorized, regardless of network

Principles:
1. Verify explicitly    — AuthN + AuthZ on every request
2. Least privilege      — Minimal access needed for the task
3. Assume breach        — Design as if attacker is already inside

Implementation:
┌─────────────────────────────────────────────────────────┐
│ • mTLS between all services (not just edge)             │
│ • Service mesh (Istio): enforce policies at network     │
│ • Identity-based access (not IP-based)                  │
│ • Short-lived credentials (rotate every hour)           │
│ • Micro-segmentation (service A can only call B, C)     │
│ • Continuous verification (not just at login)            │
│ • Encrypt all internal traffic                           │
└─────────────────────────────────────────────────────────┘

Service Mesh (Istio) example:
  - Automatic mTLS between all pods
  - Authorization policies: Service A → can call Service B (GET /api/*)
  - Traffic encryption without app code changes
```

---

## 4. DDoS Protection

```
DDoS Attack Layers:
  L3/L4: Network/Transport — SYN flood, UDP flood, amplification
  L7: Application — HTTP flood, slowloris, resource exhaustion

Protection Strategy (defense in depth):
  Layer 1: ISP/Cloud Provider (AWS Shield Standard — free, auto)
  Layer 2: CDN (CloudFront absorbs volumetric attacks)
  Layer 3: WAF (rate limiting, bot detection)
  Layer 4: Auto-scaling (absorb legitimate traffic spikes)
  Layer 5: Application (connection limits, timeouts, circuit breakers)

AWS Shield Advanced:
  - 24/7 DDoS response team
  - Cost protection (won't charge for traffic spike during attack)
  - Advanced detection & mitigation
```

---

## 5. Cloud Security Best Practices

```
IAM (Identity & Access Management):
  ✅ Least privilege: only permissions needed for specific task
  ✅ Use roles, not long-lived access keys
  ✅ MFA for all human access
  ✅ Separate accounts: dev, staging, prod
  ✅ Service accounts: unique per service, scoped permissions

  ❌ Root account for daily use
  ❌ Shared credentials between services
  ❌ Wildcard permissions (Action: "*", Resource: "*")

Data protection:
  ✅ Encrypt at rest (S3 SSE, EBS encryption, RDS encryption)
  ✅ Encrypt in transit (TLS everywhere)
  ✅ Backup encryption
  ✅ Key rotation (AWS KMS automatic rotation)

Logging & monitoring:
  ✅ CloudTrail: API call logging (who did what when)
  ✅ VPC Flow Logs: network traffic logging
  ✅ GuardDuty: threat detection (suspicious API calls, crypto mining)
  ✅ Config: compliance checking (is S3 public? is encryption on?)
```

---

## 📝 Bài tập

1. Design VPC architecture cho production app (draw diagram)
2. Setup AWS WAF rules cho API protection
3. Implement service-to-service mTLS
4. Audit IAM permissions: find over-privileged roles

---

## 📚 Tài liệu
- *AWS Security Best Practices* — AWS Whitepaper
- *Zero Trust Networks* — Gilman & Barth
- [NIST Zero Trust Architecture](https://www.nist.gov/publications/zero-trust-architecture)
