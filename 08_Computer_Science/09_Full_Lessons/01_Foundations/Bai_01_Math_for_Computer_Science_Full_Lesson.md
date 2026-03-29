# Bài 01: Math for Computer Science — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- hiểu vì sao toán rời rạc là ngôn ngữ nền của Computer Science
- dùng được logic, sets, counting và probability cho reasoning kỹ thuật cơ bản
- biết chứng minh hoặc giải thích tính đúng của một số thuật toán đơn giản

## Bạn cần biết trước
- phép toán số học cơ bản
- khái niệm hàm và phương trình ở mức phổ thông
- tư duy đọc định nghĩa cẩn thận

---

## 1. Vì sao Computer Science cần toán

Nhiều người học CS bị mắc vào hai cực:
- hoặc sợ toán và nghĩ nó quá hàn lâm
- hoặc học công thức nhưng không biết dùng vào đâu

Thực ra toán trong CS chủ yếu giúp bạn làm 4 việc:
- mô tả chính xác một vấn đề
- chứng minh một lời giải là đúng
- đếm số trường hợp, số trạng thái, số khả năng
- suy luận về rủi ro, xác suất, chi phí tăng trưởng

Ví dụ rất thực tế:
- Binary search đúng vì có invariant logic rõ ràng.
- Bloom filter cần xác suất để hiểu false positive.
- Distributed retries cần xác suất để ước lượng khả năng thất bại toàn phần.

---

## 2. Logic và phát biểu chính xác

### 2.1 Proposition và predicate
- Proposition: câu có thể xác định đúng hoặc sai.
- Predicate: câu chứa biến, cần gán giá trị cho biến rồi mới biết đúng hay sai.

Ví dụ:
- "2 là số chẵn" là proposition.
- "x là số chẵn" là predicate.

### 2.2 Các phép logic cơ bản
- AND: cả hai điều kiện đúng
- OR: ít nhất một điều kiện đúng
- NOT: phủ định
- implication `P -> Q`: nếu P đúng thì Q phải đúng

Điểm nhiều người nhầm nhất là implication. `P -> Q` không có nghĩa là `Q -> P`.

Ví dụ:
- Nếu một số chia hết cho 4 thì nó chia hết cho 2.
- Nhưng chia hết cho 2 không có nghĩa chia hết cho 4.

### 2.3 Quantifiers
- `for all`: với mọi phần tử
- `exists`: tồn tại ít nhất một phần tử

Hai câu sau khác nhau hoàn toàn:
- Với mọi mảng đã sort, thuật toán đúng.
- Tồn tại một mảng đã sort mà thuật toán đúng.

---

## 3. Chứng minh và invariant

### 3.1 Direct proof
Đi từ giả thiết tới kết luận bằng chuỗi suy luận rõ ràng.

### 3.2 Proof by contradiction
Giả sử điều ngược lại đúng, rồi suy ra mâu thuẫn.

### 3.3 Mathematical induction
Gồm 2 phần:
- base case
- inductive step

Nó cực kỳ quan trọng vì nhiều thuật toán đệ quy và nhiều loop có thể được reasoning bằng induction.

### 3.4 Loop invariant
Loop invariant là điều luôn đúng trước và sau mỗi vòng lặp.

Ví dụ với binary search:
- nếu target tồn tại, nó luôn nằm trong đoạn `[left, right]` đang xét

Nếu bạn không có invariant, bạn rất dễ code sai edge cases.

---

## 4. Sets, relations và functions

### 4.1 Sets
Các phép cơ bản:
- union
- intersection
- difference
- complement

Tư duy set rất hữu ích khi làm việc với filters, permissions, query logic và state space.

### 4.2 Relations
Một relation có thể là:
- reflexive
- symmetric
- transitive

Nếu có đủ cả ba, đó là equivalence relation.

Ứng dụng:
- grouping
- partitioning
- connected components

### 4.3 Functions
Phân biệt:
- injective
- surjective
- bijective

Trong CS, function composition cũng rất quan trọng vì nhiều pipeline data/transform chính là hàm nối hàm.

---

## 5. Counting và combinatorics

Đây là phần giúp bạn không đoán mò số lượng possibilities.

### 5.1 Rule of sum và rule of product
- Sum: chọn một trong nhiều nhóm rời nhau
- Product: làm tuần tự nhiều bước độc lập

### 5.2 Permutation vs combination
- Permutation: có xét thứ tự
- Combination: không xét thứ tự

### 5.3 Pigeonhole principle
Nếu có nhiều vật hơn số ô chứa, ít nhất một ô chứa từ hai vật trở lên.

Ứng dụng:
- collision reasoning
- lower bound reasoning

---

## 6. Probability cho engineer

Bạn không cần bắt đầu bằng xác suất quá học thuật. Hãy bắt đầu từ các câu hỏi thực tế:
- Một request có xác suất thất bại là 0.1. Retry 3 lần thì xác suất thất bại toàn bộ là bao nhiêu?
- Một cluster có 3 node độc lập, mỗi node có xác suất alive là 0.99. Xác suất còn ít nhất 2 node sống là bao nhiêu?

### 6.1 Conditional probability
Rất hữu ích khi reasoning về signal, tests, failures và experiments.

### 6.2 Expectation
Expectation không phải "kết quả sẽ luôn bằng vậy", mà là giá trị trung bình dài hạn.

### 6.3 Variance
Hai hệ thống có cùng average latency vẫn có thể rất khác nhau nếu variance khác xa nhau.

---

## 7. Graph thinking

Rất nhiều bài toán thực tế thực ra là graph:
- modules phụ thuộc nhau
- package installation order
- flight routes
- workflow states
- service dependency map

Bạn không cần chờ tới bài graph mới dùng graph thinking. Nó là một mô hình chung để nhìn quan hệ và luồng chuyển trạng thái.

---

## 8. Ví dụ phân tích

### Ví dụ 1: Retry
Nếu xác suất một lần gọi API thất bại là `p = 0.2`, và các lần retry độc lập, thì xác suất thất bại sau 3 lần là:

```text
0.2 * 0.2 * 0.2 = 0.008
```

Nghĩa là xác suất thành công ít nhất một lần là `1 - 0.008 = 0.992`.

### Ví dụ 2: Induction
Chứng minh:

```text
1 + 2 + ... + n = n(n+1)/2
```

Base case `n = 1`: đúng.

Inductive step:
Giả sử đúng với `n = k`, tức:

```text
1 + 2 + ... + k = k(k+1)/2
```

Khi đó với `k + 1`:

```text
1 + 2 + ... + k + (k+1)
= k(k+1)/2 + (k+1)
= (k+1)(k+2)/2
```

Vậy đúng với mọi `n >= 1`.

---

## 9. Sai lầm phổ biến
- học logic như ký hiệu rời rạc, không gắn với code và algorithms
- nhớ công thức tổ hợp nhưng không biết khi nào dùng
- hiểu expectation nhưng bỏ qua variance và tail risk
- xem proof là thứ chỉ dành cho trường học, trong khi production bug rất hay đến từ assumption không được chứng minh

---

## 10. Checklist sau bài
- Giải thích được proposition, predicate, quantifier
- Phân biệt được direct proof, contradiction, induction
- Tính được permutation và combination cơ bản
- Giải thích được expectation và variance ở mức trực giác
- Nhìn được ít nhất 3 tình huống engineering có thể mô hình hóa bằng graph

## 11. Bài tập thực hành
1. Tự viết một proof bằng induction cho tổng các số lẻ đầu tiên.
2. Tạo 5 ví dụ về implication và chỉ ra câu đảo sai như thế nào.
3. Tính xác suất thất bại toàn phần của 5 lần retry với `p = 0.1`.
4. Vẽ dependency graph cho 8 modules trong một ứng dụng bạn biết.
5. Viết 10 flashcards từ glossary cho bài này.

## 12. Mini deliverable
Viết một note 1 trang tên là `Math for CS essentials`, gồm:
- 5 khái niệm logic quan trọng nhất
- 3 use cases xác suất trong engineering
- 2 ví dụ graph modeling

## 13. Học tiếp
- `Bai_02_Programming_Fundamentals_Full_Lesson.md`
- `../../08_Reference_and_Review/02_Foundations_Deep_Dive.md`