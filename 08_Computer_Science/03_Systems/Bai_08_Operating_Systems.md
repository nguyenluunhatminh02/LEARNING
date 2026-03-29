# Bài 08: Operating Systems

## 🎯 Mục tiêu
- Hiểu OS là lớp trung gian quản lý tài nguyên giữa phần cứng và chương trình
- Nắm process, thread, scheduling, virtual memory, file systems, I/O và IPC
- Có mental model đủ tốt để debug performance, deadlock, memory issue và deployment behavior

## 📖 Bức tranh lớn
Operating System là bộ luật của máy tính. Nó quyết định tiến trình nào được CPU, bộ nhớ nào hợp lệ, file nào được mở, socket nào được giao tiếp và khi nào chương trình bị block. Không hiểu OS thì rất khó giải thích vì sao service treo, latency tăng, memory phình, hay một container bị kill.

---

## 1. Process, thread và execution model

### Process
- Có address space riêng
- Isolated hơn
- IPC cần cơ chế rõ ràng

### Thread
- Chia sẻ cùng address space trong một process
- Giao tiếp nhanh hơn
- Dễ sinh race condition hơn

### Phải nắm
- Program vs process vs thread
- User mode vs kernel mode
- System call là gì
- Context switch tốn chi phí ra sao

---

## 2. CPU scheduling

### Các ý chính
- Preemptive vs non-preemptive scheduling
- Time slicing
- Priority scheduling
- Round-robin
- Throughput, latency, fairness

### Trực giác thực tế
- CPU-bound task khác I/O-bound task
- Quá nhiều thread có thể làm context switching overhead tăng mạnh
- Tail latency thường chịu ảnh hưởng của contention và scheduling delay

---

## 3. Memory management

### Chủ đề cần nắm
- Virtual memory
- Page, page table, TLB ở mức trực giác
- Stack vs heap
- Allocation/free, fragmentation
- Page fault, swapping

### Vì sao quan trọng
- Service có thể chậm hoặc crash do memory pressure
- Một chương trình dùng ít CPU nhưng vẫn rất chậm vì page faults nặng
- Hiểu memory giúp bạn lý giải OOM, memory leak, mmap, shared memory

---

## 4. File systems và storage interface

### Chủ đề cần nắm
- File, inode, directory, metadata
- Buffer cache / page cache
- Sequential vs random I/O
- Durability, fsync, journaling
- SSD vs HDD vs network storage

### Liên kết tới database
- WAL, compaction, checkpoints, buffer pool đều xây trên abstraction này

---

## 5. I/O và event handling

### Chủ đề cần nắm
- Blocking I/O vs non-blocking I/O
- Polling, interrupt, DMA ở mức trực giác
- select/poll/epoll/kqueue ở mức overview
- Signals
- Pipes, sockets, standard streams

### Ứng dụng
- Web server
- Background worker
- Log processing
- High-concurrency network service

---

## 6. IPC và synchronization ở mức OS

### Cơ chế thường gặp
- Pipes
- Shared memory
- Message queues
- Sockets
- Semaphores, mutexes, condition variables

### Câu hỏi cần biết
- Giao tiếp local process nào nhanh hơn?
- Chia sẻ memory có lợi gì và rủi ro gì?
- Khi nào dùng queue thay vì shared state?

---

## 7. Containers, virtualization và isolation

### Containers
- Process isolation bằng namespaces và cgroups
- Shared kernel
- Nhẹ hơn VM

### Virtual Machines
- Isolate mạnh hơn
- Có hypervisor
- Overhead cao hơn nhưng boundary rõ hơn

### Tại sao engineer nên biết
- Resource limits ảnh hưởng GC, thread pools, file descriptors, CPU quotas
- Một app chạy tốt local chưa chắc chạy tốt trong container/Kubernetes

---

## 8. Những lỗi production liên quan tới OS

- File descriptor leak
- OOM killer
- Disk full hoặc inode full
- Too many threads/processes
- Socket backlog cạn
- Time skew, clock issues
- Permission/ownership sai

---

## ✅ Checklist ôn tập
- Giải thích được process, thread, system call, context switch
- Mô tả được virtual memory và page fault ở mức đủ dùng
- Biết sự khác nhau giữa blocking I/O và event-driven I/O
- Hiểu page cache, fsync và vì sao durability không miễn phí
- Giải thích được container dựa trên những primitive nào của OS

## 📝 Bài tập
1. Tự vẽ sơ đồ process/thread/file descriptor/socket cho một web server đơn giản.
2. So sánh process pool và thread pool cho 3 loại workload.
3. Tìm hiểu OOM killer và viết note cách điều tra memory issue trên Linux.
4. Viết chương trình nhỏ đọc file lớn theo nhiều cách và so sánh thời gian.
5. Tự giải thích vì sao fsync quá nhiều có thể làm hệ thống chậm.

## 📚 Tài liệu
- *Operating Systems: Three Easy Pieces* — OSTEP
- *Modern Operating Systems* — Andrew Tanenbaum
- *Computer Systems: A Programmer's Perspective* — CSAPP