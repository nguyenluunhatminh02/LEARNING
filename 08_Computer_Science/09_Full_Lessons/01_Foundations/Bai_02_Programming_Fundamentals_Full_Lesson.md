# Bài 02: Programming Fundamentals — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- hiểu chương trình là mô hình biến đổi state chứ không chỉ là syntax
- nắm value, reference, scope, lifetime, control flow, recursion và debugging discipline
- viết code có cấu trúc rõ hơn và ít lỗi logic cơ bản hơn

## Bạn cần biết trước
- biết viết một số đoạn code đơn giản ở ít nhất một ngôn ngữ
- biết if/else, loop, function ở mức nhập môn

---

## 1. Chương trình là gì

Một chương trình có thể được nhìn như:
- nhận input
- đọc và cập nhật state
- tạo output
- có thể tương tác với file, network, user hoặc database

Điều này nghe hiển nhiên, nhưng rất nhiều bug đến từ việc bạn không biết chính xác state nào đang tồn tại, bị sửa ở đâu, và sống bao lâu.

---

## 2. Value, reference và mutation

### 2.1 Value
Value là dữ liệu bạn thao tác, ví dụ `5`, `true`, `"hello"`.

### 2.2 Reference
Reference là cách một biến trỏ tới hoặc nắm quyền truy cập một object nào đó.

### 2.3 Mutation
Mutation là thay đổi state hiện có.

Một bug kinh điển:
- bạn truyền một object vào hàm
- hàm sửa object đó
- caller không biết object đã bị đổi

Đây là lý do phải hiểu rõ semantics của ngôn ngữ mình dùng.

---

## 3. Scope và lifetime

### Scope
Biến nhìn thấy ở đâu trong code.

### Lifetime
Biến hoặc object thực sự tồn tại bao lâu trong runtime.

Hai thứ này liên quan nhưng không trùng nhau.

Ví dụ:
- một biến local có scope trong function
- nhưng object mà nó trỏ tới có thể còn sống sau khi function kết thúc nếu vẫn còn reference khác giữ nó

---

## 4. Control flow

Control flow là trật tự thực thi của chương trình.

Các thành phần chính:
- sequence
- conditionals
- loops
- recursion
- exceptions

Mỗi lần bạn viết branch hoặc loop, bạn đang chia không gian trạng thái của chương trình thành nhiều đường đi. Code càng nhiều đường đi, reasoning càng khó.

---

## 5. Functions và abstraction

Function nên giúp bạn:
- chia nhỏ vấn đề
- đặt tên cho một thao tác rõ ràng
- cô lập logic để test và reuse

Một function tốt thường có:
- input rõ ràng
- output rõ ràng
- ít side effects bất ngờ
- một mục tiêu chính

Nếu một function dài 100 dòng, dùng nhiều flags, sửa nhiều state và gọi nhiều dependency, gần như chắc chắn nó đang làm quá nhiều việc.

---

## 6. Recursion như một công cụ reasoning

Recursion không chỉ là trick phỏng vấn. Nó là cách diễn tả bài toán lặp theo cấu trúc tự nhiên.

Bạn cần luôn kiểm tra 3 thứ:
- base case là gì
- recursive case giảm bài toán ra sao
- có nguy cơ recursion quá sâu không

Recursion tốt khi cấu trúc dữ liệu tự nhiên là tree hoặc problem giảm thành subproblem rõ ràng.

---

## 7. Debugging discipline

Đây là một kỹ năng nền tảng của engineer giỏi.

Quy trình nên thành phản xạ:
1. Reproduce bug.
2. Thu nhỏ case gây lỗi.
3. Ghi expected vs actual.
4. Kiểm tra assumptions.
5. Xác định root cause.
6. Thêm test hoặc guard nếu phù hợp.

Không nên:
- sửa ba nơi cùng lúc
- log vô định không có hypothesis
- kết luận quá sớm từ một dấu hiệu phụ

---

## 8. Ví dụ phân tích bug mutation

Giả sử bạn có hàm nhận list users rồi sắp xếp nó để hiển thị. Nếu hàm sort in-place, caller có thể bị thay đổi dữ liệu gốc mà không biết.

Điểm cần hỏi:
- function này nên mutate input hay tạo bản sao?
- contract đã nói rõ chưa?
- test có cover việc object đầu vào bị đổi không?

Từ một ví dụ nhỏ như vậy, bạn học được rất nhiều về API design và side effects.

---

## 9. Code structure và readability

3 thứ cải thiện code nhanh nhất:
- naming tốt
- functions nhỏ hơn
- boundaries rõ hơn giữa input parsing, business logic, side effects

Khi review code, hãy hỏi:
- nếu đổi cách đọc input thì business logic có cần sửa không?
- nếu đổi storage layer thì core logic có bị kéo theo không?
- nếu bug xảy ra ở giữa flow, mình có biết state đang ở đâu không?

---

## 10. Checklist sau bài
- Giải thích được difference giữa value, reference và mutation
- Phân biệt được scope với lifetime
- Mô tả được loop, recursion và exception như các nhánh control flow
- Có quy trình debug rõ ràng thay vì thử mò
- Viết được function với contract rõ hơn trước

## 11. Bài tập thực hành
1. Chọn một hàm cũ của bạn và viết lại với tên biến rõ hơn.
2. Viết một ví dụ bug do mutation ngoài ý muốn và sửa nó.
3. Viết một hàm đệ quy và một hàm lặp giải cùng bài toán.
4. Tạo 8 test cases cho một hàm parse input text.
5. Viết một checklist debug 6 bước cho chính bạn.

## 12. Mini deliverable
Viết một note 1 trang gồm:
- thế nào là side effect
- khi nào mutation là hợp lý
- 3 lỗi debugging bạn hay gặp nhất

## 13. Học tiếp
- `Bai_03_Computer_Organization_Full_Lesson.md`
- `../../08_Reference_and_Review/02_Foundations_Deep_Dive.md`