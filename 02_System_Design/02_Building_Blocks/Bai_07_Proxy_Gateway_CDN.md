# Bài 07: Proxy, API Gateway & CDN

## 🎯 Mục tiêu
- Hiểu Forward Proxy, Reverse Proxy, API Gateway
- CDN hoạt động thế nào
- Service Mesh basics

## 📖 Câu chuyện đời thường
> **Forward Proxy** giống như ông bảo vệ cổng công ty: bạn muốn gửi thư ra ngoài, phải nhờ ông gửi hộ (người ngoài không biết bạn là ai). **Reverse Proxy** giống lễ tân khách sạn: khách đến chỉ gặp lễ tân, lễ tân phân phòng phù hợp (khách không biết phòng nào trống). **API Gateway** giống như quầy thông tin tại trung tâm thương mại: mọi câu hỏi đều qua đây, nơi đây hướng dẫn bạn đến đúng cửa hàng. **CDN** giống như mạng lưới các kho hàng trải khắp cả nước: thay vì giao hàng từ Hà Nội cho khách Sài Gòn, lấy từ kho Sài Gòn cho nhanh.

---

## 1. Proxy Types

### Forward Proxy
```
[Client] → [Forward Proxy] → [Internet]

Use cases:
- Ẩn IP client (VPN, Tor)
- Bypass geo-restrictions
- Corporate firewall / content filter
- Caching cho internal network
```

### Reverse Proxy
```
[Internet] → [Reverse Proxy] → [Server A]
                              → [Server B]

Use cases:
- Load balancing
- SSL termination
- Static content caching
- DDoS protection
- Compression (gzip/brotli)
```

---

## 2. API Gateway

```
                    ┌─────────────────┐
Mobile App ──────→ │                 │ ──→ User Service
Web App ─────────→ │   API Gateway   │ ──→ Order Service
3rd Party ───────→ │                 │ ──→ Product Service
                    └─────────────────┘

Gateway handles:
✅ Authentication / Authorization (JWT verify)
✅ Rate Limiting
✅ Request/Response transformation
✅ API versioning
✅ Logging & Monitoring
✅ Circuit Breaker
✅ Request aggregation (BFF pattern)
```

### Tools phổ biến
| Tool | Type | Best for |
|---|---|---|
| Kong | Open-source | Full-featured, plugin system |
| AWS API Gateway | Managed | AWS ecosystem |
| NGINX | Open-source | High performance |
| Traefik | Open-source | Container/K8s native |
| Envoy | Open-source | Service mesh sidecar |

### Rate Limiting tại Gateway
```python
# Token Bucket Algorithm
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens/second
        self.last_refill = time.time()
    
    def allow_request(self):
        self._refill()
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False  # 429 Too Many Requests
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, 
                          self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
```

---

## 3. CDN (Content Delivery Network)

```
Không CDN:
  User (Vietnam) → [Origin Server (US)] → 200ms latency

Có CDN:
  User (Vietnam) → [CDN Edge (Singapore)] → 20ms latency
                                           ↓ cache miss
                                    [Origin Server (US)]
```

### CDN Types
```
Pull CDN:
  CDN tự fetch từ origin khi cache miss
  + Đơn giản setup
  - First request chậm (cold cache)

Push CDN:
  Developer upload content lên CDN
  + Control chính xác
  - Quản lý phức tạp hơn
```

### Cache Headers
```http
# Origin server response headers
Cache-Control: public, max-age=86400    # Cache 1 ngày
Cache-Control: private, no-cache        # Không cache (user-specific)
ETag: "abc123"                          # Version tag
Vary: Accept-Encoding                   # Cache theo encoding

# CDN cache invalidation
# Purge specific URL hoặc toàn bộ cache
```

### CDN Providers
- **Cloudflare**: DDoS protection + CDN, free tier
- **AWS CloudFront**: Tích hợp AWS ecosystem
- **Akamai**: Enterprise, largest network
- **Fastly**: Edge computing, real-time purge

---

## 4. Service Mesh (Advanced)

```
Không Service Mesh:
  Service A → [Load Balancer] → Service B
  Mỗi service tự handle: retry, timeout, auth, tracing

Có Service Mesh (Istio/Envoy):
  Service A → [Sidecar Proxy] → [Sidecar Proxy] → Service B
  Sidecar handle: mTLS, retry, circuit breaker, tracing, metrics

→ Application code chỉ focus business logic
```

---

## 5. BFF Pattern (Backend for Frontend)

```
Mobile App → [Mobile BFF] → Microservices
Web App    → [Web BFF]    → Microservices

Mỗi client type có BFF riêng:
- Mobile BFF: response nhỏ, ít data
- Web BFF: response đầy đủ, aggregated data
```

---

## 📝 Bài tập

1. Setup NGINX reverse proxy cho 2 backend services
2. Implement rate limiter (Token Bucket) bằng Redis
3. Config Cloudflare CDN cho static website
4. Vẽ architecture diagram: CDN + API Gateway + Microservices

---

## 📚 Tài liệu
- *Building Microservices* — Sam Newman (Ch.8-9)
- [Cloudflare Learning Center](https://www.cloudflare.com/learning/)
- [Kong Gateway Docs](https://docs.konghq.com/)
