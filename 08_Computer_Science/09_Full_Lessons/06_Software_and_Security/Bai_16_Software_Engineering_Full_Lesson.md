# Bài 16: Software Engineering — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- hiểu software engineering là cách biến kiến thức kỹ thuật thành hệ thống có thể bảo trì và vận hành lâu dài
- nắm requirements, architecture, testing, delivery, observability và technical decision making
- biết nhìn codebase như một hệ thống socio-technical chứ không chỉ là source code

## Bạn cần biết trước
- các bài về systems, data và programming fundamentals

---

## 1. Software engineering không chỉ là viết code

Code chỉ là một phần của software.

Software engineering còn bao gồm:
- hiểu yêu cầu
- thiết kế boundaries
- test đúng thứ cần test
- deploy an toàn
- quan sát được hệ thống
- sửa lỗi mà không phá chỗ khác

Nhiều sản phẩm thất bại không phải vì thuật toán yếu, mà vì hệ thống không maintainable.

---

## 2. Requirements và problem framing

Trước khi code, bạn cần làm rõ:
- ai dùng tính năng này
- vấn đề thật sự là gì
- success metric là gì
- failure tolerance ra sao
- non-functional requirements là gì

Nếu requirement mơ hồ, architecture và implementation cũng sẽ mơ hồ.

---

## 3. Modularity và architecture

Một architecture tốt thường giúp:
- thay đổi dễ hơn
- test dễ hơn
- reasoning rõ hơn
- blast radius nhỏ hơn

### Các từ khóa cần nắm
- cohesion
- coupling
- boundaries
- contracts
- layers

Điều quan trọng là architecture để phục vụ changeability, không phải để vẽ sơ đồ cho đẹp.

---

## 4. Code quality

### 3 thứ hiệu quả nhất
- naming rõ
- module responsibilities rõ
- side effects được cô lập hợp lý

### Dấu hiệu codebase xuống cấp
- God modules
- circular dependencies
- duplication kéo dài
- tests khó chạy
- ai sửa gì cũng sợ vỡ chỗ khác

Technical debt không thể tránh hoàn toàn, nhưng phải quản lý được.

---

## 5. Testing strategy

Bạn nên phân biệt:
- unit tests
- integration tests
- contract tests
- end-to-end tests

Điều quan trọng không phải chỉ là coverage cao, mà là test đúng behavior và failure modes quan trọng.

Một test suite tốt thường:
- chạy đủ nhanh
- ít flaky
- bảo vệ các invariants thực sự quan trọng

---

## 6. CI/CD và release engineering

Build và deploy là một phần của software engineering, không phải phần phụ.

### Cần nắm
- CI pipelines
- reproducible builds
- rollout strategies
- rollback plans
- feature flags

Một team release nhanh nhưng rollback kém là team đang tạo risk.

---

## 7. Observability và incidents

Hệ thống production cần:
- logs
- metrics
- traces
- dashboards
- alerts hợp lý
- runbooks

Khi incident xảy ra, mục tiêu không chỉ là khôi phục dịch vụ, mà còn phải học được điều gì cần sửa trong hệ thống để giảm xác suất tái diễn.

---

## 8. Decision making

Kỹ năng của senior/staff engineer nằm nhiều ở chất lượng quyết định:
- build vs buy
- monolith vs service split
- simple now vs flexible later
- optimize latency hay optimize maintainability

Nên ghi lại các quyết định quan trọng bằng ADR hoặc design doc ngắn.

---

## 9. Sai lầm phổ biến
- bắt đầu code khi requirement chưa rõ
- architecture over-engineered quá sớm
- test quá ít ở integration boundaries
- không đầu tư observability rồi production thành hộp đen
- xem postmortem như blame document thay vì learning document

---

## 10. Checklist sau bài
- Phân biệt được functional và non-functional requirements
- Giải thích được coupling, cohesion, blast radius
- Có tư duy test strategy thay vì chỉ viết unit tests
- Hiểu vai trò của CI/CD, rollback và feature flags
- Biết observability phục vụ điều tra sự cố ra sao

## 11. Bài tập thực hành
1. Viết design doc ngắn cho một feature bạn từng nghĩ tới.
2. Tạo checklist code review cá nhân.
3. Viết mini postmortem cho một bug thật hoặc giả định.
4. Thiết kế pipeline CI/CD cho một API service.
5. Chọn một module cũ và nêu 3 cải tiến maintainability.

## 12. Mini deliverable
Tạo file `software_engineering_playbook.md` gồm:
- requirement checklist
- design review checklist
- test strategy template
- incident/postmortem template

## 13. Học tiếp
- `Bai_17_Security_and_Cryptography_Full_Lesson.md`
- `../../08_Reference_and_Review/07_Software_and_Security_Deep_Dive.md`