# Bài 02: Programming Fundamentals

## 🎯 Mục tiêu
- Hiểu bản chất của chương trình, state, control flow và memory
- Viết code có cấu trúc, dễ debug, dễ test, dễ mở rộng
- Nắm nền tảng ngôn ngữ lập trình trước khi đi vào framework và tooling

## 📖 Bức tranh lớn
Một engineer mạnh không chỉ biết dùng syntax. Bạn phải hiểu chương trình là một chuỗi biến đổi trạng thái chạy trên một mô hình bộ nhớ cụ thể, có input, output, invariant, lỗi và chi phí thực thi. Khi hiểu đến mức đó, bạn học ngôn ngữ mới nhanh hơn rất nhiều.

---

## 1. Core programming model

### Các khái niệm gốc
- Value, variable, reference, object
- Expression vs statement
- Mutable vs immutable state
- Scope và lifetime
- Stack vs heap ở mức trực giác

### Phải nắm rõ
- Assignment là cập nhật binding hay copy value?
- Truyền tham số là pass-by-value, pass-by-reference hay pass-by-sharing?
- Khi nào object bị giữ lại trong memory lâu hơn mong đợi?

---

## 2. Control flow và abstraction

### Control flow
- Sequence
- Conditionals
- Loops
- Recursion
- Exceptions / error handling

### Abstraction
- Function decomposition
- Module/package boundaries
- Interface vs implementation
- Reusable utilities vs business logic

### Câu hỏi quan trọng
- Function này có làm đúng một việc không?
- Input/output contract đã rõ chưa?
- Có side effect nào không mong muốn không?

---

## 3. Data modeling trong code

### Chủ đề cần nắm
- Primitive types, collections, records/structs, classes
- Algebraic thinking: enum, tagged union ở mức khái niệm
- Domain model và naming
- Data normalization trong code

### Dấu hiệu code yếu
- Dùng string cho mọi thứ
- Một object có quá nhiều field không liên quan
- Hàm nhận 8-10 tham số rời rạc
- State bị sửa ở nhiều nơi khó kiểm soát

---

## 4. Debugging như một kỹ năng cốt lõi

### Quy trình debug nên luyện
1. Reproduce bug ổn định.
2. Thu nhỏ input hoặc điều kiện gây lỗi.
3. Xác định expected vs actual.
4. Kiểm tra assumptions từng bước.
5. Sửa tận gốc, không vá biểu hiện bề mặt.

### Công cụ nên biết
- Logging có cấu trúc
- Debugger và breakpoints
- REPL hoặc scratch script
- Unit test tái hiện bug
- Profilers cơ bản cho CPU/memory

---

## 5. Testing và correctness ở mức cơ bản

### Chủ đề cần nắm
- Unit test
- Integration test
- Edge cases và boundary cases
- Assertions
- Deterministic vs flaky test

### Tư duy quan trọng
- Test không chứng minh chương trình đúng tuyệt đối, nhưng giúp phát hiện sai nhanh và bảo vệ behavior khi refactor.
- Input rỗng, cực nhỏ, cực lớn, duplicated, invalid luôn phải được nghĩ tới.

---

## 6. Complexity và resource awareness ở mức lập trình

Ngay cả trước khi học sâu thuật toán, bạn cần tự hỏi:

- Hàm này tốn bao nhiêu thời gian theo kích thước input?
- Có tạo copy không cần thiết không?
- Có giữ data quá lâu trong memory không?
- Có vòng lặp lồng nhau vô ý không?

### Ví dụ lỗi phổ biến
- Nối string trong loop dài
- Query trong loop
- Deep copy object lớn liên tục
- Recursion sâu không kiểm soát leading to stack overflow

---

## 7. Engineering hygiene cơ bản

### Nền tảng cần có
- Naming rõ ràng
- Formatting nhất quán
- Functions ngắn, module rõ trách nhiệm
- Git basics: commit nhỏ, message rõ, review dễ hiểu
- README, docs, scripts để người khác chạy được

### Kỹ năng không thể bỏ qua
- Đọc code người khác
- Viết comment khi thật cần thiết
- Tách code production và code thử nghiệm
- Không hardcode config/secrets

---

## ✅ Checklist ôn tập
- Giải thích được khác biệt giữa value và reference
- Tự mô tả được lifecycle của một function call trong stack
- Biết viết test cho edge cases
- Có thể debug một bug bằng cách thu nhỏ phạm vi tìm kiếm
- Phân biệt được code smell do naming, abstraction, state management

## 📝 Bài tập
1. Viết lại một script 100-200 dòng thành các hàm/module rõ hơn.
2. Tạo 10 test cases cho một hàm parse input.
3. Debug một bug do mutation ngoài ý muốn.
4. Viết một CLI nhỏ đọc file CSV và sinh summary.
5. Giải thích bằng lời sự khác nhau giữa recursion và loop trên cùng một bài toán.

## 📚 Tài liệu
- *Code Complete* — Steve McConnell
- *The Pragmatic Programmer* — Hunt & Thomas
- *Structure and Interpretation of Computer Programs* — Abelson & Sussman