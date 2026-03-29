# Bài 05: Core Data Structures

## 🎯 Mục tiêu
- Nắm các data structure cốt lõi và chi phí của từng thao tác
- Biết chọn cấu trúc dữ liệu dựa trên access pattern, memory layout và trade-off
- Xây nền tảng để viết code vừa đúng vừa hiệu quả

## 📖 Bức tranh lớn
Rất nhiều bài toán không khó vì thuật toán phức tạp, mà khó vì chọn sai representation của dữ liệu. Một data structure phù hợp có thể biến code phức tạp thành đơn giản, biến `O(n^2)` thành `O(n log n)` hoặc `O(n)`.

---

## 1. Linear structures

### Array / Dynamic Array
- Random access `O(1)`
- Append thường `O(1)` amortized
- Insert/delete giữa mảng `O(n)`
- Cache-friendly, thường rất nhanh trong thực tế

### Linked List
- Insert/delete tại node đang có reference là `O(1)`
- Random access `O(n)`
- Locality kém, pointer overhead lớn
- Thực tế ít dùng hơn array nhiều hơn bạn nghĩ

### Stack / Queue / Deque
- Stack: LIFO, useful cho recursion simulation, parsing, monotonic patterns
- Queue: FIFO, useful cho BFS, scheduling, buffering
- Deque: pop/push hai đầu, useful cho sliding window, monotonic queue

---

## 2. Hash-based structures

### Hash Table / Hash Map / Hash Set
- Average insert/search/delete `O(1)`
- Worst-case có thể `O(n)` nếu collision nặng
- Cần hiểu hash function, load factor, resize, collision handling

### Dùng khi nào
- Lookup nhanh theo key
- Counting/frequency map
- De-duplication
- Memoization/cache

### Lưu ý thực tế
- Hash map nhanh nhưng không có order mặc định
- Memory overhead thường cao
- Key design quan trọng: equality + hash must consistent

---

## 3. Tree family

### Binary Tree / BST
- BST cân bằng cho search/insert/delete `O(log n)`
- BST không cân bằng có thể thành `O(n)`
- Dùng cho ordered data, range query, traversal logic

### Balanced Trees
- AVL, Red-Black Tree, B-Tree, B+Tree
- Ứng dụng trong stdlib map/set, database index, filesystem metadata

### Heap / Priority Queue
- Insert `O(log n)`
- Extract min/max `O(log n)`
- Top-K, scheduling, Dijkstra, merge K streams

### Trie
- Prefix search, autocomplete, dictionary matching
- Time theo độ dài key thay vì số phần tử
- Memory-heavy nhưng mạnh ở workloads phù hợp

---

## 4. Graph structures

### Representation
- Adjacency list: tốt cho graph thưa
- Adjacency matrix: tốt cho graph dày và lookup edge `O(1)`

### Ứng dụng
- Dependency graph
- Routing/network topology
- Social graph
- Workflow/state machine

### Kỹ năng phải có
- Mô hình hóa bài toán thành graph khi cần
- Phân biệt tree, DAG, cyclic graph

---

## 5. Specialized structures

### Union-Find / DSU
- Dynamic connectivity
- Connected components
- Kruskal MST

### Segment Tree / Fenwick Tree
- Range query + point/range update
- Rất hữu ích cho bài tối ưu truy vấn trên array

### Bloom Filter
- Membership test với false positive có kiểm soát
- Dùng cho cache, storage, network systems

### Skip List
- Alternative probabilistic to balanced tree
- Dùng trong một số database/storage systems

---

## 6. Chọn data structure như một engineer

### Hãy hỏi
- Workload là read-heavy hay write-heavy?
- Cần ordered hay unordered?
- Cần range query hay exact lookup?
- Dữ liệu có vừa RAM không?
- Chi phí memory có quan trọng không?
- Access pattern có tuần tự hay ngẫu nhiên?

### Ví dụ chọn nhanh

```text
Exact lookup nhiều           -> Hash map
Range query ordered          -> Balanced tree / B-Tree
Top-K / smallest-first       -> Heap
Prefix matching              -> Trie
Sequential scan nhanh        -> Array
Connectivity queries         -> Union-Find
Approximate membership       -> Bloom filter
```

---

## 7. Lỗi phổ biến

- Dùng linked list nơi array tốt hơn nhiều
- Dùng hash map nhưng quên cost memory và resize
- Dùng tree khi workload chỉ cần append + scan
- Không để ý duplicates, ordering, stability
- Chọn structure đẹp về lý thuyết nhưng library/runtime support yếu

---

## ✅ Checklist ôn tập
- So sánh được array, linked list, hash map, tree, heap, graph
- Tự chọn được data structure cho một bài toán mới và giải thích vì sao
- Biết ít nhất 3 specialized structures ngoài bộ cơ bản
- Giải thích được vì sao memory layout ảnh hưởng performance
- Mô hình hóa được một dependency problem thành graph

## 📝 Bài tập
1. Tự lập bảng complexity cho 10 data structures phổ biến.
2. Giải 5 bài cần hash map, 5 bài cần heap, 5 bài cần graph.
3. Viết cài đặt đơn giản cho stack, queue, hash map, heap.
4. Chọn 3 use cases production và nêu data structure hợp lý nhất.
5. So sánh array vs linked list bằng benchmark nhỏ nếu có thời gian.

## 📚 Tài liệu
- *Open Data Structures* — Pat Morin
- *The Algorithm Design Manual* — Skiena
- Track đào sâu: `../../04_DSA/`