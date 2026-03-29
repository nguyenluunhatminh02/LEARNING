# Master Question Bank for Computer Science

## Cách dùng
Question bank này dành cho:
- self-quiz hằng tuần
- oral exam practice
- interview-style review
- note-taking prompts

Hãy cố trả lời không nhìn tài liệu trước. Nếu bí, chỉ xem roadmap hoặc glossary sau cùng.

---

## 1. Foundations questions

1. Logic khác intuition đời thường ở điểm nào?
2. Vì sao `P -> Q` không đồng nghĩa `Q -> P`?
3. Khi nào nên dùng proof by contradiction thay vì direct proof?
4. Induction khác recursion ở đâu và liên hệ với nhau thế nào?
5. Loop invariant là gì và vì sao cực kỳ quan trọng?
6. Partial order khác total order như thế nào?
7. Tại sao equivalence relation lại dẫn tới partitioning?
8. Tại sao permutation và combination khác nhau về bản chất?
9. Conditional probability khác joint probability ra sao?
10. Expectation hữu ích thế nào trong engineering?
11. Vì sao variance quan trọng hơn chỉ nhìn average?
12. Tại sao graph là mô hình mạnh cho nhiều bài toán không trông giống graph?
13. Value và reference khác nhau như thế nào?
14. Scope và lifetime khác nhau ở đâu?
15. Mutation ngoài ý muốn thường đến từ đâu?
16. Tại sao debugging tốt phải bắt đầu từ reproduce?
17. Exception path nên được xem như phần nào của behavior?
18. Vì sao recursion có thể đẹp nhưng nguy hiểm với stack depth?
19. Stack và heap khác nhau thế nào ở mức thực dụng?
20. Tại sao memory leaks có thể xảy ra ngay cả khi có GC?
21. Two's complement giúp biểu diễn số âm ra sao?
22. Tại sao floating point không phù hợp cho mọi bài toán số?
23. UTF-8 khác ASCII như thế nào?
24. Cache locality là gì và vì sao nó quan trọng?
25. Sequential access thường nhanh hơn random access vì sao?

---

## 2. Algorithms and data questions

26. Big-O mô tả cái gì và không mô tả cái gì?
27. Worst case và amortized khác nhau ra sao?
28. Khi nào average case mới là metric cần quan tâm?
29. Brute force có vai trò gì ngoài việc làm baseline?
30. Làm sao biết bottleneck thật của một lời giải nằm ở đâu?
31. Vì sao constant factors vẫn quan trọng trong thực tế?
32. Dynamic array append vì sao là `O(1)` amortized?
33. Hash map lookup vì sao không luôn là `O(1)` thực tế?
34. Khi nào ordered map tốt hơn hash map?
35. Vì sao linked list thường không mạnh như textbook làm bạn nghĩ?
36. Heap khác BST ở use case nào?
37. Trie đáng dùng khi nào?
38. Khi nào adjacency matrix hợp lý hơn adjacency list?
39. Union-find giải loại bài toán nào rất tốt?
40. Segment tree và Fenwick tree nên học ở mức nào?
41. Sliding window cần điều kiện cấu trúc nào để hoạt động tốt?
42. Binary search on answer áp dụng khi nào?
43. Greedy cần loại proof nào để đáng tin?
44. Dấu hiệu của một bài dynamic programming là gì?
45. State trong DP nên được chọn theo nguyên tắc nào?
46. Vì sao state thừa biến làm DP khó hơn nhiều?
47. BFS khác DFS ở bản chất nào, không chỉ ở data structure hỗ trợ?
48. Dijkstra thất bại khi nào?
49. Khi nào Bellman-Ford đáng cân nhắc?
50. Prefix sum giải quyết dạng bài nào?
51. Difference array hữu ích ở đâu?
52. Sweep line là pattern gì?
53. Bloom filter cho gì và đánh đổi gì?
54. HyperLogLog giải quyết vấn đề gì?
55. Khi nào approximation hợp lý hơn exact algorithm?
56. Reduction giúp tư duy như thế nào?
57. Nếu một solution rất nhanh nhưng bạn không giải thích được invariant, vấn đề là gì?
58. Edge case nào thường làm binary search sai?
59. Edge case nào thường làm graph algorithm sai?
60. Vì sao duplicate handling là nguồn bug phổ biến?

---

## 3. Systems questions

61. Process khác thread ở isolation, communication và cost như thế nào?
62. System call là gì và vì sao nó có cost?
63. Context switch vì sao làm chương trình chậm hơn?
64. CPU-bound và I/O-bound workload khác nhau thế nào?
65. Scheduling ảnh hưởng tail latency ra sao?
66. Virtual memory mang lại lợi ích gì?
67. TLB và page fault khác nhau như thế nào?
68. Swapping làm hệ thống trông thế nào từ góc nhìn ứng dụng?
69. Page cache có lợi và hại gì?
70. Vì sao `fsync` quan trọng cho durability?
71. Blocking I/O và non-blocking I/O khác nhau thực sự ở đâu?
72. epoll/kqueue giải quyết vấn đề gì?
73. File descriptor leak sẽ biểu hiện thế nào?
74. Containers dựa trên primitive nào của OS?
75. VM và container khác nhau ở isolation boundary ra sao?
76. Concurrency khác parallelism ở đâu?
77. Shared mutable state nguy hiểm vì sao?
78. Race condition là gì?
79. Deadlock cần những điều kiện nào?
80. Starvation khác deadlock thế nào?
81. False sharing là gì?
82. Memory reordering có ý nghĩa thực tế gì?
83. Async I/O không giải quyết được những vấn đề nào?
84. Amdahl's law nói gì?
85. Tăng số thread vì sao không luôn tăng throughput?

---

## 4. Networking and distributed questions

86. Một HTTP request đi qua những lớp nào từ client tới server?
87. DNS tham gia ở đâu trong request path?
88. TCP handshake để làm gì?
89. Ordered reliable delivery có cái giá gì?
90. UDP phù hợp với loại workload nào?
91. QUIC khác TCP+TLS truyền thống ở điểm lớn nào?
92. Timeout nên đặt theo nguyên tắc nào?
93. Retry nguy hiểm khi nào?
94. Backoff giúp gì?
95. Idempotency có vai trò gì trong distributed systems?
96. DNS TTL ảnh hưởng gì tới failover và caching?
97. TLS thất bại có thể do những nguyên nhân nào?
98. L4 và L7 load balancer khác nhau ở đâu?
99. CDN có ích nhất với loại traffic nào?
100. Consistency model là gì ở mức sản phẩm?
101. Linearizability khác eventual consistency ở đâu?
102. Replication và partitioning giải hai bài toán khác nhau thế nào?
103. Hot partition là gì và vì sao nguy hiểm?
104. Replica lag gây ra trải nghiệm người dùng nào?
105. Consensus dùng để làm gì?
106. Raft ở mức trực giác giải bài toán gì?
107. Two-phase commit có hạn chế gì?
108. Saga phù hợp khi nào?
109. Exactly-once thường là ảo tưởng kiểu gì trong thực tế?
110. Correlation ID hỗ trợ điều tra sự cố ra sao?

---

## 5. Data and storage questions

111. Relational model mạnh ở đâu?
112. Khi nào normalization nên được ưu tiên?
113. Khi nào denormalization hợp lý?
114. Primary key và unique constraint khác nhau thế nào về vai trò?
115. SQL declarative nghĩa là gì?
116. Vì sao cùng một query logic có thể chạy với cost rất khác nhau?
117. Cardinality estimation sai gây hậu quả gì?
118. B-Tree index giúp loại truy vấn nào?
119. Composite index cần lưu ý gì về thứ tự cột?
120. Covering index là gì?
121. Over-indexing gây hại như thế nào?
122. ACID có ý nghĩa gì với nghiệp vụ?
123. Isolation levels khác nhau tác động ra sao?
124. MVCC giải quyết và đánh đổi điều gì?
125. Deadlock trong DB thường xuất hiện do đâu?
126. Query plan nên đọc những gì đầu tiên?
127. OLTP và OLAP khác nhau thế nào?
128. WAL tồn tại để làm gì?
129. Checkpoint giúp gì?
130. B-Tree và LSM-tree khác nhau ở write/read path ra sao?
131. Compaction ảnh hưởng latency thế nào?
132. Cache-aside khác write-through ở đâu?
133. Cache invalidation khó vì sao?
134. Replication không thay được backup vì sao?
135. PITR dùng trong trường hợp nào?
136. Khi nào chọn key-value store?
137. Khi nào chọn document DB?
138. Khi nào chọn search engine?
139. Khi nào chọn vector DB?
140. Polyglot persistence tạo trade-off gì?

---

## 6. Languages and tools questions

141. Static typing giúp gì hơn dynamic typing?
142. Dynamic typing mạnh ở đâu?
143. Strong typing và weak typing có phải trục so sánh đủ tốt không?
144. Nominal và structural typing khác nhau thế nào?
145. Type inference có lợi và hại gì?
146. OOP hữu ích nhất ở đâu?
147. Functional style hữu ích nhất ở đâu?
148. Immutability giúp concurrency như thế nào?
149. GC đánh đổi gì so với manual memory?
150. Ownership model mạnh ở đâu?
151. Lexer và parser khác nhau thế nào?
152. AST dùng để làm gì ngoài compiler?
153. Semantic analysis gồm những gì?
154. IR tồn tại để làm gì?
155. Optimization có thể gây trade-off gì?
156. Static linking và dynamic linking khác nhau thế nào?
157. Loader làm gì khi program khởi động?
158. Interpreter và compiler không nhất thiết đối lập tuyệt đối vì sao?
159. VM mang lại lợi ích gì?
160. JIT và AOT khác nhau ở startup và steady-state ra sao?
161. Reflection mạnh ở đâu và làm khó tối ưu ở đâu?
162. FFI gặp những loại mismatch nào?
163. Package manager và build system khác nhau thế nào?
164. Tooling maturity tác động tới team velocity ra sao?
165. Vì sao error messages của compiler/runtime cũng là feature quan trọng?

---

## 7. Software and security questions

166. Functional requirement và non-functional requirement khác nhau thế nào?
167. Coupling và cohesion là gì?
168. Blast radius là gì?
169. Unit, integration, contract và E2E tests phục vụ mục đích khác nhau ra sao?
170. Coverage cao nhưng test yếu là tình huống thế nào?
171. Feature flags giúp gì và gây rủi ro gì?
172. Canary deployment dùng khi nào?
173. Observability khác monitoring thuần ở đâu?
174. Logs, metrics, traces bổ sung cho nhau như thế nào?
175. Postmortem tốt cần có gì?
176. CIA triad là gì?
177. Authentication và authorization khác nhau thế nào?
178. Least privilege áp dụng ra sao trong ứng dụng và cloud?
179. Defense in depth nghĩa là gì thực tế?
180. Parameterized query chống được loại lỗi nào?
181. XSS khác CSRF thế nào?
182. SSRF nguy hiểm vì sao?
183. Hashing, encryption và digital signatures khác nhau thế nào?
184. Vì sao password không nên dùng fast hash?
185. Secret management tốt gồm những nguyên tắc nào?
186. Threat model nên bắt đầu từ đâu?
187. Dependency scanning giải quyết phần nào của security?
188. Logging quá mức có thể tạo risk gì?
189. Internal network vì sao không nên mặc định tin cậy?
190. Một API reset password nên được review security theo những điểm nào?

---

## 8. Theory, research and capstone questions

191. Regular language là gì?
192. Khi nào regex là không đủ mạnh?
193. CFG khác regular language ở đâu?
194. Turing machine đóng vai trò gì trong tư duy computation?
195. Decidable khác undecidable như thế nào?
196. Halting problem cho engineer bài học gì?
197. P, NP, NP-hard, NP-complete khác nhau ra sao?
198. NP-hard ảnh hưởng quyết định thiết kế như thế nào trong thực tế?
199. Reduction giúp ích gì ngoài lý thuyết thuần?
200. Heuristic khác approximation algorithm ở đâu?
201. Vì sao HCI vẫn thuộc phạm vi CS rộng?
202. Graphics đòi hỏi nền toán nào nhiều nhất?
203. AI/ML dùng những nền CS nào mạnh nhất?
204. Formal methods hữu ích ở đâu?
205. Một paper kỹ thuật nên được đọc với các câu hỏi nào?
206. Một capstone tốt nên chứng minh điều gì ngoài việc chạy được?
207. Khi nào bạn thật sự "nắm" một chủ đề?
208. Recognition, recall, transfer, synthesis khác nhau thế nào?
209. Vì sao tự giải thích lại bằng lời là một kỹ thuật học mạnh?
210. Nếu phải chọn 1 nhánh chính và 1 nhánh phụ để đào sâu, bạn sẽ chọn theo tiêu chí nào?

---

## 9. Prompts để viết note hoặc essay

1. Giải thích vì sao cache có thể làm hệ thống nhanh hơn và khó đúng hơn cùng lúc.
2. So sánh process, thread và async task như ba cách tổ chức concurrency.
3. Viết một bài về vì sao idempotency là từ khóa quan trọng của distributed systems.
4. So sánh B-Tree với LSM-tree dưới góc nhìn workload.
5. Giải thích type systems dưới góc nhìn engineering thay vì học thuật thuần.
6. Viết một bài về limits of computation và ảnh hưởng của chúng tới software engineering.

---

## 10. Cách tự chấm điểm câu trả lời

Một câu trả lời mạnh nên có:
- định nghĩa ngắn rõ
- ví dụ đúng
- phản ví dụ hoặc đối chiếu gần giống
- trade-off hoặc failure mode
- liên hệ với hệ thống thật nếu phù hợp

Nếu câu trả lời chỉ toàn buzzwords, coi như chưa đạt.