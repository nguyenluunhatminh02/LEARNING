# Bài 18: Theory of Computation

## 🎯 Mục tiêu
- Hiểu giới hạn căn bản của computation: cái gì biểu diễn được, quyết định được, tối ưu được
- Nắm automata, formal languages, computability và complexity classes ở mức đủ chắc
- Dùng lý thuyết để có tư duy sâu hơn khi đối mặt với bài toán khó

## 📖 Bức tranh lớn
Theory of Computation dạy bạn rằng không phải mọi bài toán đều giải được, và không phải bài nào giải được cũng giải nhanh được. Đây là một trong những mảng giúp engineer trưởng thành về tư duy nhất: biết khi nào tiếp tục tối ưu, khi nào chấp nhận approximation, khi nào đổi formulation của bài toán.

---

## 1. Formal languages và automata

### Chủ đề cần nắm
- Alphabet, strings, language
- Regular languages
- Finite automata: DFA, NFA
- Regular expressions

### Ứng dụng thực tế
- Lexers
- Pattern matching
- Validation rules
- Log filtering

---

## 2. Context-free grammars và parsing

### Chủ đề cần nắm
- Grammar, productions
- Parse tree
- Context-free languages
- Pushdown automata ở mức overview

### Ứng dụng
- Programming language parsing
- Query languages
- Config formats

---

## 3. Turing machines và computability

### Ý tưởng cốt lõi
- Turing machine là model tổng quát của computation
- Church-Turing thesis ở mức khái niệm
- Decidable vs undecidable problems
- Halting problem là ví dụ kinh điển

### Trực giác quan trọng
Có những bài toán không tồn tại thuật toán tổng quát để giải cho mọi input.

---

## 4. Complexity classes

### Cần nắm
- P
- NP
- NP-hard
- NP-complete
- PSPACE ở mức nhận biết

### Tư duy đúng
- NP không có nghĩa là "không giải được"
- Bài toán nhỏ hoặc cấu trúc đặc biệt vẫn có thể giải thực tế rất tốt
- Phân loại complexity giúp chọn exact, heuristic hoặc approximation strategy

---

## 5. Reductions

### Vì sao reductions quan trọng
- Chứng minh một bài toán ít nhất khó như bài toán khác
- Chuyển một bài lạ về bài quen
- Xây intuition về cấu trúc khó của bài toán

### Ứng dụng thực tế
- Scheduling, packing, routing, optimization thường có thể nhìn dưới lăng kính reductions

---

## 6. Vì sao engineer vẫn nên học phần này

- Đỡ sa vào tối ưu vô vọng khi bài toán quá khó
- Tăng khả năng mô hình hóa bài toán mới
- Hỗ trợ compiler, PL, verification, algorithms, research mindset
- Cho bạn ngôn ngữ để nói về limits và trade-offs một cách chính xác hơn

---

## 7. Học theory theo cách thực dụng

### Không cần làm gì quá mức lúc đầu
- Không cần formal proof cực dài ngay lập tức
- Không cần nhớ mọi định nghĩa như thi học phần

### Nên làm
- Hiểu ý tưởng bằng ví dụ
- Tự phân loại vài bài toán quen thuộc
- Liên kết theory với regex, parser, SAT, graph problems, optimization

---

## ✅ Checklist ôn tập
- Giải thích được regular language và finite automata ở mức cơ bản
- Hiểu CFG liên quan trực tiếp đến parsing ra sao
- Biết decidable và undecidable khác nhau thế nào
- Phân biệt được P, NP, NP-hard, NP-complete
- Có trực giác khi nào nên nghĩ tới reductions hoặc approximation

## 📝 Bài tập
1. Tự tạo DFA cho một pattern chuỗi đơn giản.
2. Viết note 1 trang về halting problem và ý nghĩa của nó.
3. Phân loại 10 bài toán bạn biết thành easy polynomial, likely NP-hard, hoặc chưa rõ.
4. Tìm ví dụ reduction đơn giản giữa hai bài toán quen thuộc.
5. Liên hệ CFG với parser của ngôn ngữ bạn đang dùng.

## 📚 Tài liệu
- *Introduction to the Theory of Computation* — Michael Sipser
- *Automata and Computability* — Kozen