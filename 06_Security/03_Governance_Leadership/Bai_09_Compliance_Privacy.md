# Bài 09: Compliance & Data Privacy

## 🎯 Mục tiêu
- GDPR, SOC2, PCI-DSS overview
- Data classification & protection
- Privacy by Design principles
- Audit & compliance automation

---

## 1. Major Compliance Frameworks

```
GDPR (General Data Protection Regulation — EU):
  Ai cần tuân theo: Bất kỳ ai xử lý data của EU citizens
  Key requirements:
    - Consent: Explicit opt-in for data collection
    - Right to access: Users can request their data
    - Right to erasure: "Right to be forgotten"
    - Data portability: Export data in machine-readable format
    - Breach notification: Report within 72 hours
    - Data minimization: Only collect what you need
    - Privacy by design: Build privacy into system architecture
  Penalties: Up to €20M or 4% of global annual revenue

SOC 2 (Service Organization Control — US):
  Ai cần: SaaS companies, cloud service providers
  Trust principles:
    - Security: Protection against unauthorized access
    - Availability: System available as committed
    - Processing Integrity: Data processed accurately
    - Confidentiality: Confidential data protected
    - Privacy: Personal information handled properly
  Process: Annual audit by independent auditor
  Types: Type I (point in time) vs Type II (over 6-12 months)

PCI-DSS (Payment Card Industry Data Security Standard):
  Ai cần: Anyone processing/storing/transmitting credit card data
  12 Requirements:
    1-2:   Network security (firewalls, secure configurations)
    3-4:   Data protection (encrypt stored data, encrypt transmission)
    5-6:   Vulnerability management (anti-virus, secure development)
    7-9:   Access control (need-to-know, unique IDs, physical access)
    10-12: Monitoring & testing (logging, regular testing, security policies)
  Tip: Use Stripe/Braintree to avoid handling card data directly
```

---

## 2. Data Classification

```
Classification Levels:
┌───────────────┬──────────────────────┬─────────────────────────┐
│ Level         │ Examples             │ Protection              │
├───────────────┼──────────────────────┼─────────────────────────┤
│ PUBLIC        │ Marketing content,   │ None required           │
│               │ public docs          │                         │
├───────────────┼──────────────────────┼─────────────────────────┤
│ INTERNAL      │ Internal docs,       │ Access control,         │
│               │ employee directory   │ no public access        │
├───────────────┼──────────────────────┼─────────────────────────┤
│ CONFIDENTIAL  │ Source code,         │ Encryption, audit logs, │
│               │ financial data,      │ need-to-know access     │
│               │ customer info        │                         │
├───────────────┼──────────────────────┼─────────────────────────┤
│ RESTRICTED    │ Passwords, API keys, │ KMS encryption,         │
│               │ PII, credit cards,   │ column-level encrypt,   │
│               │ health records       │ strict access, masking  │
└───────────────┴──────────────────────┴─────────────────────────┘

PII (Personally Identifiable Information):
  Direct PII: Name, email, phone, SSN, passport
  Indirect PII: IP address, location, device ID (can identify with other data)
  Sensitive PII: Health records, financial data, biometrics, race/religion

Data handling per classification:
  RESTRICTED: Encrypt at rest + in transit, mask in logs, 
              audit all access, auto-delete after retention period
```

---

## 3. Privacy by Design

```python
# 7 Principles (Ann Cavoukian):
# 1. Proactive not reactive
# 2. Privacy as default setting
# 3. Privacy embedded into design
# 4. Full functionality (privacy + usability)
# 5. End-to-end security
# 6. Visibility and transparency
# 7. Respect for user privacy

# Implementation examples:

# Data minimization — only collect what you need
class UserRegistration(BaseModel):
    email: str          # Required for account
    password: str       # Required for auth
    # ❌ phone: str     # Not needed for registration
    # ❌ birthday: date # Not needed unless age-restricted

# Purpose limitation — use data only for stated purpose
class ConsentRecord(BaseModel):
    user_id: str
    purpose: str        # "marketing_emails", "analytics", "personalization"
    granted: bool
    granted_at: datetime
    ip_address: str     # Record where consent was given

# Right to erasure
async def delete_user_data(user_id: str):
    """GDPR Article 17: Right to be forgotten"""
    # Soft delete: anonymize rather than hard delete (audit trail)
    await db.execute("""
        UPDATE users SET 
            email = 'deleted_' || id || '@redacted.com',
            name = 'Deleted User',
            phone = NULL,
            address = NULL,
            deleted_at = NOW()
        WHERE id = %s
    """, (user_id,))
    # Also delete from: backups policy, caches, logs, 3rd party services
    await redis.delete(f"user:{user_id}")
    await analytics_service.delete_user(user_id)
    await email_service.unsubscribe(user_id)

# Data portability
async def export_user_data(user_id: str) -> dict:
    """GDPR Article 20: Return user's data in machine-readable format"""
    return {
        "profile": await get_user_profile(user_id),
        "orders": await get_user_orders(user_id),
        "activity": await get_user_activity(user_id),
        "exported_at": datetime.now(timezone.utc).isoformat(),
    }
```

---

## 4. Compliance Automation

```yaml
# Infrastructure compliance (AWS Config rules)
# Auto-check: are all S3 buckets encrypted? Are security groups too open?

# Policy as Code (Open Policy Agent / OPA)
# Rego policy: deny deployment if no resource limits
package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources.limits
    msg := "Container must have resource limits"
}

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.securityContext.privileged
    msg := "Privileged containers are not allowed"
}
```

```python
# Audit logging (immutable)
import structlog

audit_logger = structlog.get_logger("audit")

async def access_pii(user_id: str, accessor_id: str, purpose: str):
    """Log every access to PII for compliance"""
    audit_logger.info(
        "pii_accessed",
        user_id=user_id,
        accessor_id=accessor_id,
        purpose=purpose,
        data_fields=["email", "phone"],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    # Logs sent to tamper-proof storage (S3 with object lock, or blockchain)

# Regular compliance checks:
# - Quarterly access reviews (who has access to what?)
# - Annual penetration testing
# - Continuous vulnerability scanning
# - Data retention enforcement (auto-delete after X days)
```

---

## 5. Breach Response Plan

```
Incident Response (khi bị breach):

0-1 HOUR: CONTAIN
  □ Isolate affected systems
  □ Revoke compromised credentials
  □ Activate incident response team
  □ Begin forensic investigation

1-24 HOURS: ASSESS
  □ Determine scope (what data, how many users)
  □ Identify attack vector (how they got in)
  □ Preserve evidence (forensic imaging)
  □ Notify legal team

24-72 HOURS: NOTIFY (GDPR requirement)
  □ Notify supervisory authority (within 72 hours)
  □ Notify affected users (if high risk to rights)
  □ Prepare public statement (if needed)

POST-INCIDENT:
  □ Full incident report
  □ Root cause analysis
  □ Remediation plan
  □ Update security controls
  □ Lessons learned (blameless postmortem)
```

---

## 📝 Bài tập

1. Classify tất cả data trong system (public → restricted)
2. Implement GDPR endpoints: export data, delete data, consent management
3. Setup audit logging cho mọi access đến PII
4. Create breach response playbook cho team

---

## 📚 Tài liệu
- [GDPR Official Text](https://gdpr-info.eu/)
- *Data Privacy* — Nishant Bhajaria
- [SOC 2 Compliance Guide](https://www.vanta.com/collection/soc-2)
