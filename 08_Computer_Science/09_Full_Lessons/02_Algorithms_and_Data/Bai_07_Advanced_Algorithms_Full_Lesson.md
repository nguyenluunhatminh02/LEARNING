# Bài 07: Advanced Algorithms — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- có bản đồ các nhóm thuật toán nâng cao ngoài phần coding interview cơ bản
- biết những mảng nào đáng đào sâu theo định hướng systems, data, search hoặc research
- không còn coi advanced algorithms là một vùng mơ hồ khó chạm tới

## Bạn cần biết trước
- Bài 04, 05, 06

---

## 1. Vì sao cần học advanced algorithms

Sau một thời gian học arrays, trees, DP, graph basics, bạn sẽ gặp các bài toán như:
- search trên text rất lớn
- nhiều truy vấn range liên tục
- dữ liệu streaming không thể lưu hết
- cần approximate answers vì exact quá đắt

Lúc này, advanced algorithms mở ra một bộ công cụ mới.

---

## 2. String algorithms

### Những cái nên biết tên và use case
- KMP
- Rabin-Karp
- Z algorithm
- suffix array
- Aho-Corasick

### Khi nào đáng học sâu
- text search
- log scanning
- autocomplete/search indexing
- bioinformatics hoặc parsing nặng

Điểm quan trọng là hiểu bài toán search chuỗi không chỉ có `contains()`.

---

## 3. Range query structures

### Fenwick tree
Gọn hơn, phù hợp cho một số prefix/range queries.

### Segment tree
Linh hoạt hơn, hỗ trợ nhiều dạng query/update hơn.

### Sparse table
Hữu ích khi dữ liệu tĩnh và query rất nhiều.

Bạn không nhất thiết dùng hằng ngày, nhưng nên biết chúng tồn tại để không bị giới hạn tư duy.

---

## 4. Randomized và probabilistic structures

### Randomized quicksort/select
Dùng randomness để tránh các pattern input xấu.

### Bloom filter
Membership test nhanh với false positive có kiểm soát.

### Count-Min Sketch / HyperLogLog
Tốt cho streaming analytics và approximate counting.

Chúng xuất hiện rất nhiều trong systems và data infrastructure.

---

## 5. Approximation và heuristics

Không phải mọi bài toán đều nên hoặc có thể giải exact ở scale lớn.

Bạn nên biết:
- heuristic: nhanh, thực dụng, không guarantee mạnh
- approximation: có guarantee gần tối ưu

Điều này đặc biệt quan trọng với:
- scheduling
- routing
- placement
- optimization problems lớn

---

## 6. Streaming và online algorithms

### Streaming
Data đến liên tục, không thể lưu hết.

### Online
Phải ra quyết định khi chưa biết tương lai.

Use cases:
- telemetry
- analytics
- admission control
- load shedding
- realtime ranking/counters

---

## 7. System algorithms đáng học

Đây là vùng giao giữa thuật toán và backend/distributed systems:
- consistent hashing
- token bucket
- LRU/LFU eviction
- Merkle tree
- skip list
- vector clocks / Lamport clocks

Nếu bạn hướng backend/systems, đây là nơi rất đáng đầu tư.

---

## 8. Cách chọn nhánh advanced để đào sâu

### Nếu thích search/text
đi vào string algorithms và indexing

### Nếu thích backend systems
đi vào system algorithms và probabilistic structures

### Nếu thích competitive/programming puzzles
đi vào segment tree, flows, geometry, bit tricks

### Nếu thích data infrastructure
đi vào streaming, sketches, large-scale approximate methods

---

## 9. Sai lầm phổ biến
- nghĩ advanced algorithms là "quá xa thực tế"
- đọc tên structure nhưng không hiểu use case
- cố học quá nhiều nhánh cùng lúc
- nhảy vào implementation trước khi hiểu problem class nó giải quyết

---

## 10. Checklist sau bài
- Kể được ít nhất 5 chủ đề advanced algorithms và use case của chúng
- Phân biệt được approximate structure với exact structure
- Nhận ra khi nào exact solution là quá đắt
- Chọn được một nhánh nâng cao phù hợp với mục tiêu của mình

## 11. Bài tập thực hành
1. Tóm tắt Bloom Filter, HyperLogLog và Count-Min Sketch mỗi cái trong 1 đoạn.
2. Chọn 1 system algorithm và giải thích use case production của nó.
3. Tìm một bài toán có thể dùng approximation hoặc heuristic tốt hơn exact solution.
4. Chọn 1 nhánh advanced và lập kế hoạch học 2 tuần.
5. Viết bảng mapping giữa advanced topic và ngành ứng dụng.

## 12. Mini deliverable
Tạo file `advanced_algorithms_specialization_plan.md` với:
- nhánh bạn chọn
- vì sao chọn
- tài liệu sẽ đọc
- mini project muốn làm

## 13. Học tiếp
- `../03_Systems/Bai_08_Operating_Systems_Full_Lesson.md`
- `../../08_Reference_and_Review/03_Algorithms_and_Data_Deep_Dive.md`