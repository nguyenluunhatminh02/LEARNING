# 📚 Database Master — Roadmap

## Tổng quan
Giáo trình từ cơ bản đến CTO/Staff Engineer level về Database Engineering.  
**22 bài học** chia thành **7 phần**.

```
Foundation (Bài 01-08):  SQL + Internals + Transactions → Nền tảng vững
NoSQL (Bài 09-11):       MongoDB, Redis, Cassandra, Neo4j → Biết khi nào dùng
Production (Bài 12-15):  Scaling, Modeling, DBA → Run in production
Modern DB (Bài 16-18):   Selection Framework, NewSQL, Search → CTO decisions
Advanced (Bài 19-22):    CDC, Migration, Vector DB, Governance → Staff-level
```

---

## 📁 01_SQL_Fundamentals (Bài 01–03)
| Bài | Tiêu đề | Nội dung chính |
|-----|---------|----------------|
| 01 | Database Basics & SQL | Relational model, DDL/DML, CRUD, data types |
| 02 | SQL Intermediate | JOINs, Subqueries, GROUP BY, HAVING, UNION |
| 03 | SQL Advanced | Window Functions, CTE, Recursive Queries, EXPLAIN |

## 📁 02_Database_Internals (Bài 04–06)
| Bài | Tiêu đề | Nội dung chính |
|-----|---------|----------------|
| 04 | Storage Engine & B-Tree | Pages, B-Tree, LSM-Tree, WAL |
| 05 | Indexing Deep Dive | B-Tree Index, Hash, GIN, GiST, Composite, Covering |
| 06 | Query Optimization | EXPLAIN ANALYZE, index strategy, query rewrite |

## 📁 03_Transactions_Concurrency (Bài 07–08)
| Bài | Tiêu đề | Nội dung chính |
|-----|---------|----------------|
| 07 | ACID & Transactions | ACID, isolation levels, deadlocks |
| 08 | MVCC & Concurrency Control | MVCC, locking, optimistic/pessimistic concurrency |

## 📁 04_NoSQL (Bài 09–11)
| Bài | Tiêu đề | Nội dung chính |
|-----|---------|----------------|
| 09 | MongoDB (Document DB) | BSON, CRUD, aggregation pipeline, schema design |
| 10 | Redis (Key-Value + More) | Data structures, persistence, pub/sub, Lua scripting |
| 11 | Cassandra & Graph DB | Wide-column model, CQL, Neo4j, graph queries |

## 📁 05_Scaling_Production (Bài 12–15)
| Bài | Tiêu đề | Nội dung chính |
|-----|---------|----------------|
| 12 | Replication & Sharding | Master-Slave, Multi-Master, sharding strategies |
| 13 | Data Modeling & Schema Design | Normalization, denormalization, schema patterns |
| 14 | Data Engineering Basics | ETL, Data Warehouse, OLAP vs OLTP, dbt |
| 15 | Production DBA | Backup/restore, monitoring, security, HA |

## 📁 06_Modern_Databases (Bài 16–18) 🆕
| Bài | Tiêu đề | Nội dung chính |
|-----|---------|----------------|
| 16 | Database Selection & Polyglot Persistence | Decision framework, chọn DB đúng, anti-patterns, case studies |
| 17 | Distributed SQL (NewSQL) | CockroachDB, Spanner, TiDB, CAP/PACELC, Raft consensus |
| 18 | Elasticsearch & Search Engine | Inverted index, full-text search, aggregations, ELK stack |

## 📁 07_Advanced_Patterns (Bài 19–22) 🆕
| Bài | Tiêu đề | Nội dung chính |
|-----|---------|----------------|
| 19 | CDC, Event Sourcing & Streaming | Debezium, Kafka, CQRS, Outbox pattern |
| 20 | Schema Migration & Evolution | Zero-downtime migrations, Expand-Migrate-Contract, tools |
| 21 | Vector Database & AI Data | pgvector, Pinecone, embeddings, RAG pattern, ANN algorithms |
| 22 | Data Governance, Compliance & Cost | GDPR, PII, retention, cloud cost, DR planning, team org |

---

## 🛤️ Lộ trình học

```
Tháng 1-2: SQL Fundamentals (Bài 01-03)
  → Thành thạo SQL, viết complex queries

Tháng 3:   Database Internals (Bài 04-06)
  → Hiểu engine hoạt động, tối ưu queries

Tháng 4:   Transactions & Concurrency (Bài 07-08)
  → ACID, isolation, deadlock handling

Tháng 5:   NoSQL (Bài 09-11)
  → MongoDB, Redis, Cassandra, Neo4j

Tháng 6:   Scaling & Production (Bài 12-15)
  → Replication, sharding, DBA skills

Tháng 7:   Modern Databases (Bài 16-18) 🆕
  → Database selection mindset, NewSQL, Elasticsearch

Tháng 8:   Advanced Patterns (Bài 19-22) 🆕
  → CDC/Event Sourcing, Schema Migration, Vector DB, Governance
```

---

## 🎯 Level Map

```
Bài 01-06:  Junior → Mid-level Developer
Bài 07-11:  Mid → Senior Developer  
Bài 12-15:  Senior → Staff Engineer
Bài 16-18:  Staff → Principal Engineer
Bài 19-22:  Principal → CTO / VP Engineering
```
