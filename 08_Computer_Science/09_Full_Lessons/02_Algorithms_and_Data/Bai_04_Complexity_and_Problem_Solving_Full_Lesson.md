# Bài 04: Complexity and Problem Solving — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- phân tích được time và space complexity ở mức cơ bản đến khá
- có quy trình giải bài toán rõ ràng thay vì mò pattern
- biết vì sao một lời giải đúng, chứ không chỉ vì nó pass vài test

## Bạn cần biết trước
- đã học xong 3 bài nền tảng đầu tiên
- biết vòng lặp, hàm, recursion ở mức cơ bản

---

## 1. Complexity thực sự dùng để làm gì

Complexity không chỉ để trả lời trong phỏng vấn. Nó giúp bạn trả lời những câu hỏi cực thực tế:
- dữ liệu tăng 10 lần thì runtime tăng khoảng bao nhiêu?
- chi phí memory có vượt giới hạn không?
- đoạn code nào là bottleneck lớn nhất?

Complexity là mô hình tăng trưởng, không phải thời gian chạy chính xác theo mili-giây.

---

## 2. Big-O, Big-Theta và Big-Omega

### Big-O
Upper bound, thường dùng nhiều nhất trong engineering.

### Big-Theta
Tight bound, mô tả tăng trưởng sát hơn.

### Big-Omega
Lower bound.

Trong thực tế, Big-O thường đủ để reasoning nhanh, nhưng bạn phải nhớ:
- constant factors vẫn quan trọng
- memory locality vẫn quan trọng
- I/O cost có thể lấn át CPU cost

---

## 3. Cách phân tích complexity

### Pattern 1: một loop tuyến tính
Thường là `O(n)`.

### Pattern 2: loop lồng nhau
Thường là `O(n^2)` hoặc `O(nm)`.

### Pattern 3: mỗi bước giảm bài toán một nửa
Thường là `O(log n)`.

### Pattern 4: chia đôi rồi xử lý hai nửa
Thường dẫn tới `O(n log n)` với một số loại combine step.

### Pattern 5: recursion tree
Dùng để hình dung tổng cost từ nhiều lời gọi đệ quy.

---

## 4. Quy trình giải bài toán chuẩn

Một quy trình rất đáng luyện:
1. Đọc kỹ input, output, constraints.
2. Tự nói lại bài toán bằng lời của mình.
3. Viết 2-3 ví dụ tay.
4. Làm brute force trước.
5. Tìm bottleneck của brute force.
6. Chọn representation dữ liệu hợp lý.
7. Tối ưu bằng pattern phù hợp.
8. Giải thích vì sao lời giải đúng.
9. Tính complexity.
10. Test edge cases.

Nếu bỏ qua một trong các bước trên, lời giải thường trở nên mong manh.

---

## 5. Correctness và invariants

Một solution tốt cần 2 thứ:
- đúng
- đủ nhanh

Nhiều bạn chỉ tập trung tối ưu mà quên chứng minh đúng.

### Các công cụ reasoning chính
- loop invariant
- induction
- contradiction
- exchange argument cho greedy
- optimal substructure cho dynamic programming

Ví dụ:
- Với binary search, invariant là nếu target tồn tại, nó nằm trong đoạn đang xét.

---

## 6. Worst-case, average-case và amortized

### Worst-case
Trường hợp xấu nhất.

### Average-case
Trung bình theo mô hình phân phối input nào đó.

### Amortized
Chi phí trung bình qua một chuỗi thao tác.

Ví dụ dynamic array append:
- có lúc resize tốn `O(n)`
- nhưng trung bình mỗi append vẫn `O(1)` amortized

---

## 7. Trade-off thực tế

Khi tối ưu, bạn thường đánh đổi:
- memory lấy speed
- preprocessing lấy query speed
- code simplicity lấy raw performance

Một engineer mạnh không chỉ biết tối ưu, mà biết khi nào không nên tối ưu thêm.

---

## 8. Ví dụ phân tích

### Ví dụ 1: Two Sum brute force
Kiểm tra mọi cặp phần tử:
- time `O(n^2)`
- space `O(1)`

### Ví dụ 2: Two Sum với hash map
Scan một lần, lưu phần bù đã thấy:
- time `O(n)` average
- space `O(n)`

Điểm quan trọng không chỉ là nhớ solution `hash map`, mà là hiểu bottleneck của brute force nằm ở đâu và hash map giải bottleneck đó thế nào.

---

## 9. Sai lầm phổ biến
- tính complexity sai vì bỏ qua cost của sort hoặc slicing
- chỉ học template mà không hiểu invariant
- không làm brute force baseline
- không test input rỗng, duplicates, extremes
- optimize quá sớm trong khi bài toán chưa hiểu rõ

---

## 10. Checklist sau bài
- Phân tích được complexity của code ngắn 20-30 dòng
- Phân biệt được worst-case, average-case, amortized
- Có quy trình giải bài toán rõ ràng
- Giải thích được vì sao brute force vẫn quan trọng
- Dùng được invariant để reasoning về ít nhất một thuật toán

## 11. Bài tập thực hành
1. Phân tích complexity cho 5 đoạn code bất kỳ bạn từng viết.
2. Viết brute force và optimized solution cho `two sum`.
3. Chứng minh binary search đúng bằng invariant.
4. Giải thích vì sao merge sort là `O(n log n)`.
5. Tự viết một checklist 8 bước để giải bài coding.

## 12. Mini deliverable
Tạo một file `problem_solving_template.md` gồm:
- cách restate bài toán
- cách viết brute force
- cách tìm bottleneck
- cách liệt kê edge cases

## 13. Học tiếp
- `Bai_05_Core_Data_Structures_Full_Lesson.md`
- `../../08_Reference_and_Review/03_Algorithms_and_Data_Deep_Dive.md`