# Computer Science Master Roadmap

## Mục tiêu tổng quan
Track này là bản đồ kiến thức Computer Science theo hướng vừa hàn lâm vừa thực dụng. Mục tiêu không chỉ là "biết thuật ngữ", mà là xây được mental model đủ mạnh để:

- Học nhanh công nghệ mới
- Thiết kế và debug hệ thống phức tạp
- Viết code đúng, rõ, chạy ổn định
- Phỏng vấn tốt ở các vòng coding, systems, fundamentals
- Chuyển từ vai trò implementer sang engineer có chiều sâu

---

## Cấu trúc: 20 bài học — 7 phần

### Phần 1: Foundations (Bài 01-03)
| Bài | Chủ đề | Nội dung chính |
|-----|--------|----------------|
| 01 | Math for Computer Science | Logic, sets, proofs, combinatorics, probability, graph math |
| 02 | Programming Fundamentals | Memory model, control flow, recursion, debugging, modularity |
| 03 | Computer Organization | Binary, CPU, ISA, cache, memory hierarchy, I/O |

### Phần 2: Algorithms & Data (Bài 04-07)
| Bài | Chủ đề | Nội dung chính |
|-----|--------|----------------|
| 04 | Complexity & Problem Solving | Big-O, recurrences, invariants, reductions, reasoning |
| 05 | Core Data Structures | Arrays, lists, hash tables, trees, heaps, graphs, tries |
| 06 | Algorithmic Paradigms | Divide and conquer, greedy, DP, backtracking, graph search |
| 07 | Advanced Algorithms | Strings, range queries, randomized, approximation, streaming |

### Phần 3: Systems (Bài 08-11)
| Bài | Chủ đề | Nội dung chính |
|-----|--------|----------------|
| 08 | Operating Systems | Processes, threads, scheduling, memory, file systems |
| 09 | Concurrency & Parallelism | Locks, atomics, memory model, async I/O, GPU/parallel patterns |
| 10 | Computer Networks | TCP/IP, HTTP, DNS, TLS, routing, load balancing |
| 11 | Distributed Systems | Replication, consensus, partitioning, transactions, fault tolerance |

### Phần 4: Data & Storage (Bài 12-13)
| Bài | Chủ đề | Nội dung chính |
|-----|--------|----------------|
| 12 | Relational Databases | Relational model, SQL, indexing, transactions, query plans |
| 13 | Storage Engines & NoSQL | B-Tree, LSM, WAL, caching, document/KV/graph/search/vector DB |

### Phần 5: Languages & Tools (Bài 14-15)
| Bài | Chủ đề | Nội dung chính |
|-----|--------|----------------|
| 14 | Programming Languages | Types, paradigms, semantics, memory management, interoperability |
| 15 | Compilers & Runtimes | Parsing, AST, IR, bytecode, JIT, GC, toolchains |

### Phần 6: Software & Security (Bài 16-17)
| Bài | Chủ đề | Nội dung chính |
|-----|--------|----------------|
| 16 | Software Engineering | Requirements, architecture, testing, CI/CD, observability |
| 17 | Security & Cryptography | Secure coding, auth, crypto, network security, threat modeling |

### Phần 7: Theory & Specialized (Bài 18-20)
| Bài | Chủ đề | Nội dung chính |
|-----|--------|----------------|
| 18 | Theory of Computation | Automata, grammars, computability, complexity classes |
| 19 | Graphics, HCI, AI & Electives | Rendering, UX, ML overview, scientific computing |
| 20 | Review Plan, Research & Capstones | Ôn tập, note-taking, project-based mastery, reading papers |

---

## Lớp tài liệu mở rộng

Ngoài 20 bài chính, track này còn có thư mục tham chiếu để đào sâu và ôn tập:

```text
08_Reference_and_Review/
  00_Reference_Map.md
  01_Core_Glossary.md
  02_Foundations_Deep_Dive.md
  03_Algorithms_and_Data_Deep_Dive.md
  04_Systems_Deep_Dive.md
  05_Data_and_Storage_Deep_Dive.md
  06_Languages_and_Tools_Deep_Dive.md
  07_Software_and_Security_Deep_Dive.md
  08_Theory_and_Specialized_Deep_Dive.md
  09_Master_Question_Bank.md
```

Các file này dùng cho:
- ôn tập sâu hơn sau khi đọc bài chính
- tự kiểm tra bằng oral exam / self-quiz
- làm flashcards, note-taking và project prep

Ngoài ra còn có bộ bài học đầy đủ:

```text
09_Full_Lessons/
  00_Course_Guide.md
  01_Foundations/
  02_Algorithms_and_Data/
  03_Systems/
  04_Data_and_Storage/
  05_Languages_and_Tools/
  06_Software_and_Security/
  07_Theory_and_Specialized/
```

Bộ này dùng khi bạn muốn học theo kiểu giáo trình từng bài, không chỉ dùng roadmap/checklist.

---

## Level Map

```text
Bài 01-05  → Junior nền tảng vững
Bài 06-11  → Mid/Senior hiểu hệ thống và performance
Bài 12-17  → Senior/Staff có khả năng thiết kế, vận hành, bảo mật
Bài 18-20  → Staff/Principal có góc nhìn lý thuyết, nghiên cứu, chiến lược học lâu dài
```

---

## Cách học theo mục tiêu

### 1. Nếu mục tiêu là phỏng vấn software engineer
Ưu tiên mạnh các bài 01-07, 08-10, 12, 14, 16, 18.

### 2. Nếu mục tiêu là backend/system engineer
Ưu tiên mạnh các bài 03, 08-13, 16-17.

### 3. Nếu mục tiêu là staff/principal
Học toàn bộ, đặc biệt là các bài 11, 13, 15, 16, 17, 18, 20.

### 4. Nếu mục tiêu là AI/ML engineer muốn chắc nền
Ưu tiên 01, 02, 04-05, 08-10, 12-14, 16, 18, sau đó liên kết sang 01_Master_AI.

---

## Cách học một bài

Mỗi bài nên đi theo chu trình này:

1. Đọc overview và mục tiêu đầu ra.
2. Đọc file deep dive tương ứng trong `08_Reference_and_Review/` nếu muốn học sâu.
3. Tự giải thích từng khái niệm mà không nhìn tài liệu.
4. Viết 3-5 ví dụ nhỏ hoặc diagram cho chủ đề đó.
5. Làm bài tập implement hoặc self-quiz.
6. Tổng kết bằng một note 1 trang: khái niệm, trade-off, lỗi hay gặp.

---

## Cách ôn tập lâu dài

```text
Daily:
  - 45-90 phút đọc/implement
  - 10 phút nhắc lại kiến thức hôm trước

Weekly:
  - 1 buổi review 60-90 phút
  - 1 mini quiz tự soạn
  - 1 bài viết giải thích lại cho bản thân

Monthly:
  - 1 project nhỏ hoặc 1 bug hunt / profiling / design note
  - 1 buổi tổng hợp các lỗ hổng kiến thức
```

---

## Liên kết với các track khác trong repo

- Muốn đào sâu algorithms: xem `../04_DSA/`
- Muốn đào sâu database: xem `../03_Database/`
- Muốn đào sâu system design: xem `../02_System_Design/`
- Muốn đào sâu software engineering: xem `../05_Software_Engineering/`
- Muốn đào sâu security: xem `../06_Security/`
- Muốn đào sâu AI: xem `../01_Master_AI/`

Track này đóng vai trò bản đồ nền tảng, còn các track kia là trục đào sâu theo chuyên ngành.

---

## Đầu ra sau khi hoàn thành

Bạn nên có khả năng:

- Đọc tài liệu kỹ thuật nhanh hơn vì đã hiểu các abstraction cơ bản
- Debug lỗi performance, memory, networking, concurrency có hệ thống
- Thiết kế service/backend/data pipeline với trade-off rõ ràng
- Hiểu vì sao công nghệ được thiết kế như hiện tại, thay vì chỉ biết cách dùng
- Lựa chọn hướng chuyên sâu tiếp theo: systems, backend, data, security, AI, research

---

## Capstone gợi ý

1. Viết một key-value store mini: parser, WAL, compaction, TCP server.
2. Tự làm một HTTP server + thread pool + metrics.
3. Xây mini search engine: inverted index + ranking cơ bản.
4. Viết interpreter/compiler mini cho một ngôn ngữ đơn giản.
5. Xây distributed task queue có retry, backoff, idempotency.

Mỗi capstone nên đi kèm design doc, benchmark, failure analysis và bài học rút ra.