# Bài 03: API Design — REST, GraphQL, gRPC

## 🎯 Mục tiêu
- Thiết kế RESTful API chuẩn
- Hiểu GraphQL và gRPC
- Biết khi nào dùng loại nào

---

## 1. REST API Design

### 1.1 Principles
```
- Resource-based URLs: /users, /users/123, /users/123/orders
- HTTP Methods: GET (read), POST (create), PUT (replace), PATCH (partial update), DELETE
- Stateless: mỗi request chứa đủ thông tin
- JSON response
```

### 1.2 Best Practices
```
✅ GET /users                    → List users
✅ GET /users/123                → Get user 123
✅ POST /users                   → Create user
✅ PATCH /users/123              → Update user 123
✅ DELETE /users/123             → Delete user 123
✅ GET /users/123/orders         → List orders of user 123

❌ GET /getUser?id=123           → Verb in URL
❌ POST /users/123/delete        → Action in URL

Pagination (cursor-based > offset):
  GET /users?cursor=abc123&limit=20
  → Response: { data: [...], next_cursor: "def456" }

Versioning:
  /api/v1/users    ← URL versioning (phổ biến nhất)
  Accept: application/vnd.api.v1+json  ← Header versioning

Error format:
  { "error": { "code": "NOT_FOUND", "message": "User 123 not found" } }

Rate limiting headers:
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 95
  X-RateLimit-Reset: 1700000000
```

---

## 2. GraphQL

```graphql
# Client chỉ lấy đúng fields cần → no over-fetching
query {
  user(id: 123) {
    name
    email
    orders(last: 5) {
      id
      total
      items { name, price }
    }
  }
}

# 1 request lấy user + orders + items
# REST cần 3 requests: GET /users/123 + GET /users/123/orders + GET /orders/1/items
```

### Khi nào dùng GraphQL?
- Mobile apps (cần minimize data transfer)
- Complex nested data
- Multiple clients cần data khác nhau
- ❌ Không dùng cho: simple CRUD, real-time heavy, file upload

---

## 3. gRPC

```protobuf
// Protobuf definition
service UserService {
  rpc GetUser (GetUserRequest) returns (User);
  rpc ListUsers (ListUsersRequest) returns (stream User);  // Server streaming
}

message User {
  int32 id = 1;
  string name = 2;
  string email = 3;
}
```

### Khi nào dùng gRPC?
- Microservices internal communication (nhanh, type-safe)
- Streaming data
- Low-latency requirements
- ❌ Không dùng cho: browser clients (cần proxy), public APIs

---

## 4. So sánh

| | REST | GraphQL | gRPC |
|---|------|---------|------|
| Format | JSON | JSON | Protobuf (binary) |
| Speed | Tốt | Tốt | **Nhanh nhất** |
| Flexibility | Fixed response | **Flexible query** | Fixed contract |
| Learning curve | Thấp | Trung bình | Cao |
| Best for | Public APIs | Complex queries | Microservices |

---

## 📝 Bài tập

1. Thiết kế REST API cho e-commerce: users, products, orders, reviews
2. Implement CRUD API bằng FastAPI (Python) hoặc Express (Node.js)
3. So sánh performance: REST vs gRPC cho 1000 requests
4. Thiết kế GraphQL schema cho social media app

---

## 📚 Tài liệu
- *REST API Design Rulebook* — Mark Massé
- [GraphQL Official Docs](https://graphql.org/learn/)
- [gRPC Documentation](https://grpc.io/docs/)
