# Bài 15: Compilers and Runtimes

## 🎯 Mục tiêu
- Hiểu pipeline từ source code đến machine code hoặc bytecode
- Nắm lexer, parser, AST, semantic analysis, IR, optimization, code generation, linking/loading
- Biết interpreter, VM, JIT, AOT, GC và runtime services ảnh hưởng thế nào tới behavior chương trình

## 📖 Bức tranh lớn
Compiler và runtime là lớp biến ý tưởng của bạn thành thứ CPU thật sự chạy được. Học phần này giúp bạn hiểu error messages sâu hơn, tối ưu performance có cơ sở hơn, debug weird runtime behavior tốt hơn, và nhìn ngôn ngữ lập trình như một hệ thống hoàn chỉnh chứ không chỉ là syntax.

---

## 1. Compiler pipeline tổng quan

```text
Source code
  -> Lexing
  -> Parsing
  -> AST
  -> Semantic analysis / type checking
  -> Intermediate Representation (IR)
  -> Optimization
  -> Code generation
  -> Linking / loading
  -> Execution
```

---

## 2. Lexing, parsing và AST

### Lexing
- Tokenize source thành identifiers, keywords, literals, operators

### Parsing
- Xây parse tree/AST theo grammar
- Hiểu precedence và associativity

### AST
- Cấu trúc trung gian để compiler/interpreter làm việc tiếp

### Tại sao quan trọng
- Rất nhiều tooling hiện đại như formatter, linter, refactoring, IDE đều dựa trên AST

---

## 3. Semantic analysis và type checking

### Chủ đề cần nắm
- Symbol table
- Scope resolution
- Type checking
- Name binding
- Desugaring ở mức overview

### Kết quả
- Nhiều lỗi được phát hiện trước khi chương trình chạy
- Compiler có nhiều thông tin hơn để tối ưu

---

## 4. Intermediate Representation và optimization

### IR là gì
- Một representation trung gian dễ phân tích/tối ưu hơn source code hoặc machine code

### Một số optimization phổ biến
- Constant folding
- Dead code elimination
- Inlining
- Common subexpression elimination
- Loop optimizations ở mức overview

### Điều cần nhớ
- Tối ưu không miễn phí; compile time, debugability và code size cũng là trade-off

---

## 5. Code generation, linking và loading

### Code generation
- Chuyển IR thành machine code hoặc bytecode

### Linking
- Ghép các object files/libraries
- Static vs dynamic linking

### Loading
- Hệ điều hành nạp chương trình vào memory
- Resolve symbols, setup process image, transfer control

---

## 6. Interpreters, VMs và JIT/AOT

### Interpreter
- Thực thi trực tiếp AST/bytecode
- Linh hoạt, dễ debug, nhưng thường chậm hơn native compiled code

### Virtual machine
- JVM, CLR, WASM runtimes, Python VM ở mức nào đó
- Cung cấp portability và runtime services

### JIT vs AOT
- JIT: tối ưu khi chạy, tốt cho adaptive optimization
- AOT: predictable startup/deployment hơn

---

## 7. Garbage collection và runtime services

### Chủ đề cần nắm
- Reference counting
- Mark-and-sweep
- Generational GC
- Stop-the-world vs concurrent GC ở mức overview
- Stack unwinding, exception handling
- Reflection, dynamic dispatch, runtime metadata

### Liên hệ production
- GC behavior ảnh hưởng latency, memory footprint, tuning và observability

---

## 8. Tooling rất đáng học

### Hệ sinh thái xung quanh compiler/runtime
- Build systems
- Package managers
- Debuggers
- Profilers
- Disassemblers ở mức cơ bản
- Static analyzers

### Mục tiêu thực tế
- Không cần trở thành compiler engineer mới hưởng lợi từ kiến thức này
- Chỉ cần hiểu đủ để đọc lỗi build, runtime crash, performance anomaly và stack trace một cách sâu hơn

---

## ✅ Checklist ôn tập
- Mô tả được compiler pipeline end-to-end
- Giải thích được AST, type checking, IR dùng để làm gì
- Biết khác nhau giữa interpreter, VM, JIT và AOT
- Có trực giác về GC và trade-off runtime
- Hiểu vai trò của linker, loader và build toolchain

## 📝 Bài tập
1. Đọc một chương của *Crafting Interpreters* và tự tóm tắt pipeline.
2. Tự viết parser mini cho arithmetic expressions nếu có thời gian.
3. So sánh execution model của Python, Java, Go, Rust ở mức high-level.
4. Tìm một case performance liên quan GC và giải thích.
5. Viết note 1 trang về AST và vì sao IDE tooling phụ thuộc vào nó.

## 📚 Tài liệu
- *Crafting Interpreters* — Robert Nystrom
- *Engineering a Compiler* — Cooper & Torczon
- LLVM docs và tài liệu ngôn ngữ bạn đang dùng