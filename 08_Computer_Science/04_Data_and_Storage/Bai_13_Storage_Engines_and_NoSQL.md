# Bài 13: Storage Engines and NoSQL

## 🎯 Mục tiêu
- Hiểu bên dưới database có những building blocks nào: page, WAL, B-Tree, LSM, compaction, caching, replication
- Nắm các họ NoSQL chính và framework chọn đúng công cụ cho đúng bài toán
- Kết nối storage internals với performance, durability và scaling behavior

## 📖 Bức tranh lớn
"Dùng PostgreSQL hay MongoDB hay Redis hay Cassandra?" là câu hỏi quá nông nếu bạn không hiểu workload và internals. Học storage engines giúp bạn lý giải tại sao một hệ thống write nhanh nhưng read range chậm, tại sao compaction làm latency spike, và tại sao cache giúp nhưng cũng có thể tạo inconsistency.

---

## 1. Building blocks của storage engine

### Chủ đề cốt lõi
- Page/block
- Buffer pool / cache
- Write-Ahead Log (WAL)
- Checkpoint
- Compaction
- SSTable
- Index structures

### Tư duy nền
- Disk/SSD access đắt hơn RAM rất nhiều
- Storage engine cố gắng chuyển random I/O thành sequential I/O khi có thể
- Durability gần như luôn cần logging hoặc journaling

---

## 2. B-Tree vs LSM-Tree

### B-Tree family
- Tốt cho point lookup và range query
- Phù hợp nhiều RDBMS và filesystem index
- Cập nhật tại chỗ nhiều hơn

### LSM-Tree family
- Tốt cho write-heavy workloads
- Write đi qua memtable -> WAL -> immutable files -> compaction
- Read có thể phức tạp hơn do nhiều tầng dữ liệu

### So sánh thực dụng
- B-Tree: read/range mạnh, write ổn định, model quen thuộc
- LSM: write throughput tốt, nhưng compaction và read amplification là trade-off lớn

---

## 3. Caching và memory hierarchy trong storage

### Chủ đề cần nắm
- OS page cache vs DB buffer pool
- Cache eviction
- Read-through / write-through / write-behind cache
- Cache invalidation

### Sai lầm phổ biến
- Cache data nóng nhưng quên chiến lược invalidation
- Double caching lãng phí memory
- Dùng cache như nguồn chân lý thay vì lớp tối ưu hóa

---

## 4. Families of NoSQL

### Key-Value
- Redis, Dynamo-style stores
- Rất mạnh cho simple lookup, counters, sessions, queues nhẹ

### Document
- MongoDB, Couchbase
- Schema linh hoạt, nested data, developer-friendly cho vài use cases

### Wide-column
- Cassandra, HBase
- Phù hợp workload lớn, write-heavy, partitioned by key design

### Graph
- Neo4j, JanusGraph
- Mạnh khi relationship traversal là trung tâm

### Search / inverted index
- Elasticsearch, OpenSearch
- Full-text search, relevance scoring, aggregations

### Vector databases
- pgvector, Pinecone, Milvus, Weaviate
- Similarity search cho embeddings và AI retrieval

---

## 5. Chọn công cụ theo workload

### Hỏi đúng trước khi chọn
- Access pattern là gì?
- Need exact transactions hay eventual consistency đủ?
- Read-heavy, write-heavy hay analytics-heavy?
- Dữ liệu có schema ổn định hay biến động mạnh?
- Range query, full-text search, graph traversal, vector similarity có quan trọng không?

### Nguyên tắc
- Không có database tốt nhất mọi tình huống
- Polyglot persistence là bình thường khi system đủ lớn
- Nhưng càng nhiều data store, operational complexity càng tăng

---

## 6. Replication, consistency và durability trong storage

### Chủ đề cần nắm
- Leader-follower replication
- Quorum reads/writes ở mức overview
- Read repair, anti-entropy
- Backup, PITR, disaster recovery

### Điều cần nhớ
- Replication không thay thế backup
- Backup không có restore test thì gần như chưa có backup

---

## 7. Storage cho systems engineer

### Các khái niệm rất đáng học
- LRU/LFU eviction
- Consistent hashing
- Bloom filter
- Log-structured design
- Append-only systems
- Columnar storage ở mức overview
- Object storage semantics

---

## ✅ Checklist ôn tập
- Giải thích được WAL, checkpoint, compaction để làm gì
- So sánh được B-Tree và LSM-Tree
- Chọn được loại NoSQL phù hợp cho use case đơn giản
- Hiểu cache có lợi ích và rủi ro gì
- Biết replication khác backup ở đâu

## 📝 Bài tập
1. Viết bảng so sánh PostgreSQL, Redis, MongoDB, Cassandra, Elasticsearch.
2. Giải thích data flow của một write trong LSM-based engine.
3. Thiết kế strategy cache cho một API đọc-heavy.
4. Phân tích vì sao compaction có thể gây latency spike.
5. Chọn storage stack cho một ứng dụng chat hoặc analytics và giải thích.

## 📚 Tài liệu
- *Designing Data-Intensive Applications* — Martin Kleppmann
- *Database Internals* — Alex Petrov
- Track đào sâu: `../../03_Database/`