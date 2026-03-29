# Bài 11: Distributed Systems — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- hiểu vì sao distributed systems khó hơn nhiều so với single-node systems
- nắm replication, partitioning, consistency, consensus, retries, idempotency và fault tolerance ở mức kỹ sư phần mềm
- có nền đủ tốt để đọc design docs và incident reports liên quan systems ở scale lớn hơn

## Bạn cần biết trước
- Bài 08, 09, 10

---

## 1. Điều gì làm distributed systems khó

Trong single-node program, một hàm thường:
- chạy hoặc crash
- trả kết quả hoặc ném lỗi

Trong distributed systems, mọi thứ khó hơn vì:
- mạng có latency
- messages có thể mất
- nodes có thể chết giữa chừng
- clocks không hoàn toàn đồng bộ
- partial failure là trạng thái bình thường

---

## 2. Replication

Replication là sao chép data hoặc state sang nhiều nodes.

### Lợi ích
- availability tốt hơn
- read scalability tốt hơn

### Trade-off
- consistency phức tạp hơn
- failover không miễn phí
- replica lag tạo stale reads

### Các mô hình phổ biến
- leader-follower
- multi-leader
- leaderless

---

## 3. Partitioning / sharding

Partitioning chia dữ liệu ra nhiều nodes để scale.

### Các kiểu thường gặp
- hash-based
- range-based
- directory-based ở mức overview

### Nguy cơ lớn
- hot partition
- skewed traffic
- rebalancing khó

Chỉ cần một số keys quá nóng là cả hệ thống có thể mất cân bằng nặng.

---

## 4. Consistency models

### Strong consistency / linearizability
Thấy dữ liệu như vừa được update ngay theo một thứ tự hợp lý.

### Eventual consistency
Nếu không có update mới, các replicas cuối cùng sẽ hội tụ.

### Vì sao quan trọng
Đây không chỉ là chuyện database internals. Nó ảnh hưởng trực tiếp tới UX và business semantics.

Ví dụ:
- inventory
- chat ordering
- user profile edits
- account balance views

---

## 5. Timeouts, retries và idempotency

Một timeout không chứng minh rằng phía server chưa xử lý xong.

Do đó, khi client retry:
- có thể side effect đã xảy ra rồi
- có thể message cũ vừa tới muộn
- có thể duplicate work xuất hiện

Đây là lý do idempotency cực kỳ quan trọng.

### Ví dụ
`POST /payments` nếu retry mà không có idempotency key có thể tạo hai giao dịch.

---

## 6. Consensus và coordination

Consensus giải bài toán nhiều nodes đồng ý trên một giá trị hoặc một thứ tự hành động.

### Bạn nên biết ở mức trực giác
- Raft/Paxos tồn tại để tránh split brain và giữ ordering hợp lý cho metadata hoặc log
- majority/quorum là khái niệm trung tâm
- leader election là một phần rất quan trọng

Bạn không cần tự code Raft ngay để hưởng lợi từ intuition này.

---

## 7. Distributed transactions và messaging

### Các mô hình nên biết
- two-phase commit
- saga
- outbox pattern
- at-most-once / at-least-once / effectively-once ở mức thực dụng

### Tư duy thực tế
"Exactly once" thường là kết hợp của:
- delivery semantics
- deduplication
- idempotent processing

---

## 8. Reliability patterns

Các pattern cốt lõi:
- timeout
- retry với exponential backoff
- circuit breaker
- bulkhead
- rate limiting
- load shedding
- graceful degradation

Retry không kiểm soát là một trong những cách tự phá hệ thống nhanh nhất.

---

## 9. Observability trong distributed systems

Bạn cần ít nhất:
- request ID / correlation ID
- structured logs
- metrics về latency, errors, saturation
- tracing nếu hệ thống có nhiều hops

Nếu không có observability, bạn gần như mù khi production có partial failure.

---

## 10. Checklist sau bài
- Giải thích được vì sao distributed systems khó hơn single-node systems
- Phân biệt replication với partitioning
- Nêu được các consistency models cơ bản
- Hiểu vai trò của idempotency khi retry
- Mô tả được consensus ở mức trực giác

## 11. Bài tập thực hành
1. Thiết kế retry strategy an toàn cho một payment API.
2. Viết note so sánh leader-follower và leaderless replication.
3. Tạo một incident giả định do duplicate messages.
4. Giải thích CAP/PACELC theo ngôn ngữ của bạn.
5. Vẽ data flow cho một distributed queue consumer.

## 12. Mini deliverable
Tạo file `distributed_systems_risk_checklist.md` gồm:
- retries
- idempotency
- stale reads
- hot keys/partitions
- observability
- failure recovery

## 13. Học tiếp
- `../04_Data_and_Storage/Bai_12_Relational_Databases_Full_Lesson.md`
- `../../08_Reference_and_Review/04_Systems_Deep_Dive.md`