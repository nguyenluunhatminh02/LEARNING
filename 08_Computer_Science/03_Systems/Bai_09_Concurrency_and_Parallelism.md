# Bài 09: Concurrency and Parallelism

## 🎯 Mục tiêu
- Phân biệt concurrency và parallelism
- Hiểu race condition, deadlock, memory model, async I/O, atomics và lock-free basics
- Biết thiết kế code concurrent vừa đúng vừa quan sát được khi có lỗi

## 📖 Bức tranh lớn
Concurrency là một trong những phần dễ gây bug nhất trong software engineering. Nhiều lỗi không tái hiện ổn định, chỉ xuất hiện dưới tải, phụ thuộc timing, core count, scheduler hoặc network/disk timing. Học tốt phần này giúp bạn tránh những bug khó chịu nhất trong production.

---

## 1. Concurrency vs parallelism

### Concurrency
- Nhiều tác vụ tiến triển chồng lấn theo thời gian
- Không nhất thiết chạy đồng thời thật trên nhiều core

### Parallelism
- Thực thi đồng thời thật trên nhiều core/GPU/worker

### Ví dụ
- Async web server: concurrency cao nhưng không phải request nào cũng song song trên CPU
- Data processing trên nhiều cores: parallelism rõ ràng

---

## 2. Shared state và synchronization primitives

### Primitive cần nắm
- Mutex
- RWLock
- Semaphore
- Condition variable
- Barrier
- Atomic operations

### Sai lầm phổ biến
- Lock quá rộng làm giảm throughput
- Lock ordering không nhất quán dẫn tới deadlock
- Kiểm tra condition ngoài lock rồi assume vẫn đúng

---

## 3. Race condition, deadlock, livelock, starvation

### Race condition
Behavior phụ thuộc thứ tự thực thi không được kiểm soát.

### Deadlock
Các tác vụ chờ nhau vô hạn.

### Livelock
Các tác vụ vẫn chạy nhưng không tiến triển hữu ích.

### Starvation
Một tác vụ bị bỏ đói do scheduler hoặc locking policy.

### 4 điều kiện của deadlock
- Mutual exclusion
- Hold and wait
- No preemption
- Circular wait

---

## 4. Memory model ở mức engineer

### Cần hiểu ở mức trực giác
- Compiler và CPU có thể reorder operations
- Một thread ghi rồi thread khác đọc không tự động đảm bảo thấy cùng thứ tự bạn viết trong code
- Atomics, fences, happens-before là công cụ để thiết lập trật tự nhìn thấy được

### Ứng dụng
- Double-checked locking
- Producer-consumer queue
- Lock-free counters

Không cần lao ngay vào formalism quá sâu, nhưng phải biết rằng "code nhìn có vẻ đúng" chưa đủ trong concurrent code.

---

## 5. Models of concurrency

### Threads + locks
- Phổ biến, mạnh, nhưng dễ bug

### Event loop / async-await
- Tốt cho I/O-heavy workload
- Giảm số thread, nhưng không miễn trừ race trên shared state logic

### Actor model / message passing
- Tránh shared mutable state trực tiếp
- Phù hợp với distributed thinking

### Data parallel / SIMD / GPU
- Tốt cho numerical workloads và vectorized tasks

---

## 6. Parallel performance

### Chủ đề cần nắm
- Amdahl's law
- Work distribution
- Contention
- False sharing
- Cache coherence
- Batching và work stealing ở mức overview

### Trực giác
Tăng số worker không đảm bảo tăng throughput tuyến tính. Bottleneck thường nằm ở lock contention, memory bandwidth hoặc serialized step.

---

## 7. Thiết kế hệ concurrent bền hơn

### Nguyên tắc hữu ích
- Shared mutable state càng ít càng tốt
- Ưu tiên immutability khi hợp lý
- Chọn ownership rõ ràng cho data
- Lock đúng chỗ, giữ lock ngắn
- Timeout, cancellation, backpressure phải được nghĩ tới
- Logging và metrics phải đủ để thấy queue depth, latency, retry, saturation

---

## ✅ Checklist ôn tập
- Giải thích được concurrency khác parallelism ở đâu
- Nhận diện được race, deadlock, starvation
- Biết dùng mutex/semaphore/atomic trong bối cảnh nào
- Hiểu event loop phù hợp với loại workload nào
- Nêu được ít nhất 3 lý do vì sao thêm thread không làm chương trình nhanh hơn

## 📝 Bài tập
1. Viết producer-consumer queue với thread-safe coordination.
2. Tạo một ví dụ deadlock nhỏ và sửa nó.
3. So sánh thread pool vs async I/O cho web scraping hoặc HTTP client.
4. Đọc về Amdahl's law và áp dụng cho một task xử lý data giả định.
5. Viết checklist debug concurrency bug cho chính bạn.

## 📚 Tài liệu
- *The Art of Multiprocessor Programming* — Herlihy & Shavit
- *Java Concurrency in Practice* — Goetz et al.
- Track đào sâu: `../../04_DSA/` và `../../02_System_Design/`