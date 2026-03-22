# 🗄️ GIÁO TRÌNH MASTER DATABASE — TỪ CƠ BẢN ĐẾN NÂNG CAO

> Lộ trình toàn diện để thành thạo Database Engineering & Administration
> Dành cho: Backend Engineer, DBA, Data Engineer, Solutions Architect
> Thời lượng ước tính: 10–14 tháng

---

## 📋 MỤC LỤC

- [Phase 0: Nền tảng Database](#phase-0-nền-tảng-database)
- [Phase 1: SQL Mastery](#phase-1-sql-mastery)
- [Phase 2: Database Internals — Storage Engine](#phase-2-database-internals--storage-engine)
- [Phase 3: Indexing & Query Optimization](#phase-3-indexing--query-optimization)
- [Phase 4: Transaction & Concurrency Control](#phase-4-transaction--concurrency-control)
- [Phase 5: NoSQL Databases](#phase-5-nosql-databases)
- [Phase 6: Database Scaling & Replication](#phase-6-database-scaling--replication)
- [Phase 7: Data Modeling nâng cao](#phase-7-data-modeling-nâng-cao)
- [Phase 8: Specialized Databases](#phase-8-specialized-databases)
- [Phase 9: Data Engineering & Analytics](#phase-9-data-engineering--analytics)
- [Phase 10: Production DBA & Best Practices](#phase-10-production-dba--best-practices)
- [Phase 11: Modern Databases & CTO Decisions](#phase-11-modern-databases--cto-decisions) 🆕
- [Phase 12: Advanced Patterns & Governance](#phase-12-advanced-patterns--governance) 🆕

---

## Phase 0: Nền tảng Database
**Thời lượng: 2–3 tuần**

### 0.1 Giới thiệu Database
- Database là gì? Tại sao cần database?
- File-based storage vs Database Management System (DBMS)
- Lịch sử: Hierarchical → Network → Relational → NoSQL → NewSQL
- Phân loại database:
  - Relational (SQL): PostgreSQL, MySQL, Oracle, SQL Server
  - Document: MongoDB, CouchDB
  - Key-Value: Redis, DynamoDB
  - Wide-Column: Cassandra, HBase
  - Graph: Neo4j, Amazon Neptune
  - Time-Series: InfluxDB, TimescaleDB
  - Vector: Pinecone, Milvus, pgvector
  - Search: Elasticsearch

### 0.2 Relational Model
- Edgar F. Codd và mô hình quan hệ (1970)
- **Khái niệm cốt lõi**:
  - Relation (Table), Tuple (Row), Attribute (Column)
  - Domain, Schema, Instance
  - Primary Key, Foreign Key, Candidate Key, Super Key
  - Referential Integrity
- **Relational Algebra**:
  - Selection (σ), Projection (π)
  - Join (⋈): Natural, Inner, Outer (Left, Right, Full)
  - Union (∪), Intersection (∩), Difference (−)
  - Cartesian Product (×)
  - Division (÷)

### 0.3 Cài đặt & Setup
- **PostgreSQL**: cài đặt, psql CLI, pgAdmin
- **MySQL**: cài đặt, mysql CLI, MySQL Workbench
- **SQLite**: lightweight, embedded database
- **Docker**: chạy database trong container
  ```
  docker run -d --name postgres -e POSTGRES_PASSWORD=secret -p 5432:5432 postgres:16
  docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=secret -p 3306:3306 mysql:8
  ```
- **Bài tập**: cài đặt PostgreSQL + MySQL, tạo database đầu tiên

### 📚 Tài liệu Phase 0
| Tài liệu | Loại |
|-----------|------|
| *Database System Concepts* — Silberschatz et al. | Sách |
| *PostgreSQL Documentation — Tutorial* | Tài liệu |
| *Stanford CS145: Data Management and Data Systems* | Bài giảng |

---

## Phase 1: SQL Mastery
**Thời lượng: 4–6 tuần**

### 1.1 DDL (Data Definition Language)
- **CREATE**: TABLE, DATABASE, SCHEMA, INDEX, VIEW
  ```sql
  CREATE TABLE users (
      id          SERIAL PRIMARY KEY,
      username    VARCHAR(50) UNIQUE NOT NULL,
      email       VARCHAR(255) UNIQUE NOT NULL,
      created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  ```
- **ALTER**: ADD/DROP/MODIFY column, ADD/DROP constraint
- **DROP** vs **TRUNCATE** vs **DELETE**
- Data types chi tiết:
  - Numeric: INTEGER, BIGINT, DECIMAL, FLOAT, DOUBLE
  - String: CHAR, VARCHAR, TEXT
  - Date/Time: DATE, TIME, TIMESTAMP, INTERVAL
  - Boolean, UUID, JSON/JSONB, ARRAY (PostgreSQL)
  - ENUM, BINARY/BLOB
- **Constraints**: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT

### 1.2 DML (Data Manipulation Language)
- **INSERT**: single row, multi-row, INSERT...SELECT, UPSERT (ON CONFLICT)
- **UPDATE**: single/multi column, conditional update, UPDATE...FROM
- **DELETE**: WHERE clause, DELETE...USING
- **MERGE** (SQL standard) / UPSERT patterns

### 1.3 Queries cơ bản → trung bình
- **SELECT**: columns, expressions, aliases
- **WHERE**: comparison, BETWEEN, IN, LIKE, IS NULL
- **ORDER BY**: ASC/DESC, NULLS FIRST/LAST
- **LIMIT/OFFSET** vs **FETCH FIRST**
- **DISTINCT**, **DISTINCT ON** (PostgreSQL)
- **Aggregate functions**: COUNT, SUM, AVG, MIN, MAX, STRING_AGG, ARRAY_AGG
- **GROUP BY** + **HAVING**
- **CASE WHEN**: conditional logic

### 1.4 JOINs chi tiết
- **INNER JOIN**: chỉ rows matching ở cả 2 bảng
- **LEFT JOIN** (LEFT OUTER JOIN): tất cả rows bên trái
- **RIGHT JOIN**: tất cả rows bên phải
- **FULL OUTER JOIN**: tất cả rows cả 2 bảng
- **CROSS JOIN**: Cartesian product
- **SELF JOIN**: bảng join với chính nó
- **LATERAL JOIN** (PostgreSQL): correlated subquery trong FROM
- **NATURAL JOIN**: tự match theo tên cột
- Join performance: Nested Loop, Hash Join, Merge Join
- **Bài tập**: 50 bài tập JOIN từ dễ đến khó

### 1.5 Subqueries
- **Scalar subquery**: trả về 1 giá trị
- **Row subquery**: trả về 1 row
- **Table subquery**: trả về nhiều rows
- **Correlated subquery**: phụ thuộc outer query
- **EXISTS** vs **IN**: khi nào dùng gì, performance
- Subquery trong SELECT, FROM, WHERE, HAVING

### 1.6 Advanced SQL
- **Window Functions** (quan trọng!):
  - ROW_NUMBER(), RANK(), DENSE_RANK(), NTILE()
  - SUM() OVER, AVG() OVER, COUNT() OVER
  - LAG(), LEAD(): truy cập row trước/sau
  - FIRST_VALUE(), LAST_VALUE(), NTH_VALUE()
  - PARTITION BY + ORDER BY + frame clause (ROWS/RANGE BETWEEN)
  ```sql
  SELECT
      department,
      employee,
      salary,
      RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank,
      salary - LAG(salary) OVER (PARTITION BY department ORDER BY salary) AS diff_from_prev
  FROM employees;
  ```

- **Common Table Expressions (CTE)**:
  - Non-recursive CTE: readable subqueries
  - Recursive CTE: hierarchical data, tree traversal
  ```sql
  WITH RECURSIVE org_tree AS (
      SELECT id, name, manager_id, 1 AS level
      FROM employees WHERE manager_id IS NULL
      UNION ALL
      SELECT e.id, e.name, e.manager_id, ot.level + 1
      FROM employees e JOIN org_tree ot ON e.manager_id = ot.id
  )
  SELECT * FROM org_tree;
  ```

- **Set Operations**: UNION, UNION ALL, INTERSECT, EXCEPT
- **GROUPING SETS, CUBE, ROLLUP**: multi-level aggregation
- **PIVOT / UNPIVOT**: crosstab queries
- **JSON operations** (PostgreSQL):
  - `->`, `->>`, `#>`, `#>>`
  - `jsonb_array_elements()`, `jsonb_each()`
  - JSON indexing: GIN index on JSONB
- **Full-Text Search** (PostgreSQL):
  - `tsvector`, `tsquery`
  - `to_tsvector()`, `plainto_tsquery()`
  - GIN/GiST indexes for full-text search

### 1.7 Stored Procedures, Functions & Triggers
- **Functions**:
  - SQL functions, PL/pgSQL functions
  - Input/output parameters
  - RETURNS TABLE
  - IMMUTABLE, STABLE, VOLATILE
- **Stored Procedures**: CALL, transaction control
- **Triggers**:
  - BEFORE/AFTER INSERT/UPDATE/DELETE
  - Row-level vs Statement-level
  - NEW vs OLD references
  - Use cases: audit logging, auto-update timestamps
- **Views**:
  - Regular views: virtual table
  - Materialized views: cached query results, REFRESH

### 1.8 Bài tập & Projects
- **LeetCode SQL**: 50 bài từ Easy → Hard
- **HackerRank SQL**: complete all challenges
- **Project 1**: thiết kế và query database cho e-commerce
- **Project 2**: analytics queries cho hệ thống quản lý trường học
- **Project 3**: reporting queries cho hệ thống tài chính

### 📚 Tài liệu Phase 1
| Tài liệu | Loại |
|-----------|------|
| *Learning SQL* — Alan Beaulieu | Sách |
| *SQL Performance Explained* — Markus Winand | Sách |
| *PostgreSQL Tutorial (postgresqltutorial.com)* | Website |
| *Mode Analytics SQL Tutorial* | Khóa học (miễn phí) |
| *LeetCode SQL 50* | Bài tập |

---

## Phase 2: Database Internals — Storage Engine
**Thời lượng: 4–6 tuần**

### 2.1 Disk & Memory Basics
- HDD vs SSD: random access, sequential access
- Pages/Blocks: đơn vị I/O nhỏ nhất (thường 4KB-16KB)
- Buffer Pool / Buffer Cache: cache pages trong RAM
- Tại sao database I/O matters: disk access chậm 1000x+ so với RAM

### 2.2 Page Layout
- **Slotted Pages**: header + slot array + tuples
- **Tuple layout**: header + null bitmap + data
- Fixed-length vs Variable-length records
- Row-oriented vs Column-oriented storage
  - Row store: OLTP workloads (PostgreSQL, MySQL)
  - Column store: OLAP workloads (ClickHouse, DuckDB, Parquet)

### 2.3 Storage Engines
- **B-Tree based** (truyền thống):
  - PostgreSQL: heap + B-Tree indexes
  - InnoDB (MySQL): clustered index (B+Tree)
  - Pages, internal nodes, leaf nodes
  - Insert, delete, split, merge operations
  - Fill factor

- **LSM-Tree based** (write-optimized):
  - Architecture: MemTable → SSTable (Level 0 → Level N)
  - Write path: append to WAL → insert MemTable → flush → compaction
  - Read path: MemTable → Bloom Filter → SSTable levels
  - Compaction strategies: Size-Tiered, Leveled
  - **Tools**: RocksDB, LevelDB, Cassandra
  - **So sánh B-Tree vs LSM-Tree**:
    - B-Tree: better read, worse write amplification
    - LSM-Tree: better write, worse read amplification, space amplification

### 2.4 Write-Ahead Log (WAL)
- Tại sao cần WAL: crash recovery
- WAL protocol: log trước, write data sau
- WAL segments, checkpoint
- Crash recovery: redo/undo từ WAL
- PostgreSQL WAL: pg_wal directory
- MySQL: redo log, undo log

### 2.5 Buffer Management
- Buffer Pool: hash table of pages
- Page replacement policies: LRU, Clock, LRU-K
- Dirty page flushing strategies
- Double write buffer (MySQL InnoDB)
- Prefetching / Read-ahead

### 2.6 Data Compression
- **Row-level compression**: dictionary encoding, prefix compression
- **Column-level compression** (columnar stores):
  - Run-Length Encoding (RLE)
  - Dictionary Encoding
  - Bit-Packing
  - Delta Encoding
- **Page-level compression**: LZ4, ZSTD, Snappy
- TOAST (PostgreSQL): The Oversized-Attribute Storage Technique

### 📚 Tài liệu Phase 2
| Tài liệu | Loại |
|-----------|------|
| *Database Internals* — Alex Petrov | Sách (MUST READ) |
| *CMU 15-445: Database Systems (YouTube)* — Andy Pavlo | Bài giảng |
| *PostgreSQL Internals (interdb.jp)* | Sách (miễn phí) |
| *InnoDB Documentation* | Tài liệu |

---

## Phase 3: Indexing & Query Optimization
**Thời lượng: 4–6 tuần**

### 3.1 B-Tree / B+Tree Index
- B-Tree structure: balanced, multi-way search tree
- B+Tree: data chỉ ở leaf nodes, leaf nodes linked
- **Clustered Index**: tuples lưu theo thứ tự index
  - InnoDB: always has clustered index (PK or hidden)
  - PostgreSQL: heap (no clustered index by default, nhưng có CLUSTER command)
- **Non-clustered Index**: index entries → pointer to heap/clustered index
- **Composite Index**: multi-column index
  - Leftmost prefix rule: INDEX(a, b, c) → usable for (a), (a,b), (a,b,c)
- **Covering Index**: index chứa tất cả columns cần → Index-Only Scan
- **Partial Index** (PostgreSQL): WHERE clause trong CREATE INDEX
  ```sql
  CREATE INDEX idx_active_users ON users (email) WHERE is_active = true;
  ```
- **Expression Index**:
  ```sql
  CREATE INDEX idx_lower_email ON users (LOWER(email));
  ```

### 3.2 Hash Index
- O(1) lookup cho equality queries
- Không hỗ trợ range queries
- PostgreSQL: CREATE INDEX ... USING HASH
- Sử dụng: chỉ khi 100% equality lookups

### 3.3 Advanced Index Types
- **GiST (Generalized Search Tree)**: spatial data, full-text search, range types
- **GIN (Generalized Inverted Index)**: full-text search, JSONB, arrays
- **BRIN (Block Range Index)**: very large tables, naturally ordered data
  ```sql
  -- Tốt cho bảng có dữ liệu được insert theo thứ tự (timestamps)
  CREATE INDEX idx_created_at_brin ON events USING BRIN (created_at);
  ```
- **R-Tree / GiST**: spatial indexing (PostGIS)
- **Bloom Index**: multi-column approximate index
- **Bitmap Index**: low cardinality columns (Oracle, not directly in PostgreSQL)

### 3.4 Query Execution
- **Query Processing Pipeline**:
  1. Parser → Parse Tree
  2. Analyzer → Query Tree
  3. Rewriter → Rewritten Query Tree
  4. Planner/Optimizer → Execution Plan
  5. Executor → Results
- **Query Planner strategies**:
  - **Scan types**: Sequential Scan, Index Scan, Index Only Scan, Bitmap Scan
  - **Join algorithms**: Nested Loop, Hash Join, Merge Join
  - **Sort**: In-memory sort, External merge sort
  - **Aggregate**: Hash Aggregate, Group Aggregate

### 3.5 EXPLAIN & Query Tuning
- **EXPLAIN** output đọc hiểu:
  ```sql
  EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
  SELECT * FROM orders WHERE user_id = 123 AND status = 'completed';
  ```
- Giải thích output: cost, rows, actual time, loops, buffers
- **Phát hiện problems**:
  - Sequential Scan trên bảng lớn → cần index
  - Nested Loop Join với bảng lớn → có thể cần Hash Join
  - Sort lớn → cần index hoặc tăng work_mem
  - High filter ratio → index không chọn lọc
- **Common query patterns & optimization**:
  - Sargable queries: WHERE col = value (tốt) vs WHERE UPPER(col) = 'VALUE' (xấu)
  - Avoid SELECT * → chỉ select columns cần
  - Pagination: cursor-based thay vì OFFSET
  - EXISTS vs IN vs JOIN: khi nào dùng gì
  - Batch operations: bulk insert, batch update

### 3.6 Statistics & Planner Configuration
- **pg_stats**: histogram, most common values, n_distinct
- **ANALYZE**: cập nhật statistics
- **Planner parameters**:
  - `random_page_cost`, `seq_page_cost`
  - `effective_cache_size`
  - `work_mem`: sort/hash operations memory
  - `join_collapse_limit`, `from_collapse_limit`
- Hint-based optimization (MySQL: USE INDEX, FORCE INDEX)
- PostgreSQL: pg_hint_plan extension

### 3.7 Bài tập thực hành
- **Bài tập 1**: tạo database ecommerce 10M+ rows, optimize queries
- **Bài tập 2**: analyze slow query log, tìm và fix slow queries
- **Bài tập 3**: so sánh performance trước/sau index
- **Tool**: pgbench (PostgreSQL benchmark tool)

### 📚 Tài liệu Phase 3
| Tài liệu | Loại |
|-----------|------|
| *SQL Performance Explained* — Markus Winand | Sách |
| *Use The Index, Luke (use-the-index-luke.com)* | Sách (miễn phí) |
| *PostgreSQL EXPLAIN Documentation* | Tài liệu |
| *Percona Blog — MySQL Performance* | Blog |

---

## Phase 4: Transaction & Concurrency Control
**Thời lượng: 4–5 tuần**

### 4.1 ACID Properties chi tiết
- **Atomicity**: all or nothing
  - Undo log (MySQL InnoDB)
  - Write-Ahead Log (PostgreSQL)
- **Consistency**: database luôn ở trạng thái hợp lệ
  - Constraints enforcement
  - Application-level consistency
- **Isolation**: transactions không ảnh hưởng lẫn nhau
  - Isolation levels (xem 4.2)
- **Durability**: committed data không mất
  - WAL + fsync
  - Replication

### 4.2 Isolation Levels
| Level | Dirty Read | Non-repeatable Read | Phantom Read |
|-------|-----------|-------------------|-------------|
| Read Uncommitted | ✅ Possible | ✅ Possible | ✅ Possible |
| Read Committed | ❌ | ✅ Possible | ✅ Possible |
| Repeatable Read | ❌ | ❌ | ✅ Possible* |
| Serializable | ❌ | ❌ | ❌ |

> (*) PostgreSQL's Repeatable Read dùng MVCC nên cũng prevent phantom reads

- **Read phenomena**:
  - Dirty Read: đọc data chưa commit
  - Non-repeatable Read: đọc 2 lần cho kết quả khác nhau (UPDATE)
  - Phantom Read: query 2 lần, số rows thay đổi (INSERT/DELETE)
  - Write Skew: 2 transactions đọc cùng data, write khác data → vi phạm constraint
  - Lost Update: 2 transactions cùng update 1 row

### 4.3 Concurrency Control Mechanisms

#### 4.3.1 Pessimistic Concurrency Control (Locking)
- **Lock types**: Shared (S) Lock, Exclusive (X) Lock
- **Lock granularity**: Row-level, Page-level, Table-level
- **Two-Phase Locking (2PL)**: growing phase + shrinking phase
- **Deadlock**:
  - Detection: wait-for graph
  - Prevention: wait-die, wound-wait
  - Resolution: kill one transaction
- **SELECT ... FOR UPDATE**: explicit row locking
- **SELECT ... FOR SHARE**: shared row locking
- **Advisory Locks** (PostgreSQL): application-level locking

#### 4.3.2 Optimistic Concurrency Control (MVCC)
- **MVCC (Multi-Version Concurrency Control)**:
  - Readers don't block writers, writers don't block readers
  - Mỗi row có multiple versions

- **PostgreSQL MVCC**:
  - `xmin`: transaction ID tạo tuple
  - `xmax`: transaction ID xóa/update tuple
  - Visibility rules based on transaction snapshot
  - VACUUM: dọn dead tuples
  - HOT updates (Heap-Only Tuples)

- **MySQL InnoDB MVCC**:
  - Undo log stores old versions
  - Read View: consistent snapshot
  - Purge thread: clean up old undo records

#### 4.3.3 Optimistic Concurrency Control (OCC)
- Read → Validate → Write
- No locks during read phase
- Validate before commit: check for conflicts
- Retry on conflict
- Tốt cho low-contention workloads

### 4.4 Distributed Transactions
- **Two-Phase Commit (2PC)**:
  - Prepare phase: all participants vote
  - Commit phase: coordinator decides
  - Problems: blocking, coordinator failure
- **Three-Phase Commit (3PC)**: adds pre-commit phase
- **Saga Pattern**:
  - Choreography: events trigger next step
  - Orchestration: central coordinator
  - Compensating transactions: undo completed steps
- **Outbox Pattern**: reliable event publishing
  ```
  BEGIN;
    INSERT INTO orders (...) VALUES (...);
    INSERT INTO outbox (event_type, payload) VALUES ('order_created', '...');
  COMMIT;
  -- Separate process reads outbox and publishes events
  ```

### 4.5 Concurrency Patterns trong ứng dụng
- **Optimistic Locking** (application level):
  ```sql
  UPDATE products SET stock = stock - 1, version = version + 1
  WHERE id = 123 AND version = 5;
  -- If 0 rows affected → conflict → retry
  ```
- **Pessimistic Locking**: SELECT FOR UPDATE
- **Idempotency**: request deduplication
- **Distributed Locks**: Redis SETNX, Redlock, ZooKeeper

### 📚 Tài liệu Phase 4
| Tài liệu | Loại |
|-----------|------|
| *Designing Data-Intensive Applications* — Ch. 7 | Sách |
| *Database Internals* — Ch. 5, 12-14 | Sách |
| *PostgreSQL MVCC Documentation* | Tài liệu |
| *CMU 15-445: Concurrency Control (YouTube)* | Bài giảng |

---

## Phase 5: NoSQL Databases
**Thời lượng: 4–6 tuần**

### 5.1 NoSQL Overview
- CAP Theorem: Consistency vs Availability vs Partition Tolerance
- BASE: Basically Available, Soft state, Eventually consistent
- Khi nào dùng NoSQL vs SQL:
  - Flexible schema → NoSQL
  - Complex queries, joins → SQL
  - Write-heavy, horizontal scaling → NoSQL
  - Strong consistency, ACID → SQL

### 5.2 Document Database — MongoDB
- **Concepts**: Database → Collection → Document (BSON)
- **CRUD**: insertOne/Many, find, updateOne/Many, deleteOne/Many
- **Query operators**: $eq, $gt, $in, $and, $or, $regex, $elemMatch
- **Aggregation Pipeline**: $match, $group, $sort, $project, $lookup, $unwind
- **Data Modeling**:
  - Embedded documents: denormalized, 1-to-few
  - References: normalized, 1-to-many, many-to-many
  - Patterns: Bucket, Computed, Subset, Extended Reference
- **Indexing**: single field, compound, multikey, text, 2dsphere, wildcard
- **Replica Set**: primary + secondaries, automatic failover
- **Sharding**: shard key selection, chunks, balancer
  - Hashed sharding: even distribution
  - Ranged sharding: range queries efficient
- **Transactions**: multi-document ACID transactions (since 4.0)
- **Bài tập**: xây dựng blog platform với MongoDB

### 5.3 Key-Value Store — Redis
- **Data structures**:
  - String: GET/SET, INCR, TTL
  - List: LPUSH/RPUSH, LPOP/RPOP, LRANGE
  - Set: SADD, SMEMBERS, SINTER, SUNION
  - Sorted Set: ZADD, ZRANGE, ZRANGEBYSCORE — leaderboard, rate limiting
  - Hash: HSET, HGET, HGETALL — object storage
  - Stream: XADD, XREAD, XREADGROUP — event streaming
  - HyperLogLog: PFADD, PFCOUNT — cardinality estimation
  - Bitmap: SETBIT, GETBIT, BITCOUNT — feature flags, daily active users
- **Persistence**: RDB (snapshotting), AOF (append-only file), hybrid
- **Pub/Sub**: PUBLISH, SUBSCRIBE
- **Lua scripting**: atomic operations
- **Redis Cluster**: hash slots (16384), resharding
- **Redis Sentinel**: high availability, auto failover
- **Use cases**: caching, session store, rate limiter, pub/sub, leaderboard, distributed lock
- **Bài tập**: implement rate limiter + leaderboard bằng Redis

### 5.4 Wide-Column Store — Apache Cassandra
- **Architecture**: distributed, decentralized, peer-to-peer (no master)
- **Data model**: Keyspace → Table → Row (Partition Key + Clustering Columns)
- **CQL (Cassandra Query Language)**: SQL-like syntax
- **Partition Key**: determines which node stores data
- **Clustering Columns**: sort order within a partition
- **Consistency levels**: ONE, QUORUM, ALL, LOCAL_QUORUM
- **Write path**: commit log → memtable → SSTable
- **Read path**: memtable + SSTables + bloom filter
- **Compaction strategies**: SizeTiered, Leveled, TimeWindow
- **Data modeling rules**:
  - Design tables based on queries (query-first approach)
  - Denormalization is normal
  - No joins, no subqueries
- **Bài tập**: thiết kế messaging system schema cho Cassandra

### 5.5 Graph Database — Neo4j
- **Property Graph Model**: Nodes, Relationships, Properties, Labels
- **Cypher Query Language**:
  ```cypher
  // Tìm bạn bè của bạn bè
  MATCH (user:Person {name: "Alice"})-[:FRIEND]->()-[:FRIEND]->(fof:Person)
  WHERE NOT (user)-[:FRIEND]->(fof) AND fof <> user
  RETURN DISTINCT fof.name;
  ```
- **Use cases**: social networks, recommendation engines, fraud detection, knowledge graphs
- **Khi nào dùng Graph DB**: relationships là trọng tâm, multi-hop queries
- **Bài tập**: xây dựng social network recommendation engine

### 📚 Tài liệu Phase 5
| Tài liệu | Loại |
|-----------|------|
| *MongoDB University (free courses)* | Khóa học |
| *Redis in Action* — Josiah Carlson | Sách |
| *Cassandra: The Definitive Guide* | Sách |
| *Graph Databases* — Robinson, Webber, Eifrem | Sách (miễn phí) |

---

## Phase 6: Database Scaling & Replication
**Thời lượng: 4–5 tuần**

### 6.1 Replication Fundamentals
- Tại sao cần replication: high availability, read scaling, disaster recovery
- **Single-Leader Replication**:
  - Leader handles writes, followers handle reads
  - Synchronous vs Asynchronous replication
  - Semi-synchronous: 1 sync follower + rest async
  - Replication lag, eventual consistency
  - Read-your-writes consistency
  - Monotonic reads

### 6.2 PostgreSQL Replication
- **Streaming Replication**: WAL-based, async/sync
  ```
  -- primary: postgresql.conf
  wal_level = replica
  max_wal_senders = 5
  
  -- replica: setup
  pg_basebackup -h primary_host -D /var/lib/postgresql/data -U replicator -Fp -Xs -P
  ```
- **Logical Replication**: table-level, selective replication
- **Patroni**: PostgreSQL HA with automatic failover
- **PgBouncer**: connection pooling
- **Citus**: distributed PostgreSQL (sharding extension)

### 6.3 MySQL Replication
- **Binary Log (binlog) replication**: statement-based, row-based, mixed
- **GTID-based replication**: Global Transaction ID
- **Group Replication**: multi-master
- **InnoDB Cluster**: MySQL Shell + MySQL Router + Group Replication
- **ProxySQL**: connection pooling, query routing

### 6.4 Sharding (Horizontal Partitioning)
- **Sharding strategies**:
  - **Hash-based**: shard_id = hash(shard_key) % num_shards
  - **Range-based**: shard by date range, ID range
  - **Directory-based**: lookup table
  - **Consistent Hashing**: minimize resharding

- **Shard Key selection** — CRITICAL DECISION:
  - High cardinality: nhiều giá trị khác nhau
  - Even distribution: tránh hotspots
  - Query patterns: shard key nên match query patterns
  - Ví dụ: user_id cho user data, tenant_id cho multi-tenant

- **Challenges**:
  - Cross-shard queries: expensive, avoid if possible
  - Cross-shard transactions: distributed transactions (2PC, Saga)
  - Resharding: adding/removing shards
  - Hotspots: celebrity problem
  - Referential integrity: cannot enforce across shards

- **Tools**:
  - Vitess: MySQL sharding (YouTube's solution)
  - Citus: PostgreSQL sharding
  - ShardingSphere: Java-based sharding middleware

### 6.5 Partitioning (Intra-database)
- **Table Partitioning** (PostgreSQL):
  - Range partitioning: by date
  - List partitioning: by category
  - Hash partitioning: even distribution
  ```sql
  CREATE TABLE events (
      id BIGSERIAL,
      event_type TEXT,
      created_at TIMESTAMP
  ) PARTITION BY RANGE (created_at);
  
  CREATE TABLE events_2025_q1 PARTITION OF events
      FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');
  CREATE TABLE events_2025_q2 PARTITION OF events
      FOR VALUES FROM ('2025-04-01') TO ('2025-07-01');
  ```
- **Partition pruning**: query chỉ scan partitions cần thiết
- **Partition maintenance**: add/drop/detach partitions

### 6.6 NewSQL Databases
- **CockroachDB**: distributed SQL, Raft consensus, serializable isolation
- **TiDB**: MySQL-compatible, distributed, HTAP (TiKV + TiFlash)
- **Spanner (Google)**: globally distributed, TrueTime
- **YugabyteDB**: PostgreSQL-compatible, distributed
- So sánh NewSQL: khi nào dùng thay vì traditional SQL + sharding

### 📚 Tài liệu Phase 6
| Tài liệu | Loại |
|-----------|------|
| *Designing Data-Intensive Applications* — Ch. 5, 6 | Sách |
| *High Performance MySQL* — Ch. on Replication | Sách |
| *Vitess Documentation* | Tài liệu |
| *CockroachDB Architecture Guide* | Tài liệu |

---

## Phase 7: Data Modeling nâng cao
**Thời lượng: 3–4 tuần**

### 7.1 Entity-Relationship (ER) Modeling
- **Entities**: strong entity, weak entity
- **Relationships**: 1:1, 1:N, M:N
- **Attributes**: simple, composite, multi-valued, derived
- ER diagram → Relational schema conversion
- **Tools**: dbdiagram.io, draw.io, ERDPlus

### 7.2 Normalization chi tiết
- **1NF**: atomic values, no repeating groups
- **2NF**: no partial dependencies (on part of composite PK)
- **3NF**: no transitive dependencies
- **BCNF (Boyce-Codd NF)**: every determinant is a candidate key
- **4NF**: no multi-valued dependencies
- **5NF**: no join dependencies
- **Bài tập**: normalize database schema từ 1NF → BCNF

### 7.3 Denormalization Patterns
- Khi nào denormalize: read-heavy, complex joins, performance
- **Patterns**:
  - Duplicating columns: avoid joins
  - Summary tables: pre-computed aggregations
  - Materialized views: auto-refresh
  - Embedding (NoSQL): nested documents
- **Trade-offs**: read performance ↑, write complexity ↑, storage ↑, consistency risk ↑

### 7.4 Schema Design Patterns
- **Single Table Inheritance**: polymorphism bằng 1 bảng + type column
- **Class Table Inheritance**: mỗi class 1 bảng
- **Concrete Table Inheritance**: mỗi concrete class 1 bảng
- **EAV (Entity-Attribute-Value)**: flexible schema (anti-pattern?)
- **JSON columns**: semi-structured data trong SQL
- **Temporal data**: valid-time, transaction-time, bi-temporal
- **Multi-tenant patterns**:
  - Shared database, shared schema: tenant_id column
  - Shared database, separate schema: schema per tenant
  - Separate database: database per tenant
- **Soft delete**: is_deleted flag vs deleted_at timestamp vs separate archive table
- **Audit logging**: trigger-based, CDC-based, event sourcing

### 7.5 Schema Migration
- **Migration tools**:
  - Flyway: versioned SQL migrations
  - Liquibase: XML/YAML/SQL changesets
  - Alembic (Python/SQLAlchemy)
  - Prisma Migrate (Node.js)
  - golang-migrate
- **Zero-downtime migrations**:
  - Expand and Contract pattern
  - Online schema changes: pt-online-schema-change (Percona), gh-ost (GitHub)
  - ADD COLUMN with default → safe
  - DROP COLUMN → dangerous, do in stages
  - Rename column → create new, copy, switch, drop old

### 📚 Tài liệu Phase 7
| Tài liệu | Loại |
|-----------|------|
| *Database Design for Mere Mortals* — Michael Hernandez | Sách |
| *SQL Antipatterns* — Bill Karwin | Sách |
| *Evolutionary Database Design* — Martin Fowler | Article |

---

## Phase 8: Specialized Databases
**Thời lượng: 3–4 tuần**

### 8.1 Time-Series Databases
- **Use cases**: metrics, IoT, financial data, monitoring
- **InfluxDB**: InfluxQL, Flux language, retention policies
- **TimescaleDB**: PostgreSQL extension, hypertables, continuous aggregates
- **ClickHouse**: column-oriented, extremely fast analytics
- **Concepts**: downsampling, retention policies, continuous queries
- **Bài tập**: build monitoring dashboard với TimescaleDB + Grafana

### 8.2 Search Engines
- **Elasticsearch**:
  - Architecture: cluster, node, index, shard, replica
  - Inverted index: term → document IDs
  - Mapping: text, keyword, integer, date, nested, geo_point
  - Query DSL: bool, match, term, range, nested query
  - Aggregations: metrics, bucket, pipeline
  - Analyzers: standard, custom (tokenizer + filters)
  - Relevance scoring: TF-IDF, BM25
  - Index lifecycle management (ILM)
- **OpenSearch**: Elasticsearch fork (AWS)
- **Meilisearch**: simple, fast, typo-tolerant
- **Bài tập**: build full-text search cho e-commerce catalog

### 8.3 Vector Databases
- **Use cases**: semantic search, RAG, recommendation, image similarity
- **Concepts**:
  - Vector embeddings: text/image → high-dimensional vector
  - Similarity metrics: cosine similarity, euclidean distance, dot product
  - ANN (Approximate Nearest Neighbor): HNSW, IVF, PQ
- **Tools**:
  - **pgvector**: PostgreSQL extension — đơn giản, tích hợp SQL
  - **Pinecone**: managed, serverless
  - **Milvus**: open-source, scalable
  - **Weaviate**: schema-based, multi-modal
  - **Chroma**: lightweight, Python-first
  - **Qdrant**: Rust-based, high performance
- **Bài tập**: build semantic search engine với pgvector

### 8.4 Geospatial Databases
- **PostGIS**: PostgreSQL extension
  - Geometry vs Geography types
  - Spatial indexes: GiST, SP-GiST
  - Functions: ST_Distance, ST_Within, ST_Intersects, ST_Buffer
  - Spatial joins
- **GeoHash**: encode lat/lng into string → prefix-based proximity
- **H3 (Uber)**: hexagonal hierarchical spatial index
- **Use cases**: location-based services, mapping, ride-sharing
- **Bài tập**: find nearest restaurants query với PostGIS

### 8.5 In-Memory Databases
- **Redis**: xem Phase 5.3
- **Memcached**: simple key-value, multi-threaded
- **VoltDB**: in-memory NewSQL
- **SAP HANA**: in-memory OLAP + OLTP
- Khi nào dùng: ultra-low latency, caching, session management

### 📚 Tài liệu Phase 8
| Tài liệu | Loại |
|-----------|------|
| *Elasticsearch: The Definitive Guide* | Sách (miễn phí) |
| *TimescaleDB Documentation* | Tài liệu |
| *pgvector Documentation* | Tài liệu |
| *PostGIS in Action* | Sách |

---

## Phase 9: Data Engineering & Analytics
**Thời lượng: 4–5 tuần**

### 9.1 OLTP vs OLAP
- **OLTP**: transactional, row-oriented, normalized, low latency
  - PostgreSQL, MySQL, Oracle
- **OLAP**: analytical, column-oriented, denormalized, complex queries
  - BigQuery, Snowflake, Redshift, ClickHouse

### 9.2 Data Warehousing
- **Star Schema**:
  - Fact tables: metrics, measures (sales_amount, quantity)
  - Dimension tables: descriptive (product, customer, time, location)
- **Snowflake Schema**: normalized dimensions
- **Data Vault**: Hub, Link, Satellite — flexible, auditable
- **Slowly Changing Dimensions (SCD)**:
  - Type 1: overwrite
  - Type 2: new row with version/date range
  - Type 3: new column for old value
- **Tools**: Snowflake, BigQuery, Redshift, Databricks

### 9.3 ETL / ELT Pipelines
- **ETL**: Extract → Transform → Load (traditional)
- **ELT**: Extract → Load → Transform (modern, cloud-native)
- **Tools**:
  - **Apache Airflow**: workflow orchestration, DAGs
  - **dbt (data build tool)**: SQL-based transformations
  - **Apache Spark**: distributed data processing
  - **Fivetran / Airbyte**: data ingestion
- **Change Data Capture (CDC)**:
  - Debezium: Kafka Connect-based CDC
  - PostgreSQL logical decoding
  - MySQL binlog-based CDC

### 9.4 Stream Processing
- **Apache Kafka**: event streaming platform
- **Apache Flink**: stateful stream processing
- **Apache Spark Streaming**: micro-batch processing
- **Kafka Streams**: lightweight stream processing library
- **Patterns**:
  - Event sourcing + stream processing
  - Kappa architecture: everything is a stream
  - Lambda architecture: batch + speed layers (legacy)

### 9.5 Data Lake & Lakehouse
- **Data Lake**: raw data storage (S3, ADLS)
  - Zones: raw → cleansed → curated
  - Formats: Parquet, ORC, Avro, Delta Lake
- **Lakehouse**: Data Lake + ACID transactions + schema enforcement
  - **Delta Lake**: Spark-based, ACID on data lakes
  - **Apache Iceberg**: table format, time travel, schema evolution
  - **Apache Hudi**: upserts on data lakes
- **Tools**: Databricks, AWS Lake Formation

### 📚 Tài liệu Phase 9
| Tài liệu | Loại |
|-----------|------|
| *Fundamentals of Data Engineering* — Joe Reis | Sách |
| *The Data Warehouse Toolkit* — Ralph Kimball | Sách |
| *dbt Documentation* | Tài liệu |
| *Apache Airflow Documentation* | Tài liệu |

---

## Phase 10: Production DBA & Best Practices
**Thời lượng: 3–4 tuần**

### 10.1 PostgreSQL Administration
- **Configuration tuning**:
  - `shared_buffers`: 25% RAM
  - `effective_cache_size`: 75% RAM
  - `work_mem`: per-operation sort/hash memory
  - `maintenance_work_mem`: VACUUM, CREATE INDEX
  - `max_connections` + PgBouncer connection pooling
  - `wal_buffers`, `checkpoint_completion_target`
- **VACUUM & Autovacuum**:
  - Dead tuple cleanup
  - Autovacuum tuning: `autovacuum_vacuum_threshold`, `autovacuum_vacuum_scale_factor`
  - VACUUM FULL vs regular VACUUM
  - Bloat monitoring: pgstattuple, pg_repack
- **Monitoring**:
  - `pg_stat_user_tables`: sequential scans, index usage
  - `pg_stat_statements`: slow query identification
  - `pg_stat_activity`: active connections, locks
  - `pg_stat_bgwriter`: checkpoint statistics
  - Tools: pgMonitor, pg_stat_monitor, Datadog, New Relic

### 10.2 MySQL Administration
- **InnoDB configuration**:
  - `innodb_buffer_pool_size`: 70-80% RAM
  - `innodb_log_file_size`: redo log size
  - `innodb_flush_log_at_trx_commit`: durability vs performance
  - `innodb_io_capacity`: I/O throughput hint
- **Slow Query Log**: long_query_time, mysqldumpslow
- **Performance Schema**: detailed internal metrics
- **Percona Toolkit**: pt-query-digest, pt-online-schema-change

### 10.3 Backup & Recovery
- **PostgreSQL**:
  - `pg_dump` / `pg_dumpall`: logical backup
  - `pg_basebackup`: physical backup
  - PITR (Point-In-Time Recovery): WAL archiving
  - pgBackRest: parallel backup, incremental, S3 support
  - Barman: backup management
- **MySQL**:
  - `mysqldump`: logical backup
  - `xtrabackup` (Percona): hot physical backup
  - Binary log-based PITR
- **Backup strategies**:
  - Full + Incremental + WAL archiving
  - Backup verification: test restore regularly!
  - RPO and RTO planning

### 10.4 Security
- **Authentication**: password, certificate, LDAP, Kerberos
- **Authorization**: GRANT/REVOKE, role-based access control
- **Row-Level Security (RLS)** (PostgreSQL):
  ```sql
  CREATE POLICY tenant_policy ON orders
      USING (tenant_id = current_setting('app.current_tenant')::int);
  ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
  ```
- **Encryption**:
  - At rest: Transparent Data Encryption (TDE)
  - In transit: SSL/TLS
  - Column-level: pgcrypto (PostgreSQL)
- **SQL Injection prevention**: parameterized queries, prepared statements
- **Audit logging**: pgAudit (PostgreSQL), audit_log plugin (MySQL)

### 10.5 High Availability Architecture
- **PostgreSQL HA**:
  ```
  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │   Primary    │───▶│  Standby 1  │───▶│  Standby 2  │
  │ (read/write) │    │ (read-only) │    │ (read-only) │
  └─────────────┘    └─────────────┘    └─────────────┘
         │
    ┌────┴────┐
    │ Patroni │ ← automatic failover
    └─────────┘
         │
    ┌────┴─────┐
    │ PgBouncer│ ← connection pooling
    └──────────┘
  ```
  - Patroni + etcd: automatic failover
  - PgBouncer: connection pooling
  - HAProxy: load balancing read replicas

- **MySQL HA**:
  - InnoDB Cluster (Group Replication + MySQL Router)
  - Percona XtraDB Cluster (Galera)
  - ProxySQL: query routing

### 10.6 Database Observability Dashboard
- **Metrics to monitor**:
  - Connections: active, idle, waiting
  - Query performance: average latency, p95, p99
  - Cache hit ratio: buffer pool, index
  - Replication lag
  - Disk I/O: read/write IOPS, throughput
  - Lock contention: deadlocks, lock waits
  - Table bloat, index bloat
- **Stack**: Prometheus + Grafana + pg_exporter / mysqld_exporter
- **Alerting**: query latency > threshold, replication lag > threshold, disk space

### 📚 Tài liệu Phase 10
| Tài liệu | Loại |
|-----------|------|
| *PostgreSQL 16 Administration Cookbook* | Sách |
| *High Performance MySQL* — Schwartz et al. | Sách |
| *PostgreSQL Documentation — Server Administration* | Tài liệu |
| *Percona Blog* | Blog |

---

## 🗺️ LỘ TRÌNH TỔNG QUAN

```
Phase 0  ─── Nền tảng Database (2-3 tuần)
   │
Phase 1  ─── SQL Mastery (4-6 tuần)
   │
Phase 2  ─── Storage Engine Internals (4-6 tuần)
   │
Phase 3  ─── Indexing & Query Optimization (4-6 tuần)
   │
Phase 4  ─── Transactions & Concurrency (4-5 tuần)
   │
Phase 5  ─── NoSQL Databases (4-6 tuần)
   │
Phase 6  ─── Scaling & Replication (4-5 tuần)
   │
Phase 7  ─── Data Modeling nâng cao (3-4 tuần)
   │
   ├── Phase 8  ─── Specialized Databases (3-4 tuần)
   │
   ├── Phase 9  ─── Data Engineering (4-5 tuần)
   │
   └── Phase 10 ─── Production DBA (3-4 tuần)
         │
         ├── Phase 11 ─── Modern DB & CTO Decisions (3-4 tuần) 🆕
         │
         └── Phase 12 ─── Advanced Patterns & Governance (4-5 tuần) 🆕
```

---

## Phase 11: Modern Databases & CTO Decisions 🆕
**Thời lượng: 3–4 tuần**

### 11.1 Database Selection & Polyglot Persistence
- **Decision Framework**: 7 câu hỏi chọn database
- **"PostgreSQL First" Strategy**: khi nào PG đủ, khi nào cần specialized DB
- **Polyglot Persistence**: dùng nhiều DB trong 1 hệ thống
- **Anti-patterns**: MongoDB for everything, premature sharding, Redis as primary
- **Case studies**: Uber, Discord, Shopify
- **CTO Decision Template**: Architecture Decision Record cho DB

### 11.2 Distributed SQL (NewSQL)
- **CAP Theorem & PACELC**: hiểu đúng trade-offs
- **Consistency models**: Linearizable → Sequential → Causal → Eventual
- **Google Spanner**: TrueTime, Paxos, global transactions
- **CockroachDB**: Raft consensus, geo-partitioning, PostgreSQL compatibility
- **TiDB**: HTAP (Hybrid Transactional/Analytical), MySQL compatibility
- **Consensus algorithms**: Paxos vs Raft — deep dive
- **Migration path**: PostgreSQL → Citus → CockroachDB

### 11.3 Elasticsearch & Search Engine
- **Inverted Index**: cách full-text search hoạt động
- **Text Analysis**: tokenizer, analyzer, filters
- **Search queries**: match, multi_match, bool query, fuzzy, autocomplete
- **Aggregations**: terms, range, nested (faceted search)
- **ELK Stack**: Elasticsearch + Logstash + Kibana
- **Sync patterns**: PostgreSQL → Elasticsearch (CDC, batch, dual write)
- **Alternatives**: Meilisearch, Typesense, OpenSearch

### 📚 Tài liệu Phase 11
| Tài liệu | Loại |
|-----------|------|
| *Designing Data-Intensive Applications* — Kleppmann (Ch.2,3,5,7) | Sách ⭐ |
| *Database Internals* — Alex Petrov (Ch.12-14) | Sách |
| CockroachDB Architecture Docs | Tài liệu |
| Elasticsearch: The Definitive Guide | Sách |

---

## Phase 12: Advanced Patterns & Governance 🆕
**Thời lượng: 4–5 tuần**

### 12.1 CDC, Event Sourcing & Streaming
- **Change Data Capture (CDC)**: Debezium + Kafka
- **Kafka as data backbone**: topics, partitions, consumer groups
- **Event Sourcing**: store events not state, replay, snapshots
- **CQRS**: separate read/write models
- **Outbox Pattern**: transactional guarantee for events
- **Practical**: PostgreSQL → Debezium → Kafka → Elasticsearch pipeline

### 12.2 Schema Migration & Evolution
- **Migration tools**: Flyway, Alembic, golang-migrate
- **Zero-downtime patterns**: Expand-Migrate-Contract
- **Dangerous operations**: cheat sheet + safe alternatives
- **Online schema change**: pg_osc, gh-ost
- **Database branching**: Neon, PlanetScale
- **Best practices**: forward-only, idempotent, small migrations

### 12.3 Vector Database & AI-Era Data
- **Embeddings**: text/image → vector, similarity metrics
- **pgvector**: PostgreSQL extension cho vector search
- **Specialized DBs**: Pinecone, Weaviate, Milvus, Qdrant
- **ANN algorithms**: HNSW, IVFFlat, Product Quantization
- **RAG pattern**: Vector DB + LLM
- **Chunking strategies**: fixed, semantic, recursive

### 12.4 Data Governance, Compliance & Cost
- **Data classification**: Public, Internal, Confidential, Restricted
- **GDPR**: Right to Access, Right to Erasure, Data Minimization
- **Data retention policies**: per data type
- **Security layers**: network, auth, authorization, encryption, audit
- **Cloud database strategy**: managed vs self-managed, cost optimization
- **Disaster Recovery**: RPO/RTO, hot/warm/cold standby
- **Database team organization**: per company size
- **CTO Production Checklist**: security, reliability, performance, compliance

### 📚 Tài liệu Phase 12
| Tài liệu | Loại |
|-----------|------|
| *Designing Data-Intensive Applications* — Kleppmann (Ch.11-12) | Sách ⭐ |
| *Database Reliability Engineering* — Laine Campbell | Sách |
| *Building Event-Driven Microservices* — Adam Bellemare | Sách |
| pgvector GitHub + Pinecone Learning Center | Tài liệu |

---

## 💡 LỜI KHUYÊN

1. **Hands-on là vua**: mỗi concept phải tự tay viết SQL, cấu hình, benchmark
2. **PostgreSQL first**: nếu chỉ học 1 database, hãy học PostgreSQL sâu
3. **EXPLAIN là bạn thân**: luôn kiểm tra execution plan trước khi deploy query
4. **Đọc documentation gốc**: PostgreSQL/MySQL docs là nguồn tốt nhất
5. **Benchmark**: dùng pgbench, sysbench để hiểu performance thực tế
6. **Production mindset**: luôn nghĩ về backup, monitoring, security từ đầu
7. **Blog kỹ thuật**: đọc blog của Percona, Citus, CockroachDB, PlanetScale
8. **Community**: PostgreSQL mailing list, MySQL forums, r/PostgreSQL, r/database
