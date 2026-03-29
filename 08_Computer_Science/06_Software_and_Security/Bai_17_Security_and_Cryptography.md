# Bài 17: Security and Cryptography

## 🎯 Mục tiêu
- Xây security mindset như một phần mặc định của engineering
- Nắm secure coding, authentication, authorization, cryptography, secrets, network security và threat modeling
- Biết bảo vệ hệ thống ở mức đủ thực dụng trước khi đi sâu vào security chuyên nghiệp

## 📖 Bức tranh lớn
Security không phải lớp sơn phủ cuối dự án. Nó là tập hợp các quyết định từ đầu: data nào nhạy cảm, ai được truy cập, lỗi nào có thể bị khai thác, secret nằm ở đâu, kẻ tấn công có động cơ gì và hệ thống fail như thế nào khi bị tấn công. Một hệ thống nhanh nhưng không an toàn là hệ thống chưa hoàn chỉnh.

---

## 1. Security principles cơ bản

### Cần nắm
- CIA triad: confidentiality, integrity, availability
- Least privilege
- Defense in depth
- Fail secure
- Trust boundaries

### Tư duy quan trọng
- Mọi input đều có thể ác ý hoặc sai định dạng
- Mọi secret để lộ ở sai chỗ cuối cùng sẽ bị lộ

---

## 2. Authentication và authorization

### Authentication
- Password hashing
- MFA
- Session management
- OAuth2, OIDC, tokens ở mức thực dụng

### Authorization
- RBAC
- ABAC
- Ownership checks
- Policy enforcement

### Sai lầm phổ biến
- Nhầm authentication với authorization
- Chỉ kiểm tra quyền ở UI mà không kiểm tra ở backend

---

## 3. Secure coding basics

### OWASP-level chủ đề phải nắm
- Injection
- XSS
- CSRF
- SSRF
- Broken access control
- Insecure deserialization ở mức overview
- File upload và path traversal risks

### Nguyên tắc thực dụng
- Validate input
- Encode output đúng context
- Parameterized queries
- Không trust client
- Rate limiting cho action nhạy cảm

---

## 4. Cryptography đủ dùng cho engineer

### Cần phân biệt rõ
- Hashing
- Symmetric encryption
- Asymmetric encryption
- Digital signatures
- TLS/HTTPS

### Điều không được sai
- Không dùng crypto tự chế
- Không dùng fast hash cho password
- Không hardcode secrets
- Không tắt certificate verification bừa bãi

---

## 5. Secrets, keys và data protection

### Chủ đề cần nắm
- Secrets manager
- Key rotation
- Encryption at rest vs in transit
- Data classification
- PII handling
- Audit logs

### Thực tế cần nhớ
- Secret trong source code hoặc CI logs là lỗi nghiêm trọng
- Access control với dữ liệu nhạy cảm phải được thiết kế từ đầu

---

## 6. Infrastructure và supply chain security

### Chủ đề nên biết
- Firewall, WAF, network segmentation
- Container image scanning
- Dependency scanning
- SBOM ở mức overview
- Signed builds/artifacts ở mức nhận biết

### Vì sao quan trọng
- Không chỉ application code mới là bề mặt tấn công
- Dependency và build pipeline cũng là entry point

---

## 7. Threat modeling và incident mindset

### Threat modeling
- Tài sản cần bảo vệ là gì?
- Attacker là ai?
- Entry points là gì?
- Hậu quả khi bị lộ/sửa/xóa dữ liệu là gì?

### Incident response mindset
- Detect
- Contain
- Eradicate
- Recover
- Learn

---

## 8. Security as engineering discipline

### Tích hợp vào SDLC
- Code review có góc nhìn security
- SAST/DAST/dependency audit
- Secrets scanning
- Security testing cho flows nhạy cảm
- Security docs và runbooks

---

## ✅ Checklist ôn tập
- Phân biệt được authn và authz
- Giải thích được hashing, encryption, signature khác nhau thế nào
- Nêu được 5 lỗi bảo mật ứng dụng phổ biến và cách giảm thiểu
- Biết secret nên được lưu và rotate ra sao
- Có thể làm threat model đơn giản cho một service

## 📝 Bài tập
1. Viết checklist security review cho một REST API.
2. Threat-model một ứng dụng lưu dữ liệu người dùng.
3. Tìm 5 điểm có thể sai trong flow login/reset password.
4. Viết note phân biệt hashing và encryption bằng ví dụ.
5. Kiểm tra một dự án của bạn xem đang có secret/config nào cần xử lý tốt hơn.

## 📚 Tài liệu
- *Security Engineering* — Ross Anderson
- *Designing Secure Software* — Loren Kohnfelder
- Track đào sâu: `../../06_Security/`