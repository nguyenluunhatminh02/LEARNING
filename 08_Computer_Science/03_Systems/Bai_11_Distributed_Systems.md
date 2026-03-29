# Bài 11: Distributed Systems

## 🎯 Mục tiêu
- Hiểu vì sao hệ phân tán khó hơn rất nhiều so với chương trình chạy trong một máy
- Nắm replication, partitioning, consistency, consensus, fault tolerance, idempotency và distributed transactions
- Có bộ khung tư duy để đọc design doc và thiết kế service thực tế

## 📖 Bức tranh lớn
Distributed systems bắt đầu từ một sự thật rất khó chịu: mạng không đáng tin tuyệt đối, node có thể chết giữa chừng, clock không đồng bộ hoàn hảo, và bạn không bao giờ quan sát toàn hệ thống ở một thời điểm chính xác. Phần lớn engineering ở scale là học cách sống chung với những giới hạn đó.

---

## 1. Những vấn đề cốt lõi

### Fallacies of distributed computing cần nhớ
- Mạng không phải lúc nào cũng reliable
- Latency không bằng 0
- Bandwidth không vô hạn
- Topology không cố định
- Network có cost và security boundary

### Hệ quả
- Partial failure xảy ra thường xuyên
- Retry có thể tạo duplicate work
- Timeout không đồng nghĩa chắc chắn là thất bại hoàn toàn

---

## 2. Replication và partitioning

### Replication
- Tăng availability/read scalability
- Có leader-follower, multi-leader, leaderless
- Sync vs async replication

### Partitioning / sharding
- Tăng write scalability, chia dữ liệu theo key/range/hash
- Rebalancing không hề miễn phí
- Hot partition là vấn đề thực tế rất thường gặp

---

## 3. Consistency models

### Các mức nên biết
- Strong consistency / linearizability
- Sequential consistency ở mức nhận biết
- Eventual consistency
- Read-after-write consistency
- Causal consistency ở mức overview

### Tư duy trade-off
- Strong consistency thường đổi lấy latency hoặc availability
- Eventual consistency đòi hỏi design idempotent và conflict resolution tốt hơn

---

## 4. Time, ordering và coordination

### Chủ đề quan trọng
- Physical clock vs logical clock
- Lamport clock
- Vector clock
- Clock skew
- Leader election
- Distributed locks ở mức thận trọng

### Tại sao quan trọng
- Event ordering ảnh hưởng correctness, deduplication, reconciliation và audit

---

## 5. Consensus và coordination

### Cần hiểu ở mức trực giác
- Consensus giải quyết việc nhiều node đồng ý trên một giá trị/thứ tự
- Paxos, Raft là những họ thuật toán cốt lõi
- Majority quorum, term/epoch, log replication là các khái niệm cơ bản

### Ứng dụng
- Metadata store
- Leader election
- Config management
- Distributed database internals

---

## 6. Distributed transactions và messaging

### Chủ đề cần nắm
- Two-phase commit ở mức overview
- Saga pattern
- Outbox pattern
- At-most-once, at-least-once, exactly-once ở mức thực tế
- Idempotency key

### Tư duy thực dụng
"Exactly-once" thường là sự kết hợp của delivery semantics + deduplication + idempotent processing, không phải phép màu.

---

## 7. Reliability patterns

### Nền tảng cần có
- Timeout, retry, exponential backoff
- Circuit breaker
- Bulkhead
- Health checks
- Graceful degradation
- Rate limiting, load shedding

### Điều phải nhớ
Retry không kiểm soát có thể biến lỗi cục bộ thành sự cố toàn hệ thống.

---

## 8. Observability và debugging trong distributed systems

### Tối thiểu cần có
- Correlation/request ID
- Structured logs
- Metrics: throughput, errors, saturation, queue depth
- Distributed tracing
- Red/USE metrics ở mức overview

### Mục tiêu
- Tái hiện được path của request qua nhiều service
- Thấy bottleneck, hot partition, retry storm, queue lag

---

## ✅ Checklist ôn tập
- Giải thích được vì sao distributed systems khó hơn single-node systems
- Phân biệt replication và partitioning
- Biết các consistency model phổ biến và trade-off của chúng
- Mô tả được Raft/Paxos ở mức trực giác
- Hiểu vì sao idempotency cực kỳ quan trọng khi có retry và message delivery

## 📝 Bài tập
1. Thiết kế một service có retry an toàn và idempotency key.
2. Viết note so sánh leader-follower với leaderless replication.
3. Mô phỏng một queue consumer xử lý duplicate messages.
4. Tự giải thích CAP và PACELC bằng ví dụ thực tế.
5. Phân tích failure modes cho một URL shortener hoặc payment workflow.

## 📚 Tài liệu
- *Designing Data-Intensive Applications* — Martin Kleppmann
- *Distributed Systems* — Maarten van Steen
- Track đào sâu: `../../02_System_Design/` và `../../03_Database/`