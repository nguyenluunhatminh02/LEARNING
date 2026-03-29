# Bài 03: Computer Organization — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- hiểu dữ liệu và lệnh được biểu diễn thế nào trong máy tính
- nắm CPU, registers, cache, RAM, I/O và memory hierarchy ở mức đủ dùng cho engineer
- có trực giác tốt hơn về performance, memory layout và hardware-related bugs

## Bạn cần biết trước
- binary ở mức sơ lược là lợi thế nhưng không bắt buộc
- nên đã học xong Bài 02

---

## 1. Từ code tới máy tính thực sự làm gì

Khi bạn viết code, CPU không đọc Python, Java hay C trực tiếp. Cuối cùng, hệ thống luôn phải đi về:
- instructions
- data in memory
- control flow
- reads/writes tới hardware interfaces

Hiểu điểm này giúp bạn bớt nghĩ máy tính như một hộp đen.

---

## 2. Biểu diễn dữ liệu

### 2.1 Binary và hex
Máy tính làm việc với bits. Hex chỉ là cách con người viết gọn binary hơn.

### 2.2 Signed integers và two's complement
Two's complement là cách rất phổ biến để biểu diễn số âm.

Bạn không nhất thiết phải thuộc hết phép biến đổi ngay, nhưng nên hiểu:
- có giới hạn số biểu diễn được
- overflow là hiện tượng có thật

### 2.3 Floating point
Floating point không phải số thực toán học. Nó là xấp xỉ hữu hạn.

Điều này giải thích tại sao:
- cộng/trừ các số thập phân có thể ra kết quả lạ
- finance thường không nên dùng float cho tiền

### 2.4 Text encoding
Phải phân biệt:
- character
- code point
- byte sequence
- encoding như UTF-8

Nhiều bug text thật ra là bug nhầm lẫn giữa các khái niệm này.

---

## 3. CPU ở mức engineer

CPU có những thành phần bạn nên biết:
- registers
- ALU
- control logic
- program counter

Một instruction thường đi qua ý tưởng đơn giản:
- fetch
- decode
- execute

Không cần đi quá sâu vào vi kiến trúc, nhưng bạn nên hiểu CPU không chạy "câu lệnh cấp cao" như bạn tưởng, mà chạy instructions nhỏ, đọc/ghi registers và memory liên tục.

---

## 4. Memory hierarchy

Đây là một trong những phần quan trọng nhất của bài.

Thứ tự từ nhanh đến chậm thường là:

```text
Registers -> L1/L2/L3 cache -> RAM -> SSD/HDD -> network storage
```

Ý nghĩa thực tế:
- càng gần CPU, càng nhanh và nhỏ
- càng xa, càng chậm nhưng lớn hơn
- access pattern ảnh hưởng cực mạnh tới tốc độ thực thi

### Locality
- Temporal locality: dữ liệu dùng gần đây có thể sắp dùng lại
- Spatial locality: dữ liệu gần nhau trong memory thường được truy cập gần nhau

Đây là lý do array scan thường rất nhanh.

---

## 5. Stack, heap và layout dữ liệu

### Stack
- thường dùng cho function calls, local variables, return addresses
- nhanh và có structure rõ

### Heap
- vùng cấp phát động
- linh hoạt hơn nhưng khó reasoning hơn

### Layout matters
Hai thuật toán cùng Big-O có thể chạy khác nhau rất nhiều nếu layout data khác nhau.

Ví dụ:
- array liên tục trong memory rất cache-friendly
- linked list pointer-chasing có locality kém hơn

---

## 6. I/O và cost model

Đọc RAM đã chậm hơn cache. Đọc disk còn chậm hơn rất nhiều. Đi qua network còn thêm latency, serialization và failure.

Đây là lý do vì sao các kỹ thuật sau tồn tại:
- buffering
- batching
- caching
- async I/O
- prefetching

Nếu bạn quên cost model của I/O, bạn rất dễ thiết kế code nhìn đẹp nhưng vận hành chậm.

---

## 7. Ví dụ tư duy performance

Giả sử bạn cần xử lý 10 triệu phần tử.

Hai hướng tiếp cận:
- dùng array liên tục, scan tuần tự
- dùng cấu trúc pointer-heavy, mỗi bước nhảy tới một object ở vùng nhớ khác

Dù complexity lý thuyết có thể gần nhau, cách thứ nhất thường nhanh hơn rõ rệt vì locality và cache behavior tốt hơn.

Đây là bài học rất quan trọng: Big-O không phải toàn bộ câu chuyện.

---

## 8. Sai lầm phổ biến
- nghĩ hardware details không liên quan tới application code
- nhầm RAM với storage bền vững
- bỏ qua encoding khi làm text đa ngôn ngữ
- chỉ nhìn asymptotic complexity mà không nghĩ tới locality, allocations và I/O

---

## 9. Checklist sau bài
- Giải thích được integer, float và text được biểu diễn khác nhau như thế nào
- Mô tả được memory hierarchy và vì sao cache quan trọng
- Phân biệt được stack và heap ở mức thực dụng
- Hiểu vì sao layout dữ liệu ảnh hưởng performance
- Có trực giác ban đầu về I/O cost model

## 10. Bài tập thực hành
1. Chuyển vài số decimal sang binary và hex.
2. Tự giải thích vì sao `0.1 + 0.2` có thể gây bất ngờ trong một số ngôn ngữ.
3. Viết note ngắn so sánh array và linked list dưới góc nhìn cache.
4. Tìm một bug encoding thật và mô tả nguyên nhân.
5. Vẽ sơ đồ memory hierarchy từ CPU tới network storage.

## 11. Mini deliverable
Viết một note 1-2 trang tên là `Why hardware still matters for software engineers`, trong đó giải thích:
- memory hierarchy
- stack vs heap
- I/O cost model

## 12. Học tiếp
- `../02_Algorithms_and_Data/Bai_04_Complexity_and_Problem_Solving_Full_Lesson.md`
- `../../08_Reference_and_Review/02_Foundations_Deep_Dive.md`