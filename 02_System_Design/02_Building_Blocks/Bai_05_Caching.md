# Bài 05: Caching — Từ Browser đến Database

## 🎯 Mục tiêu
- Hiểu các tầng cache trong hệ thống
- Cache strategies: write-through, write-back, write-around
- Cache eviction policies
- Redis / Memcached thực hành

## 📖 Câu chuyện đời thường
> Bạn là học sinh, mỗi lần cần tra từ mới lại ra thư viện (database). Rất mất thời gian! Vì vậy bạn **ghi chép những từ hay gặp vào sổ tay nhỏ** (cache) để tra nhanh. **Cache eviction** là khi sổ tay đầy, bạn xóa từ nào lâu không dùng nhất (LRU) hoặc từ ít dùng nhất (LFU). **Write-through** = ghi và sổ tay và thư viện cùng lúc. **Write-back** = ghi vào sổ tay trước, lúc rảnh mới cập nhật thư viện (nhanh hơn nhưng rủi ro nếu mất sổ tay). Redis giống cuốn sổ tay siêu nhanh mà cả lớp dùng chung.

---

## 1. Tầng Cache trong hệ thống

```
Client → [Browser Cache] → [CDN Cache] → [API Gateway Cache]
       → [Application Cache (Redis)] → [Database Query Cache] → [Disk]

Mỗi tầng giảm latency & load cho tầng sau
```

| Tầng | Latency | Ví dụ |
|---|---|---|
| CPU L1 Cache | ~1 ns | Hardware |
| CPU L3 Cache | ~10 ns | Hardware |
| RAM | ~100 ns | In-process cache |
| Redis/Memcached | ~1 ms | Distributed cache |
| SSD | ~100 µs | Database cache |
| Network (same DC) | ~500 µs | CDN |
| Network (cross DC) | ~50 ms | Global CDN |

---

## 2. Cache Strategies

### 2.1 Cache-Aside (Lazy Loading) ⭐ Phổ biến nhất
```python
def get_user(user_id):
    # 1. Đọc cache trước
    user = redis.get(f"user:{user_id}")
    if user:
        return json.loads(user)
    
    # 2. Cache miss → đọc DB
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)
    
    # 3. Ghi vào cache
    redis.setex(f"user:{user_id}", 3600, json.dumps(user))  # TTL 1 hour
    return user

def update_user(user_id, data):
    db.update("UPDATE users SET ... WHERE id = %s", user_id)
    redis.delete(f"user:{user_id}")  # Invalidate cache
```
- ✅ Chỉ cache data thực sự được đọc
- ❌ Cache miss đầu tiên chậm (cold start)

### 2.2 Write-Through
```python
def update_user(user_id, data):
    # Ghi DB + Cache đồng thời
    db.update(user_id, data)
    redis.set(f"user:{user_id}", json.dumps(data))
```
- ✅ Cache luôn đồng bộ với DB
- ❌ Write chậm hơn (ghi 2 nơi)
- ❌ Cache data ít được đọc → lãng phí RAM

### 2.3 Write-Back (Write-Behind)
```python
def update_user(user_id, data):
    redis.set(f"user:{user_id}", json.dumps(data))  # Ghi cache trước
    queue.push({"user_id": user_id, "data": data})   # Async ghi DB sau

# Background worker
def flush_to_db():
    while True:
        batch = queue.pop_many(100)  # Batch write
        db.bulk_update(batch)
```
- ✅ Write rất nhanh
- ❌ **Risk mất data** nếu cache crash trước khi flush

### 2.4 Read-Through
```
Cache tự động đọc từ DB khi miss (cache library tự handle)
Application code chỉ đọc từ cache, không care DB
```

---

## 3. Cache Eviction Policies

| Policy | Cơ chế | Use case |
|---|---|---|
| **LRU** (Least Recently Used) | Xóa item lâu nhất chưa dùng | ⭐ Phổ biến nhất |
| LFU (Least Frequently Used) | Xóa item ít dùng nhất | Popular content caching |
| FIFO | Xóa item cũ nhất | Simple use cases |
| TTL | Xóa sau thời gian hết hạn | Session, token |
| Random | Xóa ngẫu nhiên | Khi LRU overhead cao |

```python
# LRU Cache implementation (Python)
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_computation(n):
    return fibonacci(n)

# Redis LRU
redis.config_set('maxmemory-policy', 'allkeys-lru')
redis.config_set('maxmemory', '512mb')
```

---

## 4. Cache Invalidation — Bài toán khó nhất

```
"There are only two hard things in Computer Science:
 cache invalidation and naming things." — Phil Karlton
```

### Strategies
```python
# 1. TTL (Time-to-Live) — Đơn giản, chấp nhận stale data
redis.setex("product:123", 300, data)  # 5 phút

# 2. Event-driven invalidation — Real-time
def on_product_updated(product_id):
    redis.delete(f"product:{product_id}")
    redis.delete("product_list")  # Invalidate list cache

# 3. Versioned keys — Tránh race condition
version = redis.incr(f"product:{product_id}:version")
redis.set(f"product:{product_id}:v{version}", data)
```

### Cache Stampede Prevention
```python
# Vấn đề: 1000 requests cùng lúc cache miss → DB overload

# Solution 1: Locking
def get_with_lock(key):
    data = redis.get(key)
    if data:
        return data
    
    lock = redis.set(f"lock:{key}", "1", nx=True, ex=5)  # Distributed lock
    if lock:
        data = db.query(...)
        redis.setex(key, 3600, data)
        redis.delete(f"lock:{key}")
    else:
        time.sleep(0.1)  # Wait and retry
        return get_with_lock(key)

# Solution 2: Stale-while-revalidate
# Trả về data cũ, async refresh trong background
```

---

## 5. Redis vs Memcached

| | Redis | Memcached |
|---|---|---|
| Data structures | String, Hash, List, Set, Sorted Set | String only |
| Persistence | RDB + AOF | ❌ |
| Replication | Master-Slave | ❌ |
| Pub/Sub | ✅ | ❌ |
| Lua scripting | ✅ | ❌ |
| Multi-threading | Single-threaded* | Multi-threaded |
| Best for | Feature-rich caching | Simple key-value only |

**→ Hầu hết dùng Redis vì versatile hơn nhiều**

---

## 📝 Bài tập

1. Implement cache-aside pattern với Redis + FastAPI
2. Benchmark: so sánh response time có/không cache
3. Implement LRU cache from scratch bằng Hash Map + Doubly Linked List
4. Xử lý cache stampede cho endpoint có 10K RPS

---

## 📚 Tài liệu
- *Redis in Action* — Josiah Carlson
- *Designing Data-Intensive Applications* — Martin Kleppmann (Ch.3)
- [Redis Documentation](https://redis.io/docs/)
