# Bài 14: Programming Languages

## 🎯 Mục tiêu
- Hiểu các quyết định thiết kế của ngôn ngữ lập trình và ảnh hưởng của chúng tới correctness, ergonomics và performance
- Nắm type systems, paradigms, memory management models, modules và interoperability
- Có framework để học ngôn ngữ mới nhanh và chọn ngôn ngữ phù hợp với bài toán

## 📖 Bức tranh lớn
Ngôn ngữ lập trình là cách ta mô hình hóa computation. Mỗi ngôn ngữ tối ưu cho một tập trade-off: tốc độ, an toàn, developer productivity, concurrency, runtime portability, ecosystem. Khi hiểu nguyên lý bên dưới, bạn sẽ bớt tranh luận cảm tính kiểu "ngôn ngữ nào tốt nhất".

---

## 1. Syntax, semantics và abstraction

### Chủ đề cần nắm
- Syntax: ngôn ngữ viết ra sao
- Semantics: chương trình nghĩa là gì khi chạy
- Scope, binding, lifetime
- Name resolution
- Modules/packages/namespaces

### Tư duy đúng
- Cùng một syntax đẹp chưa chắc dẫn tới semantics đơn giản
- Abstraction tốt làm giảm bug; abstraction tệ che mất cost model

---

## 2. Type systems

### Những trục so sánh quan trọng
- Static vs dynamic typing
- Strong vs weak typing ở mức cẩn trọng
- Nominal vs structural typing
- Inference vs explicit typing
- Generics/templates
- Nullability / option types

### Lợi ích của types
- Bắt lỗi sớm
- Làm documentation sống
- Hỗ trợ refactor, autocomplete, API clarity

### Cảnh báo
- Type system mạnh không thay thế domain modeling tốt
- Dynamic language nhanh cho khám phá nhưng cần discipline hơn ở testing và observability

---

## 3. Programming paradigms

### Imperative / procedural
- Điều khiển state và steps rõ ràng

### Object-oriented
- Encapsulation, inheritance, polymorphism
- Hữu ích nhưng dễ bị lạm dụng thành hierarchy phức tạp

### Functional
- Immutability, pure functions, higher-order functions
- Rất mạnh cho concurrency và reasoning

### Declarative / logic / dataflow ở mức overview
- SQL, Prolog, build systems, stream processing DSLs

---

## 4. Memory management models

### Manual memory management
- C/C++ style, cho control cao nhưng risk lớn

### Garbage collection
- Developer productivity tốt hơn
- Trade-off là GC pauses, memory overhead, runtime complexity

### Ownership / borrow models
- Rust-style safety without GC
- Đòi hỏi tư duy lifetime rõ ràng hơn

### Ứng dụng
- Language choice ảnh hưởng latency profile, systems programming suitability, ops behavior

---

## 5. Error handling và effect management

### Các cách phổ biến
- Exceptions
- Result/Either style
- Error codes
- Panic/fail-fast

### Câu hỏi đúng
- Error nào recoverable?
- Error nào nên bubble up?
- API có ép caller xử lý lỗi hay không?

---

## 6. Concurrency support theo ngôn ngữ

### Ví dụ các model
- Native threads
- Async/await
- CSP/channels
- Actor model libraries
- Green threads/coroutines

### Điều cần suy nghĩ
- Runtime scheduler có giúp hay che giấu complexity?
- Debugging concurrent code của hệ sinh thái đó có tốt không?

---

## 7. Interoperability và ecosystem

### Chủ đề cần nắm
- FFI
- ABI compatibility ở mức overview
- Package managers
- Build tools
- Standard library quality

### Vì sao quan trọng
- Một ngôn ngữ tốt về lý thuyết nhưng ecosystem yếu có thể khiến dự án chậm đi nhiều
- Runtime deployment, tooling, observability ảnh hưởng lớn đến chi phí thực tế

---

## 8. Framework chọn ngôn ngữ

### Hỏi trước khi chọn
- Bài toán CPU-bound, I/O-bound hay latency-critical?
- Team mạnh ngôn ngữ nào?
- Ecosystem thư viện và tuyển dụng ra sao?
- Runtime footprint có giới hạn không?
- Safety/performance/productivity cần ưu tiên gì?

---

## ✅ Checklist ôn tập
- Giải thích được static vs dynamic typing và trade-off của chúng
- So sánh được OOP, functional, procedural ở mức thực dụng
- Hiểu GC, manual memory, ownership khác nhau thế nào
- Biết cách nhìn ngôn ngữ mới qua type system, runtime, package ecosystem
- Có framework chọn ngôn ngữ cho một project thật

## 📝 Bài tập
1. So sánh Python, Go, Java, Rust, JavaScript trên 5 tiêu chí của bạn.
2. Viết note 1 trang về type systems.
3. Chọn một tính năng ngôn ngữ bạn ít dùng và học sâu 1 ngày.
4. Giải thích vì sao cùng một API design có thể đẹp trong ngôn ngữ này nhưng awkward trong ngôn ngữ khác.
5. Xem qua FFI của một ngôn ngữ bạn đang dùng.

## 📚 Tài liệu
- *Programming Language Pragmatics* — Michael Scott
- *Types and Programming Languages* — Benjamin Pierce
- *Crafting Interpreters* — Robert Nystrom