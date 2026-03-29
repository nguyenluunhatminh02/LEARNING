# Software and Security Deep Dive

## Mục tiêu của file này
File này đào sâu cho:
- Software Engineering
- Security and Cryptography

Hai phần này biến kiến thức kỹ thuật thành hệ thống có thể triển khai, vận hành, bảo vệ và cải thiện trong thời gian dài.

---

## 1. Engineering is decision quality over time

Software engineering tốt không chỉ là code chạy được hôm nay. Nó là chuỗi quyết định giúp hệ thống:
- đúng
- thay đổi được
- test được
- vận hành được
- quan sát được
- bảo vệ được

Security cũng vậy: không phải checklists rời rạc, mà là cách bạn thiết kế trust boundaries và failure handling từ đầu.

---

## 2. Requirements and architecture deep dive

### Requirements clarity
Trước khi code, bạn nên làm rõ:
- actor nào dùng feature này
- success metrics là gì
- failure tolerance ra sao
- latency/SLA/SLO constraints có không
- dữ liệu nhạy cảm nào xuất hiện

### Architecture quality
Kiến trúc tốt thường có:
- boundaries tương đối rõ
- dependencies hợp lý
- contracts explicit
- blast radius được kiểm soát

Kiến trúc tệ thường có:
- modules phụ thuộc vòng tròn
- business logic lẫn với transport/storage details
- thay đổi nhỏ phải chạm nhiều nơi

---

## 3. Testing and delivery deep dive

### Testing should protect behavior, not vanity metrics

Coverage có ích nhưng không đủ. Điều quan trọng hơn là:
- test đúng invariants
- test edge cases quan trọng
- test integration points hay vỡ
- test failure/retry behavior khi cần

### CI/CD maturity signs
- build reproducible
- tests đủ nhanh để team không né chạy
- deploy rollback được
- feature flags dùng có kỷ luật
- config changes được review và traceable

---

## 4. Observability and incident discipline

### Observability stack tối thiểu
- logs có context
- metrics cho throughput/error/saturation/latency
- tracing cho request path qua nhiều services
- dashboards gắn với user-visible outcomes

### Incident discipline
- phát hiện sớm
- limit blast radius
- rollback hoặc degrade gracefully
- postmortem không đổ lỗi cá nhân
- root cause phải đi tới system fix chứ không chỉ human reminder

---

## 5. Security mindset deep dive

### Trust boundaries
Phải xác định rõ:
- client có thể giả mạo mọi input
- internal network không tự động đáng tin
- logs, metrics, analytics pipelines cũng có thể chứa dữ liệu nhạy cảm

### Security principles worth operationalizing
- least privilege
- defense in depth
- secure defaults
- auditability
- revocability

### Common misconception
"Chúng tôi có JWT/OAuth nên hệ thống đã secure" là một ngộ nhận. Authn/authz chỉ là một mảng nhỏ.

---

## 6. Authentication and authorization details that matter

### Authentication
Phải nghĩ tới:
- password hashing strong enough
- MFA cho actions nhạy cảm
- session/token expiration
- device/session revocation

### Authorization
Phải nghĩ tới:
- object-level checks
- role explosion
- policy drift giữa services
- admin/debug endpoints bị bỏ quên

### Practical question
Nếu user A sửa được tài nguyên của user B, lỗi nằm ở đâu: UI, API, DB hay policy engine? Câu trả lời đúng thường là: trust boundary bị thiết kế sai ở backend.

---

## 7. Secure coding and crypto practicality

### Secure coding
Bạn phải internalize các nguyên tắc sau tới mức thành phản xạ:
- parameterized queries
- output encoding theo context
- validate input and enforce limits
- never trust filenames/paths from clients
- rate-limit sensitive actions

### Crypto practicality
Engineer nên biết đủ để không phá:
- password dùng hashing chậm, có salt
- data-in-transit dùng TLS chuẩn
- secrets lấy từ secret store, không hardcode
- signatures khác encryption

---

## 8. Supply chain and operational security

### Nguồn risk thường bị xem nhẹ
- dependency vulnerabilities
- leaked CI tokens
- over-privileged cloud roles
- stale secrets
- misconfigured buckets or storage policies

### Maturity indicators
- dependency audit chạy định kỳ
- secrets scanning trong repo/CI
- access reviews có lịch
- incident runbooks tồn tại và dùng được

---

## 9. Mistake catalog

- code theo spec nhưng không hỏi threat model
- có tests nhưng không test authz boundaries
- log quá nhiều, vô tình lộ secrets/PII
- phụ thuộc một lớp bảo vệ duy nhất
- rollout nhanh nhưng rollback và incident handling yếu

---

## 10. What to know cold

Bạn nên biết cold:
- functional vs non-functional requirements
- unit/integration/contract/E2E test khác nhau ra sao
- logs/metrics/traces phục vụ mục đích gì
- authentication vs authorization
- hashing vs encryption vs signatures
- least privilege, defense in depth, threat modeling là gì

---

## 11. Suggested labs

### Lab 1: Security review of one API
Viết checklist cho:
- authn
- authz
- input validation
- rate limiting
- secret handling
- logging safety

### Lab 2: Mini postmortem
Tự tạo một incident giả định và viết:
- timeline
- impact
- root cause
- detection gap
- preventive actions

### Lab 3: Design review template
Tạo template review một feature mới với phần correctness, operability và security.

### Lab 4: Threat model worksheet
Liệt kê assets, actors, trust boundaries, entry points, mitigations cho một service nhỏ.

---

## 12. Oral exam questions

- Vì sao high coverage vẫn không bảo đảm quality?
- Blast radius là gì và giảm nó bằng cách nào?
- Tại sao authn không đồng nghĩa authz?
- Khi nào logging trở thành risk security?
- Vì sao "internal service" không nên tự động được tin tuyệt đối?
- Một postmortem tốt khác một blame document ở đâu?

---

## 13. Final reminder
Nếu algorithms giúp bạn giải bài toán đúng, thì software engineering và security giúp lời giải đó sống sót ngoài đời thật. Đây không phải phần phụ. Đây là nơi đa số hệ thống thực sự thắng hoặc thua.