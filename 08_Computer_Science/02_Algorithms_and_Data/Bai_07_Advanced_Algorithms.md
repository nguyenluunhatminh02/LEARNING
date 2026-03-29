# Bài 07: Advanced Algorithms

## 🎯 Mục tiêu
- Mở rộng beyond interview basics sang các họ thuật toán mạnh trong hệ thống thực tế
- Biết những mảng nên học tiếp khi muốn lên sâu hơn về systems, search, data, research
- Có bản đồ các kỹ thuật nâng cao để không bị giới hạn ở array/string/tree cơ bản

## 📖 Bức tranh lớn
Sau bộ nền tảng, advanced algorithms cho bạn những công cụ để xử lý bài toán lớn, dữ liệu dòng, truy vấn phức tạp, text/search, hệ phân tán hoặc tối ưu khó. Bạn không cần master tất cả ngay, nhưng cần biết chúng tồn tại và dùng khi nào.

---

## 1. String algorithms

### Chủ đề cần biết
- Trie
- KMP
- Rabin-Karp
- Z algorithm
- Suffix array / suffix tree ở mức overview
- Aho-Corasick cho multiple pattern matching

### Ứng dụng
- Search/autocomplete
- Log scanning
- DNA/bioinformatics
- Compiler token matching

---

## 2. Range queries và data processing

### Chủ đề cần biết
- Fenwick tree
- Segment tree
- Sparse table
- Disjoint set union on offline queries
- Mo's algorithm ở mức overview

### Ứng dụng
- Analytics queries
- Time series snapshots
- Competitive programming/algorithmic optimization

---

## 3. Randomized algorithms và probabilistic structures

### Chủ đề cần biết
- Randomized quicksort/select
- Reservoir sampling
- Hashing with randomness
- Bloom filter, Count-Min Sketch, HyperLogLog

### Ứng dụng
- Approximate counting ở scale lớn
- Cardinality estimation
- Streaming analytics
- Caching và anti-abuse systems

---

## 4. Approximation và heuristic thinking

### Tại sao cần
Nhiều bài toán thực tế là NP-hard. Đôi khi mục tiêu tốt hơn là:

- Tìm nghiệm đủ tốt nhanh
- Có guarantee gần tối ưu
- Hoặc dùng heuristic dễ vận hành

### Chủ đề nên biết
- Approximation ratio
- Greedy heuristics
- Local search
- Simulated annealing, genetic algorithms ở mức nhận biết

---

## 5. Online, streaming và external-memory mindset

### Online algorithms
- Ra quyết định khi dữ liệu đến dần, chưa thấy tương lai
- Ví dụ: scheduling, rate limiting, admission control

### Streaming algorithms
- Chỉ giữ ít memory
- Ví dụ: top-K frequent, approximate distinct count, anomaly metrics

### External-memory algorithms
- Dữ liệu không vừa RAM
- Tối ưu số lần đọc/ghi disk hoặc object storage
- Ví dụ: merge sort ngoài bộ nhớ, SSTable compaction, map-reduce style processing

---

## 6. Flow, matching, optimization families

### Nên biết ở mức overview
- Max flow / min cut
- Bipartite matching
- Min-cost flow
- Linear programming / integer programming ở mức trực giác

### Ứng dụng
- Assignment problems
- Resource allocation
- Scheduling
- Network capacity planning

---

## 7. Thuật toán cho systems engineers

### Các ví dụ rất đáng học
- Consistent hashing
- Skip list
- Raft/Paxos ở mức algorithmic intuition
- LRU/LFU cache eviction
- Token bucket / leaky bucket
- Merkle tree
- Vector clock / Lamport clock

Những thuật toán này xuất hiện trực tiếp trong backend, distributed systems, database và observability.

---

## ✅ Checklist ôn tập
- Biết ít nhất 5 chủ đề advanced algorithms và use case của chúng
- Giải thích được approximate data structure hoạt động để làm gì
- Nhận ra khi nào exact solution là quá đắt và approximation hợp lý hơn
- Có khái niệm về string/range/streaming/system algorithms
- Biết chọn một nhánh để đào sâu theo định hướng nghề nghiệp

## 📝 Bài tập
1. Tóm tắt 1 trang về Bloom Filter, HyperLogLog và Count-Min Sketch.
2. Tìm use case thực tế cho max flow hoặc bipartite matching.
3. Cài đặt LRU cache và token bucket rate limiter.
4. Đọc về consistent hashing và mô phỏng với 1000 keys.
5. Chọn 1 nhánh nâng cao để học sâu trong 2 tuần tiếp theo.

## 📚 Tài liệu
- *Algorithms* — Dasgupta, Papadimitriou, Vazirani
- *Mining of Massive Datasets* — Leskovec et al.
- Track đào sâu: `../../04_DSA/` và `../../02_System_Design/`