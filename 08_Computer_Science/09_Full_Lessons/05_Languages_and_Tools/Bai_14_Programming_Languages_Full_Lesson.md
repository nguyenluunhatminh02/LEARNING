# Bài 14: Programming Languages — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- hiểu các trục thiết kế quan trọng của ngôn ngữ lập trình
- nắm type systems, paradigms, memory models và ecosystem trade-offs ở mức practical
- có framework để học ngôn ngữ mới nhanh và chọn ngôn ngữ phù hợp cho một project

## Bạn cần biết trước
- đã học tốt foundations và systems cơ bản

---

## 1. Nhìn một ngôn ngữ như một tập trade-off

Không có ngôn ngữ tốt nhất tuyệt đối. Mỗi ngôn ngữ tối ưu cho một tập mục tiêu:
- safety
- performance
- developer productivity
- runtime portability
- concurrency model
- ecosystem

Học phần này giúp bạn bớt tranh luận cảm tính và tăng khả năng chọn công cụ hợp lý.

---

## 2. Syntax, semantics và abstraction

### Syntax
Ngôn ngữ được viết ra sao.

### Semantics
Code có nghĩa gì khi thực thi.

### Abstraction
Những gì ngôn ngữ cho phép bạn che giấu hoặc mô hình hóa gọn hơn.

Điều quan trọng là syntax đẹp chưa chắc đồng nghĩa semantics dễ reasoning.

---

## 3. Type systems

### Các trục nên phân biệt
- static vs dynamic typing
- nominal vs structural typing
- inference vs explicit typing
- generics/templates
- nullability/options

### Types giúp gì
- bắt lỗi sớm
- làm contracts rõ hơn
- hỗ trợ tooling và refactor

### Types không tự động giải quyết gì
- domain model dở
- logic business sai
- design API tệ

---

## 4. Programming paradigms

### Procedural / imperative
Rõ cost model và control flow.

### OOP
Mạnh khi model stateful domains vừa phải, nhưng dễ bị lạm dụng inheritance.

### Functional
Mạnh ở reasoning, immutability, composition.

### Declarative
Thường dùng khi bạn muốn mô tả cái gì cần có thay vì từng bước làm thế nào.

Điều quan trọng là hiểu paradigm nào hợp problem nào.

---

## 5. Memory management models

### Manual memory
Control cao nhưng bug class nặng.

### Garbage collection
Productivity cao hơn nhưng có runtime trade-offs.

### Ownership / borrowing
Safety mạnh mà không cần GC, nhưng learning curve cao hơn.

Ngôn ngữ không chỉ là cú pháp. Runtime behavior của memory model ảnh hưởng trực tiếp tới latency, footprint và operability.

---

## 6. Error handling

Các mô hình phổ biến:
- exceptions
- result/either style
- error codes
- panic/fail-fast

Điểm cần suy nghĩ:
- lỗi nào recoverable
- lỗi nào nên bubble up
- API có ép caller xử lý lỗi hay không

Chọn error model ảnh hưởng rất nhiều tới readability và reliability.

---

## 7. Concurrency support theo ngôn ngữ

Ngôn ngữ có thể hỗ trợ concurrency bằng:
- native threads
- coroutines/green threads
- async-await
- channels/CSP
- actor libraries

Khi đánh giá, hãy hỏi:
- model này hợp workload nào?
- tooling/debugging tốt không?
- runtime scheduler có đáng tin không?

---

## 8. Ecosystem và tooling

Một ngôn ngữ trong thực tế không tách rời:
- package manager
- build system
- stdlib
- formatter/linter
- debugger/profiler
- deployment story

Đây là lý do ngôn ngữ rất đẹp về lý thuyết chưa chắc là lựa chọn tốt nhất cho team.

---

## 9. Chọn ngôn ngữ cho project

Hãy hỏi:
- workload CPU-bound, I/O-bound hay latency-sensitive?
- team đã mạnh ngôn ngữ nào?
- cần hiring dễ không?
- ecosystem có thư viện cần thiết không?
- runtime footprint và ops constraints là gì?

Đây là một bài toán trade-off, không phải niềm tin cá nhân.

---

## 10. Checklist sau bài
- Giải thích được static vs dynamic typing và trade-off của chúng
- So sánh được paradigms chính ở mức practical
- Hiểu GC, manual memory, ownership khác nhau ra sao
- Đánh giá được một ngôn ngữ mới qua type system, runtime và tooling
- Có framework cơ bản để chọn ngôn ngữ cho project

## 11. Bài tập thực hành
1. So sánh Python, Go, Java, Rust, JavaScript trên 5 tiêu chí.
2. Viết note 1 trang về type systems.
3. Chọn một ngôn ngữ bạn ít biết và phân tích theo framework của bài.
4. So sánh 2 error models của 2 ngôn ngữ bạn dùng.
5. Chọn ngôn ngữ cho một backend service và giải thích vì sao.

## 12. Mini deliverable
Tạo file `language_evaluation_template.md` gồm:
- type system
- memory model
- runtime
- tooling
- ecosystem
- best-fit workloads

## 13. Học tiếp
- `Bai_15_Compilers_and_Runtimes_Full_Lesson.md`
- `../../08_Reference_and_Review/06_Languages_and_Tools_Deep_Dive.md`