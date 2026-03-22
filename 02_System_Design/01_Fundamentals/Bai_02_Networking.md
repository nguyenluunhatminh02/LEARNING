# Bài 02: Networking & HTTP

## 🎯 Mục tiêu
- TCP vs UDP, DNS, HTTP/1.1 vs 2 vs 3
- HTTPS, TLS
- WebSocket cho real-time

---

## 1. TCP vs UDP

| | TCP | UDP |
|---|-----|-----|
| Connection | Connection-oriented (3-way handshake) | Connectionless |
| Reliability | Guaranteed delivery, ordered | Best-effort, no order |
| Speed | Slower | Faster |
| Use cases | HTTP, email, file transfer | Video streaming, DNS, gaming |

---

## 2. HTTP Evolution

### HTTP/1.1
```
- 1 request per connection (head-of-line blocking)
- Keep-alive: reuse connection
- Text-based headers (verbose)
```

### HTTP/2
```
- Multiplexing: multiple requests trên 1 connection
- Header compression (HPACK)
- Server Push
- Binary framing
```

### HTTP/3 (QUIC)
```
- Dựa trên UDP (không phải TCP)
- Giải quyết head-of-line blocking ở transport layer
- Built-in encryption (TLS 1.3)
- 0-RTT connection establishment
```

---

## 3. HTTPS & TLS

```
TLS Handshake:
1. Client Hello: supported cipher suites, random number
2. Server Hello: chosen cipher, certificate
3. Client verifies certificate (CA chain)
4. Key exchange (Diffie-Hellman / ECDHE)
5. Encrypted communication begins

TLS 1.3: 1-RTT handshake (vs 2-RTT in TLS 1.2)
```

---

## 4. DNS (Domain Name System)

```
Browser → DNS Resolver flow:
1. Browser cache
2. OS cache
3. Router cache
4. ISP DNS resolver
5. Root DNS server → .com TLD → Authoritative DNS
6. Return IP address

Record types:
- A:     domain → IPv4
- AAAA:  domain → IPv6
- CNAME: domain → another domain (alias)
- MX:    domain → mail server
- NS:    domain → nameserver
- TXT:   domain → text (SPF, DKIM)
```

---

## 5. WebSocket

```
HTTP: request-response (client always initiates)
WebSocket: full-duplex, persistent connection
           server có thể push data to client

Use cases: chat, live notifications, real-time dashboards, gaming

Handshake:
GET /chat HTTP/1.1
Upgrade: websocket
Connection: Upgrade

→ HTTP 101 Switching Protocols
→ Bidirectional communication
```

---

## 6. Authentication

### JWT (JSON Web Token)
```
Header.Payload.Signature

Header:  {"alg": "HS256", "typ": "JWT"}
Payload: {"user_id": 123, "exp": 1700000000}
Signature: HMAC-SHA256(header + "." + payload, secret)

Flow:
1. Login → server returns JWT
2. Client gửi JWT trong Authorization header
3. Server verify signature → extract user info (stateless!)
```

### OAuth 2.0
```
Authorization Code Flow (phổ biến nhất):
1. User → App → Auth Server (Google, GitHub)
2. User đăng nhập, cho phép
3. Auth Server → App: authorization code
4. App → Auth Server: code → access token
5. App dùng access token gọi Resource Server
```

---

## 📝 Bài tập

1. Giải thích DNS resolution step-by-step cho "www.google.com"
2. So sánh HTTP/1.1 vs HTTP/2 performance (dùng developer tools)
3. Implement WebSocket chat đơn giản bằng Node.js hoặc Python
4. Giải thích JWT flow cho authentication, khi nào dùng refresh token

---

## 📚 Tài liệu
- *Computer Networking: A Top-Down Approach* — Kurose & Ross
- *High Performance Browser Networking* — Ilya Grigorik (miễn phí)
- MDN Web Docs — HTTP
