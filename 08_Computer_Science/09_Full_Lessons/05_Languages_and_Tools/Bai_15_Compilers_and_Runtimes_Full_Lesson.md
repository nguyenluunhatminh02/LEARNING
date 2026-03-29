# Bài 15: Compilers and Runtimes — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- hiểu pipeline từ source code tới machine code hoặc bytecode
- nắm vai trò của lexer, parser, AST, semantic analysis, IR, linking và loading
- có trực giác tốt hơn về VM, JIT, AOT, GC và runtime behavior

## Bạn cần biết trước
- Bài 14
- foundations về abstraction và computer organization hỗ trợ rất nhiều

---

## 1. Vì sao compiler và runtime đáng học với mọi engineer

Phần này không chỉ dành cho compiler engineers.

Nó giúp bạn:
- đọc error messages sâu hơn
- hiểu build pipeline tốt hơn
- biết vì sao ngôn ngữ của bạn có các guarantees nhất định
- lý giải performance behavior và runtime quirks tốt hơn

---

## 2. Compiler pipeline tổng quan

Một pipeline điển hình:

```text
source code
-> lexing
-> parsing
-> AST
-> semantic analysis
-> IR
-> optimization
-> code generation
-> linking/loading
-> execution
```

Không phải ngôn ngữ nào cũng đi đúng mọi bước theo cùng cách, nhưng mental model này rất hữu ích.

---

## 3. Lexing, parsing và AST

### Lexing
Biến text thành tokens.

### Parsing
Biến tokens thành structure theo grammar.

### AST
Biểu diễn cú pháp ở mức trừu tượng hơn parse tree, rất hữu ích cho compiler và tooling.

Điều quan trọng: formatter, linter, IDE refactor đều dựa nhiều vào AST thinking.

---

## 4. Semantic analysis

Đây là giai đoạn kiểm tra những thứ syntax alone không đủ:
- name resolution
- scope
- type checking
- symbol table construction

Đây là lý do một số lỗi được bắt trước runtime.

---

## 5. Intermediate Representation và optimization

IR giúp compiler làm việc trên representation thuận tiện hơn source hoặc machine code.

### Một số optimization nên biết tên
- constant folding
- dead code elimination
- inlining
- common subexpression elimination

### Trade-off
Optimization có thể tăng compile time, code size hoặc làm debugging khó hơn.

---

## 6. Linking và loading

### Linking
Ghép các object files và libraries lại với nhau.

### Loading
OS nạp chương trình vào memory và chuyển control để nó chạy.

Đây là nơi package/build toolchain gặp runtime reality.

---

## 7. Interpreter, VM, JIT và AOT

### Interpreter
Thực thi trực tiếp source/AST/bytecode.

### VM
Cung cấp execution environment trừu tượng hơn machine thật.

### JIT
Compile trong quá trình chạy.

### AOT
Compile trước khi chạy.

### Tư duy đúng
JIT có thể tối ưu tốt ở steady-state nhưng cold start khác AOT rất nhiều.

---

## 8. Runtime services

Runtime thường lo những việc như:
- memory management / GC
- exception handling
- dynamic dispatch
- reflection
- stack unwinding
- threading or coroutine scheduling tùy ecosystem

Vì vậy runtime behavior tác động trực tiếp đến operability và performance.

---

## 9. GC ở mức thực dụng

Bạn không cần học hết các thuật toán GC ngay, nhưng nên hiểu:
- allocation rate ảnh hưởng GC pressure
- short-lived vs long-lived objects khác nhau
- GC pauses có thể ảnh hưởng tail latency
- tuning GC là bài toán production có thật

---

## 10. Checklist sau bài
- Mô tả được compiler pipeline từ source tới execution
- Giải thích được lexer, parser, AST, semantic analysis, IR dùng để làm gì
- Phân biệt được interpreter, VM, JIT, AOT
- Hiểu vai trò của linker, loader và runtime
- Có trực giác ban đầu về GC và runtime trade-offs

## 11. Bài tập thực hành
1. Đọc một chương của *Crafting Interpreters* và tóm tắt lại.
2. Viết grammar mini cho biểu thức số học.
3. So sánh Python, Java, Go, Rust về execution model.
4. Viết note giải thích vì sao AST hữu ích cho tooling.
5. Tìm một case runtime/GC ảnh hưởng performance và mô tả nó.

## 12. Mini deliverable
Tạo file `compiler_runtime_map.md` gồm:
- pipeline stages
- key artifacts
- runtime services
- examples từ 2-3 ngôn ngữ thực tế

## 13. Học tiếp
- `../06_Software_and_Security/Bai_16_Software_Engineering_Full_Lesson.md`
- `../../08_Reference_and_Review/06_Languages_and_Tools_Deep_Dive.md`