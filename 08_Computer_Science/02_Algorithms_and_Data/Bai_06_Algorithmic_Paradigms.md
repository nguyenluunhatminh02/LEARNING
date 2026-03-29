# Bài 06: Algorithmic Paradigms

## 🎯 Mục tiêu
- Nhận diện các pattern thiết kế thuật toán quan trọng nhất
- Biết khi nào dùng divide and conquer, greedy, dynamic programming, backtracking, graph search
- Chuyển từ "nhớ bài mẫu" sang "nhìn bài toán và chọn mô hình giải"

## 📖 Bức tranh lớn
Paradigm là khuôn tư duy. Khi gặp bài toán mới, bạn không muốn lục trí nhớ xem đã gặp bài y hệt chưa. Bạn muốn nhận diện cấu trúc sâu hơn: bài này có optimal substructure không, có state transition không, có monotonic property không, có thể search trên answer không.

---

## 1. Divide and conquer

### Dấu hiệu nhận biết
- Bài toán tách được thành các bài con độc lập hoặc gần độc lập
- Kết quả bài lớn ghép từ kết quả bài con

### Ví dụ điển hình
- Merge sort
- Quick sort
- Binary search
- Closest pair of points

### Câu hỏi cần tự hỏi
- Chia như thế nào?
- Ghép kết quả ra sao?
- Recurrence là gì?

---

## 2. Greedy algorithms

### Dấu hiệu nhận biết
- Mỗi bước có lựa chọn local tốt nhất
- Có thể chứng minh local optimum dẫn tới global optimum

### Ví dụ điển hình
- Interval scheduling
- Huffman coding
- Kruskal / Prim
- Canonical coin systems trong vài trường hợp đặc biệt

### Cảnh báo
Greedy rất dễ hấp dẫn nhưng cũng rất dễ sai. Luôn tìm exchange argument hoặc counterexample.

---

## 3. Dynamic programming

### Dấu hiệu nhận biết
- Bài toán có subproblems lặp lại
- Có optimal substructure
- State có thể mô tả gọn

### Quy trình chuẩn
1. Xác định state.
2. Viết transition.
3. Xác định base cases.
4. Quyết định top-down hay bottom-up.
5. Tối ưu memory nếu cần.

### Các nhóm bài phổ biến
- Knapsack
- Longest subsequence
- Grid/path counting
- Partition / subset
- Interval DP
- Bitmask DP

---

## 4. Backtracking và search

### Dùng khi nào
- Cần enumerate combinations/permutations/solutions
- Bài có branching factor vừa phải hoặc có pruning tốt

### Kỹ năng quan trọng
- State representation
- Undo choice
- Constraint checking sớm
- Pruning bằng bounds hoặc heuristic

### Ví dụ
- N-Queens
- Sudoku
- Subset generation
- Combination sum

---

## 5. Graph traversal và shortest path mindset

### Pattern phải nắm
- BFS: shortest path trong unweighted graph, level-order exploration
- DFS: traversal, cycle detection, topological sort, components
- Dijkstra: weighted graph với edge non-negative
- Bellman-Ford: có negative edge
- Floyd-Warshall: all-pairs shortest path ở quy mô nhỏ

### Ứng dụng ngoài graph thuần
- State machine
- Word ladder
- Grid traversal
- Dependency resolution
- Package installation/order scheduling

---

## 6. Search on answer và monotonicity

### Ý tưởng
Không phải lúc nào binary search cũng search trên index. Rất nhiều bài có thể binary search trên giá trị đáp án nếu có monotonic property.

### Ví dụ
- Tốc độ tối thiểu để hoàn thành công việc
- Capacity nhỏ nhất để ship packages đúng deadline
- Ngưỡng tối ưu cho resource allocation

---

## 7. Prefix sums, sweep line, union-find, heap patterns

Đây là các paradigm nhỏ nhưng xuất hiện cực nhiều:

- Prefix sums: range aggregates
- Difference arrays: range updates
- Sweep line: interval overlap, geometry events
- Heap-driven greedy: scheduling, top-K, streaming median
- Union-find: connectivity over time

---

## 8. Cách chọn paradigm

### Hỏi tuần tự
- Có brute force tree of choices không? -> backtracking
- Có repeated subproblem không? -> DP/memoization
- Có monotonic property không? -> binary search on answer
- Có quan hệ kết nối/chuyển trạng thái không? -> graph
- Có ordered intervals/events không? -> sorting + sweep/greedy
- Có split-merge tự nhiên không? -> divide and conquer

---

## ✅ Checklist ôn tập
- Nhìn bài toán và nêu được 2-3 paradigm khả thi
- Viết được state/transition cho bài DP cơ bản
- Tìm được counterexample cho greedy sai
- Phân biệt khi nào dùng BFS, DFS, Dijkstra
- Nhận ra binary search on answer trong bài monotonic

## 📝 Bài tập
1. Chọn 10 bài bất kỳ và phân loại paradigm chính.
2. Tự viết template cho BFS, DFS, DP, backtracking.
3. Giải thích vì sao một bài greedily chọn local optimum lại sai.
4. Viết note so sánh top-down vs bottom-up DP.
5. Làm một mind map về các dấu hiệu nhận biết paradigm.

## 📚 Tài liệu
- *Algorithm Design* — Kleinberg & Tardos
- *Competitive Programmer's Handbook* — Antti Laaksonen
- Track đào sâu: `../../04_DSA/`