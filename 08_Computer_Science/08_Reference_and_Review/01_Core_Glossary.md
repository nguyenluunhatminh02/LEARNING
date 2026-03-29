# Core Glossary for Computer Science

## Cách dùng glossary này
Glossary này không thay thế textbook. Mục tiêu của nó là:
- giúp bạn không nhầm các thuật ngữ gần giống nhau
- cho bạn một định nghĩa ngắn, thực dụng
- làm nguồn flashcards tự học

Mỗi mục nên được dùng như sau:
1. Đọc định nghĩa ngắn.
2. Tự nói lại bằng lời của mình.
3. Cho một ví dụ thật.
4. Nếu có thể, tìm khái niệm đối lập hoặc gần giống để phân biệt.

---

## 1. Foundations and mathematical thinking

### Abstraction
Ẩn bớt chi tiết không cần thiết để tập trung vào interface và behavior quan trọng.

### Algorithm
Quy trình hữu hạn, rõ ràng, biến input thành output.

### Axiom
Phát biểu nền tảng được chấp nhận để xây hệ lập luận.

### Base case
Trường hợp nhỏ nhất hoặc đơn giản nhất làm điểm dừng cho recursion hoặc induction.

### Bijection
Hàm vừa one-to-one vừa onto, ghép từng phần tử của hai tập một cách tương ứng hoàn hảo.

### Cardinality
Độ lớn của một tập hợp.

### Combinatorics
Ngành toán nghiên cứu cách đếm, sắp xếp và cấu hình rời rạc.

### Complement
Phần không thuộc tập đang xét trong không gian nền.

### Conditional probability
Xác suất của một biến cố khi biết một biến cố khác đã xảy ra.

### Contradiction
Kỹ thuật chứng minh bằng cách giả sử điều ngược lại và suy ra mâu thuẫn.

### Contrapositive
Mệnh đề tương đương với `if P then Q` là `if not Q then not P`.

### Discrete mathematics
Toán học cho cấu trúc rời rạc như graph, logic, sets, counting.

### Domain
Tập input mà một hàm chấp nhận.

### Equivalence relation
Quan hệ có tính phản xạ, đối xứng và bắc cầu.

### Event
Tập con của sample space trong xác suất.

### Expectation
Giá trị trung bình dài hạn kỳ vọng của biến ngẫu nhiên.

### Function composition
Ghép đầu ra của hàm này làm đầu vào của hàm khác.

### Graph
Cấu trúc gồm nodes và edges biểu diễn quan hệ hoặc kết nối.

### Induction
Kỹ thuật chứng minh dựa trên base case và bước suy diễn từ `n` sang `n+1` hoặc mạnh hơn.

### Invariant
Điều luôn đúng trước, trong và sau một pha của thuật toán hoặc hệ thống.

### Logic
Hệ quy tắc lập luận chính xác về mệnh đề và suy diễn.

### Predicate
Mệnh đề phụ thuộc biến, khi thay biến vào sẽ nhận giá trị đúng hoặc sai.

### Proof
Lập luận chặt chẽ chứng minh một phát biểu là đúng.

### Quantifier
Ký hiệu như `for all` hoặc `exists` để mô tả phạm vi phát biểu.

### Range
Tập các giá trị đầu ra mà hàm thật sự tạo ra.

### Recurrence
Phương trình mô tả một đại lượng theo các giá trị nhỏ hơn của chính nó.

### Sample space
Tập tất cả kết quả có thể xảy ra của một thí nghiệm ngẫu nhiên.

### Set
Tập hợp các phần tử không xét thứ tự và không lặp.

### Surjection
Hàm phủ toàn bộ codomain.

### Tree
Graph liên thông không chu trình.

### Variance
Độ phân tán của biến ngẫu nhiên quanh expectation.

---

## 2. Programming and software basics

### API
Giao diện mà một module hoặc service cung cấp cho thành phần khác.

### Assertion
Điều kiện được chương trình kỳ vọng là đúng tại một điểm nào đó.

### Binding
Liên kết một tên với một giá trị, object hoặc function.

### Bug
Sai lệch giữa behavior thực tế và behavior mong muốn.

### Code smell
Dấu hiệu cho thấy code có thể đang khó hiểu hoặc khó bảo trì, dù chưa chắc sai ngay.

### Control flow
Trật tự thực thi của các câu lệnh, điều kiện, vòng lặp và lời gọi hàm.

### Debugging
Quy trình tái hiện, cô lập, hiểu và sửa lỗi.

### Deterministic
Với cùng input và trạng thái đầu, luôn cho cùng kết quả.

### Encapsulation
Ẩn state hoặc logic nội bộ phía sau interface rõ ràng.

### Exception
Cơ chế signal lỗi hoặc sự kiện bất thường trong quá trình chạy.

### Function purity
Hàm không có side effects và luôn trả cùng output cho cùng input.

### Heap memory
Vùng nhớ động cấp phát trong runtime, thường có lifetime linh hoạt hơn stack.

### Idempotent
Thực hiện cùng thao tác nhiều lần vẫn cho cùng kết quả logic như làm một lần.

### Immutable
Không thay đổi sau khi được tạo ra.

### Interface
Hợp đồng về hành vi hoặc method mà consumer có thể dựa vào.

### Modularization
Chia hệ thống thành các phần có trách nhiệm tương đối rõ.

### Mutation
Thay đổi state hiện có.

### Object lifetime
Khoảng thời gian object tồn tại và có thể được tham chiếu.

### Referential transparency
Biểu thức có thể thay bằng giá trị của nó mà không đổi behavior chương trình.

### Scope
Vùng mà một biến hoặc tên có hiệu lực.

### Side effect
Ảnh hưởng ra ngoài giá trị trả về, như ghi file, log, cập nhật state, gọi mạng.

### Stack frame
Khung dữ liệu của một lời gọi hàm trên call stack.

### State
Thông tin có thể thay đổi theo thời gian khi chương trình chạy.

### Test case
Một input và kỳ vọng đi kèm để kiểm tra behavior.

### Undefined behavior
Hành vi không được ngôn ngữ hoặc hệ thống bảo đảm kết quả xác định.

---

## 3. Algorithms and data structures

### Amortized analysis
Phân tích chi phí trung bình trên chuỗi thao tác thay vì một thao tác riêng lẻ.

### Asymptotic complexity
Cách mô tả tốc độ tăng trưởng chi phí khi input tăng lớn.

### Backtracking
Tìm kiếm qua các lựa chọn bằng cách thử, kiểm tra và quay lui.

### Balanced tree
Cây tự duy trì chiều cao nhỏ để giữ thao tác gần `O(log n)`.

### Binary search
Kỹ thuật search trên miền có tính đơn điệu bằng cách chia đôi liên tục.

### Bloom filter
Cấu trúc probabilistic kiểm tra membership với false positive có kiểm soát.

### Breadth-first search
Traversal theo từng mức, phù hợp shortest path trong graph unweighted.

### Complexity class
Nhóm bài toán được phân loại theo mức tài nguyên cần thiết.

### Divide and conquer
Chia bài toán thành bài con, giải rồi ghép kết quả.

### Dynamic programming
Giải bài toán bằng state và transition khi có overlapping subproblems.

### Edge case
Trường hợp biên dễ bị bỏ sót như input rỗng, rất lớn, duplicated.

### Fenwick tree
Cấu trúc cho prefix/range query và update hiệu quả trên mảng.

### Greedy algorithm
Thuật toán chọn local optimum ở mỗi bước với hy vọng đạt global optimum.

### Hash collision
Nhiều keys cho cùng hash bucket hoặc vị trí.

### Hash function
Hàm ánh xạ key sang giá trị băm để phục vụ lookup.

### Heap
Tree-based structure hỗ trợ truy cập phần tử ưu tiên cao nhất hoặc thấp nhất nhanh.

### Memoization
Lưu kết quả subproblem đã tính để tránh lặp lại.

### Monotonic property
Tính chất tăng/giảm một chiều, hay dùng cho binary search on answer.

### Priority queue
ADT hỗ trợ lấy phần tử ưu tiên nhất trước.

### Pruning
Cắt bỏ nhánh search chắc chắn không hữu ích.

### Range query
Truy vấn trên một đoạn hoặc miền thay vì một điểm.

### Recursion tree
Cách hình dung cost của recursion bằng một cây lời gọi.

### Reduction
Chuyển một bài toán về bài toán khác đã biết cách giải hoặc biết độ khó.

### Segment tree
Cấu trúc cây cho range query và updates phức tạp hơn Fenwick.

### Sliding window
Kỹ thuật duy trì một đoạn di chuyển trên input để tối ưu scan tuyến tính.

### Stable sort
Sort giữ nguyên thứ tự tương đối của các phần tử bằng nhau.

### Topological sort
Thứ tự tuyến tính hợp lệ của DAG theo dependency edges.

### Trie
Cấu trúc cây theo ký tự hoặc prefix.

### Union-Find
Cấu trúc quản lý connectivity và components động hiệu quả.

---

## 4. Computer systems and operating systems

### Address space
Không gian địa chỉ mà process nhìn thấy.

### Context switch
Việc CPU đổi từ execution context này sang context khác.

### Copy-on-write
Chia sẻ dữ liệu cho tới khi có bên sửa, lúc đó mới tạo bản sao riêng.

### DMA
Cơ chế cho thiết bị đọc/ghi memory không cần CPU copy từng byte.

### File descriptor
Số nguyên đại diện cho file/socket/pipe đã mở trong process.

### Fragmentation
Sự phân mảnh làm dùng memory hoặc storage kém hiệu quả.

### Interrupt
Tín hiệu làm CPU tạm dừng luồng hiện tại để xử lý sự kiện khẩn hoặc I/O.

### Kernel
Phần lõi của OS quản lý tài nguyên và cung cấp system calls.

### Kernel mode
Chế độ đặc quyền cao của CPU để chạy code hệ điều hành.

### Memory leak
Memory không còn hữu ích nhưng vẫn bị giữ lại.

### mmap
Cơ chế ánh xạ file hoặc vùng nhớ vào address space của process.

### Page fault
Sự kiện truy cập page chưa hiện diện hợp lệ trong RAM/process mapping.

### Page cache
Bộ nhớ đệm của OS cho dữ liệu file/block I/O.

### Process
Một instance đang chạy của chương trình với state và tài nguyên riêng.

### Scheduler
Thành phần quyết định luồng hoặc process nào được CPU tiếp theo.

### Semaphore
Primitive đồng bộ hóa dựa trên counter.

### Signal
Thông báo bất đồng bộ gửi tới process.

### Socket
Endpoint để giao tiếp qua network hoặc local IPC.

### System call
Lời gọi từ user-space sang kernel để yêu cầu dịch vụ hệ điều hành.

### Thread
Đơn vị thực thi nhẹ bên trong process.

### TLB
Cache cho ánh xạ virtual address sang physical mapping.

### User mode
Chế độ chạy ứng dụng thường với quyền hạn thấp hơn kernel mode.

### Virtual memory
Lớp trừu tượng cho phép process thấy address space liên tục và được bảo vệ.

---

## 5. Concurrency and parallelism

### Atomic operation
Thao tác xảy ra như một bước không thể quan sát trạng thái dở dang.

### Barrier
Điểm đồng bộ mà nhiều workers phải chờ nhau.

### Critical section
Đoạn code truy cập shared state cần bảo vệ khỏi race.

### Data race
Hai luồng truy cập cùng dữ liệu, có ít nhất một write, không đồng bộ đúng cách.

### Deadlock
Các actors chờ nhau vô hạn nên không ai tiến được.

### False sharing
Hai cores ghi lên dữ liệu khác nhau nhưng cùng cache line, gây contention vô ích.

### Happens-before
Quan hệ ordering logic bảo đảm visibility giữa các operations concurrent.

### Livelock
Các actors vẫn hoạt động nhưng không tạo tiến triển hữu ích.

### Memory ordering
Quy tắc hoặc guarantee về thứ tự quan sát các operations bộ nhớ.

### Mutex
Primitive loại trừ tương hỗ cho critical section.

### Parallelism
Thực thi đồng thời thực sự trên nhiều execution units.

### Race condition
Behavior phụ thuộc timing hoặc interleaving không được kiểm soát.

### Starvation
Một task không được phục vụ đủ lâu dù hệ thống vẫn chạy.

### Work stealing
Kỹ thuật scheduler cho worker rảnh lấy việc từ worker bận.

---

## 6. Networking and distributed systems

### ACK
Xác nhận rằng dữ liệu hoặc message đã được nhận.

### Availability
Khả năng hệ thống phản hồi hợp lệ khi được yêu cầu.

### Backoff
Cách tăng dần thời gian chờ giữa các lần retry.

### CDN
Mạng phân phối nội dung đặt cache gần người dùng.

### Congestion control
Cơ chế giảm tốc gửi để tránh quá tải mạng.

### Consistency
Mức độ các node thấy dữ liệu đồng nhất theo một mô hình nào đó.

### DNS
Hệ thống phân giải tên miền thành địa chỉ hoặc records khác.

### Eventual consistency
Nếu không có update mới, các replicas cuối cùng sẽ hội tụ cùng trạng thái.

### Fault tolerance
Khả năng tiếp tục cung cấp dịch vụ dù có thành phần lỗi.

### Handshake
Quá trình ban đầu để hai đầu thống nhất cách giao tiếp.

### Idempotency key
Khóa giúp server nhận diện request lặp lại là cùng một hành động logic.

### Latency
Độ trễ từ lúc gửi yêu cầu đến lúc nhận kết quả.

### Leader election
Chọn một node đóng vai trò điều phối hoặc source of truth tạm thời.

### Linearizability
Mô hình consistency mạnh nơi operations như xảy ra tức thời theo một thứ tự toàn cục hợp lý.

### Load balancer
Thành phần phân phối traffic đến nhiều backends.

### Packet loss
Gói tin bị mất trên đường đi.

### Partition
Tình trạng một phần hệ thống không liên lạc được với phần còn lại.

### Quorum
Số lượng node tối thiểu cần tham gia để quyết định được chấp nhận.

### Raft
Họ thuật toán consensus thực dụng dựa trên leader.

### Replication
Sao chép dữ liệu hoặc state sang nhiều node.

### Retry storm
Nhiều clients cùng retry khiến hệ thống đang lỗi càng quá tải hơn.

### Sharding
Chia dữ liệu theo key/range/hash ra nhiều partitions.

### TCP
Giao thức transport tin cậy, có thứ tự, hướng kết nối.

### Throughput
Khối lượng công việc xử lý được trên đơn vị thời gian.

### TLS
Giao thức bảo vệ tính bí mật và toàn vẹn của kết nối mạng.

### UDP
Giao thức transport nhẹ, không bảo đảm delivery hoặc order.

---

## 7. Databases and storage

### ACID
Tập tính chất atomicity, consistency, isolation, durability cho transactions.

### B-Tree
Họ cấu trúc cây cân bằng tối ưu cho block storage và range queries.

### Cardinality estimation
Ước lượng số dòng trung gian để optimizer chọn plan.

### Checkpoint
Điểm mà state bền vững được đồng bộ để giảm chi phí recovery.

### Columnar storage
Lưu dữ liệu theo cột thay vì theo hàng, phù hợp analytics.

### Compaction
Quá trình hợp nhất và dọn các file/segments trong log-structured engines.

### Covering index
Index chứa đủ cột để query không cần quay lại table chính.

### Deadlock detection
Phát hiện transactions hoặc locks đang chờ vòng lặp.

### Denormalization
Cố ý lặp dữ liệu để đổi lấy query đơn giản hoặc nhanh hơn.

### Execution plan
Kế hoạch mà DB engine chọn để chạy query.

### Index
Cấu trúc phụ giúp tìm dữ liệu nhanh hơn.

### Isolation level
Mức cô lập giữa các transactions concurrent.

### Join
Kết hợp dữ liệu từ nhiều bảng theo quan hệ nào đó.

### LSM-tree
Họ storage structure tối ưu writes bằng log-structured immutable files.

### MVCC
Cơ chế đa phiên bản giúp concurrent reads/writes giảm blocking.

### Normalization
Thiết kế schema giảm dư thừa và anomaly cập nhật.

### OLAP
Workload phân tích, thường scan lớn và aggregates nặng.

### OLTP
Workload giao dịch online với read/write ngắn, tần suất cao.

### PITR
Point-in-time recovery, khôi phục tới một thời điểm xác định.

### Query optimizer
Thành phần chọn execution plan cho câu SQL.

### Secondary index
Index không quyết định layout vật lý chính của data rows.

### WAL
Nhật ký ghi trước khi commit state chính để bảo đảm durability/recovery.

---

## 8. Programming languages and runtimes

### ABI
Binary interface giữa compiled components ở mức machine/runtime.

### AST
Cây cú pháp trừu tượng dùng cho compiler, interpreter và tooling.

### Bytecode
Mã trung gian cho virtual machine.

### Closure
Function mang theo environment lexical nơi nó được tạo.

### Compiler
Chương trình biến source code thành representation khác để thực thi.

### Desugaring
Chuyển cú pháp tiện lợi thành biểu diễn cơ bản hơn.

### Dynamic dispatch
Cơ chế chọn method/function implementation tại runtime.

### FFI
Giao tiếp giữa hai ngôn ngữ hoặc runtime khác nhau.

### Garbage collection
Tự động thu hồi memory không còn reachable.

### Generics
Cơ chế viết code đa hình theo type.

### Interpreter
Thực thi source hoặc representation trung gian trực tiếp.

### IR
Intermediate representation dùng để phân tích và tối ưu trong compiler.

### JIT
Just-in-time compilation, compile một phần khi runtime đang chạy.

### Lexer
Thành phần chuyển source text thành tokens.

### Loader
Thành phần của hệ thống nạp program và dependencies vào memory để chạy.

### Parser
Thành phần biến tokens thành tree hoặc structure theo grammar.

### Runtime
Môi trường và dịch vụ hỗ trợ chương trình chạy.

### Static typing
Loại dữ liệu được kiểm tra phần lớn trước runtime.

### Symbol table
Bảng tra tên tới binding/type/scope info trong compiler.

### Type inference
Khả năng compiler suy luận type mà không cần ghi tường minh mọi chỗ.

### VM
Máy ảo cung cấp execution model trừu tượng trên phần cứng thật.

---

## 9. Software engineering and security

### ADR
Architecture Decision Record, tài liệu ngắn ghi quyết định kiến trúc và trade-off.

### Authentication
Xác minh danh tính của actor.

### Authorization
Xác định actor được phép làm gì.

### Blast radius
Phạm vi ảnh hưởng khi một thay đổi hoặc lỗi xảy ra.

### Canary deployment
Triển khai dần cho một phần traffic nhỏ trước khi rollout rộng.

### CIA triad
Bí mật, toàn vẹn và sẵn sàng.

### CI/CD
Chuỗi tích hợp, kiểm thử, build và triển khai tự động.

### Contract test
Kiểm tra hợp đồng giữa các thành phần hoặc services.

### Defense in depth
Nhiều lớp phòng vệ thay vì tin vào một cơ chế duy nhất.

### Least privilege
Chỉ cấp quyền tối thiểu cần thiết để làm việc.

### MFA
Xác thực đa yếu tố.

### Observability
Khả năng suy ra trạng thái bên trong hệ thống từ outputs bên ngoài như logs, metrics, traces.

### Postmortem
Phân tích sau sự cố để hiểu nguyên nhân gốc và hành động cải thiện.

### RBAC
Role-based access control.

### RFC
Tài liệu đề xuất hướng tiếp cận kỹ thuật trước khi implementation.

### SAST
Phân tích tĩnh tìm lỗi hoặc lỗ hổng trong source.

### SLA
Cam kết dịch vụ với người dùng hoặc khách hàng.

### SLO
Mục tiêu mức dịch vụ nội bộ.

### Threat model
Mô hình mô tả tài sản, attacker, entry points và mitigations.

### Zero trust
Mô hình không mặc định tin cậy chỉ vì đang ở trong mạng nội bộ.

---

## 10. Theory, research and advanced thinking

### Automaton
Máy trạng thái trừu tượng dùng để mô hình hóa computation hữu hạn.

### Computability
Nghiên cứu bài toán nào có thể được giải bằng thuật toán.

### Context-free grammar
Hệ luật sinh cho ngôn ngữ có cấu trúc lồng nhau như biểu thức hoặc program.

### Decidable
Bài toán có thuật toán luôn dừng và trả lời đúng cho mọi input.

### Formal language
Tập các chuỗi trên một alphabet nào đó.

### Heuristic
Cách làm thực dụng thường tốt nhưng không luôn tối ưu hoặc không luôn có guarantee mạnh.

### NP
Lớp bài toán mà nghiệm có thể kiểm tra nhanh trong thời gian đa thức.

### NP-complete
Những bài toán vừa thuộc NP vừa khó như mọi bài trong NP thông qua reduction.

### NP-hard
Bài toán ít nhất khó như NP-complete nhưng có thể không thuộc NP.

### Regular language
Ngôn ngữ có thể nhận bởi finite automata.

### SAT
Bài toán thỏa mãn logic boolean, trung tâm trong complexity theory.

### Turing machine
Mô hình tính toán tổng quát kinh điển.

### Undecidable
Bài toán không có thuật toán tổng quát luôn giải đúng và dừng với mọi input.

---

## Cách biến glossary thành flashcards

Mẫu thẻ nên là:

```text
Front: MVCC là gì?
Back: Cơ chế nhiều phiên bản giúp reads/writes đồng thời mà giảm blocking; thường dùng trong RDBMS hiện đại.
```

Hoặc:

```text
Front: So sánh linearizability với eventual consistency.
Back: Linearizability mạnh hơn nhiều; mọi operation như xảy ra tức thời theo thứ tự toàn cục. Eventual consistency chỉ bảo đảm hội tụ cuối cùng khi không còn updates mới.
```

---

## Mẹo dùng glossary hiệu quả
- Đừng cố nhớ máy móc 100% định nghĩa.
- Ưu tiên hiểu use case, counterexample và trade-off.
- Sau khi dùng một khái niệm trong code/project, quay lại glossary để sửa định nghĩa của riêng bạn nếu cần.