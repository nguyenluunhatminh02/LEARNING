# Bài 18: Elasticsearch & Search Engine — Tìm kiếm ở production scale

## 🎯 Mục tiêu
- Elasticsearch architecture & concepts
- Full-text search, inverted index
- Aggregations & analytics
- Production patterns: ELK, search design

## 📖 Câu chuyện đời thường
> Bạn có 1 triệu email và muốn tìm email nào có từ "hợp đồng". SQL phải đọc từng email một (LIKE '%hợp đồng%') — cực chậm. **Elasticsearch** dùng **inverted index** giống mục lục cuối sách: ghi sẵn "hợp đồng" xuất hiện ở email số 45, 123, 789 — tra vào một phát là ra. Elasticsearch còn hiểu "hợp đồng", "contract", "hướng dẫn hợp đồng" là liên quan (fuzzy search). **ELK** (Elasticsearch + Logstash + Kibana) giống như: thu thập log từ mọi nơi (Logstash) → tìm kiếm nhanh (Elasticsearch) → vẽ biểu đồ đẹp (Kibana).

---

## 1. Tại sao cần Search Engine?

```
PostgreSQL full-text search:
  ✅ Đủ tốt cho < 1M documents, simple search
  ❌ Không hỗ trợ: fuzzy search, autocomplete, faceting, relevance tuning
  ❌ Chậm khi > 10M documents phức tạp

Elasticsearch:
  ✅ Sub-second search trên billions of documents
  ✅ Fuzzy matching ("pyhton" → "python")
  ✅ Autocomplete, suggestions, "did you mean?"
  ✅ Faceted search (filter by category, price range, brand)
  ✅ Relevance scoring (BM25, custom boosting)
  ✅ Log analytics (ELK stack)
  ✅ Real-time aggregations

Ai dùng ES: Google (internal), Wikipedia, GitHub, Stack Overflow,
             Uber, Netflix, Shopify... gần như mọi search feature
```

---

## 2. Core Concepts

### Inverted Index
```
Documents:
  Doc 1: "PostgreSQL is a powerful database"
  Doc 2: "Elasticsearch uses inverted index"
  Doc 3: "PostgreSQL supports full-text search in database"

Inverted Index (sau tokenization + lowercasing):
  Term          → Documents
  "postgresql"  → [Doc 1, Doc 3]
  "powerful"    → [Doc 1]
  "database"    → [Doc 1, Doc 3]
  "elasticsearch" → [Doc 2]
  "inverted"    → [Doc 2]
  "index"       → [Doc 2]
  "supports"    → [Doc 3]
  "full-text"   → [Doc 3]
  "search"      → [Doc 3]

Query "postgresql database":
  "postgresql" → [Doc 1, Doc 3]
  "database"   → [Doc 1, Doc 3]
  → Intersection: [Doc 1, Doc 3] (both match)
  → Doc 1 score higher (shorter, more dense match)
```

### Architecture
```
Cluster → Nodes → Indices → Shards → Documents

Elasticsearch Cluster:
  ┌─────────────────────────────────────────────────┐
  │ Cluster: "production"                            │
  │                                                  │
  │  Node 1 (Master)    Node 2           Node 3     │
  │  ┌────────────┐    ┌────────────┐   ┌──────────┐│
  │  │ Shard P0   │    │ Shard P1   │   │ Shard P2 ││
  │  │ Shard R1   │    │ Shard R2   │   │ Shard R0 ││
  │  └────────────┘    └────────────┘   └──────────┘│
  └─────────────────────────────────────────────────┘
  
  P = Primary shard, R = Replica shard
  Index "products" → 3 primary shards + 3 replicas
  → Any node can serve queries (parallel search)
  → 1 node dies → replicas promote to primary
```

---

## 3. CRUD & Search

### Index & Document
```python
from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Create index with mapping (schema)
es.indices.create(index="products", body={
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "product_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "asciifolding", "snowball"]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "name":        {"type": "text", "analyzer": "product_analyzer"},
            "description": {"type": "text", "analyzer": "product_analyzer"},
            "category":    {"type": "keyword"},  # exact match, aggregations
            "price":       {"type": "float"},
            "brand":       {"type": "keyword"},
            "rating":      {"type": "float"},
            "created_at":  {"type": "date"},
            "tags":        {"type": "keyword"},   # array of keywords
            "in_stock":    {"type": "boolean"}
        }
    }
})

# Index document
es.index(index="products", id=1, body={
    "name": "MacBook Pro 16 inch M3 Max",
    "description": "Laptop mạnh nhất cho developers. RAM 64GB, SSD 1TB.",
    "category": "Laptops",
    "price": 3499.99,
    "brand": "Apple",
    "rating": 4.8,
    "tags": ["laptop", "apple", "developer", "premium"],
    "in_stock": True,
    "created_at": "2024-01-15"
})

# Bulk index (efficient for large datasets)
actions = [
    {"_index": "products", "_id": i, "_source": product}
    for i, product in enumerate(products_list)
]
from elasticsearch.helpers import bulk
bulk(es, actions, chunk_size=1000)
```

### Full-Text Search
```python
# Simple match (analyzed, relevance scored)
result = es.search(index="products", body={
    "query": {
        "match": {
            "name": "macbook pro developer"
        }
    }
})

# Multi-match (search across multiple fields)
result = es.search(index="products", body={
    "query": {
        "multi_match": {
            "query": "laptop cho developers",
            "fields": ["name^3", "description", "tags^2"],
            "type": "best_fields",
            "fuzziness": "AUTO"  # fuzzy matching!
        }
    }
})
# name^3 = boost name field 3x (more relevant if matches in name)

# Bool query (complex filtering)
result = es.search(index="products", body={
    "query": {
        "bool": {
            "must": [
                {"multi_match": {"query": "laptop", "fields": ["name", "description"]}}
            ],
            "filter": [
                {"term": {"category": "Laptops"}},
                {"range": {"price": {"gte": 1000, "lte": 3000}}},
                {"term": {"in_stock": True}}
            ],
            "should": [
                {"term": {"brand": "Apple"}},  # boost Apple products
                {"range": {"rating": {"gte": 4.5}}}  # boost high-rated
            ],
            "minimum_should_match": 0
        }
    },
    "sort": [
        {"_score": "desc"},  # relevance first
        {"price": "asc"}     # then price
    ],
    "from": 0, "size": 20
})
```

### Fuzzy Search & Autocomplete
```python
# Fuzzy: "pyhton" → matches "python"
{"match": {"name": {"query": "pyhton", "fuzziness": "AUTO"}}}

# Autocomplete (suggest-as-you-type)
# Requires: completion suggester mapping
es.indices.create(index="products_suggest", body={
    "mappings": {
        "properties": {
            "suggest": {
                "type": "completion",  # special type for autocomplete
                "analyzer": "simple"
            }
        }
    }
})

# Query autocomplete
result = es.search(index="products_suggest", body={
    "suggest": {
        "product-suggest": {
            "prefix": "mac",
            "completion": {
                "field": "suggest",
                "size": 5,
                "fuzzy": {"fuzziness": 1}
            }
        }
    }
})
# → "MacBook Pro", "MacBook Air", "Mac Mini"
```

---

## 4. Aggregations (Analytics)

```python
# Faceted search: count products by category + price ranges
result = es.search(index="products", body={
    "size": 0,  # no documents, only aggregations
    "aggs": {
        "categories": {
            "terms": {"field": "category", "size": 20}
        },
        "price_ranges": {
            "range": {
                "field": "price",
                "ranges": [
                    {"key": "Budget",  "to": 500},
                    {"key": "Mid",     "from": 500, "to": 1500},
                    {"key": "Premium", "from": 1500, "to": 3000},
                    {"key": "Luxury",  "from": 3000}
                ]
            }
        },
        "brands": {
            "terms": {"field": "brand", "size": 10},
            "aggs": {
                "avg_price": {"avg": {"field": "price"}},
                "avg_rating": {"avg": {"field": "rating"}}
            }
        },
        "avg_price": {"avg": {"field": "price"}},
        "price_stats": {"stats": {"field": "price"}}
    }
})

# Result:
# categories: [{key: "Laptops", count: 150}, {key: "Phones", count: 300}]
# price_ranges: [{key: "Budget", count: 200}, {key: "Premium", count: 80}]
# brands: [{key: "Apple", count: 50, avg_price: 1200}, ...]
```

---

## 5. ELK Stack (Log Analytics)

```
ELK = Elasticsearch + Logstash + Kibana

  ┌─────────┐    ┌──────────┐    ┌──────────────┐    ┌─────────┐
  │ App Logs│──→ │ Filebeat │──→ │  Logstash    │──→ │  Elastic │──→ Kibana
  │ Nginx   │    │ (shipper)│    │ (transform)  │    │  search  │   (dashboard)
  │ Syslog  │    └──────────┘    └──────────────┘    └─────────┘
  └─────────┘

Modern alternative: Elasticsearch + Filebeat (no Logstash)
  Filebeat → Ingest Pipeline (ES) → Index → Kibana

Use cases:
  - Centralized logging (all services → 1 place)
  - Error tracking & alerting
  - Request tracing (combine with distributed tracing)
  - Security events (SIEM)
  - Business analytics (page views, conversions)
```

---

## 6. Production Patterns

### Sync Pattern: PostgreSQL → Elasticsearch
```
PostgreSQL (source of truth) → Elasticsearch (search index)

Method 1: Application-level dual write ← Simple nhưng risky
  app.save_to_postgres(product)
  app.index_to_elasticsearch(product)
  # ❌ Problem: ES down → data inconsistent

Method 2: CDC via Debezium ← Recommended
  PostgreSQL → WAL → Debezium → Kafka → ES Consumer
  # ✅ Reliable, eventually consistent
  # (Xem thêm Bài 19: CDC & Event Streaming)

Method 3: Periodic batch sync
  Cron job mỗi 5 phút: query PG changes → bulk index ES
  # ✅ Simple, ❌ delay up to 5 minutes
```

### Index Strategy
```
Per-environment:  products_dev, products_staging, products_prod
Per-time:         logs_2024_01, logs_2024_02 (monthly indices)

Index Lifecycle Management (ILM):
  Hot:   0-7 days   → SSD, 3 replicas (frequent search)
  Warm:  7-30 days  → HDD, 1 replica  (less frequent)
  Cold:  30-90 days → HDD, 0 replicas (rare access)
  Delete: >90 days  → auto-delete
```

---

## 7. Elasticsearch vs Alternatives

```
Elasticsearch:
  ✅ Most feature-rich, largest ecosystem
  ❌ Heavy (JVM), expensive memory, SSPL license

OpenSearch (AWS fork):
  ✅ Apache 2.0 license, AWS managed
  ≈ Same features as ES (fork from 7.10)

Meilisearch:
  ✅ Blazing fast, easy setup, typo-tolerant
  ❌ Limited aggregations, single-node
  → Perfect cho: simple product search, small-medium scale

Typesense:
  ✅ Easy to use, fast, open-source
  ❌ Less feature-rich than ES
  → Perfect cho: startups, simple search needs

Zinc/Quickwit:
  ✅ Lightweight alternatives
  → Perfect cho: log analytics when ES is overkill
```

---

## 📝 Bài tập

1. Setup Elasticsearch, index 10K products, implement search với fuzzy + facets
2. Build autocomplete API cho product search
3. Setup ELK stack: collect app logs, create Kibana dashboard
4. Implement PostgreSQL → Elasticsearch sync qua batch job

---

## 📚 Tài liệu
- *Elasticsearch: The Definitive Guide* — Clinton Gormley
- [Elasticsearch Official Docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Meilisearch Docs](https://docs.meilisearch.com/) — lightweight alternative
- *Relevant Search* — Doug Turnbull (relevance engineering)
