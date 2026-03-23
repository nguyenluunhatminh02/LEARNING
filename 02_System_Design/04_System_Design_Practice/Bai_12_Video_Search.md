# Bài 12: System Design Practice — Video Streaming & Search Engine

## 🎯 Mục tiêu
- Thiết kế Video Streaming Platform (YouTube)
- Thiết kế Search Engine (Google-like)

## 📖 Câu chuyện đời thường
> **Video Streaming** giống như một đài truyền hình cá nhân. Khi bạn xem phim, không ai gửi cả cuốn phim 1 lần (file quá lớn!). Thay vào đó, họ gửi từng đoạn nhỏ (chunk), và nếu WiFi chậm thì giảm chất lượng cho mượt (adaptive bitrate). Video được lưu ở nhiều độ phân giải (360p, 720p, 1080p) giống như có nhiều phiên bản ảnh: nhỏ cho điện thoại, lớn cho TV. **Search Engine** giống thư viện có hệ thống index: thay vì đọc từng cuốn sách để tìm từ "AI", bạn mở mục lục chủ đề và tra ngay — đó là inverted index.

---

## PART A: Video Streaming (YouTube)

### Step 1: Requirements

```
Functional:
- Upload videos
- Stream/watch videos (adaptive bitrate)
- Search videos
- Like, comment, subscribe

Non-functional:
- Fast upload processing
- Smooth playback (no buffering)
- Global availability
- Support mobile + web

Scale:
- 2B monthly active users
- 500 hours video uploaded per minute
- Average video watch: 5 minutes
```

### Step 2: Video Upload Pipeline

```
User uploads video (1080p, 2GB)
         │
         ▼
┌─────────────────┐
│  Upload Service  │ → Store original in Object Storage (S3)
└────────┬────────┘
         │ trigger
┌────────▼────────┐
│  Message Queue   │ (Kafka)
└────────┬────────┘
         │
┌────────▼────────────────────┐
│   Video Processing Pipeline │
│                              │
│  1. Transcoding              │
│     → 240p, 360p, 480p,     │
│       720p, 1080p, 4K       │
│                              │
│  2. Thumbnail generation     │
│     → Multiple thumbnails    │
│                              │
│  3. Content moderation       │
│     → AI check (nudity,     │
│       violence, copyright)   │
│                              │
│  4. Metadata extraction      │
│     → Duration, codec, size  │
└────────┬────────────────────┘
         │
┌────────▼────────┐
│   CDN Upload     │ → Push segments to edge servers
└────────┬────────┘
         │
┌────────▼────────┐
│  DB Update       │ → Video status: "ready"
└─────────────────┘
```

### Step 3: Video Streaming (HLS/DASH)

```
Adaptive Bitrate Streaming:

Video chia thành segments (2-10 seconds each)
Mỗi segment có nhiều quality levels

.m3u8 manifest file:
  #EXTM3U
  #EXT-X-STREAM-INF:BANDWIDTH=800000,RESOLUTION=640x360
  360p/segment_001.ts
  #EXT-X-STREAM-INF:BANDWIDTH=2000000,RESOLUTION=1280x720
  720p/segment_001.ts
  #EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080
  1080p/segment_001.ts

Client tự động switch quality based on bandwidth:
  Wifi ổn → 1080p
  Network chậm → tự hạ 360p
  Network phục hồi → tăng lại 720p
```

### Step 4: Architecture

```
                    ┌──────────────────┐
                    │       CDN        │ ← Serve video segments
                    │  (CloudFront)    │    (cache tại edge)
                    └────────▲─────────┘
                             │
┌─────────┐  API  ┌─────────┴─────────┐
│  Client  │─────→│   API Gateway      │
└─────────┘      └─────────┬─────────┘
                           │
         ┌─────────────────┼──────────────────┐
         │                 │                  │
  ┌──────▼────┐    ┌──────▼──────┐   ┌──────▼───────┐
  │  Upload   │    │   Stream    │   │   Search     │
  │  Service  │    │   Service   │   │   Service    │
  └──────┬────┘    └──────┬──────┘   └──────┬───────┘
         │                │                  │
  ┌──────▼────┐    ┌──────▼──────┐   ┌──────▼───────┐
  │    S3     │    │    Redis    │   │Elasticsearch │
  │ (videos)  │    │  (metadata  │   │  (search     │
  │           │    │   cache)    │   │   index)     │
  └───────────┘    └─────────────┘   └──────────────┘
                   ┌─────────────┐
                   │ PostgreSQL  │ (users, videos metadata)
                   └─────────────┘
```

### Video Metadata DB

```sql
CREATE TABLE videos (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    title VARCHAR(255),
    description TEXT,
    status VARCHAR(20),  -- uploading, processing, ready, failed
    duration_sec INT,
    view_count BIGINT DEFAULT 0,
    like_count BIGINT DEFAULT 0,
    created_at TIMESTAMP,
    thumbnail_url TEXT,
    manifest_url TEXT
);

-- Denormalized view count (eventual consistency ok)
-- Increment views via Kafka → batch update
```

---

## PART B: Search Engine Design

### Step 1: Core Components

```
Web Crawler → Indexer → Query Processor → Ranker → Results

1. Crawler: thu thập web pages
2. Indexer: tạo inverted index
3. Query Processor: parse + expand query
4. Ranker: rank results (PageRank + relevance)
```

### Step 2: Inverted Index

```
Documents:
  Doc1: "the cat sat on the mat"
  Doc2: "the dog sat on the log"
  Doc3: "the cat and the dog"

Inverted Index:
  "cat"  → [Doc1, Doc3]
  "sat"  → [Doc1, Doc2]
  "dog"  → [Doc2, Doc3]
  "mat"  → [Doc1]
  "log"  → [Doc2]
  "and"  → [Doc3]

Query "cat sat" → intersection([Doc1,Doc3], [Doc1,Doc2]) = [Doc1]
```

```python
# Simple inverted index
from collections import defaultdict

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(set)
    
    def add_document(self, doc_id, text):
        tokens = text.lower().split()
        for token in tokens:
            self.index[token].add(doc_id)
    
    def search(self, query):
        tokens = query.lower().split()
        if not tokens:
            return set()
        
        result = self.index.get(tokens[0], set())
        for token in tokens[1:]:
            result = result.intersection(self.index.get(token, set()))
        return result
```

### Step 3: Ranking — TF-IDF + PageRank

```python
import math

def tf_idf(term, document, all_documents):
    # TF: frequency of term in document
    tf = document.count(term) / len(document)
    
    # IDF: inverse document frequency
    containing = sum(1 for doc in all_documents if term in doc)
    idf = math.log(len(all_documents) / (1 + containing))
    
    return tf * idf

# PageRank (simplified)
# PR(A) = (1-d) + d × Σ(PR(T) / L(T))
# d = damping factor (0.85)
# T = pages linking to A
# L(T) = number of outbound links from T
```

### Step 4: Search Architecture

```
User query "best restaurants NYC"
         │
  ┌──────▼──────┐
  │Query Parser  │ → tokenize, remove stop words, expand synonyms
  └──────┬──────┘
         │  "best restaurant new york city"
  ┌──────▼──────┐
  │ Index Shards │ → query multiple shards in parallel
  │ (distributed │    Shard 1: top-100 results
  │  across DCs) │    Shard 2: top-100 results
  └──────┬──────┘    Shard 3: top-100 results
         │
  ┌──────▼──────┐
  │   Merger     │ → merge results from all shards
  └──────┬──────┘
         │
  ┌──────▼──────┐
  │   Ranker     │ → apply ML ranking model
  │              │    features: relevance, freshness, authority,
  │              │    user location, click history
  └──────┬──────┘
         │
  ┌──────▼──────┐
  │  Response    │ → top-10 results + snippets + ads
  └─────────────┘
```

---

## 📝 Bài tập

1. Implement video upload + HLS streaming pipeline (FFmpeg + S3 + CloudFront)
2. Build simple inverted index search engine bằng Python
3. Design: Spotify — music streaming + recommendations
4. Estimate: YouTube cần bao nhiêu storage/year?

---

## 📚 Tài liệu
- *System Design Interview Vol 2* — Alex Xu (Ch.14: YouTube)
- *Information Retrieval* — Manning, Raghavan, Schütze
- [Netflix Tech Blog](https://netflixtechblog.com/)
