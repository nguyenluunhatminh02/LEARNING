# Bài 08: Operating Systems — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- hiểu operating system là lớp quản lý tài nguyên và cô lập chương trình như thế nào
- nắm process, thread, virtual memory, file systems, I/O và containers ở mức engineer
- có framework để reasoning về memory issues, system calls, blocking và resource limits

## Bạn cần biết trước
- Bài 03 là nền rất hữu ích
- nên đã học xong phần algorithms cơ bản

---

## 1. Operating System thực sự làm gì

OS không chỉ là "một phần mềm trung gian". Nó chịu trách nhiệm cho nhiều thứ cốt lõi:
- quản lý CPU time
- quản lý memory
- quản lý file và thiết bị I/O
- bảo vệ process này khỏi process khác
- cung cấp abstractions như files, processes, sockets, virtual memory

Nếu không có OS, mỗi chương trình phải tự xử lý hardware details ở mức rất thấp.

---

## 2. Processes và threads

### Process
- có address space riêng
- có file descriptors, environment, process state riêng
- cách ly tốt hơn

### Thread
- chia sẻ address space với thread khác trong cùng process
- nhẹ hơn process
- giao tiếp nhanh hơn nhưng dễ sinh race hơn

### Khi reasoning một service
Hãy luôn biết:
- một request đang chạy ở process nào
- có bao nhiêu threads/workers
- tài nguyên nào chia sẻ giữa chúng

---

## 3. System calls và user/kernel mode

Application code thường chạy ở user mode.

Khi cần:
- đọc file
- mở socket
- cấp phát một số vùng nhớ đặc biệt
- spawn process

thì phải đi qua system call vào kernel mode.

Ý nghĩa thực tế:
- system call có cost
- context switch có cost
- nhiều abstraction tiện lợi cuối cùng vẫn dựa trên những primitive này

---

## 4. Scheduling

OS phải quyết định ai được CPU và khi nào.

### Một số mục tiêu thường phải cân bằng
- throughput
- latency
- fairness
- responsiveness

### Điều engineer cần hiểu
- CPU-bound tasks và I/O-bound tasks tạo pressure rất khác nhau
- quá nhiều threads có thể làm scheduler và cache locality tệ đi
- tail latency có thể tăng vì queueing và contention chứ không chỉ vì compute time

---

## 5. Virtual memory

Virtual memory giúp mỗi process có cảm giác như có không gian địa chỉ riêng, liên tục và an toàn hơn.

Bạn nên hiểu các khái niệm sau ở mức trực giác:
- pages
- page tables
- TLB
- page faults
- swapping

### Tại sao quan trọng
- app chậm bất thường đôi khi là vì page faults
- memory "dùng nhiều" có thể không đồng nghĩa với memory thật sự resident trong RAM
- containers và cgroups làm pressure memory càng đáng chú ý hơn

---

## 6. File systems và durability

OS cho bạn abstraction file, nhưng phía dưới là storage với cost và constraints thật.

### Khái niệm nên nắm
- inode, metadata
- page cache
- buffered I/O
- `fsync`
- journaling

### Điểm rất thực tế
Một write thành công ở app không đồng nghĩa dữ liệu đã bền xuống disk ngay.

Đây là lý do databases dùng WAL và gọi `fsync`/sync points cẩn thận.

---

## 7. I/O model

### Blocking I/O
Thread chờ tới khi thao tác hoàn tất.

### Non-blocking I/O
Thread không cần đứng yên đợi toàn bộ thao tác.

### Event-driven I/O
Dựa trên polling mechanisms như `epoll`/`kqueue` để quản lý nhiều I/O sources hiệu quả hơn.

Bạn không cần thuộc hết API hệ điều hành, nhưng nên hiểu tại sao chúng tồn tại.

---

## 8. Containers và virtualization

### Containers
- dựa trên namespaces và cgroups
- chia sẻ kernel
- nhẹ hơn VM

### Virtual Machines
- cách ly mạnh hơn
- có hypervisor
- cost cao hơn nhưng boundary rõ hơn

### Tư duy production
Ứng dụng chạy tốt trên máy local chưa chắc chạy tốt trong container khi:
- memory limit nhỏ hơn
- CPU quota bị giới hạn
- file descriptors bị chặn thấp

---

## 9. Các vấn đề OS-level thường gặp
- OOM killer
- file descriptor leak
- thread explosion
- disk full hoặc inode full
- permission mismatch
- clock skew
- CPU throttling

---

## 10. Checklist sau bài
- Giải thích được process, thread, system call, context switch
- Hiểu virtual memory ở mức đủ để không mù khi gặp OOM/page faults
- Biết vì sao page cache và `fsync` quan trọng
- Nắm blocking vs non-blocking I/O
- Hiểu container dựa trên primitive nào của OS

## 11. Bài tập thực hành
1. Vẽ sơ đồ process/thread/file descriptors của một web service đơn giản.
2. Viết note giải thích OOM killer.
3. Tự mô tả khi nào nên dùng thread pool, process pool hoặc event loop.
4. Tìm hiểu `ulimit` và liệt kê 5 giới hạn OS hay gặp.
5. Viết 1 trang về page cache và durability.

## 12. Mini deliverable
Tạo file `os_debugging_checklist.md` gồm:
- memory symptoms
- CPU symptoms
- file descriptor symptoms
- disk symptoms
- command/checkpoint điều tra cơ bản

## 13. Học tiếp
- `Bai_09_Concurrency_and_Parallelism_Full_Lesson.md`
- `../../08_Reference_and_Review/04_Systems_Deep_Dive.md`