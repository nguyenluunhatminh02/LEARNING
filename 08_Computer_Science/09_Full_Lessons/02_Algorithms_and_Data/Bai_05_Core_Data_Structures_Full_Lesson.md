# Bài 05: Core Data Structures — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- nắm data structures cốt lõi và trade-off của từng loại
- biết chọn cấu trúc dữ liệu dựa trên access pattern, không chỉ theo thói quen
- hiểu vì sao representation quyết định rất lớn tới performance và độ đơn giản của lời giải

## Bạn cần biết trước
- đã học xong Bài 04

---

## 1. Vì sao data structure quan trọng hơn nhiều người nghĩ

Rất nhiều bài toán không cần thuật toán quá thông minh. Chỉ cần chọn đúng data structure, lời giải đã:
- ngắn hơn
- đúng hơn
- nhanh hơn

Chọn sai structure thường làm bạn phải "chữa cháy" bằng các if/else, loops thừa và logic khó hiểu.

---

## 2. Arrays và dynamic arrays

### Điểm mạnh
- random access `O(1)`
- locality tốt
- scan nhanh

### Điểm yếu
- chèn/xóa giữa mảng đắt
- resize có cost spike

### Khi nào nên dùng
- dữ liệu cần duyệt tuần tự
- cần truy cập theo index
- workload thiên về append + read

---

## 3. Linked lists

Linked list giúp bạn hiểu pointer/reference, nhưng trong thực tế hiện đại nó ít thắng array hơn bạn tưởng.

### Điểm mạnh
- insert/delete tại vị trí có sẵn node reference là `O(1)`

### Điểm yếu
- random access `O(n)`
- locality kém
- overhead pointer lớn

### Bài học lớn
Đừng chọn structure theo textbook complexity một cách máy móc.

---

## 4. Stacks, queues và deques

### Stack
Rất mạnh cho:
- recursion simulation
- parsing
- monotonic patterns

### Queue
Rất mạnh cho:
- BFS
- scheduling
- buffering

### Deque
Rất mạnh cho:
- sliding window tối ưu
- monotonic queue
- hai đầu push/pop linh hoạt

---

## 5. Hash maps và hash sets

### Ưu điểm
- lookup nhanh trung bình
- đếm tần suất tốt
- de-duplication tự nhiên
- memoization tiện

### Nhược điểm
- không giữ order mặc định
- memory overhead lớn hơn array
- collision và resize không miễn phí

### Câu hỏi nên hỏi
- key có stable không?
- có cần ordering không?
- read/write ratio là gì?

---

## 6. Trees và ordered structures

### BST và balanced trees
Phù hợp khi:
- cần ordered traversal
- cần range query
- cần predecessor/successor

### Heap
Phù hợp khi:
- cần luôn lấy min/max nhanh
- top-K
- scheduling

### Trie
Phù hợp khi:
- prefix search
- autocomplete
- dictionary matching

### B-Tree family
Phù hợp mạnh trong storage/database vì thiết kế thân thiện block/page I/O.

---

## 7. Graph representations

Graph không phải chỉ là một chapter DSA. Nó là một mô hình rất rộng.

### Adjacency list
Tốt cho graph thưa.

### Adjacency matrix
Tốt khi graph dày hoặc cần edge lookup rất nhanh.

### Edge list
Đơn giản, hữu ích trong một số thuật toán và input formats.

---

## 8. Specialized structures đáng biết

### Union-Find
Giỏi ở dynamic connectivity.

### Segment tree / Fenwick tree
Tốt cho range queries.

### Bloom filter
Approximate membership với false positive có kiểm soát.

### Skip list
Probabilistic ordered structure, xuất hiện trong một số storage systems.

---

## 9. Chọn structure theo workload

Hãy tập hỏi:
- exact lookup hay ordered traversal?
- range query hay point query?
- updates thường xuyên hay mostly read-only?
- data có vừa RAM không?
- locality có quan trọng không?

Ví dụ nhanh:
- Top-K -> heap
- dedup -> hash set
- prefix lookup -> trie
- connectivity -> union-find
- scan + index access -> array

---

## 10. Sai lầm phổ biến
- dùng linked list vì complexity đẹp trên giấy
- dùng hash map khi thật ra cần ordered behavior
- chọn tree nhưng workload thực chỉ cần array + sort một lần
- không tính memory overhead
- quên rằng structure đẹp lý thuyết nhưng library support yếu có thể làm project khổ hơn

---

## 11. Checklist sau bài
- So sánh được array, linked list, stack, queue, hash map, tree, heap, graph
- Chọn được data structure phù hợp cho một bài toán mới và giải thích vì sao
- Biết ít nhất 4 specialized structures ngoài bộ cơ bản
- Hiểu vai trò của memory layout trong performance

## 12. Bài tập thực hành
1. Tự lập bảng complexity cho 10 data structures.
2. Implement stack, queue, heap và union-find ở mức cơ bản.
3. Chọn 5 use cases production và mapping sang data structure phù hợp.
4. So sánh array và linked list trong một note reasoning.
5. Tìm một bài cần prefix search và giải thích vì sao trie hợp lý.

## 13. Mini deliverable
Viết một file `data_structure_selection_guide.md` với 2 cột:
- use case
- structure + trade-off

## 14. Học tiếp
- `Bai_06_Algorithmic_Paradigms_Full_Lesson.md`
- `../../08_Reference_and_Review/03_Algorithms_and_Data_Deep_Dive.md`