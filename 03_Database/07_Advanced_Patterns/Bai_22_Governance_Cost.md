# Bài 22: Data Governance, Compliance & Cloud Cost — CTO Responsibilities

## 🎯 Mục tiêu
- Data governance framework
- GDPR, PII handling, data retention
- Cloud database strategy & cost optimization
- Disaster Recovery planning
- Database team organization

---

## 1. Data Governance — Tại sao CTO phải quan tâm?

```
Data Governance = Quản trị data: ai được access gì, data lưu ở đâu,
                  giữ bao lâu, xóa khi nào, bảo mật thế nào

Nếu không có Data Governance:
  ❌ GDPR violation → fine up to 4% annual revenue (€20M+)
  ❌ Data breach → reputation damage, lawsuits
  ❌ Data sprawl → data everywhere, nobody knows what's where
  ❌ Compliance audit fail → business blocked in regulated industries
  ❌ Analyst dùng sai data → wrong business decisions

CTO responsibilities:
  → Define data classification (PII, sensitive, internal, public)
  → Ensure compliance (GDPR, CCPA, HIPAA, SOC2)
  → Data retention policies
  → Access control & audit trails
  → Incident response plan for data breaches
```

---

## 2. Data Classification

```
Level 1 — PUBLIC:
  Marketing content, blog posts, public API docs
  → Không cần encrypt, access control minimal

Level 2 — INTERNAL:
  Internal reports, employee directories, internal tools data
  → Basic access control, don't expose externally

Level 3 — CONFIDENTIAL:
  Business financials, contracts, strategic plans
  → Encrypt at rest + in transit, role-based access, audit logs

Level 4 — RESTRICTED (PII / Sensitive):
  Passwords, SSN, credit cards, health records, biometric data
  → Encrypt everything, strict access, data masking, minimal retention

PII (Personally Identifiable Information):
  ┌─────────────────────────────────────────────┐
  │ Direct PII:    name, email, phone, SSN,     │
  │                address, date of birth       │
  │                                             │
  │ Indirect PII:  IP address, device ID,       │
  │                location data, cookies       │
  │                                             │
  │ Sensitive PII: health records, financial,   │
  │                race, religion, sexual       │
  │                orientation, biometric       │
  └─────────────────────────────────────────────┘
```

---

## 3. GDPR & Compliance

### GDPR Requirements cho Database
```sql
-- 1. Right to Access: user có thể request tất cả data của họ
-- → Cần biết data lưu ở đâu (data mapping)

SELECT * FROM users WHERE id = 123;
SELECT * FROM orders WHERE user_id = 123;
SELECT * FROM user_events WHERE user_id = 123;
-- Export: JSON/CSV format, deliver within 30 days

-- 2. Right to Erasure (Right to be Forgotten)
-- → Delete ALL user data across ALL systems

BEGIN;
DELETE FROM user_events WHERE user_id = 123;
DELETE FROM order_items WHERE order_id IN (SELECT id FROM orders WHERE user_id = 123);
DELETE FROM orders WHERE user_id = 123;
DELETE FROM user_addresses WHERE user_id = 123;
DELETE FROM users WHERE id = 123;
COMMIT;
-- Also: Elasticsearch, Redis cache, backups, logs, analytics...
-- → CẦN data map: user_id references ở TẤT CẢ systems

-- 3. Data Minimization: chỉ collect data CẦN THIẾT
-- ❌ "Collect everything, figure out later"
-- ✅ "Only collect what we need, with clear purpose"

-- 4. Encryption at rest
-- PostgreSQL: Transparent Data Encryption (TDE) hoặc pgcrypto
-- Cloud: RDS encryption enabled by default

-- 5. Pseudonymization
-- Thay real data bằng pseudonym, giữ mapping riêng
UPDATE users SET 
    email = 'user_' || id || '@anonymized.com',
    name = 'User ' || id,
    phone = NULL
WHERE account_closed_at IS NOT NULL 
  AND account_closed_at < NOW() - INTERVAL '2 years';
```

### Data Retention Policy
```
Data Type          | Retention    | After Retention      
-------------------|------------- |---------------------
Active user data   | While active | Anonymize after 2yr inactive
Order history      | 7 years      | Required by tax law  
Payment data       | 7 years      | PCI-DSS requirement  
Access logs        | 90 days      | Delete automatically 
Session data       | 24 hours     | Delete automatically (Redis TTL)
Analytics events   | 2 years      | Aggregate then delete
Support tickets    | 3 years      | Anonymize            
Marketing consent  | While active | Delete with account  

Implementation:
  → Automated job: mỗi ngày chạy cleanup/anonymization
  → Monitoring: alert nếu data quá retention period
  → Audit: quarterly review retention compliance
```

---

## 4. Database Security Layers

```
Layer 1 — Network:
  VPC, private subnets, security groups
  DB KHÔNG expose ra internet
  Only app servers can reach DB

Layer 2 — Authentication:
  Strong passwords / IAM authentication
  Certificate-based auth for services
  MFA for DBA access

Layer 3 — Authorization:
  Principle of Least Privilege
  Role-based access (RBAC)
  Row-Level Security (RLS)

Layer 4 — Encryption:
  At rest: AES-256 (disk encryption)
  In transit: TLS 1.3
  Application-level: encrypt PII fields

Layer 5 — Audit:
  Log ALL access to sensitive data
  Who accessed what, when, from where
  Immutable audit logs (write to separate system)

Layer 6 — Monitoring:
  Alert on unusual access patterns
  Alert on bulk data export
  Alert on privilege escalation
```

```sql
-- PostgreSQL audit logging
-- pgAudit extension
CREATE EXTENSION pgaudit;
-- postgresql.conf:
-- pgaudit.log = 'read, write, ddl'
-- pgaudit.log_catalog = off

-- Sample audit log:
-- 2024-01-15 10:30:00 UTC,admin,mydb,SELECT,users,"SELECT * FROM users WHERE id=123"
-- 2024-01-15 10:30:05 UTC,app_user,mydb,UPDATE,users,"UPDATE users SET email=..."

-- Data masking for non-production
CREATE VIEW users_masked AS
SELECT 
    id,
    CONCAT(LEFT(email, 3), '***@', SPLIT_PART(email, '@', 2)) AS email,
    CONCAT(LEFT(name, 1), '***') AS name,
    CONCAT(LEFT(phone, 3), '****', RIGHT(phone, 2)) AS phone,
    created_at
FROM users;

-- Dev/staging environments: use masked views only
GRANT SELECT ON users_masked TO dev_readonly;
-- NEVER copy production PII to dev environments!
```

---

## 5. Cloud Database Strategy

### Managed vs Self-Managed
```
Managed (RDS, Cloud SQL, Atlas):
  ✅ Automated backups, patching, monitoring
  ✅ Easy scaling, multi-AZ
  ✅ No DBA needed for basic operations
  ❌ Less control, vendor lock-in
  ❌ More expensive (2-3x self-managed)
  → Best for: most companies, especially < 50 engineers

Self-Managed (EC2/GCE + PostgreSQL):
  ✅ Full control, cheaper at scale
  ✅ Any extension, any configuration
  ❌ Need dedicated DBA(s)
  ❌ You handle: backups, HA, patching, monitoring
  → Best for: large companies with DBA team, special requirements
```

### Cost Optimization
```
Top cost drivers (cloud database):
  1. Instance size (compute) — 40-60% of cost
  2. Storage (IOPS, throughput) — 20-30%
  3. Data transfer — 10-20%
  4. Backups — 5-10%

Optimization strategies:

1. Right-size instances:
   Monitor CPU/memory → downsize if < 40% utilized
   Use burstable instances (t3/t4g) for dev/staging
   Reserved instances: 30-60% savings for 1-3 year commitment

2. Read replicas for read-heavy:
   Instead of scaling primary → add read replicas
   Route analytics to replica (save primary resources)

3. Connection pooling (PgBouncer):
   100 app connections → 20 DB connections
   → Can use smaller instance

4. Storage optimization:
   Partition old data → move to cheaper storage
   Archive to S3 (0.023$/GB vs $0.115/GB for gp3)
   Delete unused indexes (save storage + IOPS)

5. Serverless (Aurora Serverless, Neon):
   Pay per use → perfect for dev/staging, variable workloads
   Auto-scale to zero when no traffic

6. Multi-region strategy:
   Primary: main region
   Read replicas: other regions (saves data transfer)
   Don't deploy globally unless you NEED global write
```

### Cost Comparison (Monthly, rough estimates)
```
Workload: 4 vCPU, 16GB RAM, 500GB storage

AWS RDS PostgreSQL:
  On-demand: ~$550/month
  Reserved (1yr): ~$380/month
  Reserved (3yr): ~$250/month

GCP Cloud SQL:
  On-demand: ~$500/month
  Committed use: ~$350/month

Self-managed (EC2 + PostgreSQL):
  c5.xlarge: ~$125 + storage ~$50 = ~$175/month
  But: +DBA time, +monitoring tools, +backup storage

Serverless (Neon):
  Compute: $0.16/hour active
  Storage: $0.75/GB/month
  Low-traffic app: ~$20/month (scales to zero!)
```

---

## 6. Disaster Recovery (DR)

```
RPO (Recovery Point Objective): Chấp nhận mất bao nhiêu data?
  RPO = 0:       Synchronous replication (no data loss)
  RPO = 1 hour:  Hourly WAL archiving
  RPO = 24 hours: Daily backup

RTO (Recovery Time Objective): Chấp nhận downtime bao lâu?
  RTO = 0:        Hot standby, automatic failover
  RTO < 5 min:    Warm standby, quick promote
  RTO < 1 hour:   Cold standby, restore from backup
  RTO < 24 hours: Restore from offsite backup

DR Strategy Matrix:
  ┌──────────────┬─────────┬─────────┬──────────────────┐
  │ Strategy     │ RPO     │ RTO     │ Cost             │
  ├──────────────┼─────────┼─────────┼──────────────────┤
  │ Backup only  │ 24hr    │ hours   │ $                │
  │ Pilot light  │ minutes │ 30min   │ $$               │
  │ Warm standby │ seconds │ minutes │ $$$              │
  │ Hot standby  │ 0       │ seconds │ $$$$             │
  │ Multi-active │ 0       │ 0       │ $$$$$            │
  └──────────────┴─────────┴─────────┴──────────────────┘

Production recommendation:
  - Tier 1 (critical): Hot standby, RPO=0, RTO<1min
    → Patroni + synchronous replication
  - Tier 2 (important): Warm standby, RPO<5min, RTO<15min
    → Async replication + automated promote
  - Tier 3 (non-critical): Backup, RPO=24hr, RTO<4hr
    → Daily pg_dump + WAL archiving

★ DR Testing:
  "A disaster recovery plan that isn't tested isn't a plan"
  → Monthly: simulate failover (Patroni switchover)
  → Quarterly: full restore test from backup
  → Annually: full DR drill (simulate region failure)
```

---

## 7. Database Team Organization

```
Company size → DB team structure:

Startup (10-30 eng):
  No dedicated DBA
  → Senior backend engineers handle DB
  → Use managed services (RDS, Cloud SQL)
  → Playbook: backup, monitoring, common issues

Scale-up (30-100 eng):
  1 DBA / Database Reliability Engineer (DBRE)
  → Manages all databases
  → Sets standards, reviews migrations
  → Handles production incidents

Growth (100-500 eng):
  Database Platform Team (3-5 people)
  → DBRE Lead + DBREs + Platform engineers
  → Builds internal tools: migration framework, monitoring
  → Defines: schema review process, access control

Enterprise (500+ eng):
  Central DB team + Embedded DBREs
  → Central team: standards, tooling, platform
  → Embedded DBREs: in product teams, domain expertise
  → Data governance team (compliance, privacy)

CTO checkpoints:
  □ Backup tested monthly?
  □ DR plan documented and drilled?
  □ Migration review process exists?
  □ PII inventory updated?
  □ Access control reviewed quarterly?
  □ Cost reviewed monthly?
  □ Performance baseline established?
  □ On-call rotation for DB incidents?
```

---

## 8. CTO Database Checklist

```markdown
## Production Database Readiness Checklist

### Security
- [ ] Database in private network (not internet-accessible)
- [ ] TLS encryption for all connections
- [ ] Encryption at rest enabled
- [ ] Least privilege: app user has only needed permissions
- [ ] No shared credentials between services
- [ ] Audit logging enabled (pgAudit)
- [ ] PII fields identified and protected

### Reliability
- [ ] Automated backups (verified with restore test)
- [ ] Replication configured (sync for critical, async for others)
- [ ] Automated failover (Patroni/managed HA)
- [ ] DR plan documented with RPO/RTO targets
- [ ] DR tested quarterly

### Performance
- [ ] Connection pooling (PgBouncer)
- [ ] Indexes reviewed and optimized
- [ ] Slow query logging enabled
- [ ] pg_stat_statements monitoring
- [ ] Autovacuum tuned
- [ ] Buffer pool hit ratio > 99%

### Operations
- [ ] Schema migration process with review
- [ ] Monitoring dashboard (Grafana)
- [ ] Alerting on: connections, replication lag, disk, errors
- [ ] On-call runbook for common incidents
- [ ] Capacity planning (growth projections)

### Compliance
- [ ] Data classification done
- [ ] GDPR/privacy compliance verified
- [ ] Data retention policies implemented
- [ ] Right to erasure process documented
- [ ] Dev/staging environments anonymized
- [ ] Access reviews quarterly

### Cost
- [ ] Right-sized instances (not over-provisioned)
- [ ] Reserved instances for production
- [ ] Unused indexes/tables cleaned up
- [ ] Cost monitored and alerting on anomalies
```

---

## 📝 Bài tập

1. Tạo data classification cho e-commerce system (identify all PII)
2. Implement automated data retention: anonymize users inactive > 2 years
3. Design DR plan cho application: define RPO/RTO, implement
4. Calculate cloud DB cost: compare RDS vs self-managed vs serverless

---

## 📚 Tài liệu
- *GDPR for Dummies* (Wiley) — practical compliance guide
- [AWS Well-Architected: Data Protection](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/data-protection.html)
- *Database Reliability Engineering* — Laine Campbell, Charity Majors ⭐
- [OWASP Database Security](https://owasp.org/www-community/Database_Security)
- *The Manager's Path* — Camille Fournier (team organization)
