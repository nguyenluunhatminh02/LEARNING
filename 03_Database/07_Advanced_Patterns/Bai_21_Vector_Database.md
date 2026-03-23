# Bài 21: Vector Database & AI-Era Data — Embeddings, Similarity Search

## 🎯 Mục tiêu
- Vector embeddings là gì, tại sao quan trọng
- Vector similarity search (ANN)
- pgvector (PostgreSQL extension)
- Specialized: Pinecone, Weaviate, Milvus, Qdrant
- RAG pattern with vector DB

## 📖 Câu chuyện đời thường
> Bạn vào cửa hàng nước hoa và nói: "Tôi muốn mùi giống loại này nhưng nhẹ hơn". Bạn không tìm theo tên (keyword search) mà theo **cảm nhận** (similarity search). Vector DB làm đúng việc này: mỗi chai nước hoa được mã hóa thành một dãy số (embedding) thể hiện "bản chất" của nó. Khi bạn nói "giống loại này", hệ thống tìm các vector gần nhất trong không gian đa chiều. Đây là công nghệ đằng sau **RAG**: khi bạn hỏi ChatGPT về tài liệu công ty, nó tìm đoạn văn bản có "ý nghĩa gần nhất" với câu hỏi của bạn.

---

## 1. Tại sao Vector Database là must-know cho CTO?

```
AI revolution → mọi thứ thành VECTOR:
  Text    → [0.12, -0.45, 0.78, ...] (768-1536 dimensions)
  Image   → [0.33, 0.91, -0.22, ...] 
  Audio   → [0.55, -0.12, 0.67, ...]
  Code    → [0.44, 0.23, -0.88, ...]

Vector = numerical representation that captures MEANING
  "Python programming" → [0.12, 0.45, ...]
  "Lập trình Python"   → [0.13, 0.44, ...]  ← gần nhau! (similar meaning)
  "Cooking recipes"    → [0.89, -0.33, ...]  ← xa! (different meaning)

Use cases đang EXPLODE:
  ✅ Semantic search ("tìm products giống cái này")
  ✅ RAG — Retrieval-Augmented Generation (ChatGPT + your data)
  ✅ Recommendation ("users giống bạn also liked...")
  ✅ Image search (tìm ảnh giống)
  ✅ Anomaly detection
  ✅ De-duplication (tìm content gần giống)

2024-2026: EVERY application sẽ cần vector search
→ CTO PHẢI hiểu technology này
```

---

## 2. Embeddings — Biến text/image thành vector

```python
# OpenAI text embeddings
from openai import OpenAI
client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="PostgreSQL is a powerful relational database"
)
vector = response.data[0].embedding
# → [0.023, -0.045, 0.012, ...] (1536 dimensions)

# Open-source alternative: Sentence-Transformers
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "PostgreSQL is a powerful database",
    "Cơ sở dữ liệu PostgreSQL rất mạnh",  # Vietnamese
    "I love cooking pasta"
]
embeddings = model.encode(sentences)
# embeddings[0] ≈ embeddings[1] (similar meaning!)
# embeddings[0] ≠ embeddings[2] (different topic)
```

### Similarity Metrics
```
Cosine Similarity: cos(θ) = (A·B) / (||A|| × ||B||)
  → Measures angle between vectors
  → Range: -1 (opposite) to 1 (identical)
  → Most common for text embeddings

Euclidean Distance (L2): √Σ(ai - bi)²
  → Measures straight-line distance
  → Range: 0 (identical) to ∞

Inner Product (Dot Product): Σ(ai × bi)
  → Fast, used when vectors are normalized
  
Hình dung:
  Cosine = "2 mũi tên chỉ cùng hướng?"
  Euclidean = "2 điểm cách nhau bao xa?"
```

---

## 3. pgvector — Vector Search trong PostgreSQL

```sql
-- Install extension
CREATE EXTENSION vector;

-- Create table with vector column
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    embedding vector(1536),  -- 1536-dimensional vector
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Insert document with embedding
INSERT INTO documents (title, content, embedding) 
VALUES (
    'PostgreSQL Performance',
    'Tips to optimize PostgreSQL queries...',
    '[0.023, -0.045, 0.012, ...]'::vector  -- 1536 numbers
);

-- Similarity search: tìm 5 documents gần nhất
SELECT id, title, 
       1 - (embedding <=> query_embedding) AS similarity  -- cosine distance
FROM documents
ORDER BY embedding <=> '[0.031, -0.042, ...]'::vector  -- <=> = cosine distance
LIMIT 5;

-- Operators:
-- <=>  cosine distance
-- <->  L2 (Euclidean) distance  
-- <#>  inner product (negative)

-- Filter + vector search
SELECT id, title, 
       1 - (embedding <=> query_embedding) AS similarity
FROM documents
WHERE metadata->>'category' = 'database'
  AND created_at > '2024-01-01'
ORDER BY embedding <=> '[0.031, -0.042, ...]'::vector
LIMIT 10;
```

### pgvector Indexing
```sql
-- HNSW index (Hierarchical Navigable Small World) — recommended
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 200);

-- IVFFlat index (Inverted File with Flat compression)
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);  -- number of clusters

-- HNSW vs IVFFlat:
-- HNSW: slower to build, faster queries, better recall ⭐
-- IVFFlat: faster to build, needs training data, lower recall

-- Performance tips:
SET hnsw.ef_search = 100;  -- higher = more accurate, slower
-- Default 40, increase for better recall
```

### pgvector — Practical RAG Pattern
```python
import psycopg2
from openai import OpenAI

client = OpenAI()

def embed_text(text: str) -> list[float]:
    response = client.embeddings.create(
        model="text-embedding-3-small", input=text
    )
    return response.data[0].embedding

def search_similar(query: str, top_k: int = 5):
    query_vector = embed_text(query)
    
    conn = psycopg2.connect("postgresql://...")
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, content,
               1 - (embedding <=> %s::vector) AS similarity
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, [str(query_vector), str(query_vector), top_k])
    
    return cur.fetchall()

def ask_with_context(question: str):
    # Step 1: Tìm documents liên quan
    relevant_docs = search_similar(question, top_k=5)
    
    # Step 2: Build context from documents
    context = "\n".join([f"- {doc[1]}: {doc[2]}" for doc in relevant_docs])
    
    # Step 3: Ask LLM with context (RAG)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Answer based on this context:\n{context}"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

# Usage
answer = ask_with_context("Làm sao optimize PostgreSQL query?")
```

---

## 4. Specialized Vector Databases

### Pinecone (Managed, Serverless)
```python
from pinecone import Pinecone

pc = Pinecone(api_key="your-key")
index = pc.Index("products")

# Upsert vectors
index.upsert(vectors=[
    {"id": "prod_1", "values": [0.1, 0.2, ...], "metadata": {"category": "laptop"}},
    {"id": "prod_2", "values": [0.3, 0.4, ...], "metadata": {"category": "phone"}},
])

# Query with metadata filter
results = index.query(
    vector=[0.15, 0.25, ...],
    top_k=10,
    filter={"category": {"$eq": "laptop"}},
    include_metadata=True
)
```

### Weaviate (Open-source, Full-featured)
```python
import weaviate

client = weaviate.Client("http://localhost:8080")

# Auto-vectorize text (built-in models!)
client.schema.create_class({
    "class": "Document",
    "vectorizer": "text2vec-openai",  # auto-embed!
    "properties": [
        {"name": "title", "dataType": ["text"]},
        {"name": "content", "dataType": ["text"]},
        {"name": "category", "dataType": ["text"]}
    ]
})

# Insert (auto-vectorized)
client.data_object.create(
    class_name="Document",
    data_object={"title": "PostgreSQL Guide", "content": "...", "category": "database"}
)

# Semantic search (no vector needed — auto-vectorizes query!)
result = client.query.get("Document", ["title", "content"]).with_near_text({
    "concepts": ["how to optimize database queries"]
}).with_limit(5).do()
```

### Comparison Table
```
| Feature      | pgvector    | Pinecone   | Weaviate    | Milvus     | Qdrant     |
|------------- |------------ |----------- |------------ |----------- |----------- |
| Type         | PG Extension| Managed    | Open-source | Open-source| Open-source|
| Scale        | ~5M vectors | Billions   | ~50M        | Billions   | ~100M      |
| Auto-embed   | No          | No         | ✅ Yes      | No         | No         |
| Hybrid search| SQL + vector| Metadata   | BM25+vector | ✅         | ✅         |
| Managed      | Via PG host | ✅ Only    | ✅ + self   | Zilliz     | ✅ + self  |
| Cost         | Free        | $$$        | Free + paid | Free + paid| Free + paid|
| Best for     | < 5M vecs   | Serverless | Full-feature| Big scale  | Performance|
```

---

## 5. ANN (Approximate Nearest Neighbor) Algorithms

```
Exact search: compare query with ALL vectors → O(N) → too slow for millions

ANN: Find TOP-K approximate nearest neighbors → much faster

Algorithms:
  ┌─────────────────────────────────────────────────┐
  │ HNSW (Hierarchical Navigable Small World)       │
  │ → Graph-based, best quality, most common ⭐     │
  │ → Used by: pgvector, Weaviate, Qdrant           │
  │                                                  │
  │ Layer 3: [A] ——————————— [D]                    │
  │ Layer 2: [A] —— [B] ——— [D]                    │
  │ Layer 1: [A] [B] [C] [D] [E] [F]               │
  │ Layer 0: [A][B][C][D][E][F][G][H][I]           │
  │                                                  │
  │ Search: start top layer → navigate down          │
  │ → O(log N) average                              │
  └─────────────────────────────────────────────────┘

  IVF (Inverted File Index):
    → Cluster vectors → search only relevant clusters
    → Faster build, lower recall than HNSW

  Product Quantization (PQ):
    → Compress vectors: 1536 floats → 192 bytes
    → 8x memory reduction, slight accuracy loss
    → Used for billions of vectors (memory constraint)

  ScaNN (Google):
    → Anisotropic quantization + efficient scoring
    → Used by Google for large-scale search
```

---

## 6. Chunking Strategies (cho RAG)

```
Problem: Documents dài (10+ pages) → embedding toàn bộ = poor retrieval
Solution: Chia thành chunks → embed mỗi chunk

Strategy 1: Fixed-size chunks
  "Split mỗi 500 tokens, overlap 50 tokens"
  ✅ Simple, ❌ có thể cắt giữa câu

Strategy 2: Semantic chunking
  Chia theo paragraph, section headers
  ✅ Preserves meaning, ❌ uneven sizes

Strategy 3: Recursive splitting
  Split by "\n\n" → nếu quá dài → split by "\n" → split by ". "
  ✅ Good balance (LangChain default)

Best practices:
  - Chunk size: 200-1000 tokens (depends on use case)
  - Overlap: 10-20% (prevents losing context at boundaries)
  - Include metadata: filename, section, page number
  - Test with YOUR data: no one-size-fits-all
```

---

## 7. CTO Decision: pgvector vs Specialized DB

```
Dùng pgvector khi:
  ✅ < 5 triệu vectors
  ✅ Đã dùng PostgreSQL (no new infra)
  ✅ Cần SQL queries KẾT HỢP vector search
  ✅ Team nhỏ, budget limited
  ✅ MVP / early stage

Dùng Specialized (Pinecone/Weaviate/Qdrant) khi:
  ✅ > 10 triệu vectors
  ✅ Need sub-10ms latency at scale
  ✅ Vector search là CORE feature (not just a feature)
  ✅ Need advanced: hybrid search, auto-embedding, multi-tenancy
  ✅ Have budget for managed service

★ Recommendation:
  "Start with pgvector, migrate when you hit limits"
  (giống strategy PostgreSQL-first ở Bài 16)
```

---

## 📝 Bài tập

1. Setup pgvector: embed 1000 documents, build semantic search API
2. Implement RAG: pgvector + OpenAI cho Q&A trên documentation
3. Compare recall/latency: pgvector HNSW vs IVFFlat
4. Design vector search architecture cho e-commerce product similarity

---

## 📚 Tài liệu
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Pinecone Learning Center](https://www.pinecone.io/learn/)
- [HNSW Paper](https://arxiv.org/abs/1603.09320)
- *Building LLM Applications* — covers RAG patterns
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
