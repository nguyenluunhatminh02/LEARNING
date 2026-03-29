# Theory and Specialized Deep Dive

## Mục tiêu của file này
File này đào sâu cho:
- Theory of Computation
- Graphics, HCI, AI and Electives
- Review, Research and Capstones

Mục tiêu là biến phần cuối của roadmap từ "điểm kết" thành bệ phóng cho chuyên sâu dài hạn.

---

## 1. Why theory still matters

Theory of Computation giúp bạn hiểu:
- giới hạn của automation
- cấu trúc của bài toán khó
- khi nào exact solution là không thực tế
- tại sao parser, regex, SAT, optimization và verification lại nối được với nhau

Đây không phải kiến thức "để thi đại học". Nó giúp bạn reasoning sắc hơn và bớt lãng phí thời gian vào hướng vô vọng.

---

## 2. How to study theory pragmatically

### Bước 1
Hiểu intuition bằng ví dụ nhỏ.

### Bước 2
Học định nghĩa formal sau khi đã có direct intuition.

### Bước 3
Liên kết với use case thật:
- regex engine
- parser
- SAT solver
- scheduling and optimization

### Bước 4
Tự phân loại một số bài toán quen thuộc vào các nhóm complexity.

---

## 3. Automata and grammars deep dive

### Finite automata matters because
- nhiều validation problems thật ra là regular languages
- lexers và tokenizers dùng ideas tương tự
- state machine thinking cực hữu ích cho protocols và workflows

### CFG matters because
- parsing nested syntax cần mạnh hơn regular languages
- programming languages, config formats, query DSLs đều liên quan grammar thinking

### Questions to ask
- pattern này regular hay cần stack-like memory?
- grammar này mơ hồ ở đâu?
- parser failures phản ánh grammar design hay implementation issues?

---

## 4. Computability and impossibility intuition

Bạn không cần tự chứng minh halting problem quá hình thức mỗi tuần, nhưng nên internalize rằng:
- có những bài toán không có thuật toán tổng quát đúng cho mọi input
- nhiều bài kiểm tra properties của program rất dễ rơi vào vùng này
- do đó tooling, static analysis và verification đều phải dựa vào approximations, restrictions hoặc trade-offs

---

## 5. Complexity classes and decision quality

### P, NP, NP-hard, NP-complete
Điều quan trọng nhất không phải định nghĩa học thuộc, mà là trực giác quyết định:
- nếu bài có dấu hiệu NP-hard, có nên tìm exact algorithm cho scale này không?
- có exploit cấu trúc domain đặc biệt nào không?
- heuristic hoặc approximation có đủ tốt cho business không?

### This matters in real systems
- scheduling
- routing
- placement
- resource allocation
- compiler optimization
- search and ranking

---

## 6. Specialized tracks selection

### Graphics
Đi sâu nếu bạn thích:
- geometry
- rendering
- simulation
- game/visualization/AR-VR

### HCI
Đi sâu nếu bạn thích:
- product usability
- interaction quality
- accessibility
- human factors

### AI/ML
Đi sâu nếu bạn thích:
- modeling
- optimization
- data pipelines
- research iteration

### PL/compilers/tooling
Đi sâu nếu bạn thích:
- parsers
- static analysis
- developer tools
- language design

### Formal methods
Đi sâu nếu bạn thích:
- proofs
- correctness
- verification
- safety-critical systems

---

## 7. Research reading deep dive

Khi đọc paper, đừng chỉ hỏi "kết quả có tốt không". Hãy hỏi:
- baseline nào được chọn?
- metric nào được tối ưu?
- assumptions có thực tế không?
- chi phí vận hành có bị giấu không?
- giới hạn của paper là gì?

Một paper tốt cho học tập là paper khiến bạn nhìn lại assumptions của mình, không chỉ paper có nhiều công thức.

---

## 8. Capstones as synthesis

Capstone tốt nên bắt bạn chạm nhiều lớp cùng lúc:
- data structure và algorithm choices
- OS/network/runtime realities
- storage design
- testing and observability
- security boundaries
- trade-off documentation

Nếu capstone chỉ có code demo chạy happy path, nó chưa đủ giá trị.

---

## 9. Artifact checklist for serious learning

Mỗi capstone hoặc research project nên có:
- problem statement
- constraints
- architecture sketch
- rationale for chosen approach
- benchmark or evaluation plan
- failure scenarios
- open questions

---

## 10. What to know cold

Bạn nên biết cold:
- DFA/NFA/CFG ở mức high-level
- decidable vs undecidable
- P vs NP vs NP-hard vs NP-complete
- heuristic vs approximation vs exact solution
- các nhánh chuyên sâu lớn của CS và chúng yêu cầu nền tảng gì

---

## 11. Suggested labs

### Lab 1: State machine note
Biểu diễn một protocol hoặc workflow đơn giản bằng finite state machine.

### Lab 2: Grammar exercise
Viết grammar mini cho arithmetic expressions hoặc config format đơn giản.

### Lab 3: NP-hard reasoning note
Chọn một bài toán thực tế có flavor NP-hard và giải thích cách tiếp cận heuristic khả thi.

### Lab 4: Paper summary
Đọc một paper hoặc technical design nổi tiếng và tóm tắt bằng 1-2 trang với phần assumptions/trade-offs.

---

## 12. Oral exam questions

- Khi nào regular expressions là không đủ?
- Vì sao undecidability quan trọng với static analysis?
- NP-hard ảnh hưởng quyết định thiết kế như thế nào trong thực tế?
- Chọn chuyên sâu nào nếu bạn thích vừa systems vừa tooling?
- Một capstone tốt cần chứng minh điều gì ngoài việc chạy được?

---

## 13. Final reminder
Phần cuối của roadmap không phải "đọc cho biết". Đây là nơi bạn chuyển từ người học nền tảng sang người định hình hướng chuyên môn của chính mình.