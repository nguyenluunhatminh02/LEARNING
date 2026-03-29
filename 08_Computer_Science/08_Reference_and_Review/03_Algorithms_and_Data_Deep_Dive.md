# Algorithms and Data Deep Dive

## Mục tiêu của file này
File này đào sâu cho các bài:
- Complexity and Problem Solving
- Core Data Structures
- Algorithmic Paradigms
- Advanced Algorithms

Mục tiêu là biến việc học thuật toán từ "luyện đề" thành năng lực mô hình hóa và reasoning bền vững.

---

## 1. Học algorithms đúng cách

Sai cách phổ biến nhất là:
- nhớ solution theo pattern bề mặt
- không hiểu vì sao solution đúng
- không biết khi nào pattern đó không còn áp dụng

Học đúng hơn là:
- nhận diện structure của bài toán
- viết brute force baseline
- xác định bottleneck
- chọn representation phù hợp
- chứng minh invariant hoặc optimality
- phân tích complexity và edge cases

---

## 2. Complexity beyond Big-O slogans

### 2.1 Những câu hỏi phải luôn tự hỏi
- Input size thật là gì?
- Có nhiều biến kích thước không, ví dụ `n` và `m`?
- Time complexity có ẩn trong library call không?
- Space complexity có gồm recursion stack không?
- Worst case hay average case mới quan trọng với workload này?

### 2.2 Constant factors và cache effects

Trong production và benchmark thật:
- constant factors matters
- allocations matters
- branch patterns matters
- locality matters

Bạn không được bỏ asymptotics, nhưng cũng không được dùng nó như vũ khí duy nhất.

### 2.3 Amortized analysis nên nắm ở mức nào

Ít nhất bạn nên giải thích được:
- dynamic array append
- hash table resize
- union-find với path compression

Nếu chưa giải thích được, phần intuition về data structure vẫn còn chưa chắc.

---

## 3. Deep dive theo nhóm data structure

### 3.1 Array và dynamic array

Điểm mạnh:
- locality tốt
- random access `O(1)`
- scan rất nhanh

Điểm yếu:
- insert/delete giữa mảng đắt
- resize có cost spike

Khi nào cực đáng dùng:
- hot path cần scan hoặc random access
- workloads thiên về append + read

### 3.2 Linked list

Điểm bạn phải nhớ:
- bài học lớn nhất của linked list là hiểu pointer/reference, không phải vì nó luôn hữu ích trong production
- rất nhiều trường hợp array tốt hơn linked list dù complexity lý thuyết trông không chênh lệch nhiều

### 3.3 Hash map

Đào sâu vào:
- hash quality
- collision resolution
- resizing
- iteration order
- memory overhead

Các câu hỏi review:
- vì sao hash map lookup có thể chậm bất thường?
- key mutable nguy hiểm ra sao?
- khi nào tree map tốt hơn hash map?

### 3.4 Trees và ordered structures

Phải phân biệt:
- binary tree
- BST
- balanced BST
- heap
- B-Tree family
- trie

Nhiều người mới học hay gom chúng vào một nhóm mơ hồ là "cây" rồi mất đi intuition quan trọng.

### 3.5 Graph representations

Nắm:
- adjacency list
- adjacency matrix
- edge list

Câu hỏi thực dụng:
- graph có sparse hay dense?
- query chủ yếu là traversal hay edge existence?
- có cần weighted edges không?

---

## 4. Problem-solving workflow chi tiết

### Bước 1: restate the problem
Tự nói lại bằng lời ngắn gọn:
- input là gì
- output là gì
- constraint mạnh nhất là gì
- điều gì bắt buộc đúng

### Bước 2: build examples
Không chỉ một ví dụ happy path. Hãy thêm:
- empty input
- duplicate values
- already sorted / reverse sorted
- max constraint style input

### Bước 3: write brute force
Brute force cho bạn:
- baseline correctness
- cách kiểm thử lời giải tối ưu
- insight về bottleneck

### Bước 4: optimize intentionally
Tối ưu phải trả lời được:
- ta đang giảm bước nào?
- ta đang thêm memory hay preprocessing gì?
- assumption mới là gì?

### Bước 5: prove and test
Nếu không thể giải thích vì sao lời giải đúng, bạn chỉ đang hy vọng.

---

## 5. Deep dive cho major paradigms

### 5.1 Two pointers và sliding window

Điều kiện nên nghĩ tới:
- mảng hoặc chuỗi
- tính chất ordered hoặc monotonic nào đó
- cửa sổ cần mở rộng và co lại theo điều kiện

Sai lầm hay gặp:
- không xác định rõ invariant của window
- xử lý duplicates sai
- update answer sai thời điểm

### 5.2 Divide and conquer

Phải tự hỏi:
- chia theo đâu là tự nhiên nhất?
- combine step tốn bao nhiêu?
- subproblem có độc lập đủ không?

### 5.3 Greedy

Khi thấy greedy hấp dẫn, hãy ép bản thân làm 1 trong 2 việc:
- tìm exchange argument
- hoặc cố tình săn counterexample

Nếu làm được một trong hai, bạn đang học đúng.

### 5.4 Dynamic programming

Quy trình cần luyện thành phản xạ:
- state là gì
- transition là gì
- base cases là gì
- dimension nào thật sự cần thiết
- có thể nén memory không

Sai lầm thường gặp:
- state thừa biến
- state thiếu biến
- nhảy vào code trước khi viết transition trên giấy

### 5.5 Graph algorithms

Phải nắm rất chắc:
- BFS cho shortest path unweighted
- DFS cho traversal, cycle detection, topo, components
- Dijkstra cho weighted non-negative
- Union-find cho connectivity

Sau đó mới đến:
- Bellman-Ford
- Floyd-Warshall
- MST
- max flow/matching overview

---

## 6. Advanced algorithms should not be mysterious

Bạn không cần master mọi advanced topic ngay, nhưng ít nhất phải biết chúng tồn tại để chọn đúng khi gặp vấn đề phù hợp.

### String algorithms
Đáng học khi:
- search nhiều patterns
- prefix/suffix matters
- parsing/tokenization nặng

### Range query structures
Đáng học khi:
- nhiều query trên mảng cố định hoặc gần cố định
- update/query xen kẽ

### Approximate/streaming structures
Đáng học khi:
- data quá lớn
- exact answer đắt
- cardinality/frequency/approx membership là đủ

### System algorithms
Đáng học khi:
- xây cache
- phân mảnh dữ liệu
- load balancing
- distributed coordination

---

## 7. Mistake catalog

### Mistake 1: Nhầm representation
Ví dụ:
- dùng list cho exact lookup thay vì hash set
- dùng recursion sâu không cần thiết trên input rất lớn

### Mistake 2: Nhầm complexity due to hidden work
Ví dụ:
- slice string/array trong loop tưởng là `O(1)`
- sort lặp đi lặp lại trong subroutine

### Mistake 3: Overfit template
Ví dụ:
- thấy substring là auto sliding window dù bài không có monotonic property
- thấy shortest path là auto Dijkstra dù graph unweighted

### Mistake 4: Ignore invariants
Triệu chứng:
- code chạy đúng vài test đầu rồi chết ở edge cases

### Mistake 5: No failure thinking
Ví dụ:
- chia cho 0, overflow, empty graph, disconnected graph, duplicate nodes, negative weights

---

## 8. What to know cold

Bạn nên biết cold:
- arrays vs linked lists vs hash maps vs heaps vs trees vs graphs
- BFS vs DFS vs Dijkstra
- greedy vs DP
- brute force vs optimized with preprocessing
- worst case vs amortized
- topological sort, union-find, prefix sums, binary search on answer

---

## 9. Suggested weekly deep practice

### Tuần A: Complexity and reasoning
- phân tích 5 snippets code
- viết invariant cho 3 algorithms
- giải thích amortized analysis cho 2 structures

### Tuần B: Data structures
- implement 2 structures from scratch
- benchmark nhẹ hoặc so sánh reasoning-based
- viết 1 bảng use cases

### Tuần C: Paradigms
- chọn 12 bài và phân loại paradigm
- viết template riêng cho BFS, DFS, DP, backtracking, binary search on answer

### Tuần D: Advanced topics
- chọn 1 nhánh: string, range query, streaming, system algorithms
- đọc sâu và làm 1 mini implementation

---

## 10. Self-check questions

### Complexity
- Vì sao `O(n log n)` không luôn chậm hơn `O(n)` trong thực tế?
- Khi nào amortized analysis là mô hình đúng để dùng?

### Data structures
- Vì sao hash map có thể không phù hợp cho ordered iteration?
- Vì sao B-Tree khác balanced BST trong bối cảnh storage?

### Paradigms
- Làm sao biết một bài có optimal substructure?
- Khi nào binary search on answer áp dụng được?
- Tại sao greedy cần proof đặc biệt?

### Graph mindset
- Bài toán nào trông không giống graph nhưng thực ra là graph?
- Khi nào connectivity query nên nghĩ ngay đến union-find?

---

## 11. Practical labs

### Lab 1: LRU cache
Implement LRU để học:
- hash map + doubly linked list
- invariants giữa 2 cấu trúc phối hợp
- complexity reasoning

### Lab 2: Shortest path notebook
Tự mô tả bằng tay BFS và Dijkstra trên cùng graph.

### Lab 3: DP journal
Mỗi bài DP phải ghi:
- state
- transition
- base cases
- traversal order
- optimized memory version nếu có

### Lab 4: Streaming structures
Đọc Bloom Filter hoặc HyperLogLog và viết summary 1 trang.

---

## 12. Reading map

### Cốt lõi
- CLRS hoặc Kleinberg & Tardos
- NeetCode/LeetCode chỉ như practice layer, không thay thế lý thuyết

### Nâng cao
- *The Algorithm Design Manual*
- *Algorithms* của DPV
- *Mining of Massive Datasets*

---

## 13. Dấu hiệu bạn đã khá vững

Bạn khá vững khi:
- thấy bài mới nhưng vẫn mô hình hóa được
- ít bị lệ thuộc keyword-template
- phân tích được complexity và failure cases trong vài phút
- giải thích được vì sao một lời giải đúng, không chỉ là code chạy qua test

---

## 14. Cảnh báo cuối
Đừng biến algorithms thành môn học chỉ để thi. Đây là ngôn ngữ tư duy chung của software engineering, databases, search, networking, distributed systems và AI. Nếu học tốt, bạn sẽ nhìn thấy cấu trúc của vấn đề nhanh hơn người khác.