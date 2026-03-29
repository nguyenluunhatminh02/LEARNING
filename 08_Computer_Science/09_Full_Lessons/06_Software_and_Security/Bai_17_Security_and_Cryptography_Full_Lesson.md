# Bài 17: Security and Cryptography — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- có security mindset nền tảng cho software engineer
- hiểu authn, authz, secure coding, cryptography, secrets và threat modeling ở mức practical
- tránh được một số sai lầm bảo mật rất phổ biến trong ứng dụng và hệ thống

## Bạn cần biết trước
- Bài 16 là tiền đề rất tốt

---

## 1. Security là một phần của engineering

Security không phải bước cuối cùng. Nó phải xuất hiện từ lúc bạn xác định:
- dữ liệu nào nhạy cảm
- actor nào có quyền gì
- đâu là trust boundary
- hậu quả khi hệ thống bị lạm dụng hoặc bị lỗi là gì

Một hệ thống nhanh nhưng không an toàn là hệ thống chưa hoàn chỉnh.

---

## 2. Các nguyên tắc nền tảng

### CIA triad
- confidentiality
- integrity
- availability

### Các nguyên tắc khác
- least privilege
- defense in depth
- fail secure
- secure defaults

Những từ này chỉ hữu ích khi bạn biến chúng thành quyết định kỹ thuật cụ thể.

---

## 3. Authentication và authorization

### Authentication
Xác minh bạn là ai.

### Authorization
Xác định bạn được làm gì.

Đây là cặp khái niệm bị nhầm rất nhiều.

Ví dụ:
- user đăng nhập thành công chưa có nghĩa họ được sửa tài nguyên của người khác

### Các chủ đề nên biết
- password hashing
- MFA
- sessions/tokens
- RBAC
- ownership checks

---

## 4. Secure coding

Một số lỗi nền tảng nên nắm thật chắc:
- SQL injection
- XSS
- CSRF
- SSRF
- broken access control
- insecure file handling

### Quy tắc thực dụng
- parameterized queries
- validate input
- encode output theo context
- không trust client
- giới hạn rate cho actions nhạy cảm

---

## 5. Cryptography cho engineer

Bạn không cần tự thiết kế crypto. Bạn cần hiểu đủ để không dùng sai.

### Cần phân biệt rõ
- hashing
- symmetric encryption
- asymmetric encryption
- digital signatures
- TLS

### Điều không nên làm
- dùng fast hash cho password
- hardcode secrets
- tự tạo crypto scheme
- tắt certificate verification bừa bãi

---

## 6. Secrets và key management

Secrets nên được:
- lưu trong secret manager hoặc môi trường an toàn
- rotate định kỳ
- cấp theo least privilege
- không log ra ngoài

Đây là điểm rất hay bị xem nhẹ cho tới khi có incident.

---

## 7. Threat modeling

Threat modeling bắt đầu bằng các câu hỏi:
- tài sản nào cần bảo vệ?
- attacker là ai?
- entry points là gì?
- hậu quả của compromise là gì?
- mitigations nào hợp lý nhất?

Đây là kỹ năng thực dụng hơn nhiều người nghĩ.

---

## 8. Supply chain và operational security

Security không chỉ nằm trong business logic.

Bạn cũng phải nghĩ tới:
- dependencies
- CI/CD credentials
- cloud permissions
- logging of sensitive data
- container/image hygiene

---

## 9. Sai lầm phổ biến
- nghĩ có JWT là đủ secure
- kiểm tra auth ở UI nhưng quên backend
- log secrets/PII
- không phân loại data sensitivity
- chỉ nghĩ tới attacker bên ngoài mà quên internal trust boundaries

---

## 10. Checklist sau bài
- Phân biệt rõ authn và authz
- Giải thích được hashing, encryption, signatures khác nhau thế nào
- Nêu được các lỗi secure coding nền tảng và cách giảm thiểu
- Biết secret nên được quản lý ra sao
- Làm được threat model đơn giản cho một service

## 11. Bài tập thực hành
1. Viết security checklist cho một REST API.
2. Threat-model một ứng dụng quản lý tài khoản người dùng.
3. Tự thiết kế flow reset password và review security risks.
4. Viết một note phân biệt hashing và encryption.
5. Kiểm tra một project của bạn xem có secrets/config nào đang để sai chỗ không.

## 12. Mini deliverable
Tạo file `security_review_pack.md` gồm:
- authn/authz checks
- input validation checks
- secret handling checks
- threat model template
- logging safety checks

## 13. Học tiếp
- `../07_Theory_and_Specialized/Bai_18_Theory_of_Computation_Full_Lesson.md`
- `../../08_Reference_and_Review/07_Software_and_Security_Deep_Dive.md`