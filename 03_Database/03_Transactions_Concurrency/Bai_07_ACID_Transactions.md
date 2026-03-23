# Bài 07: ACID & Transactions

## 🎯 Mục tiêu
- Hiểu ACID properties
- Transaction isolation levels
- Deadlocks — detect & prevent
- Practical transaction patterns

## 📖 Câu chuyện đời thường
> Bạn chuyển tiền từ tài khoản A sang B. **Atomicity** = hoặc cả 2 việc thành công (A trừ, B cộng) hoặc không việc nào xảy ra — không có chuyện A mất tiền mà B chưa nhận. **Consistency** = số dư không bao giờ âm (luật của ngân hàng). **Isolation** = 2 người chuyển tiền cùng lúc không bị xung đột, giống 2 người ở 2 quầy giao dịch không thấy nhau. **Durability** = khi ngân hàng nói "thành công" thì dù mất điện, tiền vẫn ở đó. **Deadlock** giống 2 xe trong hẻ nhỏ đối đầu: không ai chịu lùi → kẹt cả 2.

---

## 1. ACID

```
A — Atomicity:  Transaction = all or nothing
    Chuyển tiền: trừ A + cộng B → cả 2 thành công hoặc cả 2 rollback

C — Consistency: Data luôn valid (constraints, rules)
    Balance >= 0, email unique, FK references valid

I — Isolation:  Concurrent transactions không ảnh hưởng nhau
    2 users mua cùng sản phẩm → không bán quá stock

D — Durability: Committed data không mất dù server crash
    WAL → fsync → data on disk
```

---

## 2. Transaction Basics

```sql
BEGIN;  -- Start transaction

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Check: nếu balance < 0 → rollback
-- Hoặc: dùng CHECK constraint
COMMIT;  -- Persist changes

-- Nếu có lỗi:
ROLLBACK;  -- Undo tất cả changes trong transaction
```

### SAVEPOINT (nested transactions)
```sql
BEGIN;
INSERT INTO orders (user_id, total) VALUES (1, 100);

SAVEPOINT sp1;
INSERT INTO order_items (order_id, product_id) VALUES (1, 999);
-- Oops, product 999 doesn't exist → error

ROLLBACK TO SAVEPOINT sp1;  -- Chỉ rollback order_items, giữ orders
INSERT INTO order_items (order_id, product_id) VALUES (1, 1);  -- Retry

COMMIT;
```

---

## 3. Isolation Levels

### Concurrency Problems
```
Dirty Read:     Đọc data chưa committed (uncommitted changes)
Non-repeatable Read: Đọc 2 lần, kết quả khác (row modified by another tx)
Phantom Read:   Đọc 2 lần, số rows khác (rows added/deleted by another tx)
```

### 4 Isolation Levels (SQL Standard)

| Level | Dirty Read | Non-repeatable Read | Phantom Read |
|---|---|---|---|
| Read Uncommitted | ❌ possible | ❌ possible | ❌ possible |
| Read Committed ⭐ | ✅ prevented | ❌ possible | ❌ possible |
| Repeatable Read | ✅ prevented | ✅ prevented | ❌ possible* |
| Serializable | ✅ prevented | ✅ prevented | ✅ prevented |

```sql
-- PostgreSQL default: Read Committed
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
SELECT * FROM products WHERE id = 1;  -- price = 100
-- Another transaction updates price to 200 and commits
SELECT * FROM products WHERE id = 1;  -- STILL price = 100 (snapshot)
COMMIT;
```

### Practical Isolation Choice
```
Read Committed (default):
  ✅ Mỗi statement thấy latest committed data
  ✅ Good for most OLTP applications
  ❌ Không bảo đảm consistent view across statements

Repeatable Read:
  ✅ Transaction thấy snapshot tại thời điểm BEGIN
  ✅ Consistent reads within transaction
  ❌ Serialization errors → phải retry

Serializable:
  ✅ Full isolation — như chạy tuần tự
  ❌ Performance impact, frequent retries
  Use: financial transactions, inventory management
```

---

## 4. Deadlocks

```
Transaction A:                Transaction B:
  UPDATE accounts SET ...     
  WHERE id = 1;  (lock row 1)
                                UPDATE accounts SET ...
                                WHERE id = 2;  (lock row 2)
  UPDATE accounts SET ...     
  WHERE id = 2;  (WAIT for B)
                                UPDATE accounts SET ...
                                WHERE id = 1;  (WAIT for A)
  
  → DEADLOCK! Both waiting for each other
  → PostgreSQL detects → kills one transaction
```

### Prevention Strategies
```sql
-- Strategy 1: Lock in consistent order
-- Luôn lock id nhỏ trước → id lớn sau
BEGIN;
SELECT * FROM accounts WHERE id IN (1, 2) ORDER BY id FOR UPDATE;
-- Row 1 locked, then Row 2 locked → no deadlock possible
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Strategy 2: Lock timeout
SET lock_timeout = '5s';  -- Fail fast thay vì wait forever

-- Strategy 3: Advisory locks
SELECT pg_advisory_lock(hashtext('transfer_1_2'));
-- ... do work ...
SELECT pg_advisory_unlock(hashtext('transfer_1_2'));
```

---

## 5. Practical Patterns

### Optimistic Locking (versioning)
```sql
-- Dùng version column thay vì lock
-- Good cho read-heavy, low-contention scenarios

-- Read
SELECT id, name, price, version FROM products WHERE id = 1;
-- → price=100, version=5

-- Update (check version)
UPDATE products 
SET price = 120, version = version + 1
WHERE id = 1 AND version = 5;
-- If affected_rows = 0 → another transaction modified → retry

-- Application code:
-- if result.rowcount == 0:
--     raise ConcurrentModificationError("Retry transaction")
```

### Pessimistic Locking (SELECT FOR UPDATE)
```sql
-- Lock row explicitly → prevent others from modifying
BEGIN;
SELECT * FROM inventory WHERE product_id = 1 FOR UPDATE;
-- Row is locked until COMMIT/ROLLBACK

-- Check stock and decrement
-- If stock >= quantity_ordered:
UPDATE inventory SET stock = stock - 1 WHERE product_id = 1;
COMMIT;

-- Variations:
FOR UPDATE NOWAIT;        -- Fail immediately if locked
FOR UPDATE SKIP LOCKED;   -- Skip locked rows (queue processing)
```

---

## 📝 Bài tập

1. Implement money transfer đảm bảo ACID
2. Demo dirty read vs repeatable read scenario
3. Tạo deadlock, sau đó fix bằng consistent ordering
4. Implement optimistic locking cho product update

---

## 📚 Tài liệu
- *Designing Data-Intensive Applications* — Kleppmann (Ch.7)
- [PostgreSQL Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html)
