# Bài 10: Computer Networks

## 🎯 Mục tiêu
- Hiểu dữ liệu đi qua mạng như thế nào từ process này sang process khác
- Nắm TCP/IP, DNS, HTTP, TLS, routing, load balancing và network troubleshooting basics
- Có khả năng suy luận latency, reliability, retries, timeouts, packet loss và bottleneck mạng

## 📖 Bức tranh lớn
Hầu hết hệ thống hiện đại đều là hệ phân tán ở một mức nào đó, nghĩa là có mạng chen vào giữa các thành phần. Mạng làm xuất hiện delay, packet loss, partial failure, retry, congestion và security concerns. Nếu không hiểu mạng, bạn khó thiết kế backend, API, service mesh hay production system tốt.

---

## 1. Layered networking mindset

### Mô hình cần biết
- OSI model ở mức khái niệm
- TCP/IP model ở mức thực dụng

### Các lớp thực tế nên nhớ
- Link: Ethernet, Wi-Fi
- Internet: IP, routing
- Transport: TCP, UDP, QUIC
- Application: HTTP, DNS, SMTP, gRPC, WebSocket

### Tư duy quan trọng
Mỗi lớp che giấu một phần phức tạp, nhưng không làm nó biến mất. Lỗi application đôi khi xuất phát từ transport hoặc network path.

---

## 2. IP, routing và packet delivery

### Chủ đề cần nắm
- IP address, subnet, CIDR
- Router, gateway
- NAT
- MTU ở mức trực giác
- TTL

### Ứng dụng thực tế
- VPC/subnet design
- Private vs public network
- Service-to-service connectivity
- Cross-region latency

---

## 3. TCP, UDP và QUIC

### TCP
- Reliable, ordered, connection-oriented
- Three-way handshake
- Retransmission, flow control, congestion control

### UDP
- Unreliable, unordered, lightweight
- Phù hợp cho streaming/realtime/game/telemetry tùy case

### QUIC
- Chạy trên UDP nhưng cung cấp reliability + TLS modernized
- Nền tảng cho HTTP/3

### Câu hỏi quan trọng
- Khi nào ordered delivery là lợi ích, khi nào là gánh nặng?
- Retries ở app layer tương tác ra sao với retries ở transport layer?

---

## 4. DNS, HTTP và API protocols

### DNS
- Domain -> IP mapping
- Recursive resolver, authoritative server
- TTL, caching

### HTTP
- Request/response model
- Methods, status codes, headers
- Keep-alive, idempotency, caching, content negotiation
- HTTP/1.1 vs HTTP/2 vs HTTP/3

### Protocols ứng dụng khác
- gRPC
- WebSocket
- Server-Sent Events
- Message queues/protocols như AMQP, Kafka protocol ở mức nhận biết

---

## 5. Network security cơ bản

### Chủ đề cần nắm
- TLS/HTTPS
- Certificates
- mTLS ở service-to-service
- Firewall, WAF, VPN, Zero Trust ở mức overview

### Liên hệ với application
- Auth không thay thế transport security
- TLS termination ở đâu ảnh hưởng observability, routing và trust boundary

---

## 6. Latency, throughput và reliability

### Các nguồn latency
- DNS lookup
- TCP/TLS handshake
- Queueing
- Serialization/deserialization
- Packet loss/retransmit
- Cross-region distance

### Thực hành tốt
- Timeout phải rõ ràng
- Retry cần backoff và idempotency
- Connection pooling rất quan trọng
- Cần phân biệt p50 và p99 latency

---

## 7. Load balancing, CDN và edge

### Load balancing
- L4 vs L7
- Round-robin, least connections, consistent hashing

### CDN/Edge
- Caching static content gần người dùng
- Giảm origin load
- Giảm latency địa lý

### Khi nào quan trọng
- Public APIs, web apps, media delivery, global traffic

---

## 8. Troubleshooting mindset

### Các câu hỏi điều tra chuẩn
- Có phải DNS issue không?
- Kết nối timeout hay bị reset?
- Packet loss hay congestion ở đâu?
- TLS handshake fail vì cert, cipher hay clock skew?
- Load balancer, proxy, app hay database là điểm nghẽn?

---

## ✅ Checklist ôn tập
- Giải thích được TCP, UDP, QUIC khác nhau thế nào
- Mô tả được đường đi của một HTTP request từ client đến server
- Biết DNS và TLS tham gia ở đâu
- Hiểu vai trò của timeout, retry, backoff, idempotency
- Phân biệt được L4/L7 load balancing và CDN

## 📝 Bài tập
1. Vẽ sơ đồ request path cho một web app thực tế.
2. Viết note so sánh HTTP/1.1, HTTP/2, HTTP/3.
3. Tự giải thích vì sao retry sai cách có thể làm outage tệ hơn.
4. Dùng `ping`, `tracert`, `nslookup` hoặc công cụ tương đương để hiểu một domain.
5. Soạn checklist chẩn đoán khi API bị timeout.

## 📚 Tài liệu
- *Computer Networking: A Top-Down Approach* — Kurose & Ross
- *HTTP: The Definitive Guide* — Gourley et al.
- Track đào sâu: `../../02_System_Design/`