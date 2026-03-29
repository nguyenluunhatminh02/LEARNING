# Foundations Deep Dive

## Mục tiêu của file này
File này mở rộng cho 3 bài đầu:
- Math for Computer Science
- Programming Fundamentals
- Computer Organization

Mục tiêu không phải nhồi thêm textbook, mà là giúp bạn biết phải đào sâu cái gì, đến mức nào, và kiểm tra hiểu biết của bản thân ra sao.

---

## 1. Foundations thực chất là gì

Foundations trong CS không chỉ là "học mấy định nghĩa cơ bản". Nó là ba lớp chồng lên nhau:

### Lớp 1: Formal thinking
Bạn phải đủ chính xác khi dùng ngôn ngữ, logic và assumptions.

### Lớp 2: Programming model
Bạn phải hiểu code thực sự thay đổi state thế nào, memory sống ra sao, lỗi xuất hiện do đâu.

### Lớp 3: Machine model
Bạn phải hiểu phần cứng, memory hierarchy và execution model ảnh hưởng đến performance và correctness ra sao.

Nếu thiếu một trong ba lớp này, kiến thức phía trên thường trở nên mong manh.

---

## 2. Deep dive cho Math for CS

### 2.1 Logic và proof

Bạn nên nắm thật chắc:
- proposition và predicate
- implication vs equivalence
- direct proof
- contradiction
- contrapositive
- induction
- loop invariants

Bạn nên tự trả lời được:
- tại sao `P -> Q` không giống `Q -> P`
- tại sao chỉ cần một phản ví dụ là đủ bác bỏ phát biểu `for all`
- tại sao induction là một mô hình reasoning cực quan trọng cho recursion và loops

Sai lầm hay gặp:
- dùng từ ngữ đời thường mơ hồ thay cho phát biểu logic rõ ràng
- chứng minh bằng ví dụ thay vì chứng minh tổng quát
- viết code binary search nhưng không có invariant trong đầu

### 2.2 Sets, functions, relations

Phải hiểu:
- union, intersection, difference
- relation và equivalence classes
- partial order
- injective/surjective/bijective

Liên hệ thực tế:
- partial order -> dependency graph
- equivalence classes -> grouping/clustering/union-find
- function composition -> pipeline transforms

### 2.3 Counting và probability

Đào sâu vừa đủ vào:
- permutations và combinations
- inclusion-exclusion
- conditional probability
- expectation
- variance
- binomial và normal intuition

Liên hệ engineering:
- false positive rate
- retry success probability
- load distribution
- reliability of replicated components

### 2.4 Graph thinking as math

Bạn nên coi graph như một ngôn ngữ chung của nhiều bài toán:
- dependencies
- route planning
- workflow engines
- build systems
- access control relationships

---

## 3. Deep dive cho Programming Fundamentals

### 3.1 Value model

Hãy thật chắc các câu hỏi sau:
- assignment có copy dữ liệu hay chỉ copy reference?
- function nhận object rồi sửa object đó thì caller thấy gì?
- khi nào mutation là hợp lý, khi nào immutability an toàn hơn?

### 3.2 Control flow and state transitions

Bạn nên học cách nhìn chương trình như một state machine nhỏ:
- mỗi branch thay đổi tập trạng thái có thể xảy ra
- mỗi loop phải có progress condition
- mỗi exception path là một nhánh behavior cần nghĩ tới

### 3.3 Recursion vs iteration

Không nên học recursion chỉ như một mẹo phỏng vấn.

Phải hiểu:
- base case
- recursive case
- stack growth
- relation giữa recursion tree và complexity
- tail recursion chỉ là optimization trong một số runtimes, không phải phép màu phổ quát

### 3.4 Debugging discipline

Một cách debug trưởng thành thường có dạng:
1. Reproduce reliably.
2. Reduce the case.
3. State expected vs actual.
4. Check invariants.
5. Confirm root cause.
6. Add test if phù hợp.

Anti-patterns:
- sửa nhiều chỗ cùng lúc
- thêm log vô tội vạ mà không có hypothesis
- tin vào cảm giác thay vì đo

### 3.5 Code structure

Bạn nên luyện những điều rất cơ bản nhưng cực quan trọng:
- function naming
- module boundaries
- input/output contracts
- error propagation
- avoiding hidden dependencies

---

## 4. Deep dive cho Computer Organization

### 4.1 Representation matters

Phải nhớ:
- integer overflow là hiện tượng rất thật, không phải chi tiết nhỏ
- floating point không biểu diễn mọi số thập phân chính xác
- encoding bugs thường đến từ assumption sai về text, bytes và locale

### 4.2 CPU pipeline intuition

Không cần thành hardware engineer, nhưng nên hiểu:
- CPU không chạy source code, nó chạy instructions
- instructions cần data trong registers/cache/memory
- branch prediction và pipeline stalls ảnh hưởng performance

### 4.3 Memory hierarchy intuition

Một trong những mental models đáng giá nhất:
- data layout tốt thường quan trọng ngang với Big-O ở scale vừa và lớn
- tuần tự hóa access pattern thường thân thiện cache hơn pointer chasing
- locality không phải detail nhỏ; nó là nguồn gốc của nhiều cải thiện performance lớn

### 4.4 I/O cost model

Bạn cần internalize rằng:
- RAM nhanh hơn disk rất nhiều
- network còn thêm latency, packetization và failure
- syscall cũng có cost
- batch, buffer và async tồn tại vì cost model này

---

## 5. Những lỗ hổng nền tảng thường gặp

### Hổng kiểu 1: Biết syntax nhưng không biết model
Triệu chứng:
- viết code được nhưng không giải thích vì sao bug xảy ra
- khó debug mutation/reference issues

### Hổng kiểu 2: Biết công thức nhưng không biết ứng dụng
Triệu chứng:
- nhớ expectation/variance nhưng không áp dụng vào reliability hay experiments

### Hổng kiểu 3: Biết Big-O nhưng không biết hardware reality
Triệu chứng:
- đánh giá algorithm chỉ bằng asymptotic, không để ý locality, I/O và allocations

### Hổng kiểu 4: Viết code được nhưng không mô tả invariant
Triệu chứng:
- binary search, partition, sliding window dễ sai edge case

---

## 6. Những thứ nên biết "cold"

"Biết cold" nghĩa là có thể nói ngay không cần nghĩ quá lâu.

Bạn nên biết cold:
- difference giữa process, thread, function call, stack frame
- difference giữa value và reference
- difference giữa proof by contradiction và induction
- difference giữa cache, RAM, disk
- difference giữa ASCII, Unicode, UTF-8
- difference giữa recursion và iteration
- difference giữa asymptotic cost và actual runtime behavior

---

## 7. Study sequence đề xuất cho foundations

### Tuần 1
- logic, sets, functions
- value/reference, scope/lifetime

### Tuần 2
- induction, invariants, recursion
- stack/heap, memory model

### Tuần 3
- probability basics, graphs as modeling tool
- CPU, cache, memory hierarchy

### Tuần 4
- review toàn bộ bằng mini explanations và flashcards
- làm 1 mini project hoặc 1 long-form note

---

## 8. Self-check questions

### Nhóm khái niệm
- Vì sao induction phù hợp để reasoning về recursion?
- Khi nào một relation là partial order nhưng không phải total order?
- Vì sao linked list thường thua dynamic array về performance thực tế?
- Tại sao floating point dễ gây bug ở finance?

### Nhóm ứng dụng
- Nếu một bug chỉ xuất hiện khi danh sách rất dài, bạn nghi đầu tiên điều gì về complexity hoặc memory?
- Nếu text hiển thị sai tiếng Việt/tiếng Nhật, bạn sẽ kiểm tra encoding ở đâu?
- Nếu một loop chạy mãi, bạn diễn đạt missing invariant hoặc missing progress condition ra sao?

### Nhóm reasoning
- Hãy chứng minh một loop đơn giản là đúng.
- Hãy đưa phản ví dụ cho một phát biểu tổng quát do chính bạn tự đặt ra.
- Hãy mô tả stack frame của một hàm recursive sâu 4 mức.

---

## 9. Labs và mini exercises

### Lab 1: Memory behavior note
Viết một note 1-2 trang trả lời:
- stack là gì
- heap là gì
- vì sao local variable và heap object có lifecycle khác nhau

### Lab 2: Encoding lab
Tạo vài chuỗi Unicode và UTF-8 bytes, giải thích sự khác nhau giữa character count và byte count.

### Lab 3: Invariant lab
Chọn 3 thuật toán cơ bản và viết invariant cho từng cái.

### Lab 4: Cache intuition lab
So sánh duyệt array liên tục với pattern truy cập nhảy xa theo trực giác, không cần benchmark phức tạp.

---

## 10. Deliverables nên tạo cho bản thân

- 1 file flashcards logic/probability
- 1 note về value/reference và memory model
- 1 note về cache/memory hierarchy
- 1 bài giải thích recursion + induction
- 1 sơ đồ về execution của function call và stack frame

---

## 11. Khi nào coi foundations là đủ chắc

Bạn đủ chắc khi:
- đọc tài liệu algorithms không bị vấp vì proof notation
- debug mutation/reference bugs không hoảng loạn
- nói về cache, memory, I/O không còn thấy "mơ hồ"
- giải thích được code behavior bằng model bên dưới, không chỉ bằng mô tả bề mặt

---

## 12. Sách nên ưu tiên đọc theo thứ tự

1. *Mathematics for Computer Science* hoặc notes tương đương
2. *Code Complete* hoặc *The Pragmatic Programmer*
3. *Computer Systems: A Programmer's Perspective*
4. *Code* của Petzold nếu muốn trực giác phần cứng tốt hơn

---

## 13. Cảnh báo quan trọng
Đừng dành quá lâu để đọc foundations mà không viết gì. Sau mỗi nhóm khái niệm, bạn nên tạo ít nhất một artifact: note, code snippet, mini explanation, quiz, hoặc lab nhỏ. Nếu không, phần lớn kiến thức sẽ chỉ dừng ở recognition.