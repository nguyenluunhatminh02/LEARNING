# Bài 06: API Design Mastery

## 🎯 Mục tiêu
- RESTful maturity model
- Versioning, pagination, error handling
- Idempotency, backward compatibility

## 📖 Câu chuyện đời thường
> API giống hợp đồng giữa 2 công ty. **Versioning** giống như phiên bản hợp đồng: khi cập nhật điều khoản, bạn tạo v2 mới nhưng vẫn hỗ trợ v1 cho đối tác chưa cập nhật. **Pagination** giống đọc sách theo trang: không ai đưa bạn cả 10.000 trang cùng lúc, mà đưa từng chương (page=1, size=20). **Error handling** giống chẩn đoán bệnh: nói rõ "404 = không tìm thấy" chứ không phải chỉ nói "lỗi". **Backward compatibility** là cam kết: "tôi thêm món mới vào menu nhưng không xóa món cũ" — khách cũ vẫn gọi được món yêu thích.

---

## 1. RESTful Maturity Model (Richardson)

```
Level 0: HTTP as tunnel (POST everything to /api)
Level 1: Resources (/users, /orders)
Level 2: HTTP Verbs (GET, POST, PUT, DELETE) + Status codes
Level 3: HATEOAS (hypermedia links in responses)
```

---

## 2. API Design Best Practices

```python
# FastAPI example

# ✅ Resource naming
GET    /api/v1/users              # list
GET    /api/v1/users/123          # get
POST   /api/v1/users              # create
PATCH  /api/v1/users/123          # partial update
DELETE /api/v1/users/123          # delete
GET    /api/v1/users/123/orders   # nested resource

# ✅ Filtering, sorting, pagination
GET /api/v1/products?category=electronics&min_price=100&sort=-created_at&limit=20&cursor=abc

# ✅ Consistent error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [
      {"field": "email", "message": "Must be a valid email address"}
    ]
  }
}

# ✅ Status codes
200 OK           — success (GET, PATCH)
201 Created      — resource created (POST)
204 No Content   — success, no body (DELETE)
400 Bad Request  — validation error
401 Unauthorized — no auth
403 Forbidden    — no permission
404 Not Found
409 Conflict     — duplicate, version conflict
422 Unprocessable — semantic error
429 Too Many Requests — rate limited
500 Internal Error
```

---

## 3. Pagination

```python
# Cursor-based pagination (preferred)
@app.get("/api/v1/products")
def list_products(cursor: str = None, limit: int = 20):
    query = "SELECT * FROM products"
    if cursor:
        query += f" WHERE id > {decode_cursor(cursor)}"
    query += f" ORDER BY id LIMIT {limit + 1}"
    
    items = db.fetchall(query)
    has_next = len(items) > limit
    items = items[:limit]
    
    return {
        "data": items,
        "pagination": {
            "next_cursor": encode_cursor(items[-1].id) if has_next else None,
            "has_next": has_next
        }
    }
```

---

## 4. Idempotency

```python
# POST requests need idempotency key to prevent duplicates
@app.post("/api/v1/payments")
def create_payment(request: PaymentRequest, idempotency_key: str = Header()):
    existing = redis.get(f"idempotency:{idempotency_key}")
    if existing:
        return json.loads(existing)  # return cached response
    
    result = process_payment(request)
    redis.setex(f"idempotency:{idempotency_key}", 86400, json.dumps(result))
    return result
```

---

## 5. Versioning & Backward Compatibility

```
Versioning strategies:
  URL:    /api/v1/users → /api/v2/users
  Header: Accept: application/vnd.myapi.v2+json
  
Backward compatible changes (SAFE):
  ✅ Add new endpoint
  ✅ Add optional field to request
  ✅ Add field to response
  ✅ Add new enum value

Breaking changes (need new version):
  ❌ Remove/rename field
  ❌ Change field type
  ❌ Make optional field required
  ❌ Change URL structure
```

---

## 📝 Bài tập

1. Design complete REST API cho e-commerce (OpenAPI/Swagger)
2. Implement cursor pagination + filtering
3. Add idempotency key middleware
4. Document API versioning strategy (ADR)

---

## 📚 Tài liệu
- *RESTful Web APIs* — Leonard Richardson
- *API Design Patterns* — JJ Geewax
- [Stripe API Reference](https://stripe.com/docs/api) (excellent API design example)

## 🔗 Liên kết chéo
- → **Security Bài 02: Authentication** — JWT/OAuth2 cho API auth
- → **System Design Bài 05-06: Load Balancing & Caching** — API performance
- → **DB Bài 05: Indexing** — database performance ảnh hưởng API latency
- → **AI Bài 29: Model Deployment** — serving ML model qua REST/gRPC API
