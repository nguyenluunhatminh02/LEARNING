# Bài 18: Theory of Computation — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- hiểu vì sao có giới hạn căn bản đối với computation
- nắm automata, grammars, computability và complexity classes ở mức đủ chắc
- dùng theory để reasoning tốt hơn về bài toán khó, parser, verification và optimization

## Bạn cần biết trước
- Bài 01, 04, 06 là nền rất tốt

---

## 1. Vì sao theory vẫn quan trọng

Theory of Computation dạy bạn 3 điều lớn:
- không phải mọi bài toán đều giải được tổng quát
- không phải bài toán nào giải được cũng giải nhanh được
- cấu trúc formal của bài toán giúp chọn hướng tiếp cận đúng hơn

Đây là phần tăng chất lượng tư duy, không chỉ tăng thuật ngữ bạn biết.

---

## 2. Formal languages và automata

### Những khái niệm đầu tiên
- alphabet
- string
- language
- regular language
- DFA/NFA

### Vì sao có ích
- regex và tokenization
- state machine thinking
- protocol/workflow modeling

Nếu bạn làm parser, protocol hoặc validation, phần này không hề xa thực tế.

---

## 3. Grammars và parsing

### Context-free grammars
Cho phép biểu diễn cấu trúc lồng nhau như biểu thức toán hoặc chương trình.

### Tại sao quan trọng
- compiler/parser
- config formats
- DSLs

Thông điệp lớn là: regex không đủ cho mọi thứ có cấu trúc nested.

---

## 4. Computability

Ý tưởng cốt lõi:
- có những bài toán không có thuật toán tổng quát luôn đúng và luôn dừng

Ví dụ kinh điển là halting problem.

Không cần lao vào proof quá sớm, nhưng bạn phải internalize giới hạn này vì nó ảnh hưởng tới static analysis, verification và automation nói chung.

---

## 5. Complexity classes

### Những cái nên biết
- P
- NP
- NP-hard
- NP-complete

### Bài học lớn
Nếu một bài toán có flavor NP-hard, bạn nên bắt đầu nghĩ tới:
- exploit cấu trúc đặc biệt
- heuristic
- approximation
- bounded search

Chứ không phải cứ mặc định exact solution cho scale rất lớn.

---

## 6. Reductions

Reduction giúp bạn:
- chứng minh một bài toán khó không kém bài khác
- chuyển bài lạ về bài quen
- xây intuition về "hình dạng" của độ khó

Đây là một kỹ năng tư duy rất đáng giá, không chỉ là trick lý thuyết.

---

## 7. Liên hệ với engineering thực tế

Theory chạm vào rất nhiều nơi:
- parser design
- SAT/constraint solving
- scheduling
- route optimization
- compiler analysis
- formal verification

Nó không phải thứ tách biệt hoàn toàn khỏi systems và software engineering.

---

## 8. Sai lầm phổ biến
- nghĩ theory hoàn toàn vô dụng cho engineering
- học thuộc định nghĩa nhưng không nối được với ví dụ thật
- thấy NP-hard rồi bỏ cuộc luôn dù bài toán thực tế có cấu trúc đặc biệt dễ hơn

---

## 9. Checklist sau bài
- Giải thích được regular language và CFG ở mức high-level
- Hiểu decidable vs undecidable
- Phân biệt được P, NP, NP-hard, NP-complete
- Nhìn ra khi nào nên nghĩ tới heuristic hoặc approximation

## 10. Bài tập thực hành
1. Tạo DFA cho một pattern chuỗi đơn giản.
2. Viết grammar mini cho biểu thức cộng trừ nhân chia.
3. Viết note 1 trang về halting problem và ý nghĩa của nó.
4. Phân loại 10 bài toán quen thuộc theo độ khó ở mức trực giác.
5. Tìm một ví dụ reduction đơn giản.

## 11. Mini deliverable
Tạo file `theory_for_engineers.md` gồm:
- automata intuition
- grammar intuition
- computability limits
- complexity classes and decisions

## 12. Học tiếp
- `Bai_19_Graphics_HCI_AI_and_Electives_Full_Lesson.md`
- `../../08_Reference_and_Review/08_Theory_and_Specialized_Deep_Dive.md`