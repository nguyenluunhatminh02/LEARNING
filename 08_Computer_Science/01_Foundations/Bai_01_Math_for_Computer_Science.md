# Bài 01: Math for Computer Science

## 🎯 Mục tiêu
- Xây nền tảng toán rời rạc đủ để đọc thuật toán, chứng minh và phân tích hệ thống
- Hiểu logic, tập hợp, quan hệ, hàm, tổ hợp, xác suất và các kỹ thuật chứng minh
- Biết phần nào của linear algebra, calculus và statistics thực sự hữu ích cho engineer

## 📖 Bức tranh lớn
Computer Science dùng toán không phải để làm đẹp lời giải, mà để mô tả chính xác cấu trúc, ràng buộc và hành vi của hệ thống. Bạn cần toán để trả lời những câu như:

- Thuật toán này luôn đúng hay chỉ đúng trong vài case?
- Có bao nhiêu trạng thái có thể xảy ra?
- Xác suất collision, lỗi, retry success là bao nhiêu?
- Graph này có chu trình, đường đi ngắn nhất, hay điểm nghẽn ở đâu?

---

## 1. Logic và chứng minh

### Chủ đề cần nắm
- Proposition, predicate, truth table
- AND, OR, NOT, implication, equivalence
- Quantifiers: `for all`, `exists`
- De Morgan's laws
- Direct proof, proof by contradiction, proof by contrapositive
- Mathematical induction và strong induction
- Loop invariant trong thuật toán

### Bạn phải làm được
- Đọc và viết điều kiện logic chính xác
- Chứng minh một thuật toán lặp hoặc đệ quy là đúng
- Tìm phản ví dụ khi một phát biểu sai

### Ví dụ tư duy
Nếu nói: "Thuật toán đúng với mọi input đã sort" thì bạn phải phân biệt được:

```text
For all arrays A, if A is sorted then algorithm(A) is correct.
```

với:

```text
There exists a sorted array A such that algorithm(A) is correct.
```

Hai câu trên khác nhau hoàn toàn về độ mạnh của phát biểu.

---

## 2. Tập hợp, quan hệ, hàm

### Tập hợp
- Union, intersection, difference, complement
- Cartesian product
- Power set

### Quan hệ
- Reflexive, symmetric, transitive
- Equivalence relation
- Partial order, total order

### Hàm
- Injective, surjective, bijective
- Inverse function
- Composition
- Growth of functions: so sánh `log n`, `n`, `n log n`, `n^2`, `2^n`

### Ứng dụng trong CS
- Equivalence relation: partition state space, DSU/union-find
- Partial order: dependency graph, topological sort
- Function composition: pipelines, compilers, data transformation

---

## 3. Tổ hợp và đếm

### Chủ đề cần nắm
- Rule of sum, rule of product
- Permutation, combination
- Pigeonhole principle
- Inclusion-exclusion
- Recurrence relations cơ bản

### Ứng dụng thực tế
- Tính số case test cần cover
- Ước lượng search space của backtracking
- Tính số trạng thái trong distributed system, cache key space, password/key space

### Công thức nền tảng

```text
Permutation: P(n, k) = n! / (n-k)!
Combination: C(n, k) = n! / (k!(n-k)!)
```

---

## 4. Xác suất và thống kê cho engineer

### Chủ đề cần nắm
- Sample space, event, conditional probability
- Bayes rule
- Random variable, expectation, variance
- Common distributions: Bernoulli, Binomial, Poisson, Normal, Exponential
- Law of large numbers, central limit theorem ở mức trực giác

### Ứng dụng thực tế
- A/B testing
- Retry success probability
- False positive của Bloom filter
- Queueing intuition: latency, throughput, tail latency
- Reliability: xác suất nhiều thành phần cùng fail

### Ví dụ cần hiểu
- Nếu một request thành công với xác suất 0.9, 3 lần retry độc lập thì xác suất thất bại hoàn toàn là bao nhiêu?
- Nếu hệ thống có 3 replicas độc lập, xác suất available là bao nhiêu?

---

## 5. Graph math và discrete structures

### Chủ đề cần nắm
- Graph, node, edge, degree
- Directed vs undirected, weighted vs unweighted
- Path, cycle, connected components
- Tree, spanning tree, DAG
- Matrix representation: adjacency matrix, incidence matrix

### Ứng dụng thực tế
- Dependency resolution
- Routing, social graph, workflow engine
- Build systems, package managers, scheduling, deadlock detection

---

## 6. Linear algebra, calculus và statistics nên học đến đâu

### Linear algebra
- Vector, matrix, dot product
- Matrix multiplication
- Eigenvalues/eigenvectors ở mức trực giác
- Projection, norm, distance

### Calculus
- Derivative như tốc độ thay đổi
- Gradient như hướng tăng nhanh nhất
- Integral như tích lũy tổng

### Statistics
- Mean, median, percentile, standard deviation
- Confidence interval và p-value ở mức thực dụng
- Sampling bias, survivorship bias, Simpson's paradox

### Khi nào thật sự cần sâu
- AI/ML, graphics, optimization, simulation, robotics

---

## ✅ Checklist ôn tập
- Giải thích được induction là gì và dùng khi nào
- Chứng minh được tính đúng của binary search hoặc BFS
- Tự tính được permutation/combination cơ bản
- Tính được conditional probability và expectation đơn giản
- Phân biệt được graph, tree, DAG và các ứng dụng của chúng
- Giải thích được vì sao `n log n` tăng chậm hơn `n^2`

## 📝 Bài tập
1. Chứng minh tổng `1 + 2 + ... + n = n(n+1)/2` bằng induction.
2. Tìm phản ví dụ cho một greedy algorithm sai do bạn tự nghĩ ra.
3. Tính xác suất ít nhất 1 request thành công sau `k` lần retry.
4. Vẽ dependency graph cho một project có 10 modules.
5. Viết 10 flashcards cho logic và probability.

## 📚 Tài liệu
- *Mathematics for Computer Science* — MIT
- *Discrete Mathematics and Its Applications* — Kenneth Rosen
- *Introduction to Probability* — Blitzstein & Hwang