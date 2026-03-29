# Bài 20: Review Plan, Research and Capstones

## 🎯 Mục tiêu
- Biến toàn bộ track thành một hệ thống học và ôn tập bền vững
- Biết cách tổng hợp kiến thức, đọc tài liệu sâu, làm capstone và xây portfolio kỹ thuật
- Chuyển từ "đọc nhiều" sang "nắm chắc, dùng được, giải thích được"

## 📖 Bức tranh lớn
Học CS theo kiểu gom thật nhiều tài liệu rất dễ tạo ảo giác tiến bộ. Điều tạo năng lực thật là chu kỳ: học -> áp dụng -> giải thích lại -> ôn -> làm project -> rút kinh nghiệm. Bài cuối cùng này là phần nối tất cả các mảnh kiến thức thành một hệ thống lâu dài.

---

## 1. Cách ôn tập kiến thức kỹ thuật

### 4 tầng nhớ cần luyện
- Recognition: nhìn thấy thuật ngữ là nhớ ra
- Recall: tự nói lại không cần nhìn
- Transfer: áp dụng sang bài toán mới
- Synthesis: kết nối nhiều chủ đề thành một lời giải thống nhất

### Chu kỳ ôn gợi ý
```text
Ngày 1: học mới
Ngày 2: nhắc lại 10-15 phút
Ngày 7: self-quiz
Ngày 21: giải thích lại bằng note hoặc voice
Ngày 45: áp dụng vào bài tập/project
```

---

## 2. Note-taking và knowledge base

### Nên lưu cho mỗi bài
- 5-10 khái niệm cốt lõi
- 3 trade-offs quan trọng
- 3 lỗi phổ biến
- 1 diagram hoặc mental model
- 3 câu hỏi tự kiểm tra

### Mẫu note tốt
```text
Khái niệm:
Trade-off:
Failure mode:
Ví dụ thực tế:
Liên hệ với bài khác:
```

---

## 3. Self-testing và interview-style review

### Cách tự kiểm tra
- Whiteboard explanation
- Flashcards cho thuật ngữ và trade-offs
- Viết code template từ trí nhớ
- So sánh 2 công nghệ/hai mô hình bằng bảng
- Phân tích một incident giả định

### Câu hỏi ôn tập rất tốt
- Tại sao hệ thống này chậm?
- Nếu scale 10x thì vỡ ở đâu trước?
- Nếu node chết giữa giao dịch thì sao?
- Nếu dữ liệu sai lệch thì ai chịu trách nhiệm phát hiện?

---

## 4. Đọc sách, docs và paper

### Cách đọc hiệu quả
- Đọc với câu hỏi cụ thể, không đọc vô định
- Gạch ra assumptions và trade-offs của tác giả
- So sánh với hệ thống bạn biết
- Tóm tắt sau mỗi chương/paper

### Khi đọc paper
- Problem statement là gì?
- Novelty là gì?
- Assumptions có thực tế không?
- Cost vận hành/triển khai là gì?

---

## 5. Capstone projects đề xuất

### Capstone 1: Mini Database / KV Store
- In-memory table
- WAL
- SSTable hoặc B-Tree index đơn giản
- TCP/HTTP interface
- Benchmark reads/writes

### Capstone 2: Mini HTTP Server / Reverse Proxy
- Routing
- Thread pool hoặc async I/O
- Logging/metrics
- Rate limiting
- Caching cơ bản

### Capstone 3: Search/Analytics Engine
- Inverted index hoặc event aggregation
- Ranking/aggregation
- Batch + incremental update

### Capstone 4: Tiny Language / Interpreter
- Lexer
- Parser
- AST evaluation
- Variables/functions

### Capstone 5: Distributed Task Queue
- Producer/consumer
- Retry/backoff
- Idempotency
- Failure handling

---

## 6. Portfolio artifacts nên có

- README rõ ràng
- Design doc / architecture diagram
- Benchmark hoặc profiling notes
- Failure analysis
- Trade-off analysis
- Test strategy
- Lessons learned

Những artifact này quan trọng gần như code, vì chúng chứng minh bạn hiểu hệ thống chứ không chỉ copy implementation.

---

## 7. Kế hoạch 3 tháng, 6 tháng, 12 tháng

### 3 tháng
- Học hết Bài 01-10
- Làm 1 project nhỏ về algorithms/systems
- Tạo note base cá nhân

### 6 tháng
- Học hết Bài 01-17
- Hoàn thành 1 capstone nghiêm túc
- Ôn theo self-quiz hằng tuần

### 12 tháng
- Học hết toàn bộ track
- Chọn 1-2 nhánh chuyên sâu
- Viết 2-3 design docs hoặc technical essays
- Có portfolio chứng minh chiều sâu kỹ thuật

---

## ✅ Checklist ôn tập cuối track
- Giải thích được 20 bài ở mức high-level mà không nhìn tài liệu
- Tự code được một số thành phần cốt lõi: parser, cache, queue, index, concurrent worker, network client/server đơn giản
- Biết cách đọc design doc và paper kỹ thuật với góc nhìn phản biện
- Có ít nhất một capstone thật sự hoàn chỉnh
- Có hệ thống note/review để không mất kiến thức sau vài tháng

## 📝 Bài tập
1. Chọn 1 capstone và viết design doc trước khi code.
2. Lập lịch review 8 tuần cho 20 bài.
3. Tạo 50 flashcards cho các khái niệm lõi.
4. Viết một technical essay 1000-1500 từ từ một bài bất kỳ.
5. Tự đánh giá lỗ hổng kiến thức của mình theo 20 bài và ưu tiên 3 mảng cần lấp ngay.

## 📚 Tài liệu
- *How to Take Smart Notes* — Sönke Ahrens
- *The Manager's Path* và tài liệu design docs/RFCs nếu bạn hướng senior/staff
- Sách/paper theo nhánh chuyên sâu bạn chọn