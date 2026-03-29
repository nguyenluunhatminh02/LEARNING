# Bài 16: Software Engineering

## 🎯 Mục tiêu
- Biến kiến thức CS thành năng lực xây sản phẩm và hệ thống có thể bảo trì lâu dài
- Nắm requirements, design, testing, delivery, observability, refactoring, collaboration và technical decision making
- Hiểu vì sao code đúng hôm nay chưa chắc là software tốt trong 6 tháng tới

## 📖 Bức tranh lớn
Computer Science cho bạn nguyên lý. Software Engineering cho bạn cách biến nguyên lý đó thành hệ thống mà đội ngũ thật sự có thể xây, review, deploy, vận hành, sửa lỗi và mở rộng cùng nhau. Rất nhiều thất bại trong sản phẩm không đến từ thuật toán kém mà đến từ yêu cầu mơ hồ, code khó bảo trì, test yếu, release thiếu kiểm soát hoặc observability tệ.

---

## 1. Requirements và problem framing

### Chủ đề cần nắm
- Functional vs non-functional requirements
- Constraints, assumptions, trade-offs
- Acceptance criteria
- Success metrics

### Kỹ năng quan trọng
- Biến yêu cầu mơ hồ thành spec cụ thể
- Hỏi đúng câu hỏi trước khi code
- Tách must-have, should-have, nice-to-have

---

## 2. Design và architecture

### Chủ đề cần nắm
- Modularity
- Coupling vs cohesion
- Layered architecture
- Clean/hexagonal architecture ở mức thực dụng
- Domain boundaries
- API contracts và versioning

### Điều phải nhớ
- Kiến trúc tốt làm thay đổi dễ hơn, không phải để sơ đồ đẹp hơn
- Abstraction nên che giấu phức tạp nhưng không che cost model

---

## 3. Code quality và maintainability

### Nền tảng
- Naming
- Small functions, clear modules
- Explicit contracts
- Refactoring liên tục
- Technical debt management

### Dấu hiệu codebase đi xuống
- God classes/modules
- Circular dependency
- Duplicate logic
- Hidden side effects
- Tests chậm và flaky

---

## 4. Testing strategy

### Các tầng test
- Unit tests
- Integration tests
- Contract tests
- End-to-end tests
- Load/performance tests ở mức cần thiết

### Tư duy đúng
- Không chạy theo coverage mù quáng
- Test nên tập trung vào behavior và invariants quan trọng
- Test pyramid vẫn hữu ích, nhưng hãy điều chỉnh theo sản phẩm

---

## 5. Delivery, CI/CD và release engineering

### Chủ đề cần nắm
- Trunk-based vs branching strategies
- CI pipelines
- Artifact build và reproducibility
- Deployment strategies: rolling, blue-green, canary
- Feature flags
- Rollback strategy

### Vì sao quan trọng
- Tốc độ ra feature không có ý nghĩa nếu release không ổn định
- Build không reproducible là nguồn lỗi rất tốn thời gian

---

## 6. Observability và operations

### Tối thiểu cần có
- Logs có cấu trúc
- Metrics
- Traces
- Dashboards
- Alerts có ngưỡng hợp lý
- Runbooks và postmortems

### Mục tiêu
- Lỗi xảy ra thì phát hiện nhanh
- Điều tra được nguyên nhân
- Rút kinh nghiệm để lỗi đó ít lặp lại hơn

---

## 7. Performance, reliability và scalability

### Cần nắm
- Capacity planning
- Load testing
- Bottleneck analysis
- Graceful degradation
- Error budgets/SLO ở mức overview

### Tư duy quan trọng
- Reliability là tính năng
- Performance tuning phải đo và ưu tiên đúng chỗ

---

## 8. Collaboration và technical leadership ở mức engineer

### Kỹ năng nên luyện
- Code review chất lượng
- Design review
- Viết ADR/RFC
- Chia nhỏ công việc
- Mentoring và documentation

### Dấu hiệu trưởng thành
- Không chỉ fix bug, mà cải thiện hệ thống để bug tương tự khó quay lại
- Không chỉ code nhanh, mà ra quyết định có thể giải thích được

---

## ✅ Checklist ôn tập
- Phân biệt được yêu cầu chức năng và phi chức năng
- Thiết kế được module boundaries rõ ràng cho một service nhỏ
- Chọn được test strategy hợp lý cho một tính năng
- Hiểu pipeline release cơ bản và rollback strategy
- Biết metrics/logs/traces hỗ trợ điều tra sự cố ra sao

## 📝 Bài tập
1. Viết design doc ngắn cho một feature mới.
2. Tạo checklist code review cá nhân.
3. Phân tích một bug production và viết mini postmortem.
4. Thiết kế CI/CD flow cho một service backend.
5. Refactor một module cũ và ghi lại trade-off đã chọn.

## 📚 Tài liệu
- *Accelerate* — Forsgren, Humble, Kim
- *A Philosophy of Software Design* — John Ousterhout
- Track đào sâu: `../../05_Software_Engineering/`