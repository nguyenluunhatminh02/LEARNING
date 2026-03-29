# Bài 13: Storage Engines and NoSQL — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- hiểu các building blocks dưới database như WAL, B-Tree, LSM-tree, compaction, caching
- phân biệt các họ NoSQL chính và khi nào nên dùng chúng
- có framework chọn storage system theo workload thay vì theo xu hướng

## Bạn cần biết trước
- Bài 12

---

## 1. Vì sao phải nhìn xuống dưới database engine

Nếu chỉ nhìn ở mức SQL hoặc API, bạn sẽ khó lý giải:
- vì sao write nhanh nhưng read range chậm
- vì sao latency spike theo chu kỳ
- vì sao compaction, checkpoint hoặc cache invalidation lại quan trọng

Engine matters because physical reality matters.

---

## 2. WAL, checkpoints và recovery

Storage engine phải quan tâm không chỉ fast path mà cả crash recovery.

### WAL
Ghi log trước khi cập nhật state chính để hỗ trợ durability và recovery.

### Checkpoint
Giúp rút ngắn thời gian recovery bằng cách định kỳ chốt một trạng thái ổn định hơn.

Một hệ dữ liệu tốt không chỉ nhanh khi khỏe, mà còn hồi phục được khi xấu.

---

## 3. B-Tree vs LSM-tree

### B-Tree family
Phù hợp khi:
- point lookup và range query đều quan trọng
- read path ổn định cần được ưu tiên

### LSM-tree family
Phù hợp khi:
- writes rất nhiều
- append/log-structured design có lợi

### Trade-off
- B-Tree thường đọc/range tốt hơn
- LSM thường ghi tốt hơn nhưng dễ có read amplification và compaction pressure

---

## 4. Cache và memory hierarchy trong storage

### Page cache / buffer pool
Giúp tránh chạm disk quá thường xuyên.

### Cache patterns
- cache-aside
- read-through
- write-through
- write-behind

### Điểm phải nhớ
Cache là optimization layer, không phải source of truth.

Và cache invalidation là một trong những vấn đề khó nhất vì correctness và freshness phải cân bằng.

---

## 5. NoSQL families

### Key-value
Rất hợp cho exact lookup, sessions, counters, simple caches.

### Document
Hợp với nested data và schema linh hoạt hơn.

### Wide-column
Hợp với scale lớn và access patterns thiết kế quanh partition key.

### Graph
Hợp khi relationship traversal là trung tâm.

### Search engine
Hợp cho full-text search và aggregations.

### Vector database
Hợp cho similarity search trên embeddings.

---

## 6. Cách chọn storage system

Đừng bắt đầu bằng công nghệ. Hãy bắt đầu bằng workload.

Hỏi 5 câu:
- read-heavy hay write-heavy?
- exact lookup, range query, full-text hay similarity search?
- consistency cần tới đâu?
- data shape ổn định hay rất linh hoạt?
- operational complexity team chịu được tới đâu?

---

## 7. Replication, backup và durability

### Replication
Giúp availability và scale reads.

### Backup
Giúp disaster recovery.

Replication không thay thế backup. Đây là điểm phải nhớ thật chắc.

### Những gì nên nghĩ tới
- replication lag
- restore testing
- PITR
- cross-region strategy

---

## 8. Sai lầm phổ biến
- chọn NoSQL chỉ vì "schema linh hoạt"
- thêm cache trước khi biết bottleneck thật
- tưởng replication là đủ cho DR
- bỏ qua hot keys/hot partitions
- không nghĩ tới compaction, write amplification, read amplification

---

## 9. Checklist sau bài
- Giải thích được WAL, checkpoint, compaction
- So sánh được B-Tree và LSM-tree
- Phân biệt được các họ NoSQL chính
- Chọn được storage type phù hợp cho vài use cases phổ biến
- Hiểu replication, backup và cache giải các bài toán khác nhau

## 10. Bài tập thực hành
1. So sánh PostgreSQL, Redis, MongoDB, Cassandra, Elasticsearch theo use case.
2. Viết 1 trang về B-Tree vs LSM-tree.
3. Thiết kế cache strategy cho một endpoint read-heavy.
4. Chọn storage stack cho một hệ thống chat hoặc analytics.
5. Viết checklist review durability và recovery cho một data service.

## 11. Mini deliverable
Tạo file `storage_selection_framework.md` gồm:
- workload questions
- storage options
- trade-offs
- operational risks

## 12. Học tiếp
- `../05_Languages_and_Tools/Bai_14_Programming_Languages_Full_Lesson.md`
- `../../08_Reference_and_Review/05_Data_and_Storage_Deep_Dive.md`