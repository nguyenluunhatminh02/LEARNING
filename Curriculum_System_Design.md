# 🏗️ GIÁO TRÌNH MASTER SYSTEM DESIGN — TỪ CƠ BẢN ĐẾN NÂNG CAO

> Lộ trình toàn diện để thiết kế hệ thống phân tán quy mô lớn
> Dành cho: Software Engineer, Backend Engineer, Solutions Architect
> Thời lượng ước tính: 10–14 tháng

---

## 📋 MỤC LỤC

- [Phase 0: Nền tảng Computer Science](#phase-0-nền-tảng-computer-science)
- [Phase 1: Networking & Web Fundamentals](#phase-1-networking--web-fundamentals)
- [Phase 2: Building Blocks của System Design](#phase-2-building-blocks-của-system-design)
- [Phase 3: Database & Storage Design](#phase-3-database--storage-design)
- [Phase 4: Distributed Systems](#phase-4-distributed-systems)
- [Phase 5: Thiết kế hệ thống thực tế](#phase-5-thiết-kế-hệ-thống-thực-tế)
- [Phase 6: Microservices Architecture](#phase-6-microservices-architecture)
- [Phase 7: Reliability & Performance](#phase-7-reliability--performance)
- [Phase 8: Cloud Architecture & DevOps](#phase-8-cloud-architecture--devops)
- [Phase 9: Case Studies nâng cao](#phase-9-case-studies-nâng-cao)

---

## Phase 0: Nền tảng Computer Science
**Thời lượng: 3–4 tuần**

### 0.1 Operating Systems Basics
- Process vs Thread
- Concurrency vs Parallelism
- Context switching, scheduling
- Memory management: virtual memory, paging
- I/O models: blocking, non-blocking, async, multiplexing (epoll, kqueue)
- File systems basics

### 0.2 Data Structures cho System Design
- Hash Table: O(1) lookup — nền tảng của cache, database index
- Tree: B-Tree, B+Tree — database indexing
- Bloom Filter: kiểm tra tồn tại (probabilistic)
- Skip List: sorted data structure (Redis)
- Trie: prefix matching (autocomplete)
- Consistent Hashing: phân phối dữ liệu đều
- Merkle Tree: data integrity verification

### 0.3 Algorithms quan trọng
- Hashing algorithms: MD5, SHA-256, MurmurHash
- Sorting & Searching tối ưu
- Graph algorithms: BFS, DFS, Dijkstra (routing)
- Rate limiting algorithms: Token Bucket, Leaky Bucket, Sliding Window
- Leader Election: Bully, Ring
- Consensus algorithms overview: Paxos, Raft (giới thiệu)

### 0.4 Estimation & Back-of-the-Envelope Calculations
- Các con số quan trọng cần nhớ:
  - Latency: L1 cache (0.5ns), RAM (100ns), SSD (150μs), HDD (10ms), Network (150ms)
  - Throughput: SSD (~500MB/s), HDD (~100MB/s), 1Gbps network (~125MB/s)
  - Storage: 1 char = 1 byte (ASCII), 1 tweet ≈ 140 bytes
- Tính QPS (Queries Per Second)
- Tính storage requirements
- Tính bandwidth requirements
- **Bài tập**: estimate cho Twitter, YouTube, WhatsApp

### 📚 Tài liệu Phase 0
| Tài liệu | Loại |
|-----------|------|
| *Operating Systems: Three Easy Pieces (OSTEP)* | Sách (miễn phí) |
| *Jeff Dean's Numbers Every Programmer Should Know* | Tham khảo |
| *System Design Primer — GitHub* | Tổng hợp |

---

## Phase 1: Networking & Web Fundamentals
**Thời lượng: 3–4 tuần**

### 1.1 Mô hình OSI & TCP/IP
- 7 layers OSI: Physical → Application
- TCP vs UDP: khi nào dùng gì?
- TCP: 3-way handshake, flow control, congestion control
- UDP: streaming, gaming, DNS

### 1.2 HTTP & HTTPS
- HTTP/1.1: keep-alive, head-of-line blocking
- HTTP/2: multiplexing, server push, header compression
- HTTP/3: QUIC (UDP-based)
- HTTPS: TLS handshake, certificates
- HTTP methods: GET, POST, PUT, PATCH, DELETE
- Status codes: 2xx, 3xx, 4xx, 5xx
- Headers: Cache-Control, ETag, Content-Type, Authorization

### 1.3 API Design
- **REST API**:
  - Resource-based URLs
  - Stateless
  - Versioning: URL vs Header
  - Pagination: cursor-based vs offset-based
  - Rate limiting
  - HATEOAS
- **GraphQL**:
  - Query, Mutation, Subscription
  - Schema-first design
  - N+1 problem & DataLoader
  - So sánh REST vs GraphQL
- **gRPC**:
  - Protocol Buffers (protobuf)
  - Unary, Server streaming, Client streaming, Bidirectional streaming
  - Khi nào dùng gRPC: microservices internal communication
- **WebSocket**:
  - Full-duplex communication
  - Handshake process
  - Use cases: chat, real-time notifications, live data

### 1.4 DNS & CDN
- **DNS**: resolution process, record types (A, AAAA, CNAME, MX, NS, TXT)
- DNS caching: browser → OS → ISP → recursive resolver
- **CDN**: edge servers, PoP (Point of Presence)
  - Push CDN vs Pull CDN
  - Cache invalidation strategies
  - CDN providers: CloudFront, Cloudflare, Akamai
- **Bài tập**: thiết kế DNS resolution cho multi-region app

### 1.5 Security Fundamentals
- Authentication vs Authorization
- **Authentication methods**: Session-based, Token-based (JWT), OAuth 2.0, OpenID Connect
- **JWT**: header, payload, signature, refresh tokens
- **OAuth 2.0 flows**: Authorization Code, Client Credentials, PKCE
- **API Security**: rate limiting, API keys, CORS, CSRF protection
- Encryption: symmetric (AES) vs asymmetric (RSA)
- Hashing passwords: bcrypt, scrypt, Argon2

### 📚 Tài liệu Phase 1
| Tài liệu | Loại |
|-----------|------|
| *Computer Networking: A Top-Down Approach* — Kurose & Ross | Sách |
| *High Performance Browser Networking* — Ilya Grigorik | Sách (miễn phí) |
| *MDN Web Docs — HTTP* | Tài liệu |
| *REST API Design Rulebook* | Sách |

---

## Phase 2: Building Blocks của System Design
**Thời lượng: 4–6 tuần**

### 2.1 Load Balancing
- Tại sao cần Load Balancer?
- **Thuật toán**:
  - Round Robin, Weighted Round Robin
  - Least Connections, Weighted Least Connections
  - IP Hash
  - Consistent Hashing
- **Loại LB**:
  - Layer 4 (Transport): TCP/UDP level — nhanh hơn
  - Layer 7 (Application): HTTP level — thông minh hơn
- **Tools**: Nginx, HAProxy, AWS ALB/NLB, Envoy
- Health checks: active vs passive
- Session persistence (sticky sessions)
- Global Server Load Balancing (GSLB)
- **Bài tập**: cấu hình Nginx load balancer cho 3 backend servers

### 2.2 Caching
- **Cache ở đâu?**: Client → CDN → Load Balancer → Application → Database
- **Caching strategies**:
  - Cache-Aside (Lazy Loading)
  - Write-Through
  - Write-Behind (Write-Back)
  - Read-Through
  - Refresh-Ahead
- **Cache eviction policies**: LRU, LFU, FIFO, TTL
- **Cache problems**:
  - Cache stampede (thundering herd)
  - Cache penetration
  - Cache avalanche
  - Hot key problem
- **Tools**: Redis, Memcached
- Redis data structures: String, List, Set, Sorted Set, Hash, Stream
- Redis cluster, Redis Sentinel
- **Bài tập**: implement caching layer cho REST API bằng Redis

### 2.3 Message Queues & Event Streaming
- **Tại sao cần Message Queue?**: decoupling, async processing, buffering
- **Message Queue patterns**:
  - Point-to-Point (Queue)
  - Publish-Subscribe (Topic)
- **Apache Kafka**:
  - Architecture: Broker, Topic, Partition, Consumer Group
  - Offset management
  - Exactly-once semantics
  - Log compaction
  - Kafka Connect, Kafka Streams
- **RabbitMQ**: Exchange types (direct, fanout, topic, headers), routing
- **Amazon SQS/SNS**: managed queue service
- **So sánh**: Kafka vs RabbitMQ vs SQS
- **Bài tập**: xây dựng event-driven system với Kafka

### 2.4 Proxy & Reverse Proxy
- **Forward Proxy**: client-side, VPN, anonymity
- **Reverse Proxy**: server-side, Nginx, load balancing, SSL termination
- API Gateway: authentication, rate limiting, request routing, transformation
  - Kong, AWS API Gateway, Apigee
- Service Mesh: Istio, Linkerd — sidecar proxy pattern

### 2.5 Storage Systems
- **Block Storage**: EBS, iSCSI — cho databases, VMs
- **File Storage**: NFS, EFS — shared file systems
- **Object Storage**: S3, GCS, MinIO — unstructured data (images, videos, backups)
- **So sánh**: khi nào dùng loại nào
- **Data formats**: JSON, Avro, Parquet, Protocol Buffers
  - Row-based vs Columnar storage

### 📚 Tài liệu Phase 2
| Tài liệu | Loại |
|-----------|------|
| *Designing Data-Intensive Applications* — Martin Kleppmann | Sách (MUST READ) |
| *Redis Documentation* | Tài liệu |
| *Kafka: The Definitive Guide* | Sách |
| *ByteByteGo — System Design 101 (GitHub)* | Tổng hợp |

---

## Phase 3: Database & Storage Design
**Thời lượng: 4–6 tuần**

### 3.1 Relational Databases (SQL)
- ACID properties: Atomicity, Consistency, Isolation, Durability
- Normalization: 1NF, 2NF, 3NF, BCNF
- Denormalization: khi nào và tại sao
- Indexing: B-Tree index, Hash index, Composite index, Covering index
- Query optimization: EXPLAIN, execution plan
- **Transactions**: isolation levels (Read Uncommitted → Serializable)
- **Locking**: shared lock, exclusive lock, optimistic vs pessimistic locking
- **Tools**: PostgreSQL, MySQL

### 3.2 NoSQL Databases
- **Document Store**: MongoDB — flexible schema, embedded documents
- **Key-Value Store**: Redis, DynamoDB — O(1) lookup
- **Wide-Column Store**: Cassandra, HBase — distributed, write-heavy
- **Graph Database**: Neo4j — relationships, social networks
- **Time-Series DB**: InfluxDB, TimescaleDB — metrics, IoT
- **So sánh SQL vs NoSQL**: CAP theorem, use cases
- **Bài tập**: chọn database phù hợp cho 5 scenario khác nhau

### 3.3 Database Scaling
- **Vertical Scaling**: bigger machine — giới hạn
- **Read Replicas**: master-slave replication
  - Sync vs Async replication
  - Replication lag
- **Sharding (Horizontal Partitioning)**:
  - Hash-based sharding
  - Range-based sharding
  - Directory-based sharding
  - Consistent hashing
  - Problems: cross-shard queries, hotspots, resharding
- **Connection Pooling**: PgBouncer, HikariCP

### 3.4 Search & Analytics
- **Elasticsearch**:
  - Inverted index
  - Full-text search, fuzzy matching
  - Aggregations
  - ELK Stack (Elasticsearch + Logstash + Kibana)
- **Data Warehousing**: BigQuery, Snowflake, Redshift
  - OLTP vs OLAP
  - Star schema, Snowflake schema
  - ETL vs ELT

### 📚 Tài liệu Phase 3
| Tài liệu | Loại |
|-----------|------|
| *Designing Data-Intensive Applications* — Ch. 2-7 | Sách |
| *PostgreSQL Documentation* | Tài liệu |
| *MongoDB University (free courses)* | Khóa học |
| *Use The Index, Luke* | Sách (miễn phí) |

---

## Phase 4: Distributed Systems
**Thời lượng: 4–6 tuần**

### 4.1 Distributed Systems Fundamentals
- Tại sao cần distributed systems?
- **Challenges**: network partitions, clock skew, partial failure
- **CAP Theorem**: Consistency, Availability, Partition Tolerance — chọn 2/3
- **PACELC Theorem**: mở rộng CAP
- **Consistency models**:
  - Strong consistency
  - Eventual consistency
  - Causal consistency
  - Read-your-writes consistency

### 4.2 Consensus & Coordination
- **Two-Phase Commit (2PC)**: prepare → commit/abort
- **Three-Phase Commit (3PC)**
- **Paxos**: proposer, acceptor, learner
- **Raft**: leader election, log replication — dễ hiểu hơn Paxos
- **ZooKeeper / etcd**: distributed coordination service
  - Leader election
  - Distributed locks
  - Configuration management
  - Service discovery

### 4.3 Distributed Data Patterns
- **Replication**:
  - Single-leader (master-slave)
  - Multi-leader
  - Leaderless (Dynamo-style): quorum reads/writes (W + R > N)
- **Partitioning (Sharding)**:
  - Key range partitioning
  - Hash partitioning
  - Consistent hashing with virtual nodes
- **Distributed Transactions**:
  - Saga pattern: choreography vs orchestration
  - Outbox pattern
  - Event sourcing + CQRS

### 4.4 Clocks & Ordering
- **Physical clocks**: NTP, GPS, atomic clocks — inaccurate!
- **Logical clocks**: Lamport timestamps
- **Vector clocks**: detect concurrent events
- **Hybrid Logical Clocks (HLC)**: CockroachDB
- **Conflict resolution**: Last-Write-Wins (LWW), CRDTs
- **CRDTs (Conflict-free Replicated Data Types)**: G-Counter, PN-Counter, LWW-Register

### 4.5 Nền tảng lý thuyết
- **FLP Impossibility**: consensus impossible in async systems with even 1 failure
- **Byzantine Fault Tolerance (BFT)**
- **Gossip Protocol**: epidemic-style information dissemination
- **Phi Accrual Failure Detector**
- **Split-brain problem** và cách giải quyết

### 📚 Tài liệu Phase 4
| Tài liệu | Loại |
|-----------|------|
| *Designing Data-Intensive Applications* — Ch. 8-12 | Sách |
| *Distributed Systems* — Maarten van Steen | Sách (miễn phí) |
| *MIT 6.824: Distributed Systems (YouTube)* | Bài giảng |
| *Raft Visualization (raft.github.io)* | Interactive |

---

## Phase 5: Thiết kế hệ thống thực tế
**Thời lượng: 6–8 tuần**

### 5.1 Framework thiết kế hệ thống
1. **Clarify requirements**: functional vs non-functional
2. **Estimate scale**: users, QPS, storage, bandwidth
3. **High-level design**: components diagram
4. **Deep dive**: detailed design cho từng component
5. **Identify bottlenecks**: single points of failure, scaling issues
6. **Trade-offs**: discuss alternatives và lý do chọn

### 5.2 URL Shortener (TinyURL)
- Requirements: shorten URL, redirect, analytics
- Base62 encoding vs hash-based
- Read-heavy system: caching strategy
- Database choice: SQL vs NoSQL
- Analytics: click tracking
- **Key concepts**: hashing, caching, redirect (301 vs 302)

### 5.3 Rate Limiter
- Token Bucket algorithm
- Sliding Window Counter
- Distributed rate limiting: Redis-based
- Rate limit by: IP, user, API key
- **Key concepts**: concurrency, distributed counting

### 5.4 Chat System (WhatsApp/Messenger)
- 1:1 chat, group chat
- WebSocket for real-time delivery
- Message storage: per-user inbox
- Online/offline status
- Read receipts, typing indicators
- Push notifications
- End-to-end encryption
- **Key concepts**: WebSocket, message queue, presence service

### 5.5 Social Media Feed (Twitter/Instagram)
- **Fan-out-on-write** vs **Fan-out-on-read**
- News feed generation
- Timeline service
- Celebrity/hot user problem
- Hybrid approach
- Ranking algorithm
- **Key concepts**: fan-out, caching, ranking

### 5.6 Video Streaming (YouTube/Netflix)
- Video upload & processing pipeline
- Transcoding: multiple resolutions, formats (HLS, DASH)
- CDN for video delivery
- Adaptive bitrate streaming
- Video recommendation: collaborative filtering
- **Key concepts**: CDN, transcoding, blob storage

### 5.7 Search Engine (Google Search)
- Web crawling: BFS, politeness policy, duplicate detection
- Indexing: inverted index
- Ranking: PageRank, TF-IDF, BM25
- Query processing: tokenization, spell correction
- Typeahead / Autocomplete
- **Key concepts**: inverted index, crawling, ranking

### 5.8 E-commerce System (Amazon)
- Product catalog service
- Shopping cart
- Order management
- Payment processing
- Inventory management: distributed locks
- Search & recommendation
- **Key concepts**: consistency, distributed transactions, microservices

### 📚 Tài liệu Phase 5
| Tài liệu | Loại |
|-----------|------|
| *System Design Interview Vol. 1 & 2* — Alex Xu | Sách |
| *ByteByteGo — YouTube Channel* | Video |
| *Grokking the System Design Interview* | Khóa học |
| *donnemartin/system-design-primer (GitHub)* | Tổng hợp |

---

## Phase 6: Microservices Architecture
**Thời lượng: 4–5 tuần**

### 6.1 Monolith vs Microservices
- Monolithic architecture: ưu và nhược
- When to use microservices (và khi nào KHÔNG nên)
- Strangler Fig pattern: migrate monolith → microservices
- Domain-Driven Design (DDD): bounded context, aggregate, entity, value object

### 6.2 Communication Patterns
- **Synchronous**: REST, gRPC
  - Service discovery: Consul, Eureka, DNS-based
  - Client-side vs Server-side load balancing
- **Asynchronous**: Message Queue, Event Bus
  - Event-driven architecture
  - Choreography vs Orchestration
  - Saga pattern cho distributed transactions
- **API Gateway**: routing, authentication, rate limiting, circuit breaking

### 6.3 Data Management
- Database per service pattern
- Shared database anti-pattern
- **Event Sourcing**: store events thay vì state
- **CQRS (Command Query Responsibility Segregation)**:
  - Separate read/write models
  - Event store + read-optimized projections
- **Outbox Pattern**: reliable event publishing
- **Change Data Capture (CDC)**: Debezium

### 6.4 Resilience Patterns
- **Circuit Breaker**: closed → open → half-open
- **Retry** with exponential backoff + jitter
- **Timeout**: request timeout, connection timeout
- **Bulkhead**: isolate failures
- **Fallback**: graceful degradation
- **Tools**: Resilience4j, Hystrix (deprecated), Polly (.NET)

### 6.5 Service Mesh & Observability
- **Service Mesh**: Istio, Linkerd
  - Sidecar proxy (Envoy)
  - mTLS, traffic management, observability
- **Distributed Tracing**: Jaeger, Zipkin, OpenTelemetry
- **Logging**: structured logging, log aggregation (ELK, Loki)
- **Metrics**: Prometheus + Grafana
  - RED metrics: Rate, Errors, Duration
  - USE metrics: Utilization, Saturation, Errors
- **Alerting**: PagerDuty, OpsGenie

### 📚 Tài liệu Phase 6
| Tài liệu | Loại |
|-----------|------|
| *Building Microservices* — Sam Newman | Sách |
| *Microservices Patterns* — Chris Richardson | Sách |
| *Domain-Driven Design* — Eric Evans | Sách |
| *microservices.io* — Chris Richardson | Website |

---

## Phase 7: Reliability & Performance
**Thời lượng: 3–4 tuần**

### 7.1 Reliability Engineering
- **SLA, SLO, SLI**: availability targets
  - 99.9% = 8.76 hours downtime/year
  - 99.99% = 52.6 minutes downtime/year
  - 99.999% = 5.26 minutes downtime/year
- **Error budgets**: balance reliability vs velocity
- **Redundancy**: active-active, active-passive
- **Disaster Recovery**:
  - RPO (Recovery Point Objective)
  - RTO (Recovery Time Objective)
  - Backup strategies: hot, warm, cold standby
  - Multi-region deployment

### 7.2 Scalability Patterns
- **Horizontal scaling** vs **Vertical scaling**
- **Stateless services**: externalize state (Redis, DB)
- **Database read replicas** + write splitting
- **Sharding patterns**
- **CQRS**: separate read/write workloads
- **Async processing**: background jobs, message queues
- **Auto-scaling**: CPU-based, custom metrics

### 7.3 Performance Optimization
- **Caching hierarchy**: L1 (in-process) → L2 (distributed) → CDN
- **Database performance**:
  - Query optimization, EXPLAIN ANALYZE
  - Index tuning
  - Connection pooling
  - Read replicas
  - Materialized views
- **Application performance**:
  - Profiling: CPU, memory, I/O
  - Async/non-blocking I/O
  - Batch processing
  - Pagination: cursor-based
- **Network optimization**:
  - CDN
  - Compression (gzip, brotli)
  - HTTP/2, HTTP/3
  - Connection reuse

### 7.4 Chaos Engineering
- Principles of chaos engineering
- **Tools**: Chaos Monkey (Netflix), Litmus, Gremlin
- Game days: planned failure exercises
- Steady state hypothesis
- **Bài tập**: thiết kế chaos experiment cho microservices app

### 📚 Tài liệu Phase 7
| Tài liệu | Loại |
|-----------|------|
| *Site Reliability Engineering (SRE Book)* — Google | Sách (miễn phí) |
| *The Site Reliability Workbook* — Google | Sách (miễn phí) |
| *High Performance MySQL* | Sách |
| *Web Scalability for Startup Engineers* — Artur Ejsmont | Sách |

---

## Phase 8: Cloud Architecture & DevOps
**Thời lượng: 4–5 tuần**

### 8.1 Cloud Fundamentals
- **IaaS vs PaaS vs SaaS vs FaaS**
- **AWS Core Services**:
  - Compute: EC2, ECS, EKS, Lambda, Fargate
  - Storage: S3, EBS, EFS
  - Database: RDS, DynamoDB, ElastiCache, Aurora
  - Networking: VPC, Route 53, CloudFront, ALB/NLB
  - Messaging: SQS, SNS, EventBridge, Kinesis
- **Multi-region architecture**: data replication, failover
- **Well-Architected Framework**: 6 pillars

### 8.2 Containerization & Orchestration
- **Docker**: image, container, Dockerfile, multi-stage build
- **Docker Compose**: multi-container apps
- **Kubernetes**:
  - Pod, Deployment, Service, Ingress
  - ConfigMap, Secret
  - Horizontal Pod Autoscaler (HPA)
  - Persistent Volumes
  - Helm charts
  - **Bài tập**: deploy microservices app lên Kubernetes

### 8.3 CI/CD Pipeline
- **Git workflow**: trunk-based development, GitFlow
- **CI**: build → test → lint → security scan
- **CD**: staging → canary/blue-green → production
- **Deployment strategies**:
  - Rolling update
  - Blue-Green deployment
  - Canary deployment
  - Feature flags
- **Tools**: GitHub Actions, GitLab CI, Jenkins, ArgoCD

### 8.4 Infrastructure as Code (IaC)
- **Terraform**: HCL, state management, modules
- **AWS CloudFormation / CDK**
- **Pulumi**: IaC with programming languages
- **Configuration management**: Ansible
- **GitOps**: ArgoCD, Flux

### 8.5 Security Architecture
- **Zero Trust Architecture**: never trust, always verify
- **Network security**: VPC, security groups, NACLs, WAF
- **Secrets management**: HashiCorp Vault, AWS Secrets Manager
- **IAM**: principle of least privilege, RBAC
- **Compliance**: SOC 2, GDPR, HIPAA considerations
- **OWASP Top 10**: SQL injection, XSS, CSRF, SSRF...

### 📚 Tài liệu Phase 8
| Tài liệu | Loại |
|-----------|------|
| *AWS Well-Architected Framework* | Whitepaper (miễn phí) |
| *Kubernetes in Action* — Marko Lukša | Sách |
| *Terraform: Up & Running* — Yevgeniy Brikman | Sách |
| *The Phoenix Project* — Gene Kim | Sách |

---

## Phase 9: Case Studies nâng cao
**Thời lượng: 4–6 tuần**

### 9.1 Real-time Systems
- **Uber/Grab**: ride matching, real-time location tracking
  - Geospatial indexing: Geohash, Quadtree, H3
  - ETA calculation
  - Surge pricing
- **Trading System**: low-latency, order matching engine
  - LMAX Disruptor pattern
  - Sub-millisecond processing

### 9.2 Large-Scale Data Systems
- **Google Maps**: tile rendering, shortest path, real-time traffic
- **Web Crawler at scale**: distributed crawling, deduplication
- **Notification System**: push, SMS, email — at-least-once delivery
- **Distributed File System**: GFS, HDFS

### 9.3 Social & Collaboration
- **Collaborative Editor (Google Docs)**: OT vs CRDT
- **Social Graph**: friend recommendation, degree of separation
- **Live Streaming (Twitch)**: RTMP, WebRTC, HLS, chat at scale

### 9.4 Payment & Financial Systems
- **Payment Processing**: idempotency, double-entry bookkeeping
- **Digital Wallet**: balance consistency, distributed transactions
- **Fraud Detection**: real-time ML inference, rules engine

### 9.5 Thiết kế hệ thống cho AI/ML
- **ML Feature Store**: real-time vs batch features
- **Model Serving Platform**: A/B testing, canary deployment cho models
- **Recommendation System**: collaborative filtering, content-based, hybrid
- **Search Ranking System**: multi-stage ranking pipeline

### 📚 Tài liệu Phase 9
| Tài liệu | Loại |
|-----------|------|
| *System Design Interview Vol. 2* — Alex Xu | Sách |
| *Tech blogs*: Uber, Netflix, Instagram, Airbnb | Blog |
| *InfoQ, High Scalability* | Website |
| *Papers We Love (GitHub)* | Tổng hợp papers |

---

## 🗺️ LỘ TRÌNH TỔNG QUAN

```
Phase 0 ─── CS Fundamentals (3-4 tuần)
   │
Phase 1 ─── Networking & Web (3-4 tuần)
   │
Phase 2 ─── Building Blocks (4-6 tuần)
   │
Phase 3 ─── Database & Storage (4-6 tuần)
   │
Phase 4 ─── Distributed Systems (4-6 tuần)
   │
Phase 5 ─── System Design Practice (6-8 tuần)
   │
   ├── Phase 6 ─── Microservices (4-5 tuần)
   │
   ├── Phase 7 ─── Reliability & Performance (3-4 tuần)
   │
   └── Phase 8 ─── Cloud & DevOps (4-5 tuần)
         │
Phase 9 ─── Advanced Case Studies (4-6 tuần)
```

---

## 🎯 MẸO HỌC SYSTEM DESIGN

1. **Đọc tech blog** của các công ty lớn: Netflix, Uber, Meta, Google, Airbnb
2. **Practice whiteboard**: vẽ diagram trên giấy/whiteboard tool
3. **Mock interviews**: luyện với bạn hoặc dùng Pramp, interviewing.io
4. **Đi từ đơn giản → phức tạp**: bắt đầu single server, rồi mới scale up
5. **Trade-offs**: không có giải pháp hoàn hảo, luôn discuss trade-offs
6. **Hands-on**: deploy thực tế, đọc source code open-source systems
7. **Stay updated**: follow system design channels (ByteByteGo, Hussein Nasser)
