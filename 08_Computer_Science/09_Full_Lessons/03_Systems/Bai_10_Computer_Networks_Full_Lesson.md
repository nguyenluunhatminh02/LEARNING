# Bài 10: Computer Networks — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- hiểu đường đi của dữ liệu qua mạng từ client tới server và ngược lại
- nắm IP, TCP, UDP, DNS, HTTP, TLS, load balancing ở mức thực dụng
- có khung suy nghĩ tốt hơn về timeout, retry, latency và packet loss

## Bạn cần biết trước
- Bài 08 và 09 hỗ trợ rất tốt

---

## 1. Vì sao engineer nào cũng nên hiểu mạng

Hầu hết software hiện đại là networked software.

Một request có thể đi qua:
- DNS
- TCP handshake
- TLS handshake
- load balancer
- reverse proxy
- app server
- downstream services
- database/cache

Nếu không hiểu mạng, bạn rất khó debug timeout và reliability issues.

---

## 2. Layered model

Bạn không cần học OSI như học thuộc lòng, nhưng nên hiểu khái niệm layer:
- link layer
- IP layer
- transport layer
- application layer

Ý nghĩa:
- mỗi layer giải một lớp vấn đề
- lỗi ở tầng dưới có thể biểu hiện như bug ở tầng trên

---

## 3. IP và routing

IP chịu trách nhiệm địa chỉ và forwarding packets qua mạng.

### Khái niệm nên biết
- IP address
- subnet/CIDR
- router/gateway
- NAT

Ứng dụng thực tế:
- VPC/network design
- private vs public endpoints
- cross-region connectivity

---

## 4. TCP, UDP và QUIC

### TCP
- reliable
- ordered
- connection-oriented

### UDP
- lightweight
- không bảo đảm delivery/order

### QUIC
- chạy trên UDP
- kết hợp nhiều lợi ích hiện đại cho HTTP/3

Tư duy đúng:
- ordered delivery có lợi nhưng cũng có cost
- reliability không miễn phí

---

## 5. DNS

DNS biến tên miền thành địa chỉ hoặc records cần thiết.

### Những thứ nên hiểu
- resolver
- authoritative server
- TTL
- caching

DNS không phải chi tiết phụ. Nhiều sự cố thật ra nằm ở đây.

---

## 6. HTTP và application protocols

### HTTP
- request/response
- methods
- status codes
- headers
- caching
- keep-alive

### Những câu hỏi engineering nên đặt
- request này có idempotent không?
- retry an toàn không?
- payload có quá lớn không?
- có cần streaming hoặc WebSocket không?

---

## 7. TLS và bảo vệ kết nối

TLS giúp bảo vệ:
- confidentiality
- integrity
- server identity

Bạn không cần thuộc chi tiết handshake từng byte, nhưng nên hiểu:
- certificate chain
- expired cert sẽ làm gì
- clock skew có thể làm TLS fail

---

## 8. Latency, timeout và retry

Một request chậm có thể do:
- DNS delay
- TCP/TLS setup
- queueing
- app compute
- DB query
- packet loss/retransmit
- downstream dependency

### Quy tắc thực dụng
- timeout phải rõ ràng
- retry phải có backoff
- retry side effects cần idempotency
- connection pooling thường rất quan trọng

---

## 9. Load balancing và CDN

### Load balancer
Phân phối traffic tới nhiều backends.

### CDN
Đưa content gần người dùng hơn.

Use cases:
- public APIs
- static content
- media delivery
- global apps

---

## 10. Checklist sau bài
- Mô tả được request path cơ bản từ client tới server
- Phân biệt được TCP, UDP, QUIC ở mức thực dụng
- Hiểu vai trò của DNS, HTTP và TLS
- Biết timeout/retry/backoff/idempotency liên quan nhau ra sao
- Hiểu load balancer và CDN giải quyết vấn đề gì

## 11. Bài tập thực hành
1. Vẽ request path cho một app web bạn biết.
2. So sánh HTTP/1.1, HTTP/2, HTTP/3 ở mức high-level.
3. Viết note giải thích vì sao retry sai cách làm outage nặng hơn.
4. Tự tạo checklist điều tra API timeout.
5. Phân tích vai trò của DNS TTL trong failover.

## 12. Mini deliverable
Tạo file `network_request_path_template.md` với các bước:
- client
- DNS
- TLS
- LB/proxy
- app
- downstreams
- storage

## 13. Học tiếp
- `Bai_11_Distributed_Systems_Full_Lesson.md`
- `../../08_Reference_and_Review/04_Systems_Deep_Dive.md`