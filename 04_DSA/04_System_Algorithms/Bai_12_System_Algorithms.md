# Bài 12: System-Level Algorithms & Probabilistic Data Structures

## 🎯 Mục tiêu
- Consistent Hashing
- Bloom Filter, HyperLogLog
- Skip List, Count-Min Sketch

---

## 1. Consistent Hashing

```python
import hashlib
from bisect import bisect_right

class ConsistentHash:
    def __init__(self, nodes, virtual_nodes=150):
        self.ring = {}
        self.sorted_keys = []
        self.vnodes = virtual_nodes
        for node in nodes:
            self.add_node(node)
    
    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)
    
    def add_node(self, node):
        for i in range(self.vnodes):
            vkey = self._hash(f"{node}:{i}")
            self.ring[vkey] = node
            self.sorted_keys.append(vkey)
        self.sorted_keys.sort()
    
    def get_node(self, key):
        h = self._hash(key)
        idx = bisect_right(self.sorted_keys, h) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]

# Used in: Load Balancing, DB Sharding, CDN, Distributed Cache
```

---

## 2. Bloom Filter

```python
import mmh3

class BloomFilter:
    def __init__(self, size=1000000, num_hashes=7):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size
    
    def add(self, item):
        for i in range(self.num_hashes):
            idx = mmh3.hash(item, i) % self.size
            self.bit_array[idx] = 1
    
    def might_contain(self, item):
        for i in range(self.num_hashes):
            idx = mmh3.hash(item, i) % self.size
            if self.bit_array[idx] == 0:
                return False  # DEFINITELY not in set
        return True  # PROBABLY in set (false positive possible)

# Space: 10 bits/item → 1% false positive rate
# Used in: spam filter, cache, DB (avoid disk lookups)
```

---

## 3. HyperLogLog — Count Distinct

```
Problem: count unique visitors (cardinality) in billions → too much memory for Set

HyperLogLog: estimate cardinality with ~1.5KB memory
  Error rate: ~2%

Concept: hash values → count leading zeros
  More leading zeros → likely more unique values

Redis: PFADD visitors "user1" "user2"
       PFCOUNT visitors → approximate unique count
```

---

## 4. Skip List

```
Level 3:  1 ─────────────────────── 9
Level 2:  1 ──────── 4 ─────────── 9
Level 1:  1 ─── 3 ── 4 ── 6 ── 7 ─ 9
Level 0:  1  2  3  4  5  6  7  8  9

Search 7:
  L3: 1→9 (too far) → go down
  L2: 1→4→9 (too far) → go down
  L1: 4→6→7 ✅

O(log N) search, insert, delete
Used in: Redis sorted sets, LevelDB
```

---

## 5. Count-Min Sketch

```
Matrix of counters:
  hash1(item) → increment row 1
  hash2(item) → increment row 2
  hash3(item) → increment row 3

Query frequency: min(row1[h1], row2[h2], row3[h3])
→ Approximate count (never underestimates)

Used in: real-time analytics, network traffic monitoring
```

---

## 📝 Bài tập
1. Implement Consistent Hashing, test adding/removing nodes
2. Implement Bloom Filter, measure false positive rate
3. Implement Skip List from scratch
4. Compare: exact count (Set) vs HyperLogLog for 10M items

## 🎯 LeetCode Practice List (System Design + Algorithms)

**Design Problems (apply system algorithms):**
- #380 Insert Delete GetRandom O(1) (Medium) ⭐
- #432 All O`one Data Structure (Hard)
- #460 LFU Cache (Hard)
- #895 Maximum Frequency Stack (Hard)
- #1166 Design File System (Medium)
- #588 Design In-Memory File System (Hard)

**Bit Manipulation (related to Bloom Filter concepts):**
- #136 Single Number (Easy)
- #191 Number of 1 Bits (Easy)
- #338 Counting Bits (Easy)

> Focus chính của bài này là implement system-level data structures từ scratch, không chỉ giải LeetCode.

## 📚 Tài liệu
- *Algorithms* — Sedgewick & Wayne
- [Redis Data Structures](https://redis.io/docs/data-types/)
