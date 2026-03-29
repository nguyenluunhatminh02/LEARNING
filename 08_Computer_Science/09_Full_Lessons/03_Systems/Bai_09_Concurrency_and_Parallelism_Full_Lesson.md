# Bài 09: Concurrency and Parallelism — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- phân biệt concurrency và parallelism một cách rõ ràng
- hiểu race conditions, deadlocks, atomics, memory ordering và async I/O ở mức engineer
- có trực giác tốt hơn để thiết kế code concurrent ít bug hơn

## Bạn cần biết trước
- Bài 08
- kiến thức căn bản về functions, state và data structures

---

## 1. Concurrency và parallelism khác nhau ở đâu

### Concurrency
Nhiều tác vụ tiến triển chồng lấn theo thời gian.

### Parallelism
Nhiều tác vụ thật sự chạy cùng lúc trên nhiều execution units.

Ví dụ:
- async web server xử lý hàng nghìn connections là concurrency mạnh
- matrix computation trên 8 cores là parallelism rõ rệt

Nhầm lẫn hai khái niệm này là nguồn của nhiều thiết kế sai.

---

## 2. Shared mutable state là nguồn rủi ro lớn nhất

Concurrency khó không phải vì có nhiều threads, mà vì có shared mutable state cùng timing khó đoán.

Do đó, khi thiết kế concurrent system, hãy hỏi:
- state nào thật sự phải chia sẻ?
- state nào có thể immutable?
- có thể dùng message passing thay cho shared memory không?

---

## 3. Synchronization primitives

### Mutex
Bảo vệ critical section.

### RWLock
Hữu ích khi reads nhiều, writes ít.

### Semaphore
Kiểm soát số lượng workers/resource slots.

### Condition variable
Dùng để chờ trạng thái nào đó thay đổi.

### Atomics
Thích hợp cho counters, flags, một số patterns cụ thể.

Chọn primitive sai có thể làm code vừa chậm vừa sai.

---

## 4. Race, deadlock, livelock, starvation

### Race condition
Kết quả phụ thuộc timing hoặc interleaving không kiểm soát.

### Deadlock
Các luồng giữ resource và chờ nhau vô hạn.

### Livelock
Vẫn hoạt động nhưng không tạo tiến triển hữu ích.

### Starvation
Một task bị bỏ đói do policy hoặc contention.

### Thực hành tốt
- lock ordering nhất quán
- giữ critical section ngắn
- giới hạn số shared resources
- thêm timeouts/cancellation khi phù hợp

---

## 5. Memory model ở mức đủ dùng

Bạn không cần formal proofs quá sớm, nhưng phải hiểu:
- compiler có thể reorder
- CPU có thể reorder
- thread B không tự động thấy write của thread A theo thứ tự bạn nghĩ

Các từ khóa cần internalize:
- atomic
- happens-before
- visibility
- fences ở mức khái niệm

Nếu bỏ qua memory model, nhiều concurrent bugs sẽ trông như "ma ám".

---

## 6. Models of concurrency

### Threads + locks
Mạnh, phổ biến, nhưng dễ bug.

### Event loop / async-await
Rất hợp cho I/O-bound workloads.

### Actor / message passing
Giảm shared mutable state trực tiếp.

### Data parallel / SIMD / GPU
Tốt cho numerical workloads.

Không có model nào thắng tuyệt đối; phải chọn theo workload và team skill.

---

## 7. Performance thinking

Thêm nhiều workers không bảo đảm tốc độ tăng tuyến tính.

Các bottlenecks thường gặp:
- lock contention
- work imbalance
- false sharing
- memory bandwidth
- serialized hot path nhỏ nhưng quá quan trọng

Hãy nhớ Amdahl's law: nếu một phần đáng kể của chương trình vẫn phải chạy tuần tự, speedup tối đa bị chặn rất mạnh.

---

## 8. Async I/O không phải phép màu

Async có thể giảm số thread cần dùng và tận dụng I/O wait tốt hơn, nhưng nó không tự sửa:
- race ở shared caches/maps
- backpressure
- cancellation bugs
- CPU-bound task làm nghẽn event loop

---

## 9. Ví dụ tư duy thiết kế

Giả sử bạn xây một queue consumer:
- nếu nhiều workers cùng cập nhật shared counter và shared map state, bạn cần synchronization rõ ràng
- nếu workers xử lý độc lập và chỉ publish results qua queue khác, reasoning đơn giản hơn nhiều

Thông điệp: thiết kế ownership của state quan trọng ngang primitive bạn chọn.

---

## 10. Checklist sau bài
- Giải thích được concurrency khác parallelism
- Nhận diện được race, deadlock, starvation, livelock
- Biết mutex, semaphore, atomic dùng lúc nào
- Hiểu vì sao memory ordering quan trọng
- Biết async I/O hợp và không hợp với loại workload nào

## 11. Bài tập thực hành
1. Viết producer-consumer queue nhỏ.
2. Tự tạo một ví dụ deadlock và sửa nó.
3. So sánh thread pool và async I/O cho một bài web scraping giả định.
4. Tóm tắt Amdahl's law bằng ví dụ số.
5. Viết checklist debug concurrency bug.

## 12. Mini deliverable
Tạo file `concurrency_design_principles.md` gồm:
- ownership of state
- synchronization rules
- timeout/cancellation rules
- logging/metrics tối thiểu cho concurrent components

## 13. Học tiếp
- `Bai_10_Computer_Networks_Full_Lesson.md`
- `../../08_Reference_and_Review/04_Systems_Deep_Dive.md`