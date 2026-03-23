# Bài 04: API Security

## 🎯 Mục tiêu
- Rate limiting & throttling
- Input validation & sanitization
- API authentication strategies
- CORS configuration

## 📖 Câu chuyện đời thường
> API của bạn giống cửa sổ giao dịch ngân hàng. **Rate limiting** = giới hạn mỗi người chỉ được giao dịch 100 lần/ngày — chống lãng phí và tấn công. **Input validation** = kiểm tra phiếu gửi tiền: số tiền hợp lệ không? tài khoản có tồn tại không? **CORS** giống quy định ai được gọi điện vào quầy: chỉ chi nhánh được ủy quyền mới gọi được, người lạ bị từ chối. Mỗi lỗ hổng API giống một lỗ thủng trên tường ngân hàng — hacker sẽ tìm thấy và khai thác nếu bạn không vá.

---

## 1. Rate Limiting

```python
# Prevent abuse, brute force attacks, DDoS
# Algorithms: Fixed Window, Sliding Window, Token Bucket, Leaky Bucket

import time
from redis import Redis

redis = Redis()

# Sliding Window Rate Limiter
class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window = window_seconds
    
    def is_allowed(self, key: str) -> bool:
        now = time.time()
        pipe = redis.pipeline()
        # Remove old entries
        pipe.zremrangebyscore(key, 0, now - self.window)
        # Add current request
        pipe.zadd(key, {str(now): now})
        # Count requests in window
        pipe.zcard(key)
        # Set expiry
        pipe.expire(key, self.window)
        results = pipe.execute()
        return results[2] <= self.max_requests

# Different limits per endpoint
LIMITS = {
    "/api/login":     RateLimiter(5, 60),      # 5 attempts/min
    "/api/signup":    RateLimiter(3, 3600),     # 3/hour
    "/api/data":      RateLimiter(100, 60),     # 100/min
    "/api/expensive": RateLimiter(10, 60),      # 10/min
}

# Response headers:
# X-RateLimit-Limit: 100
# X-RateLimit-Remaining: 42
# X-RateLimit-Reset: 1709200000
# HTTP 429 Too Many Requests when exceeded
```

---

## 2. Input Validation

```python
from pydantic import BaseModel, validator, Field, EmailStr
from typing import Annotated
import re

class CreateUserRequest(BaseModel):
    email: EmailStr
    name: Annotated[str, Field(min_length=1, max_length=100)]
    age: Annotated[int, Field(ge=13, le=150)]
    bio: Annotated[str, Field(max_length=500)] = ""
    
    @validator("name")
    def validate_name(cls, v):
        if not re.match(r'^[\w\s\-\.]+$', v):
            raise ValueError("Name contains invalid characters")
        return v.strip()

# ✅ Validation Checklist:
# 1. Type checking (Pydantic does this automatically)
# 2. Length limits (prevent memory exhaustion)
# 3. Format validation (email, URL, phone)
# 4. Range validation (age, price, quantity)
# 5. Whitelist characters (names, usernames)
# 6. Sanitize output (HTML encoding for display)

# File Upload Validation
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB

async def upload_file(file: UploadFile):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, "Invalid file type")
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(400, "File too large")
    # Also verify magic bytes, not just content_type header
    if content[:2] != b'\xff\xd8' and content[:8] != b'\x89PNG\r\n\x1a\n':
        raise HTTPException(400, "Invalid file content")
```

---

## 3. API Authentication Strategies

```python
# Strategy 1: API Keys (simple, for server-to-server)
# Header: X-API-Key: sk_live_abc123
# ✅ Simple, no expiry management
# ❌ No user identity, hard to rotate, often leaked

# Strategy 2: Bearer Token (JWT)
# Header: Authorization: Bearer eyJhbGciOi...
# ✅ Stateless, contains claims
# ❌ Can't revoke before expiry

# Strategy 3: OAuth 2.0 (for third-party access)
# ✅ Scoped access, token revocation, refresh flow
# ❌ Complex implementation

# Strategy 4: Mutual TLS (mTLS) — service-to-service
# Both client and server present certificates
# ✅ Strongest auth for internal services
# ❌ Certificate management overhead

# Recommended Architecture:
#   External clients → API Gateway (JWT + rate limiting)
#     → Internal services (mTLS between services)
#     → Each service verifies JWT claims for authorization

# Example: API Gateway middleware
from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_auth(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
```

---

## 4. CORS (Cross-Origin Resource Sharing)

```python
from fastapi.middleware.cors import CORSMiddleware

# ❌ DANGEROUS: Allow everything
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# ✅ SAFE: Explicit whitelist
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://myapp.com",
        "https://admin.myapp.com",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
    allow_credentials=True,
    max_age=3600,  # Preflight cache duration
)

# CORS explains:
# Browser: "Can https://myapp.com call https://api.myapp.com?"
# Server: "Yes, from these origins, with these methods"
# Prevents: malicious site making API calls with user's cookies
```

---

## 5. Security Headers

```python
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "0"  # Deprecated, use CSP
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response

app.add_middleware(SecurityHeadersMiddleware)
```

---

## 📝 Bài tập

1. Implement sliding window rate limiter với Redis
2. Build comprehensive input validation với Pydantic
3. Setup CORS properly cho frontend + API architecture
4. Add all security headers to existing API

---

## 📚 Tài liệu
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [Security Headers](https://securityheaders.com/)
