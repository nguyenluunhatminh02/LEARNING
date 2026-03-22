# Bài 10: Redis — Key-Value Store & Beyond

## 🎯 Mục tiêu
- Redis data structures
- Caching, sessions, rate limiting, pub/sub
- Persistence (RDB, AOF)
- Redis Cluster & Sentinel

---

## 1. Data Structures

```python
import redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# STRING — cache, counters
r.set("user:1:name", "Alice")
r.get("user:1:name")                 # "Alice"
r.setex("session:abc", 3600, "data") # TTL 1 hour
r.incr("page:views")                 # atomic counter
r.incrby("product:1:stock", -5)      # decrement stock

# HASH — objects (like a mini-document)
r.hset("user:1", mapping={"name": "Alice", "email": "a@b.com", "age": "30"})
r.hget("user:1", "name")             # "Alice"
r.hgetall("user:1")                  # {"name": "Alice", "email": "a@b.com", "age": "30"}
r.hincrby("user:1", "age", 1)        # atomic increment field

# LIST — queue, recent items
r.lpush("queue:emails", "email1", "email2")  # push left
r.rpop("queue:emails")                        # pop right (FIFO queue)
r.lrange("recent:posts", 0, 9)               # latest 10 posts

# SET — unique items, tags
r.sadd("user:1:skills", "python", "redis", "sql")
r.sismember("user:1:skills", "python")    # True
r.sinter("user:1:skills", "user:2:skills") # common skills

# SORTED SET — leaderboard, rankings
r.zadd("leaderboard", {"alice": 1500, "bob": 1200, "charlie": 1800})
r.zrevrange("leaderboard", 0, 2, withscores=True)  # top 3
r.zincrby("leaderboard", 50, "alice")               # alice +50 points
r.zrevrank("leaderboard", "alice")                   # rank (0-based)
```

---

## 2. Use Cases

### Session Store
```python
import json, secrets

def create_session(user_id, data):
    session_id = secrets.token_urlsafe(32)
    r.setex(f"session:{session_id}", 86400, json.dumps({
        "user_id": user_id, **data
    }))
    return session_id

def get_session(session_id):
    data = r.get(f"session:{session_id}")
    return json.loads(data) if data else None
```

### Rate Limiting (Sliding Window)
```python
def is_rate_limited(user_id, limit=100, window=60):
    key = f"rate:{user_id}"
    now = time.time()
    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, now - window)
    pipe.zcard(key)
    pipe.zadd(key, {str(now): now})
    pipe.expire(key, window)
    results = pipe.execute()
    return results[1] >= limit
```

### Distributed Lock
```python
import uuid

def acquire_lock(lock_name, timeout=10):
    token = str(uuid.uuid4())
    acquired = r.set(f"lock:{lock_name}", token, nx=True, ex=timeout)
    return token if acquired else None

def release_lock(lock_name, token):
    # Lua script for atomic check-and-delete
    script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    end
    return 0
    """
    r.eval(script, 1, f"lock:{lock_name}", token)
```

### Pub/Sub
```python
# Publisher
r.publish("notifications", json.dumps({"user": 1, "msg": "New order"}))

# Subscriber
pubsub = r.pubsub()
pubsub.subscribe("notifications")
for message in pubsub.listen():
    if message['type'] == 'message':
        print(json.loads(message['data']))
```

---

## 3. Persistence

```
RDB (Snapshot):
  Periodic snapshot to disk (dump.rdb)
  save 900 1      # save if 1 key changed in 900s
  save 300 10     # save if 10 keys changed in 300s
  ✅ Compact, fast restart
  ❌ Data loss between snapshots

AOF (Append-Only File):
  Log every write command
  appendonly yes
  appendfsync everysec   # fsync every second (balance)
  ✅ Minimal data loss (~1s)
  ❌ Larger file, slower restart

Best: RDB + AOF (both enabled)
```

---

## 4. Redis Cluster & Sentinel

```
Sentinel (High Availability):
  Monitor master → if down → promote slave to master
  [Master] → [Slave 1]
           → [Slave 2]
  [Sentinel 1, Sentinel 2, Sentinel 3] monitoring

Cluster (Horizontal Scaling):
  16384 hash slots distributed across nodes
  [Node A: slots 0-5460]
  [Node B: slots 5461-10922]
  [Node C: slots 10923-16383]
  Each node has replicas for failover
```

---

## 📝 Bài tập

1. Implement leaderboard system bằng Sorted Set
2. Implement distributed rate limiter bằng Redis
3. So sánh: Redis strings vs hashes cho user profiles
4. Setup Redis Sentinel (Docker Compose)

---

## 📚 Tài liệu
- *Redis in Action* — Josiah Carlson
- [Redis University (free)](https://university.redis.com/)
- [Redis Documentation](https://redis.io/docs/)
