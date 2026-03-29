# Bài 03: Computer Organization

## 🎯 Mục tiêu
- Hiểu máy tính lưu dữ liệu và thực thi lệnh như thế nào
- Nắm CPU, bộ nhớ, cache, bus, I/O và hệ quả của chúng tới performance
- Xây mental model để sau này học OS, database, compiler và performance tuning dễ hơn

## 📖 Bức tranh lớn
Nếu bạn không hiểu máy tính bên dưới, rất khó lý giải vì sao một đoạn code đơn giản lại chậm, vì sao cache miss làm latency tăng mạnh, vì sao memory layout ảnh hưởng lớn đến throughput, hoặc vì sao concurrency bug lại khó đoán. Computer Organization là cầu nối giữa code và phần cứng.

---

## 1. Dữ liệu được biểu diễn như thế nào

### Chủ đề cần nắm
- Binary, hexadecimal
- Signed/unsigned integer
- Two's complement
- Floating point cơ bản
- ASCII, Unicode, UTF-8, UTF-16

### Ứng dụng thực tế
- Overflow/underflow
- Serialization/deserialization
- Encoding bugs khi xử lý text đa ngôn ngữ
- So sánh số thực và sai số tính toán

---

## 2. CPU và instruction execution

### Thành phần chính
- Program counter
- Registers
- ALU
- Control unit
- Instruction decoder

### Chu trình cơ bản
```text
Fetch instruction -> Decode -> Execute -> Memory access -> Write back
```

### Chủ đề nên biết
- ISA là gì
- Assembly ở mức đọc hiểu cơ bản
- Function call, stack frame, return address
- Branch prediction và pipeline ở mức trực giác

---

## 3. Memory hierarchy

### Các tầng bộ nhớ
```text
Registers -> L1/L2/L3 Cache -> RAM -> SSD/HDD -> Network/Remote storage
```

### Ý nghĩa thực tế
- Càng gần CPU càng nhanh và nhỏ
- Cache locality quyết định performance của nhiều chương trình
- Sequential access thường thân thiện cache hơn random access

### Các khái niệm phải hiểu
- Cache hit vs miss
- Temporal locality
- Spatial locality
- Page và page fault ở mức chuẩn bị cho OS

---

## 4. Bộ nhớ, địa chỉ và layout dữ liệu

### Chủ đề cần nắm
- Address space
- Pointer/reference ở mức khái niệm
- Stack memory vs heap memory
- Struct/class layout ảnh hưởng cache thế nào
- Alignment và padding cơ bản

### Hệ quả thực tế
- Object nhỏ nhưng phân tán khắp heap có thể chậm hơn array liên tục trong memory
- Linked list thường tệ hơn array trên CPU hiện đại ở nhiều workload vì locality kém

---

## 5. I/O, interrupts và DMA

### Chủ đề cần nắm
- Polling vs interrupt
- Disk I/O, network I/O
- DMA là gì
- System call là cầu nối từ user space sang kernel space

### Tại sao quan trọng
- Phần lớn ứng dụng production không chỉ CPU-bound mà còn I/O-bound
- Hiểu I/O giúp bạn lý giải blocking, async, buffering và batching

---

## 6. Hiệu năng nhìn từ phần cứng

### Các bottleneck thường gặp
- Cache miss
- Branch misprediction
- Memory bandwidth limit
- False sharing trong concurrency
- Disk seek hoặc random I/O

### Quy tắc thực dụng
- Đừng tối ưu mù; hãy đo trước.
- Big-O tốt chưa chắc chạy nhanh nếu layout memory tệ.
- Batching, streaming và data locality thường đem lại cải thiện lớn.

---

## 7. Kết nối với các môn tiếp theo

- OS: virtual memory, scheduling, interrupt handling
- Databases: page, buffer pool, storage engine, WAL
- Compilers: code generation, calling convention
- Concurrency: cache coherence, atomic operations, memory ordering
- Performance engineering: profiling CPU/cache/memory

---

## ✅ Checklist ôn tập
- Giải thích được vì sao máy tính dùng binary và two's complement
- Biết khác biệt cơ bản giữa stack và heap
- Mô tả được memory hierarchy và vì sao cache quan trọng
- Giải thích được function call sử dụng stack frame thế nào
- Nêu được ít nhất 3 nguyên nhân phần cứng làm chương trình chậm

## 📝 Bài tập
1. Chuyển đổi qua lại giữa decimal, binary và hex cho vài số ví dụ.
2. Tự giải thích vì sao duyệt array thường nhanh hơn linked list.
3. Đọc một đoạn assembly đơn giản của hàm cộng/loop.
4. Viết note 1 trang về memory hierarchy.
5. Tìm một ví dụ bug do encoding UTF-8/Unicode và giải thích nguyên nhân.

## 📚 Tài liệu
- *Computer Systems: A Programmer's Perspective* — Bryant & O'Hallaron
- *Code: The Hidden Language of Computer Hardware and Software* — Charles Petzold
- *Computer Organization and Design* — Patterson & Hennessy