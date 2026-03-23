# Bài 04: Load Balancing & Reverse Proxy

## 🎯 Mục tiêu
- Hiểu Load Balancer hoạt động thế nào
- Các thuật toán load balancing
- Layer 4 vs Layer 7
- Health checks & failover

## 📖 Câu chuyện đời thường
> Bạn đến ngân hàng giờ cao điểm, có 20 người xếp hàng. Ngay cửa có một nhân viên điều phối: "Quầy 1 đang trống, mời anh! Quầy 3 sắp xong, chị chờ chút!" — người đó chính là **Load Balancer**. **Round Robin** = đến lượt quầy nào thì vào quầy đó. **Least Connections** = ai rảnh nhất thì nhận khách. **Health check** = kiểm tra quầy nào đã đóng (server chết) thì không đưa khách vào nữa. Không có load balancer, tất cả đổ vào 1 quầy → quầy đó quá tải, các quầy khác ngồi chơi.

---

## 1. Load Balancer là gì?

```
Client → [Load Balancer] → Server 1
                         → Server 2
                         → Server 3

Phân phối traffic đều giữa các server
→ Tăng throughput, giảm latency, tăng availability
```

---

## 2. Thuật toán Load Balancing

### 2.1 Round Robin
```
Request 1 → Server A
Request 2 → Server B
Request 3 → Server C
Request 4 → Server A  (quay lại)
```
- Đơn giản nhất
- Không xét server load → server yếu bị quá tải

### 2.2 Weighted Round Robin
```
Server A (weight=5): nhận 5 requests
Server B (weight=3): nhận 3 requests
Server C (weight=2): nhận 2 requests
```

### 2.3 Least Connections
```
Server A: 10 connections → SKIP
Server B: 3 connections  → CHỌN (ít nhất)
Server C: 7 connections  → SKIP
```
- Tốt cho long-lived connections (WebSocket, DB)

### 2.4 IP Hash (Sticky Sessions)
```python
server_index = hash(client_ip) % num_servers
# Cùng client → cùng server → giữ session
```
- Dùng khi cần session affinity
- ❌ Phân tải không đều nếu 1 IP có nhiều traffic

### 2.5 Least Response Time
- Chọn server có response time thấp nhất
- Cần monitor liên tục

---

## 3. Layer 4 vs Layer 7

| | Layer 4 (Transport) | Layer 7 (Application) |
|---|---|---|
| Quyết định dựa trên | IP + Port | URL, Headers, Cookies |
| Speed | **Nhanh hơn** | Chậm hơn (parse HTTP) |
| SSL Termination | Không | **Có** |
| Content routing | Không | **Có** |
| Use case | TCP/UDP traffic | HTTP/HTTPS routing |

```
Layer 7 routing example:
  /api/*       → API servers
  /static/*    → CDN / Static servers
  /ws/*        → WebSocket servers
  *.jpg, *.css → Object storage
```

---

## 4. Health Checks

```yaml
# NGINX health check config
upstream backend {
    server 10.0.0.1:8080;
    server 10.0.0.2:8080;
    server 10.0.0.3:8080 backup;  # chỉ dùng khi server khác down
}

# Active health check
health_check interval=5s fails=3 passes=2;
# Mỗi 5s check 1 lần, 3 lần fail → remove, 2 lần pass → add lại
```

### Passive Health Check
- Monitor responses thực tế
- Server trả 5xx liên tục → tự động remove

---

## 5. Reverse Proxy vs Forward Proxy

```
Forward Proxy:
  Client → [Proxy] → Internet
  (Client giấu IP, bypass firewall)

Reverse Proxy:
  Internet → [Proxy] → Server
  (Server được bảo vệ, SSL termination, caching)

Load Balancer = Reverse Proxy + traffic distribution
```

---

## 6. Tools phổ biến

| Tool | Type | Use case |
|---|---|---|
| NGINX | L4/L7 | Web server + reverse proxy |
| HAProxy | L4/L7 | High-performance LB |
| AWS ALB | L7 | Cloud HTTP load balancing |
| AWS NLB | L4 | Cloud TCP/UDP load balancing |
| Envoy | L7 | Service mesh sidecar |
| Traefik | L7 | Container-native LB |

---

## 📝 Bài tập

1. Setup NGINX load balancer với 3 backend servers (Docker Compose)
2. So sánh Round Robin vs Least Connections với wrk benchmark
3. Implement health check endpoint `/health` cho ứng dụng
4. Vẽ diagram: client → LB → servers cho 1 hệ thống thực tế

---

## 📚 Tài liệu
- *NGINX Documentation* — nginx.org
- *The Art of Scalability* — Martin Abbott
- [HAProxy Documentation](http://docs.haproxy.org/)
