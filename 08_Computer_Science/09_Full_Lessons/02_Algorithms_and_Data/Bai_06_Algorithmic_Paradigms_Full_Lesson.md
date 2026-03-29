# Bài 06: Algorithmic Paradigms — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- nhận diện được các paradigm thiết kế thuật toán quan trọng nhất
- chọn được hướng giải hợp lý khi gặp bài toán mới
- hiểu khi nào dùng divide and conquer, greedy, DP, backtracking, graph search

## Bạn cần biết trước
- Bài 04 và Bài 05

---

## 1. Paradigm là gì

Paradigm là khuôn tư duy để nhìn bài toán.

Thay vì nhớ 100 solution rời rạc, bạn học cách nhìn cấu trúc sâu hơn:
- có chia nhỏ được không?
- có optimal substructure không?
- có monotonic property không?
- có state transition hay connectivity không?

---

## 2. Divide and conquer

### Dấu hiệu nhận biết
- bài toán chia được thành bài con tương tự
- kết quả có thể ghép lại

### Ví dụ
- merge sort
- binary search
- quick sort

### Câu hỏi quan trọng
- chia ở đâu?
- combine step tốn bao nhiêu?
- subproblems có độc lập đủ không?

---

## 3. Greedy

Greedy chọn lựa chọn tốt nhất tại từng bước.

### Dùng tốt khi
- local optimum dẫn tới global optimum
- có proof như exchange argument

### Ví dụ
- interval scheduling
- MST algorithms như Kruskal/Prim

### Cảnh báo
Greedy rất hấp dẫn nhưng rất dễ sai nếu bạn không có proof hoặc ít nhất không đi săn counterexample.

---

## 4. Dynamic programming

DP phù hợp khi:
- có overlapping subproblems
- có optimal substructure
- state mô tả được gọn

### Quy trình nên thuộc lòng
1. Chọn state.
2. Viết transition.
3. Xác định base cases.
4. Chọn top-down hay bottom-up.
5. Tối ưu memory nếu cần.

### Sai lầm phổ biến
- state quá nhiều biến
- thiếu biến cần thiết
- code trước khi viết rõ transition

---

## 5. Backtracking

Backtracking phù hợp khi bạn cần enumerate các khả năng và cắt bớt nhánh không cần thiết.

### Ví dụ
- permutations/combinations
- N-Queens
- Sudoku

### Kỹ năng chính
- state representation
- choose / explore / un-choose
- pruning sớm

---

## 6. Graph traversal mindset

### BFS
- shortest path trong graph unweighted
- level by level

### DFS
- traversal
- cycle detection
- connected components
- topological sort

### Dijkstra
- weighted graph không có cạnh âm

Điểm quan trọng là nhiều bài không trông như graph nhưng thực ra là graph:
- word ladder
- dependency resolution
- grid traversal
- state transitions

---

## 7. Binary search on answer

Đây là pattern nhiều người biết muộn.

Nếu đáp án thuộc một miền có tính đơn điệu, bạn có thể search trên chính đáp án thay vì trên array index.

Ví dụ:
- capacity nhỏ nhất đủ để ship hàng trong D ngày
- tốc độ tối thiểu để hoàn thành K công việc

---

## 8. So sánh nhanh các paradigm

### Nếu có split-merge tự nhiên
Hãy nghĩ divide and conquer.

### Nếu có lựa chọn local đẹp và proof được
Hãy nghĩ greedy.

### Nếu có repeated subproblems
Hãy nghĩ DP.

### Nếu có cây lựa chọn lớn cần enumerate
Hãy nghĩ backtracking.

### Nếu có connectivity, transitions, shortest path
Hãy nghĩ graph.

---

## 9. Sai lầm phổ biến
- thấy từ khóa nào đó là gán ngay một paradigm
- không thử brute force trước nên không thấy structure của bài
- dùng DP cho bài greedy được và ngược lại
- dùng DFS/BFS mà không rõ graph model thực sự là gì

---

## 10. Checklist sau bài
- Nhìn bài toán và nêu được ít nhất 2 hướng giải khả thi
- Viết được state và transition cho DP cơ bản
- Nêu được counterexample cho greedy sai
- Phân biệt được BFS, DFS và Dijkstra
- Nhận ra binary search on answer khi có monotonicity

## 11. Bài tập thực hành
1. Chọn 10 bài bất kỳ và gán paradigm chính cho từng bài.
2. Viết template riêng cho BFS, DFS, DP, backtracking.
3. Tìm 2 counterexample cho một greedy strategy do bạn tự nghĩ ra.
4. Chọn một bài DP và viết state/transition bằng lời trước khi code.
5. Tìm một bài có thể giải bằng binary search on answer.

## 12. Mini deliverable
Làm một sơ đồ `algorithmic_paradigms_map.md` gồm:
- paradigm
- dấu hiệu nhận biết
- use cases
- lỗi thường gặp

## 13. Học tiếp
- `Bai_07_Advanced_Algorithms_Full_Lesson.md`
- `../../08_Reference_and_Review/03_Algorithms_and_Data_Deep_Dive.md`