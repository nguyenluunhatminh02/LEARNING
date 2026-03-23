# Bài 01: CS Fundamentals & Back-of-the-Envelope Estimation

## 🎯 Mục tiêu
- Data structures quan trọng cho System Design
- Estimation: tính QPS, storage, bandwidth
- Các con số mọi engineer cần nhớ

## 📖 Câu chuyện đời thường
> Bạn muốn mở một quán cà phê. Trước khi xây, bạn cần ước lượng: "Mỗi ngày bao nhiêu khách? Cần bao nhiêu bàn? Kho chứa bao nhiêu cà phê?" — đó chính là **Back-of-the-Envelope Estimation**. Nếu bạn không ước lượng, có thể thuê mặt bằng quá nhỏ (server yếu) hoặc quá lớn (lãng phí tiền). Việc nhớ các con số latency giống như biết khoảng cách từ nhà đến chợ, từ chợ đến kho hàng — để biết "lấy hàng mất bao lâu" không cần đo lại mỗi lần.

---

## 1. Các con số quan trọng (Latency Numbers)

```
Operation                          Time
─────────────────────────────────────────────
L1 cache reference                 0.5 ns
L2 cache reference                 7 ns
Main memory (RAM) reference        100 ns
SSD random read                    150 μs      (150,000 ns)
HDD seek                           10 ms       (10,000,000 ns)
Send 1 KB over 1 Gbps network     10 μs
Read 1 MB from SSD                 1 ms
Read 1 MB from HDD                 20 ms
Send packet CA → Netherlands → CA  150 ms
```

**Key takeaways:**
- RAM nhanh hơn SSD ~1000x, SSD nhanh hơn HDD ~100x
- Network roundtrip ~150ms (tối thiểu)
- → Cache mọi thứ có thể vào RAM

---

## 2. Data Structures cho System Design

| Structure | Dùng trong | Ứng dụng |
|-----------|-----------|---------|
| **Hash Table** | Cache, DB index | O(1) lookup |
| **B-Tree / B+Tree** | Database indexing | Range queries |
| **Bloom Filter** | Membership test | "URL đã crawl chưa?" |
| **Consistent Hashing** | Distributed systems | Phân chia data evenly |
| **Trie** | Prefix search | Autocomplete |
| **Skip List** | Sorted data (Redis) | Range queries, O(log n) |
| **Merkle Tree** | Data integrity | Blockchain, sync |
| **HyperLogLog** | Cardinality estimation | Đếm unique visitors |

### Bloom Filter
```
Kiểm tra "phần tử có TRONG tập không?" — probabilistic
- "Có" → có thể đúng (false positive possible)
- "Không" → CHẮC CHẮN không (no false negative)

Dùng: kiểm tra URL đã crawl, email đã tồn tại, cache check
Space: cực kỳ nhỏ (vài MB cho hàng tỷ phần tử)
```

### Consistent Hashing
```
Vấn đề: hash(key) % N servers → thêm/bớt server → rehash TẤT CẢ keys
Giải pháp: Consistent Hashing ring → chỉ rehash ~1/N keys

Dùng: DynamoDB, Cassandra, CDN routing, load balancing
```

---

## 3. Back-of-the-Envelope Estimation

### 3.1 Estimation Framework
```
1. Estimate DAU (Daily Active Users)
2. Calculate QPS (Queries Per Second)
   QPS = DAU × queries_per_user / 86400
   Peak QPS ≈ 2–5 × average QPS
3. Calculate Storage
4. Calculate Bandwidth
```

### 3.2 Ví dụ: Estimate cho Twitter
```
Assumptions:
- 300M MAU, 50% DAU = 150M DAU
- Mỗi user xem feed 5 lần/ngày, mỗi lần load 20 tweets
- 10% users tweet 1 tweet/ngày

QPS (Read):
  150M × 5 × 20 / 86400 ≈ 175K tweets read/sec
  Peak: ~500K/sec

QPS (Write):
  15M tweets / 86400 ≈ 175 tweets/sec
  → Read-heavy system!

Storage (1 year):
  15M tweets/day × 365 days = 5.5B tweets/year
  Mỗi tweet: ~300 bytes text + 1KB metadata ≈ 1.3KB
  Text storage: 5.5B × 1.3KB ≈ 7.15TB/year
  
  Media (20% tweets có ảnh, mỗi ảnh ~500KB):
  1.1B × 500KB = 550TB/year

Bandwidth:
  Read: 500K tweets/sec × 1.3KB = 650MB/s (text only)
  + Media: significant
```

### 3.3 Powers of 2 — Quick Reference
```
2^10 = 1 Thousand (KB)
2^20 = 1 Million (MB)
2^30 = 1 Billion (GB)
2^40 = 1 Trillion (TB)
2^50 = 1 Quadrillion (PB)
```

---

## 📝 Bài tập

1. Estimate cho YouTube: storage, bandwidth, QPS
2. Estimate cho WhatsApp: messages/sec, storage cho 1 năm
3. Giải thích khi nào dùng Bloom Filter vs Hash Table
4. Vẽ Consistent Hashing ring cho 5 servers, 3 virtual nodes mỗi server

---

## 📚 Tài liệu
- *System Design Interview Vol. 1* — Alex Xu (Ch. 2: Estimation)
- *Jeff Dean's Numbers Every Programmer Should Know*
- *donnemartin/system-design-primer* (GitHub)
