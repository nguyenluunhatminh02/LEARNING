# Bài 10: System Design Practice — URL Shortener & Rate Limiter

## 🎯 Mục tiêu
- Áp dụng system design framework
- Thiết kế URL Shortener (TinyURL)
- Thiết kế Rate Limiter
- Estimation, database design, scaling

## 📖 Câu chuyện đời thường
> **URL Shortener** giống như dịch vụ gửi hàng có mã vận đơn. Thay vì viết địa chỉ dài như "Số 123, đường ABC, phường X, quận Y, TP.HCM", bạn chỉ cần gửi mã "VN7X9K" — hệ thống tự tra ra địa chỉ đầy đủ. **Rate Limiter** giống như kiểm soát vào cửa hộp đêm: tối đa 200 người, ai đến sau phải chờ. Mục đích là bảo vệ hệ thống khỏi bị quá tải — dù có 10.000 người muốn vào cùng lúc, bạn vẫn kiểm soát được.

---

## PART A: URL Shortener (TinyURL)

### Step 1: Requirements

```
Functional:
- Tạo short URL từ long URL
- Redirect short URL → long URL
- Custom alias (optional)
- Expiration (optional)

Non-functional:
- Low latency redirect (<100ms)
- High availability (99.99%)
- URL không đoán được

Scale:
- 100M URLs/day write
- 10:1 read/write ratio → 1B reads/day
- Store 5 years → 100M × 365 × 5 = ~182B URLs
```

### Step 2: Back-of-envelope Estimation

```
Write: 100M/day = 1160 writes/sec
Read:  1B/day   = 11600 reads/sec (peak: ~x3 = 35K RPS)

Storage per URL: ~500 bytes
Total: 182B × 500 bytes = ~91 TB (5 years)

Short URL length:
  Base62: [a-zA-Z0-9] = 62 chars
  62^7 = 3.5 trillion combinations → đủ cho 182B URLs
  → short URL = 7 chars
```

### Step 3: API Design

```
POST /api/v1/shorten
  Body: { "long_url": "https://...", "custom_alias": "my-link", "expiry": "2025-12-31" }
  Response: { "short_url": "https://tiny.url/aB3xK9z" }

GET /{short_code}
  → 301 Redirect to long_url (cacheable)
  → 302 Redirect (if need analytics — not cached)
```

### Step 4: Database Design

```sql
CREATE TABLE urls (
    id BIGSERIAL PRIMARY KEY,
    short_code VARCHAR(7) UNIQUE NOT NULL,
    long_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    user_id BIGINT
);

CREATE INDEX idx_short_code ON urls(short_code);
-- short_code lookup = O(1) with hash index
```

### Step 5: Short Code Generation

```python
# Approach 1: Base62 encoding of auto-increment ID
import string

CHARSET = string.ascii_letters + string.digits  # 62 chars

def encode_base62(num):
    if num == 0:
        return CHARSET[0]
    result = []
    while num:
        result.append(CHARSET[num % 62])
        num //= 62
    return ''.join(reversed(result))

# ID=1000000 → "4c92"
# Predictable → cần thêm random offset hoặc shuffle charset

# Approach 2: MD5/SHA256 hash + take first 7 chars
import hashlib
def generate_short_code(long_url):
    hash_hex = hashlib.md5(long_url.encode()).hexdigest()
    return encode_base62(int(hash_hex[:12], 16))[:7]

# Approach 3: Pre-generate unique IDs (Snowflake ID)
# Dùng distributed ID generator để tránh collision
```

### Step 6: Architecture

```
┌─────────┐    ┌───────────┐    ┌──────────────┐
│ Client   │───→│   CDN     │───→│ Load Balancer│
└─────────┘    └───────────┘    └──────┬───────┘
                                       │
                     ┌─────────────────┼─────────────────┐
                     │                 │                 │
              ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
              │ App Server 1│  │ App Server 2│  │ App Server 3│
              └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
                     │                │                 │
              ┌──────▼─────────────────────────────────┐
              │           Redis Cache                   │
              │     (short_code → long_url)             │
              └──────┬─────────────────────────────────┘
                     │ cache miss
              ┌──────▼─────────────────────────────────┐
              │         PostgreSQL (Sharded)            │
              │  Shard by: hash(short_code) % N        │
              └────────────────────────────────────────┘
```

---

## PART B: Rate Limiter

### Step 1: Requirements

```
Functional:
- Limit requests per user/IP/API key
- Different limits per API endpoint
- Return 429 Too Many Requests khi exceed

Non-functional:
- Low latency (<1ms overhead)
- Distributed (shared across servers)
- Accurate counting
```

### Step 2: Algorithms

#### Token Bucket ⭐ Phổ biến nhất
```python
# Redis implementation
import time, redis

r = redis.Redis()

def is_allowed(user_id, capacity=10, refill_rate=1):
    """capacity=10 tokens, refill 1 token/sec"""
    key = f"rate:{user_id}"
    now = time.time()
    
    pipe = r.pipeline()
    pipe.hgetall(key)
    result = pipe.execute()[0]
    
    tokens = float(result.get(b'tokens', capacity))
    last_refill = float(result.get(b'last_refill', now))
    
    # Refill tokens
    elapsed = now - last_refill
    tokens = min(capacity, tokens + elapsed * refill_rate)
    
    if tokens >= 1:
        tokens -= 1
        allowed = True
    else:
        allowed = False
    
    pipe.hset(key, mapping={'tokens': tokens, 'last_refill': now})
    pipe.expire(key, 60)
    pipe.execute()
    
    return allowed
```

#### Sliding Window Log
```python
def is_allowed_sliding_log(user_id, limit=100, window=60):
    """100 requests per 60 seconds"""
    key = f"rate:{user_id}"
    now = time.time()
    window_start = now - window
    
    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, window_start)  # Remove old entries
    pipe.zcard(key)                                # Count current
    pipe.zadd(key, {str(now): now})               # Add current request
    pipe.expire(key, window)
    results = pipe.execute()
    
    count = results[1]
    return count < limit
```

#### Sliding Window Counter (Memory efficient)
```
Window = 1 minute, Limit = 100

Current window (40% elapsed): 40 requests
Previous window: 80 requests

Weighted count = 80 × (1 - 0.4) + 40 = 88 < 100 → ALLOW
```

### Step 3: Distributed Rate Limiting

```
Challenge: Multiple servers → consistent counting

Solution 1: Centralized Redis
  All servers → Redis → atomic operations
  + Simple
  - Redis = single point of failure

Solution 2: Local + Sync
  Each server: local counter
  Periodically sync to central store
  + Fast (no network call per request)
  - Slightly inaccurate

Solution 3: Sticky sessions
  Same user → same server (via IP hash LB)
  + Simple local counting
  - Uneven distribution
```

### Rate Limiter Response
```http
HTTP/1.1 429 Too Many Requests
Retry-After: 30
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1700000030

{ "error": "Rate limit exceeded. Retry after 30 seconds." }
```

---

## 📝 Bài tập

1. Implement full URL shortener (FastAPI + Redis + PostgreSQL)
2. Implement distributed rate limiter với Redis
3. Load test URL shortener với wrk/locust: target 10K RPS
4. Thêm analytics: count clicks per URL, clicks by country

---

## 📚 Tài liệu
- *System Design Interview* — Alex Xu (Ch.8: URL Shortener, Ch.4: Rate Limiter)
- *Designing Data-Intensive Applications* — Martin Kleppmann
