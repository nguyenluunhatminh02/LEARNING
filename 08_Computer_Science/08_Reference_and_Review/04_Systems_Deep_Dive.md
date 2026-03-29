# Systems Deep Dive

## Mục tiêu của file này
File này đào sâu cho các bài:
- Operating Systems
- Concurrency and Parallelism
- Computer Networks
- Distributed Systems

Đây là nhóm kiến thức tạo khác biệt lớn giữa người chỉ viết code được và người hiểu hệ thống đang sống như thế nào trong production.

---

## 1. Systems mindset

Một systems engineer tốt có 4 phản xạ:

### Phản xạ 1: luôn nghĩ tới resource limits
CPU, memory, disk, network, file descriptors, queue length, thread count đều hữu hạn.

### Phản xạ 2: luôn nghĩ tới latency path
Mỗi request đi qua những lớp nào, lớp nào có thể block, queue hay retry?

### Phản xạ 3: luôn nghĩ tới failure modes
Node chết, packet mất, disk chậm, DNS lỗi, lock contention, GC pause, kernel limits.

### Phản xạ 4: luôn nghĩ tới observability
Nếu production hỏng, mình nhìn số liệu nào trước để biết chuyện gì đang xảy ra?

---

## 2. Operating Systems deep dive

### 2.1 Process model

Bạn phải thật chắc:
- process có address space riêng
- thread chia sẻ address space của process
- file descriptors gắn với process state
- fork/exec model ở Unix tồn tại để làm gì

Các câu hỏi tự kiểm tra:
- khi spawn process mới, cái gì được copy, cái gì được share?
- vì sao process isolation mạnh hơn thread isolation?
- vì sao context switch không miễn phí?

### 2.2 Scheduling intuition

Không cần thành kernel hacker, nhưng nên hiểu:
- scheduler tối ưu fairness, throughput, responsiveness bằng các heuristic và policies
- CPU-bound task và I/O-bound task tạo áp lực khác nhau lên scheduler
- quá nhiều runnable threads dễ làm cache locality và latency tệ đi

### 2.3 Virtual memory and paging

Phải internalize:
- virtual memory là abstraction cực mạnh cho isolation và allocation
- page fault không luôn là lỗi, nhưng có thể rất đắt
- TLB miss và page fault là hai khái niệm khác nhau
- swapping nặng có thể làm ứng dụng trông như "đơ" dù không crash

### 2.4 Filesystems and durability

Phải hiểu ở mức thực dụng:
- write thành công ở app chưa chắc đã bền xuống disk ngay
- page cache và write-back làm performance tốt hơn nhưng durability reasoning khó hơn
- `fsync` tồn tại vì cần ranh giới rõ hơn về độ bền dữ liệu

### 2.5 OS limits thường gặp trong production

Checklist điều tra:
- `ulimit` file descriptors
- process/thread count
- CPU throttling/cgroup limits
- memory RSS vs virtual size
- disk IOPS và disk full
- inode exhaustion

---

## 3. Concurrency deep dive

### 3.1 Shared state is the real enemy

Concurrency không nguy hiểm vì có nhiều threads. Nó nguy hiểm vì có shared mutable state cộng với timing không dự đoán được.

Do đó, khi thiết kế concurrent system, câu hỏi đầu tiên nên là:
- state nào thật sự phải chia sẻ?
- có thể chuyển sang immutable/message passing không?
- ownership của state thuộc ai?

### 3.2 Locking strategy

Bạn nên biết:
- coarse-grained lock đơn giản nhưng bóp throughput
- fine-grained lock tăng concurrency nhưng tăng complexity và risk deadlock
- lock ordering là kỹ thuật cực thực dụng để tránh deadlock

### 3.3 Memory model intuition

Đây là phần nhiều người bỏ qua vì "khó" nhưng lại rất quan trọng.

Phải hiểu trực giác rằng:
- compiler và CPU có thể reorder
- một write ở thread A không tự động visible đúng lúc cho thread B
- atomic operations và synchronization primitives thiết lập visibility guarantees

### 3.4 Async I/O is not magic

Async/await giúp quản lý I/O concurrency tốt hơn ở nhiều workload, nhưng không giải quyết tự động:
- race conditions ở shared caches/maps
- backpressure
- cancellation correctness
- long CPU-bound tasks chặn event loop

### 3.5 Parallel performance traps

Các bẫy kinh điển:
- lock contention
- false sharing
- work imbalance
- serialization step nhỏ nhưng nằm trong hot path
- memory bandwidth saturation

---

## 4. Networking deep dive

### 4.1 The real request path

Một HTTP request thật ngoài production có thể đi qua:
- client app
- local DNS cache
- recursive resolver
- CDN/edge
- load balancer
- reverse proxy
- app server
- internal service mesh
- downstream services
- database/cache

Nếu không map path này, bạn sẽ chẩn đoán timeout rất mù mờ.

### 4.2 Latency decomposition

Khi API chậm, hãy nghĩ:
- DNS delay?
- TCP handshake?
- TLS handshake?
- queueing tại LB?
- app compute?
- DB query?
- downstream call?
- retransmit do packet loss?

### 4.3 Retries and timeouts

Đây là nơi nhiều hệ thống tự phá mình.

Phải hiểu:
- timeout quá ngắn gây retry giả
- timeout quá dài làm tài nguyên bị giữ quá lâu
- retry không idempotent có thể gây duplicate effects
- fan-out + retries có thể nhân tải rất mạnh

### 4.4 TCP intuition that matters

Bạn không cần thuộc toàn bộ RFC, nhưng nên hiểu:
- ordered reliable delivery có cost
- head-of-line blocking có thể quan trọng
- congestion control ảnh hưởng throughput thực
- connection pooling và keep-alive rất có giá trị

### 4.5 DNS and TLS are not side details

Rất nhiều outage hoặc latency issue liên quan tới:
- DNS misconfiguration
- TTL không phù hợp
- expired certificates
- trust chain problems
- clock skew làm TLS fail

---

## 5. Distributed systems deep dive

### 5.1 Partial failure mindset

Trong single-node app, bạn thường nghĩ operation thành công hoặc thất bại rõ ràng.
Trong distributed systems, bạn thường chỉ biết:
- request timeout
- không rõ server có xử lý hay chưa
- reply có thể lost dù side effect đã xảy ra

Đây là lý do idempotency, reconciliation và observability quan trọng đến vậy.

### 5.2 Consistency models are product decisions too

Consistency không chỉ là chuyện database internals. Nó ảnh hưởng trực tiếp tới UX và business rules.

Ví dụ:
- inventory oversell
- stale profile data
- chat message ordering
- balance hiển thị sai tạm thời

### 5.3 Replication choices

Khi chọn replication strategy, hãy hỏi:
- read-heavy hay write-heavy?
- geo-distributed hay single region?
- failover time acceptable là bao lâu?
- app chịu stale reads đến mức nào?

### 5.4 Partitioning and hot keys

Nhiều hệ thống scale tốt trên slide nhưng vỡ ngoài đời vì:
- hot tenant
- hot key
- skewed traffic distribution
- poor partitioning function

Do đó, hashing hay range partitioning đều phải được xem xét cùng workload thật.

### 5.5 Consensus intuition

Raft/Paxos không phải để "cho vui". Chúng giải bài toán thực tế:
- làm sao nhiều node đồng ý ai là leader
- làm sao metadata/config thay đổi có trật tự rõ ràng
- làm sao log replicated nhưng không split-brain tùy tiện

Bạn không cần tự implement Raft từ đầu để hưởng lợi từ intuition này.

### 5.6 Messaging semantics

Phải phân biệt:
- message delivered
- message processed
- side effect committed

Ba điều này không tự động đồng nghĩa.

### 5.7 Sagas, outbox, idempotency

Đây là những pattern cực đáng học vì chúng biến distributed side effects thành thứ có thể reason được.

---

## 6. Failure mode catalog

### OS-level
- OOM killer
- file descriptors exhausted
- disk full
- CPU throttling
- time sync issues

### Concurrency-level
- race condition
- deadlock
- starvation
- event loop blocked
- unbounded queue growth

### Network-level
- DNS outage
- packet loss
- TLS handshake failures
- slow downstream
- retry amplification

### Distributed-level
- split brain
- stale reads
- duplicate messages
- hot partition
- replica lag

---

## 7. What to know cold

Biết cold nghĩa là có thể giải thích nhanh, chính xác:
- process vs thread
- blocking vs non-blocking I/O
- mutex vs semaphore
- TCP vs UDP vs QUIC
- timeout vs retry vs backoff
- replication vs partitioning
- strong consistency vs eventual consistency
- idempotency là gì và vì sao bắt buộc khi retry side effects

---

## 8. System troubleshooting playbooks

### Playbook 1: API timeout tăng đột ngột
Kiểm tra theo thứ tự:
1. error rate tổng quát
2. downstream latency
3. CPU/memory saturation
4. connection pool exhaustion
5. queue depth
6. DNS/TLS/network anomalies
7. recent deploy/config changes

### Playbook 2: service bị kill trong container
Kiểm tra:
1. memory limit
2. OOM events
3. RSS growth
4. thread count
5. file descriptors
6. GC behavior nếu runtime có GC

### Playbook 3: duplicate side effects
Kiểm tra:
1. retries ở client và server
2. idempotency key
3. at-least-once consumers
4. timeout semantics
5. outbox/dedup strategy

---

## 9. Suggested labs

### Lab A: Mini thread pool server
Học được:
- socket accept loop
- worker pool
- queueing
- shutdown handling

### Lab B: Async I/O demo
Học được:
- event loop
- backpressure
- timeouts/cancellation

### Lab C: Retry experiment
Mô phỏng downstream chậm/lỗi để thấy retry storm.

### Lab D: Replica lag thought experiment
Thiết kế read/write path và xác định chỗ stale data có thể xuất hiện.

---

## 10. Oral exam questions

- Vì sao too many threads có thể làm hệ thống chậm hơn?
- Tại sao page cache vừa hữu ích vừa làm durability reasoning khó hơn?
- Khi nào async I/O tốt hơn thread-per-request?
- Vì sao timeout không chứng minh được operation chưa chạy ở phía server?
- Hot partition là gì và vì sao khó phát hiện sớm?
- Tại sao retries phải đi kèm idempotency?

---

## 11. Reading sequence

1. OSTEP cho OS fundamentals
2. CSAPP cho machine + systems intuition
3. Kurose & Ross cho networking
4. DDIA cho distributed systems và storage intuition

---

## 12. Dấu hiệu bạn đã tiến bộ thật trong systems

Bạn đã tiến bộ khi:
- không còn mô tả sự cố bằng từ mơ hồ như "server lag"
- thay vào đó nói được: CPU saturation, queue buildup, replica lag, lock contention, page faults, DNS timeout, retry amplification
- mỗi lần đọc incident report, bạn nhìn thấy model phía sau chứ không chỉ timeline sự kiện

---

## 13. Cảnh báo cuối
Systems knowledge rất dễ tạo ảo giác "mình hiểu vì đã đọc bài blog". Hãy ép bản thân gắn mỗi khái niệm với ít nhất một hiện tượng production, một metric, một failure mode và một design trade-off. Nếu chưa làm được như vậy, kiến thức đó vẫn còn nông.