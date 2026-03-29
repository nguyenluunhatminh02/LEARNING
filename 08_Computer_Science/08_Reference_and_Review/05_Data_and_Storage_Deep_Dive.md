# Data and Storage Deep Dive

## Mục tiêu của file này
File này đào sâu cho:
- Relational Databases
- Storage Engines and NoSQL

Đây là phần giúp bạn hiểu dữ liệu không chỉ ở mức schema và query, mà ở mức engine, durability, workload fit và operational trade-off.

---

## 1. Data mindset

Khi nhìn một hệ dữ liệu, luôn hỏi 5 câu trước:
- Dữ liệu nào là source of truth?
- Workload chính là read-heavy, write-heavy hay analytics-heavy?
- Cần consistency mạnh tới mức nào?
- Recovery objective là gì?
- Hot path nằm ở app, cache hay storage engine?

Nếu không trả lời được 5 câu này, mọi tranh luận chọn database thường rất nông.

---

## 2. Relational modeling deep dive

### 2.1 Schema là design, không phải paperwork

Schema tốt giúp:
- ép business rules bằng constraints
- giảm ambiguity trong code
- hỗ trợ query predictable hơn
- giảm data anomalies

Schema kém dẫn tới:
- duplicated truth
- update anomalies
- app logic rải rác phải tự bù các constraint bị thiếu

### 2.2 Normalization vs denormalization

Không có câu trả lời tuyệt đối.

Normalization mạnh khi:
- correctness và consistency quan trọng
- update patterns phức tạp
- business entities có quan hệ rõ

Denormalization hợp lý khi:
- đọc nhiều hơn ghi rất rõ
- join cost hoặc complexity gây vấn đề thật
- chấp nhận được dữ liệu duplicate có chiến lược sync rõ ràng

### 2.3 Keys matter more than people think

Phải suy nghĩ kỹ về:
- natural key vs surrogate key
- composite key khi domain yêu cầu uniqueness đa chiều
- unique constraints để bảo vệ idempotency

---

## 3. Query execution intuition

### 3.1 SQL là declarative, execution plan mới là operational reality

Hai query viết khác nhau nhưng logic tương đương có thể ra plan rất khác.

Do đó, ngoài viết SQL đúng, bạn nên học nhìn:
- scan type
- join order
- join strategy
- rows estimated vs actual
- sort/hash/materialization costs

### 3.2 Cardinality estimation is central

Nhiều plan tệ không phải vì database "ngu", mà vì cardinality estimation sai. Khi estimate sai, optimizer có thể chọn join order hoặc index usage tệ hẳn.

### 3.3 Indexes are workload-specific

Một index tốt không chỉ là "có index". Nó phải khớp với:
- filter columns
- join predicates
- order by
- selectivity
- covering needs

---

## 4. Transactions and concurrency deep dive

### 4.1 Isolation is product behavior

Isolation level không chỉ là lựa chọn kỹ thuật nội bộ. Nó quyết định:
- user có thấy stale data không
- double booking có thể xảy ra không
- inventory có oversell không
- reports có đọc state trung gian không

### 4.2 Locks vs MVCC intuition

Phải hiểu:
- locks giúp serialization nhưng dễ contention
- MVCC giúp nhiều reads không block writes theo cách truyền thống
- nhưng MVCC không miễn phí; nó kéo theo version cleanup, visibility rules và storage overhead

### 4.3 Deadlocks are normal, not shameful

Deadlocks trong DB không có nghĩa bạn dở. Nó nghĩa là concurrency real. Điều quan trọng là:
- hiểu access order
- giữ transaction ngắn
- retry strategy rõ ràng
- monitor lock waits và deadlock frequency

---

## 5. Storage engine intuition

### 5.1 WAL, checkpoint, recovery

Phải internalize:
- để dữ liệu bền, engine gần như luôn cần log hoặc journal
- commit không chỉ là đổi một bit trong RAM
- recovery path quan trọng ngang fast path

### 5.2 B-Tree family

Phù hợp khi:
- range query nhiều
- point lookup có order semantics
- read performance ổn định quan trọng

### 5.3 LSM family

Phù hợp khi:
- write throughput lớn
- append/log-structured path có lợi
- chấp nhận complexity từ compaction và read amplification

### 5.4 Compaction is not background trivia

Compaction ảnh hưởng trực tiếp tới:
- tail latency
- disk bandwidth
- write amplification
- temporary space usage

---

## 6. Cache and data access patterns

### 6.1 Cache is an optimization, not truth

Những câu hỏi cần trả lời trước khi thêm cache:
- stale data chấp nhận được bao lâu?
- invalidation xảy ra thế nào?
- miss storm xử lý ra sao?
- cache warm-up có ảnh hưởng launch/failover không?

### 6.2 Common patterns
- cache-aside
- read-through
- write-through
- write-behind

Mỗi pattern giải một nhóm trade-off khác nhau.

### 6.3 Hot keys and thundering herd

Phải có intuition về:
- hot read keys
- stampede khi cache miss đồng thời
- singleflight/request coalescing
- admission policy

---

## 7. NoSQL selection framework

### 7.1 Key-value
Chọn khi:
- exact lookup theo key là trung tâm
- latency cực thấp quan trọng
- schema logic chủ yếu ở application layer

### 7.2 Document
Chọn khi:
- entity shape tương đối linh hoạt
- nested document tự nhiên với domain
- không cần quá nhiều relational joins/phức tạp giao dịch liên bảng

### 7.3 Wide-column
Chọn khi:
- scale rất lớn
- partitioning theo access pattern rõ ràng
- write-heavy and availability-oriented design

### 7.4 Search engine
Chọn khi:
- full-text search, ranking, inverted index, aggregations là trọng tâm

### 7.5 Vector store
Chọn khi:
- semantic similarity search là trọng tâm
- embeddings là representation chính của retrieval problem

---

## 8. Operational questions you should ask

- backup chạy bao lâu, restore đã test chưa?
- replication lag đo bằng gì?
- slow queries được lưu ở đâu?
- index bloat hay compaction pressure có đang tăng không?
- capacity planning dựa trên read/write mix nào?
- multi-region strategy có cần thật không hay chỉ làm system phức tạp hơn?

---

## 9. Mistake catalog

- thêm index theo cảm giác, không dựa trên query plans
- cache trước khi hiểu bottleneck thật
- tin rằng replication là đủ cho disaster recovery
- chọn NoSQL chỉ vì schema "flexible" mà không có workload reasoning
- nhồi JSON vào relational table rồi mất constraints và index semantics

---

## 10. What to know cold

Bạn nên biết cold:
- ACID là gì
- MVCC là gì
- index giúp gì và trade-off gì
- B-Tree vs LSM-tree
- cache-aside vs write-through
- replication vs backup
- OLTP vs OLAP
- document DB vs key-value vs search vs vector DB

---

## 11. Suggested labs

### Lab 1: Query plan walkthrough
Viết 3 queries và dự đoán plan trước khi xem `EXPLAIN`.

### Lab 2: Index design note
Chọn một schema và đề xuất index cho 5 access patterns khác nhau.

### Lab 3: Cache design exercise
Thiết kế cache cho endpoint read-heavy và ghi rõ invalidation policy.

### Lab 4: Storage engine comparison
Viết 1-2 trang so sánh B-Tree, LSM, inverted index, vector index.

---

## 12. Oral exam questions

- Vì sao một query đúng vẫn có thể rất chậm?
- Khi nào denormalization là hợp lý?
- Vì sao MVCC giúp đọc đồng thời nhưng không miễn phí?
- Compaction tạo latency spike bằng cơ chế nào?
- Vì sao cache invalidation khó?
- Tại sao replication không thay thế backup?

---

## 13. Reading sequence

1. SQL fundamentals + indexing
2. transactions/isolation/MVCC
3. storage engine internals
4. NoSQL families and selection
5. production operations and capacity

---

## 14. Final reminder
Data systems cần được học ở hai lớp cùng lúc: logic correctness và physical reality. Nếu bạn chỉ hiểu schema mà không hiểu engine, hoặc chỉ hiểu engine mà không hiểu domain constraints, quyết định của bạn thường sẽ lệch.