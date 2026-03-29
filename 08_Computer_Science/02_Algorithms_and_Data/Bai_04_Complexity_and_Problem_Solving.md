# Bài 04: Complexity and Problem Solving

## 🎯 Mục tiêu
- Hiểu cách phân tích thời gian và bộ nhớ của lời giải
- Biết lập luận vì sao một thuật toán đúng, đủ nhanh và đáng tin cậy
- Xây quy trình giải bài toán thay vì thử mò theo pattern rời rạc

## 📖 Bức tranh lớn
Complexity không chỉ dành cho phỏng vấn. Nó là công cụ để trả lời câu hỏi rất thực tế: giải pháp này còn chạy nổi khi data tăng 10x hay 100x không? Tư duy problem solving tốt giúp bạn tránh lao vào code quá sớm khi chưa hiểu constraints, invariants và trade-off.

---

## 1. Big-O, Big-Theta, Big-Omega

### Phải nắm
- `O(f(n))`: upper bound
- `Theta(f(n))`: tight bound
- `Omega(f(n))`: lower bound
- Worst-case, average-case, amortized-case
- Time complexity vs space complexity

### Trực giác quan trọng
- `O(n)` và `O(2n)` cùng bậc tăng trưởng nhưng constant factor vẫn có ý nghĩa trong thực tế.
- Một giải pháp `O(n log n)` với locality tốt có thể nhanh hơn một giải pháp `O(n)` nhưng cache rất tệ ở data size thực tế.

### Các bậc tăng trưởng thường gặp

```text
O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(n^3) < O(2^n) < O(n!)
```

---

## 2. Kỹ thuật phân tích complexity

### Các pattern cơ bản
- Một loop qua `n` phần tử -> `O(n)`
- Hai loop lồng nhau -> thường `O(n^2)`
- Mỗi vòng giảm bài toán đi một nửa -> `O(log n)`
- Chia đôi rồi xử lý hai nửa -> thường dẫn tới recurrence `T(n) = 2T(n/2) + ...`

### Chủ đề nâng cao vừa đủ
- Recurrence relations
- Master theorem ở mức trực giác
- Amortized analysis: dynamic array, stack với rollback, union-find

### Ví dụ trực giác amortized
Dynamic array append có lúc tốn `O(n)` do resize, nhưng trung bình mỗi append vẫn là `O(1)` amortized.

---

## 3. Correctness và invariants

### Các công cụ lập luận
- Loop invariant
- Recursive invariant
- Proof by induction
- Exchange argument cho greedy
- Optimal substructure cho dynamic programming

### Bạn phải tập trả lời
- Biến nào luôn đúng sau mỗi iteration?
- Base case là gì?
- Nếu dừng thuật toán ở bước này thì điều kiện đúng nào được đảm bảo?

---

## 4. Quy trình giải bài toán chuẩn

1. Đọc kỹ input, output, constraints.
2. Tự viết lại bài toán bằng ngôn ngữ của mình.
3. Làm 2-3 ví dụ tay, bao gồm edge cases.
4. Chọn representation của data.
5. Nghĩ brute force trước để có baseline.
6. Tìm bottleneck lớn nhất.
7. Tối ưu bằng pattern phù hợp: sort, hash, heap, DP, graph, binary search, etc.
8. Chứng minh ý tưởng đúng.
9. Tính time/space complexity.
10. Code, test, debug, review lại assumption.

---

## 5. Brute force, optimize, and trade-off

### Quy tắc thực dụng
- Brute force đúng luôn tốt hơn tối ưu sai.
- Tối ưu bằng cách đổi cấu trúc dữ liệu thường đơn giản hơn đổi toàn bộ thuật toán.
- Nếu input nhỏ, lời giải đơn giản có thể là lựa chọn tốt hơn.
- Space-for-time trade-off là kỹ năng rất quan trọng: hash map, prefix sum, caching.

### Các optimization direction phổ biến
- Preprocessing
- Sorting trước khi query
- Caching / memoization
- Two pointers / sliding window
- Divide and conquer
- Parallelization

---

## 6. Lower bounds và reductions ở mức engineer

Bạn không cần đi quá hàn lâm ngay từ đầu, nhưng nên hiểu:

- Comparison sort khó tốt hơn `O(n log n)` trong mô hình so sánh chuẩn
- Nhiều bài toán có thể reduce về graph, shortest path, matching, flow
- Nếu thấy một bài giống subset/partition/scheduling khó, hãy nghĩ đến NP-hardness để biết khi nào nên dừng tìm exact solution

---

## 7. Sai lầm phổ biến

- Tính sai complexity vì bỏ qua loop ẩn trong library call
- Nhầm average case với worst case
- Chọn data structure không hợp access pattern
- Chỉ học solution pattern mà không hiểu invariant
- Không test edge cases như empty input, duplicates, very large input

---

## ✅ Checklist ôn tập
- Tự phân tích được complexity của code 20-30 dòng
- Giải thích được amortized analysis bằng ví dụ dynamic array
- Dùng loop invariant để giải thích binary search hoặc partitioning
- Viết được quy trình từ brute force tới optimized solution
- Biết khi nào nên dừng tối ưu để giữ code đơn giản

## 📝 Bài tập
1. Phân tích time/space complexity cho 5 hàm bạn từng viết.
2. Viết brute force và optimized solution cho bài `two sum`.
3. Chứng minh binary search đúng bằng loop invariant.
4. Giải thích vì sao merge sort là `O(n log n)`.
5. Tự soạn 10 edge cases cho một bài array/string.

## 📚 Tài liệu
- *Algorithm Design* — Kleinberg & Tardos
- *Introduction to Algorithms* — CLRS
- Track đào sâu: `../../04_DSA/`