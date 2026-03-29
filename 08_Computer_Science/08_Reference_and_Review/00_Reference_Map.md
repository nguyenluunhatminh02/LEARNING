# Computer Science Reference Map

## Mục đích của thư mục này
Thư mục `08_Reference_and_Review` là lớp mở rộng cho track `08_Computer_Science`.

20 bài chính ở các phần trước đóng vai trò:
- cho bạn bức tranh lớn
- làm checklist học tuần tự
- giúp bạn không lạc trong rừng chủ đề

Các file trong thư mục này đóng vai trò:
- đào sâu khái niệm và thuật ngữ
- hệ thống hóa câu hỏi tự kiểm tra
- cung cấp study plan dài hạn
- gợi ý lab, mini project và reading sequence

Nếu 20 bài chính là "roadmap", thì thư mục này là "workbook + handbook + oral exam prep".

---

## Cách dùng hợp lý

### Cách 1: Học tuần tự
1. Đọc một bài chính trong `01_...` đến `07_...`
2. Mở file deep dive tương ứng trong `08_Reference_and_Review`
3. Tự trả lời câu hỏi trong phần self-check
4. Làm 1 bài lab hoặc 1 mini note
5. Cuối tuần quay lại glossary để đảm bảo hiểu đúng thuật ngữ

### Cách 2: Ôn phỏng vấn hoặc review nền tảng
1. Đọc `01_Core_Glossary.md`
2. Chọn một phần cần ôn sâu, ví dụ systems hoặc databases
3. Dùng deep dive file như question bank mở rộng
4. Viết lại câu trả lời bằng lời của chính bạn
5. So sánh với code/project bạn đang làm

### Cách 3: Chuẩn bị cho capstone
1. Chọn capstone ở `Bai_20`
2. Dùng reference map để xác định kiến thức nền cần ôn
3. Tạo checklist implementation + benchmark + failure analysis
4. Chỉ bắt đầu code sau khi đã rõ constraints và trade-offs

---

## Bản đồ liên kết giữa các phần

### Foundations
Liên kết mạnh tới:
- Algorithms and Data
- Programming Languages
- Theory of Computation
- AI/ML foundations

### Algorithms and Data
Liên kết mạnh tới:
- Databases
- Search engines
- Distributed systems
- Systems performance

### Systems
Liên kết mạnh tới:
- Backend engineering
- Cloud/Kubernetes
- Operating databases in production
- Performance debugging

### Data and Storage
Liên kết mạnh tới:
- Backend systems
- Analytics/data engineering
- Search and retrieval
- AI retrieval systems

### Languages and Tools
Liên kết mạnh tới:
- Tooling/compilers
- Runtime behavior
- Performance tuning
- Cross-language systems

### Software and Security
Liên kết mạnh tới:
- Production readiness
- Compliance and trust boundaries
- Secure architecture
- Reliability and delivery

### Theory and Specialized
Liên kết mạnh tới:
- Research papers
- Hard optimization problems
- PL/compilers
- Advanced specialization choices

---

## Mức độ nắm kiến thức nên phân tầng

### Tầng 1: Recognition
Bạn nhận ra thuật ngữ khi đọc tài liệu và biết nó thuộc phần nào.

### Tầng 2: Explanation
Bạn giải thích được khái niệm bằng lời đơn giản, không lệ thuộc textbook wording.

### Tầng 3: Application
Bạn dùng kiến thức đó để viết code, debug hoặc thiết kế một thành phần thật.

### Tầng 4: Trade-off reasoning
Bạn biết khi nào nên chọn A thay vì B và hậu quả của lựa chọn đó.

### Tầng 5: Synthesis
Bạn nối nhiều mảng với nhau, ví dụ:
- cache + concurrency + consistency
- GC + container limits + latency
- index + workload + execution plan

---

## Mẫu học cho mỗi chủ đề

```text
Bước 1: Nhìn khái niệm và định nghĩa ngắn
Bước 2: Vẽ sơ đồ hoặc mental model
Bước 3: Làm 1 ví dụ nhỏ hoặc trace execution bằng tay
Bước 4: So sánh với 1-2 khái niệm gần giống để tránh nhầm
Bước 5: Làm 3 câu hỏi tự kiểm tra
Bước 6: Gắn khái niệm với project hoặc incident thực tế
```

---

## Bảng ưu tiên theo mục tiêu nghề nghiệp

### Nếu mục tiêu là Backend Engineer
Ưu tiên rất cao:
- Systems
- Data and Storage
- Software and Security
- Networks
- Concurrency

Ưu tiên cao vừa:
- Algorithms and Data
- Programming Languages

### Nếu mục tiêu là Systems/Performance Engineer
Ưu tiên rất cao:
- Computer Organization
- Operating Systems
- Concurrency and Parallelism
- Storage Engines
- Compilers and Runtimes

### Nếu mục tiêu là Staff/Principal
Ưu tiên rất cao:
- Distributed Systems
- Data and Storage
- Software Engineering
- Security
- Review, research and capstones

### Nếu mục tiêu là AI/ML Engineer nền tảng mạnh
Ưu tiên rất cao:
- Math for CS
- Programming fundamentals
- Algorithms
- Systems
- Data and Storage
- Programming Languages / runtimes

---

## Mẫu note sau mỗi tuần

```text
Chủ đề học:
3 điều đã hiểu rõ:
3 điểm còn mơ hồ:
1 bug hoặc failure mode đáng nhớ:
1 project/lab nên làm tiếp:
1 câu hỏi muốn đào sâu tuần sau:
```

---

## Mẫu oral exam tự luyện

Tự bấm thời gian 3-5 phút và trả lời không nhìn tài liệu:

- Giải thích process khác thread thế nào.
- Vì sao hash map thường nhanh nhưng không miễn phí.
- Vì sao retry có thể làm outage nặng hơn.
- B-Tree và LSM-tree khác nhau ở đâu.
- Static typing và dynamic typing đánh đổi điều gì.
- Tại sao NP-hard không đồng nghĩa là vô dụng trong thực tế.

Nếu nói ấp úng hoặc lan man, nghĩa là bạn chưa nắm thật chắc.

---

## Mẫu mini project theo phần

### Foundations
- viết parser expression nhỏ
- viết note chứng minh một thuật toán

### Algorithms and Data
- implement LRU, heap, trie, union-find

### Systems
- mini HTTP server, thread pool, event loop demo

### Data and Storage
- mini KV store, index demo, query benchmark

### Languages and Tools
- lexer/parser mini, AST visitor, bytecode toy VM

### Software and Security
- API với auth, tests, metrics, threat model

### Theory and Specialized
- DFA parser toy, SAT-style reasoning note, paper summary

---

## Cách đánh giá đã hiểu hay chưa

Một chủ đề chỉ được coi là "thật sự hiểu" khi bạn làm được cả 4 việc sau:

1. Định nghĩa đúng bằng ngôn ngữ của bạn.
2. Cho ví dụ đúng và phản ví dụ đúng.
3. So sánh được với khái niệm gần giống.
4. Nêu được ít nhất một trade-off hoặc failure mode.

---

## Trình tự khuyến nghị khi đào sâu

```text
Math / Programming / Computer Organization
  -> Complexity / Data Structures / Paradigms
  -> Operating Systems / Concurrency / Networks
  -> Distributed Systems / Databases / Storage
  -> Languages / Runtimes / Security / Software Engineering
  -> Theory / Research / Specialized tracks / Capstones
```

---

## Tài liệu trong thư mục này

- `01_Core_Glossary.md`
- `02_Foundations_Deep_Dive.md`
- `03_Algorithms_and_Data_Deep_Dive.md`
- `04_Systems_Deep_Dive.md`
- Các file tiếp theo sẽ bám cùng format cho những phần còn lại

---

## Ghi chú quan trọng
Mục tiêu của phần mở rộng này không phải là nhét thật nhiều chữ, mà là tăng mật độ kiến thức có thể dùng. Khi một file quá dài, hãy đọc theo mục tiêu cụ thể thay vì đọc tuyến tính từ trên xuống.