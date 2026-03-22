# Bài 04: Storage Engine & B-Tree

## 🎯 Mục tiêu
- Hiểu database lưu data trên disk thế nào
- B-Tree vs LSM-Tree
- Write-Ahead Log (WAL)
- Pages, buffer pool

---

## 1. Data Storage on Disk

```
Database = collection of FILES on disk

PostgreSQL data directory:
  base/           → database files
    16384/        → database OID
      16385       → table file (mỗi table = 1+ files)
      16385_fsm   → free space map
      16385_vm    → visibility map

Mỗi file chia thành PAGES (blocks):
  Page size = 8KB (PostgreSQL default)
  Table 1GB = 131,072 pages
```

### Page Structure (PostgreSQL)
```
┌────────────────────────────────────────┐
│ Page Header (24 bytes)                 │
│   - LSN, checksum, flags              │
├────────────────────────────────────────┤
│ Item Pointers (line pointers)          │
│   [offset1] [offset2] [offset3] ...   │
├────────────────────────────────────────┤
│                                        │
│           Free Space                   │
│                                        │
├────────────────────────────────────────┤
│ Tuple 3 (row data)                     │
│ Tuple 2 (row data)                     │
│ Tuple 1 (row data)                     │
│ Special Space                          │
└────────────────────────────────────────┘

Rows thêm từ DƯỚI lên, pointers thêm từ TRÊN xuống
→ Gặp nhau = page full
```

---

## 2. B-Tree — Index Structure chính

```
B-Tree = Balanced Tree, mỗi node = 1 page (8KB)

                    [50]
                   /    \
          [20, 35]       [70, 85]
         /   |   \      /   |   \
    [10,15][25,30][40,45][60,65][75,80][90,95]
    ↓       ↓       ↓     ↓      ↓      ↓
   Data   Data    Data   Data   Data   Data

Properties:
- Balanced: tất cả leaf nodes cùng depth
- Sorted: data trong mỗi node sorted
- Fan-out cao: mỗi node chứa ~100-500 keys
- Depth thấp: 1M rows ≈ 3 levels, 1B rows ≈ 4 levels
- Lookup: O(log N) — 1B rows = ~4 disk reads
```

### B-Tree Operations
```
Search key=42:
  Root [50] → 42 < 50 → go left
  Node [20,35] → 42 > 35 → go right
  Leaf [40,45] → found 42 between → get row pointer
  → Total: 3 page reads → 3 × ~0.1ms (SSD) = 0.3ms

Insert key=33:
  Navigate to correct leaf
  If leaf has space → insert
  If leaf full → SPLIT: create new leaf, push middle key up
  If parent full → cascade split up

Delete key=42:
  Navigate to leaf → remove
  If leaf < half full → MERGE with sibling or REDISTRIBUTE
```

---

## 3. LSM-Tree (Log-Structured Merge Tree)

```
LSM-Tree: Optimized cho WRITE-heavy workloads

Write path:
  1. Write to WAL (durability)
  2. Write to MemTable (in-memory sorted structure)
  3. When MemTable full → flush to disk as SSTable (Sorted String Table)
  4. Background compaction: merge SSTables

Read path:
  1. Check MemTable
  2. Check Level-0 SSTables (most recent)
  3. Check Level-1, Level-2... (older)
  → Use Bloom Filter to skip SSTables that don't contain key

┌──────────┐
│ MemTable │ ← Writes go here (RAM)
└────┬─────┘
     │ flush
┌────▼─────┐
│ Level 0  │ SSTable, SSTable, SSTable
└────┬─────┘
     │ compaction (merge + sort)
┌────▼─────┐
│ Level 1  │ SSTable (larger, sorted)
└────┬─────┘
     │ compaction
┌────▼─────┐
│ Level 2  │ SSTable (even larger)
└──────────┘
```

### B-Tree vs LSM-Tree

| | B-Tree | LSM-Tree |
|---|---|---|
| Write speed | Slower (random I/O) | **Faster** (sequential I/O) |
| Read speed | **Faster** (1 lookup) | Slower (check multiple levels) |
| Space usage | More (fragmentation) | **Less** (compacted) |
| Write amplification | Lower | Higher (compaction) |
| Use case | **OLTP, general** | Write-heavy, time-series |
| Used by | PostgreSQL, MySQL | RocksDB, Cassandra, LevelDB |

---

## 4. Write-Ahead Log (WAL)

```
Problem: Server crash giữa lúc write → data corrupt?

Solution: WAL — ghi log TRƯỚC khi modify data pages

Write flow:
  1. Write change to WAL (sequential, fast) → fsync
  2. Modify page in buffer pool (memory)
  3. Dirty page flushed to disk later (checkpoint)

Crash recovery:
  1. Đọc WAL từ last checkpoint
  2. Replay tất cả changes → data consistent

WAL = append-only log file
  → Sequential write = FAST (100x faster than random write)
  → Guarantee durability even with crash
```

```sql
-- PostgreSQL WAL settings
SHOW wal_level;           -- minimal, replica, logical
SHOW max_wal_size;        -- default 1GB
SHOW checkpoint_timeout;  -- default 5 min

-- WAL used for:
-- 1. Crash recovery
-- 2. Replication (streaming WAL to replicas)
-- 3. Point-in-time recovery (PITR)
```

---

## 5. Buffer Pool

```
Buffer Pool = cache of pages in RAM

Read flow:
  1. Check buffer pool (RAM) → cache hit? return
  2. Cache miss → read page from disk → put in buffer pool → return

LRU eviction: khi buffer pool đầy, evict least recently used pages

PostgreSQL: shared_buffers (default 128MB, production: 25% of RAM)

┌──────────────────────────────────────┐
│         Buffer Pool (RAM)            │
│  [Page 1] [Page 5] [Page 23] ...    │
│     ↕         ↕         ↕           │
└──────────────────────────────────────┘
         ↕ read/write
┌──────────────────────────────────────┐
│         Disk (Data Files)            │
│  [Page 1][Page 2][Page 3]...        │
└──────────────────────────────────────┘
```

```sql
-- Check buffer pool hit ratio
SELECT 
    sum(heap_blks_read) AS disk_reads,
    sum(heap_blks_hit) AS cache_hits,
    ROUND(sum(heap_blks_hit) * 100.0 / 
          NULLIF(sum(heap_blks_hit) + sum(heap_blks_read), 0), 2) AS hit_ratio
FROM pg_statio_user_tables;
-- Target: > 99% hit ratio
```

---

## 📝 Bài tập

1. Vẽ B-Tree cho các key: 5, 15, 25, 35, 45, 55, 65 (order=3)
2. So sánh B-Tree vs LSM-Tree cho: e-commerce vs IoT logging
3. Check buffer pool hit ratio cho PostgreSQL của bạn
4. Giải thích WAL giúp crash recovery thế nào

---

## 📚 Tài liệu
- *Database Internals* — Alex Petrov (Ch.2-4)
- *Designing Data-Intensive Applications* — Kleppmann (Ch.3)
- [PostgreSQL Page Layout](https://www.postgresql.org/docs/current/storage-page-layout.html)
