# Bài 11: System Design Practice — Chat System & Social Feed

## 🎯 Mục tiêu
- Thiết kế Real-time Chat (WhatsApp/Messenger)
- Thiết kế News Feed (Facebook/Twitter)

## 📖 Câu chuyện đời thường
> **Chat system** giống như hệ thống bộ đàm trong tòa nhà: khi bạn nói, mọi người trong nhóm nghe ngay (real-time). Nhưng nếu bạn offline, tin nhắn được lưu lại và giao khi bạn online (message persistence). **News Feed** giống như một người phát báo mỗi sáng: họ chọn bài từ nhiều nguồn (bạn bè, group, trang theo dõi), sắp xếp theo độ quan trọng và giao cho bạn một tờ báo cá nhân hóa. Vấn đề là: nếu Lady Gaga có 100 triệu follower, mỗi lần đăng bài thì phải gửi đến 100 triệu người — đó là bài toán **fan-out** kinh điển.

---

## PART A: Real-time Chat System

### Step 1: Requirements

```
Functional:
- 1:1 chat + Group chat (up to 500 members)
- Send text, images, files
- Online/offline status
- Read receipts (seen)
- Message history (persistent)

Non-functional:
- Real-time delivery (<200ms same region)
- Offline message delivery (khi user online lại)
- 500M daily active users
- Mỗi user gửi ~40 messages/day
```

### Step 2: Estimation

```
Messages/day: 500M × 40 = 20B messages/day
QPS: 20B / 86400 = ~230K msg/sec (peak: ~500K)
Storage: 20B × 100 bytes = ~2TB/day → ~730TB/year
```

### Step 3: Protocol Choice

```
HTTP Long Polling:
  Client → Server: "any new messages?" (hold 30s)
  ❌ Server resource waste, delay

WebSocket: ⭐
  Client ↔ Server: persistent bidirectional connection
  ✅ Real-time, low overhead
  ❌ Stateful → need connection management

Server-Sent Events (SSE):
  Server → Client: one-way push
  ✅ Simple
  ❌ Chỉ 1 chiều
```

### Step 4: Architecture

```
┌──────┐  WebSocket  ┌─────────────┐     ┌───────────────┐
│User A│────────────→│ Chat Server │────→│ Message Queue │
└──────┘             │   (WS)      │     │   (Kafka)     │
                     └─────────────┘     └───────┬───────┘
                                                 │
┌──────┐  WebSocket  ┌─────────────┐     ┌───────▼───────┐
│User B│←────────────│ Chat Server │←────│ Message Router│
└──────┘             │   (WS)      │     └───────┬───────┘
                     └─────────────┘             │
                                          ┌──────▼──────┐
                                          │  Cassandra   │
                                          │ (msg store)  │
                                          └─────────────┘
```

### Step 5: Message Flow

```
1:1 Chat Flow:
  A sends "Hello" to B
  → Chat Server receives via WebSocket
  → Generate message_id (Snowflake)
  → Push to Kafka topic: "chat.messages"
  → Message Router:
      If B online: find B's Chat Server → push via WebSocket
      If B offline: store in "undelivered" queue
  → Store in Cassandra
  → Send push notification (if offline)

Group Chat:
  A sends to Group G (members: A, B, C, D)
  → Fan-out: send to B, C, D individually
  → Small groups (<500): fan-out on write
  → Large groups: fan-out on read (lazy load)
```

### Step 6: Data Model (Cassandra)

```sql
-- Messages table (partition by chat_id for efficient retrieval)
CREATE TABLE messages (
    chat_id UUID,
    message_id TIMEUUID,    -- ordered by time
    sender_id UUID,
    content TEXT,
    type VARCHAR,            -- text, image, file
    created_at TIMESTAMP,
    PRIMARY KEY (chat_id, message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);

-- User chat list
CREATE TABLE user_chats (
    user_id UUID,
    chat_id UUID,
    last_message_at TIMESTAMP,
    unread_count INT,
    PRIMARY KEY (user_id, last_message_at)
) WITH CLUSTERING ORDER BY (last_message_at DESC);
```

### Online Presence

```python
# Heartbeat approach
# Client gửi heartbeat mỗi 5s → Redis update

def heartbeat(user_id):
    redis.setex(f"online:{user_id}", 10, "1")  # TTL 10s

def is_online(user_id):
    return redis.exists(f"online:{user_id}")

# Subscribe to presence changes
# Chỉ track cho friends/group members (tránh broadcast toàn bộ)
```

---

## PART B: News Feed System

### Step 1: Requirements

```
Functional:
- User post content (text, image, video)
- View personalized news feed (friends/following posts)
- Like, comment, share
- Sorted by relevance + time

Scale:
- 300M DAU, mỗi user xem feed ~10 times/day
- Feed QPS: 300M × 10 / 86400 = ~35K RPS
```

### Step 2: Feed Generation Approaches

#### Fan-out on Write (Push model) ⭐
```
User A posts → immediately push to all followers' feeds

A has 500 followers:
  Post → write to 500 feed caches

✅ Fast read: feed đã sẵn sàng
❌ Slow write: celebrity với 10M followers → 10M writes!
❌ Waste: inactive users cũng được push
```

#### Fan-out on Read (Pull model)
```
User B opens feed → pull posts from all friends at read time

B follows 500 users:
  Read → query 500 users' recent posts → merge + rank

✅ No wasted writes
❌ Slow read: phải aggregate nhiều nguồn
```

#### Hybrid ⭐⭐ (Best approach)
```
Normal users (< 10K followers): Fan-out on WRITE
Celebrities (> 10K followers):  Fan-out on READ

Feed = pre-computed feed + real-time celebrity posts
```

### Step 3: Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Post Service                          │
│  User → [Post Service] → DB + Kafka("post.created")     │
└──────────────────────────────────────┬───────────────────┘
                                       │
┌──────────────────────────────────────▼───────────────────┐
│                   Fan-out Service                        │
│  Listen Kafka → get follower list → write to feed cache  │
│  (skip celebrities, skip inactive users)                 │
└──────────────────────────────────────┬───────────────────┘
                                       │
┌──────────────────────────────────────▼───────────────────┐
│                   Feed Cache (Redis)                     │
│  feed:{user_id} → sorted set of post_ids (by score)     │
│  Keep latest 500 posts per user                          │
└──────────────────────────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼───────────────────┐
│                   Feed Service                           │
│  GET /feed → read from cache + merge celebrity posts     │
│  → Ranking (ML model) → return top N posts               │
└──────────────────────────────────────────────────────────┘
```

### Step 4: Feed Ranking

```python
# Simple ranking score
def calculate_score(post, user):
    time_decay = 1.0 / (hours_since(post.created_at) + 1)
    affinity = get_affinity(user.id, post.author_id)  # interaction history
    engagement = post.likes * 0.1 + post.comments * 0.3 + post.shares * 0.5
    
    score = time_decay * 0.3 + affinity * 0.4 + engagement * 0.3
    return score

# Production: ML ranking model (features: user, post, context)
```

### Step 5: Feed Storage (Redis)

```python
# Write: add post to followers' feeds
def fan_out_post(post):
    followers = get_non_celebrity_followers(post.author_id)
    
    pipe = redis.pipeline()
    for follower_id in followers:
        key = f"feed:{follower_id}"
        pipe.zadd(key, {post.id: post.created_at.timestamp()})
        pipe.zremrangebyrank(key, 0, -501)  # Keep latest 500
    pipe.execute()

# Read: get feed
def get_feed(user_id, page=1, size=20):
    key = f"feed:{user_id}"
    start = (page - 1) * size
    post_ids = redis.zrevrange(key, start, start + size - 1)
    
    # Merge với celebrity posts
    celebrity_ids = get_celebrity_followings(user_id)
    celebrity_posts = db.query(
        "SELECT * FROM posts WHERE author_id IN %s "
        "ORDER BY created_at DESC LIMIT 50", celebrity_ids
    )
    
    # Merge, rank, return
    all_posts = fetch_posts(post_ids) + celebrity_posts
    ranked = sorted(all_posts, key=lambda p: calculate_score(p, user_id), reverse=True)
    return ranked[:size]
```

---

## 📝 Bài tập

1. Implement simple chat server với WebSocket (FastAPI + Redis)
2. Implement news feed fan-out on write với Redis sorted sets
3. Design: Instagram stories (ephemeral content, 24h expiry)
4. Estimate: WhatsApp xử lý bao nhiêu messages/sec peak?

---

## 📚 Tài liệu
- *System Design Interview* — Alex Xu (Ch.12: Chat, Ch.11: News Feed)
- [Facebook Engineering: News Feed](https://engineering.fb.com/)
