# Bài 15: Production DBA — Backup, Monitoring, Security, HA

## 🎯 Mục tiêu
- Backup & restore strategies
- Monitoring & alerting
- Security hardening
- High Availability setup

---

## 1. Backup Strategies

```bash
# Logical Backup (pg_dump)
pg_dump -h localhost -U admin -Fc mydb > backup.dump    # custom format
pg_dump -h localhost -U admin -Fp mydb > backup.sql     # plain SQL

# Restore
pg_restore -h localhost -U admin -d mydb backup.dump

# Parallel dump (faster for large DBs)
pg_dump -j 4 -Fd -f backup_dir mydb

# Physical Backup (pg_basebackup) — full cluster
pg_basebackup -h primary -U replicator -D /backup -Fp -Xs -P

# Point-in-Time Recovery (PITR)
# Restore to any point: "restore to 2024-01-15 10:30:00"
# Requires: base backup + WAL archives
```

### Backup Schedule
```
Daily:   Full logical backup (pg_dump)
Hourly:  WAL archiving (continuous)
Weekly:  Full physical backup (pg_basebackup)
Test:    Monthly restore test ← CRITICAL!

Rule: Backup chưa test restore = chưa có backup
```

---

## 2. Monitoring

```sql
-- Active queries
SELECT pid, state, query_start, NOW() - query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active' AND query NOT LIKE '%pg_stat%'
ORDER BY duration DESC;

-- Long-running queries (>5 min)
SELECT pid, query, NOW() - query_start AS duration
FROM pg_stat_activity
WHERE state = 'active' AND NOW() - query_start > INTERVAL '5 min';

-- Kill long query
SELECT pg_cancel_backend(pid);    -- graceful
SELECT pg_terminate_backend(pid); -- force

-- Table sizes
SELECT 
    relname AS table,
    pg_size_pretty(pg_total_relation_size(relid)) AS total,
    pg_size_pretty(pg_relation_size(relid)) AS data,
    pg_size_pretty(pg_indexes_size(relid)) AS indexes
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC LIMIT 20;

-- Connection usage
SELECT count(*), state FROM pg_stat_activity GROUP BY state;
SHOW max_connections;  -- default 100
```

### Monitoring Stack
```
PostgreSQL → pg_stat_statements (slow queries)
           → pgBadger (log analyzer)
           → Prometheus + postgres_exporter → Grafana dashboards

Key metrics:
  - Connection count & utilization
  - Transactions per second
  - Cache hit ratio (target >99%)
  - Replication lag
  - Dead tuples / bloat
  - Disk usage growth rate
  - Lock waits
```

---

## 3. Security

```sql
-- Principle of Least Privilege
CREATE ROLE app_readonly LOGIN PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE mydb TO app_readonly;
GRANT USAGE ON SCHEMA public TO app_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_readonly;

CREATE ROLE app_readwrite LOGIN PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE mydb TO app_readwrite;
GRANT USAGE ON SCHEMA public TO app_readwrite;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_readwrite;

-- Never use superuser for application connections!

-- Row Level Security
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_orders ON orders
    USING (user_id = current_setting('app.user_id')::bigint);

-- SSL/TLS connections
-- postgresql.conf: ssl = on
-- pg_hba.conf: hostssl all all 0.0.0.0/0 scram-sha-256
```

### pg_hba.conf (Authentication)
```
# TYPE  DATABASE  USER      ADDRESS         METHOD
local   all       postgres                  peer
hostssl mydb      app_user  10.0.0.0/8     scram-sha-256
host    all       all       0.0.0.0/0      reject
```

---

## 4. High Availability

```
Patroni + etcd (production HA):
  [Patroni Node 1 (Primary)] ↔ [etcd cluster] ↔ [Patroni Node 2 (Standby)]
                                                  [Patroni Node 3 (Standby)]

  Patroni manages:
    - Leader election
    - Automatic failover
    - Replication setup
    - Configuration management

HAProxy for routing:
  Write traffic → Primary (port 5432)
  Read traffic  → Standbys (port 5433)
```

### Zero-Downtime Migration
```
1. Setup new database
2. Logical replication: old → new (continuous sync)
3. Application reads from both (shadow traffic)
4. Switch writes to new → verify → done
5. Stop replication, decommission old

Tools: pglogical, Bucardo, AWS DMS
```

---

## 📝 Bài tập

1. Setup automated backup with pg_dump + cron, test restore
2. Create Grafana dashboard for PostgreSQL monitoring
3. Configure pg_hba.conf with SSL and role-based access
4. Setup Patroni HA cluster (3 nodes, Docker Compose)

---

## 📚 Tài liệu
- *PostgreSQL 14 Administration Cookbook*
- [Patroni Documentation](https://patroni.readthedocs.io/)
- [pgMonitor](https://github.com/CrunchyData/pgmonitor)
