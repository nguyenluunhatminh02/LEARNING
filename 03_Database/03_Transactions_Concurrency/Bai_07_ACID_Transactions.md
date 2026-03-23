# Bài 07: ACID & Transactions

## 🎯 Mục tiêu

- Hiểu ACID properties
- Transaction isolation levels
- Deadlocks — detect & prevent
- Practical transaction patterns

---

## 📖 Câu chuyện đời thường

> Bạn chuyển tiền từ tài khoản A sang B. **Atomicity** = hoặc cả 2 việc thành công (A trừ, B cộng) hoặc không việc nào xảy ra — không có chuyện A mất tiền mà B chưa nhận. **Consistency** = số dư không bao giờ âm (luật của ngân hàng). **Isolation** = 2 người chuyển tiền cùng lúc không bị xung đột, giống 2 người ở 2 quầy giao dịch không thấy nhau. **Durability** = khi ngân hàng nói "thành công" thì dù mất điện, tiền vẫn ở đó. **Deadlock** giống 2 xe trong hẻ nhỏ đối đầu: không ai chịu lùi → kẹt cả 2.

---

## 1. ACID Properties

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

### Basic Transaction Structure

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

### SAVEPOINT (Nested Transactions)

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
|-------|------------|---------------------|--------------|
| Read Uncommitted | ❌ possible | ❌ possible | ❌ possible |
| Read Committed ⭐ | ✅ prevented | ❌ possible | ❌ possible |
| Repeatable Read | ✅ prevented | ✅ prevented | ❌ possible* |
| Serializable | ✅ prevented | ✅ prevented | ✅ prevented |

### Isolation Level Examples

```sql
-- PostgreSQL default: Read Committed
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
SELECT * FROM products WHERE id = 1;  -- price = 100
-- Another transaction updates price to 200 and commits
SELECT * FROM products WHERE id = 1;  -- STILL price = 100 (snapshot)
COMMIT;
```

### Detailed Isolation Explanations

#### 1. Dirty Read (Đọc dữ liệu "rác" / Đọc tin đồn)

**Tình huống:** Bạn hỏi nhân viên cửa hàng: "iPhone 15 giá bao nhiêu?". Cùng lúc đó, ông Quản lý đang ngồi trong phòng gõ máy tính, định giảm giá từ 20 triệu xuống 18 triệu (đang gõ nháp, chưa bấm nút Lưu/Commit).

Nhân viên nhìn lén màn hình quản lý và báo bạn: "Dạ 18 triệu".

Tuy nhiên, 1 phút sau quản lý đổi ý, không giảm giá nữa và ấn Hủy (Rollback).

**Hậu quả:** Bạn ra quầy thanh toán đưa 18 triệu nhưng hệ thống thu ngân báo giá 20 triệu. Bạn đã bị lừa bởi một dữ liệu chưa chính thức.

**Cách khắc phục:** Nâng mức Isolation lên Read Committed (Nhân viên chỉ được phép báo giá khi thông báo đã có dấu mộc đỏ/đã ấn Lưu).

---

#### 2. Non-repeatable Read (Đọc trước sau bất nhất)

**Tình huống:** Bạn vừa bước vào cửa hàng, xem bảng giá thấy iPhone 15 giá 18 triệu (Lần đọc 1). Bạn nói: "Để em ra ghế đá ngồi suy nghĩ chút".

Trong lúc bạn ra ngoài, quản lý chính thức quyết định tăng giá lên 20 triệu và đã dán bảng giá mới lên tường (Đã Commit).

Bạn quay lại, nhìn lên tường lần nữa để quyết định mua (Lần đọc 2), thì ngỡ ngàng thấy giá đã là 20 triệu. Trong cùng một buổi đi mua sắm (1 Transaction), bạn đọc giá 2 lần nhưng ra 2 kết quả khác nhau do có người khác xen vào cập nhật.

**Cách khắc phục:** Nâng mức Isolation lên Repeatable Read (Cửa hàng cam kết: Giá bạn thấy lúc bước qua cửa sẽ được "đóng băng" giữ nguyên cho riêng bạn cho đến khi bạn ra về, dù thị trường có biến động thế nào).

---

#### 3. Phantom Read (Bóng ma xuất hiện)

**Tình huống:** Cửa hàng đang áp dụng chính sách "Đóng băng giá" (Repeatable Read) ở trên, bạn rất an tâm. Bạn đi một vòng và đếm trên kệ thấy có đúng 5 chiếc iPhone 15 màu hồng. Bạn quay mặt đi để lấy ví tiền.

Trong tích tắc đó, nhân viên kho vừa bê từ trong kho ra thêm 2 chiếc mới tinh và xếp lên kệ (Hành động Insert thêm dòng mới).

Bạn quay mặt lại đếm lần nữa để gom hàng thì ủa, sao biến thành 7 chiếc. Số lượng 5 chiếc cũ không bị ai lấy đi, giá không đổi, nhưng có 2 chiếc "bóng ma" tự nhiên xuất hiện thêm.

**Cách khắc phục:** Nâng mức Isolation lên Serializable.

---

### Tổng kết 4 mức độ Isolation (Từ yếu đến mạnh)

Dựa vào câu chuyện mua hàng trên, ta có thể tóm tắt 4 mức độ của Database:

- **Read Uncommitted (Dễ dãi nhất):** Ai đang gõ nháp cái gì cũng đọc được. Rất nhanh nhưng dễ ăn quả lừa (bị Dirty Read).

- **Read Committed (Chỉ tin đồ chính thức):** Chỉ đọc dữ liệu người ta đã nhấn "Lưu". Khắc phục được tin đồn nhảm, nhưng dữ liệu có thể bị ai đó thay đổi giữa chừng lúc mình đang làm việc.

- **Repeatable Read (Chụp ảnh màn hình):** Lúc bắt đầu công việc, Database tự động "chụp" lại một bản sao dữ liệu (Snapshot) cho riêng bạn. Mọi thay đổi của người khác bạn không quan tâm. Cực kỳ ổn định cho các bài toán tính toán, báo cáo tài chính.

- **Serializable (Đóng cửa tiệm, xếp hàng 1-1):** Phục vụ từng khách một. Bạn bước vào cửa hàng là người ta khóa trái cửa lại, nhân viên kho cũng không được mang thêm hàng ra. Bạn mua xong đi về thì khách thứ 2 mới được vào. Tuyệt đối an toàn không sai 1 li, nhưng hệ thống sẽ cực kỳ chậm nếu có đông người sử dụng.

---

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

### Deadlock Example

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

---

### 🎬 Vở kịch đời thường: Kẹt xe ở hẻm 123

Tưởng tượng có một con hẻm nhỏ rất hẹp, chỉ vừa khít cho một chiếc ô tô đi qua.

**Buổi sáng:** Chiếc Xe Xanh đi từ đầu hẻm đi vào (chiếm nửa đầu hẻm).

**Cùng lúc đó:** Chiếc Xe Đỏ đi từ cuối hẻm đi ngược lại (chiếm nửa cuối hẻm).

**Chạm trán ở giữa hẻm:**

- Xe Xanh bóp còi: "Anh lùi lại nhường đường cho tôi đi tới!"
- Xe Đỏ bật pha chớp chớp: "Không, tôi vào trước, anh lùi lại cho tôi đi!"

**Kết quả:** Không ai chịu nhường ai. Cả hai tài xế tắt máy, khóa cửa xe đi ăn phở. Con hẻm bị tê liệt hoàn toàn. Đây chính là DEADLOCK!

---

### 💻 Dịch sang ngôn ngữ Database

Bây giờ, hãy đối chiếu câu chuyện trên vào hệ thống cơ sở dữ liệu của bạn:

- **Chiếc xe (Tài xế):** Chính là các Transactions (Transaction A và Transaction B).
- **Đoạn đường xe đang đứng:** Là Dòng dữ liệu (Row) đã bị khóa (LOCKED).
- **Hành động bóp còi đòi đi tới:** Là trạng thái WAITING (chờ đợi Database nhả khóa của dòng dữ liệu tiếp theo).

**Ví dụ thực tế trong code (Hệ thống chuyển tiền):**

- **Xe Xanh (Transaction A):** Đang trừ tiền tài khoản của Alice (đã Lock Alice) và chuẩn bị cộng tiền cho Bob.
- **Xe Đỏ (Transaction B):** Cùng lúc đó, lại đang trừ tiền của Bob (đã Lock Bob) và chuẩn bị cộng tiền cho Alice.

**Đụng độ:** Transaction A chờ Bob mở khóa, còn Transaction B thì chờ Alice mở khóa. Cả 2 treo vĩnh viễn!

---

### 👮‍♂️ Công an xuất hiện (Cách Database xử lý Deadlock)

Database (như PostgreSQL hay MySQL) rất thông minh, nó có một anh "Cảnh sát giao thông" chuyên đi tuần tra (Deadlock Detector).

Khi anh cảnh sát phát hiện 2 xe đứng nhìn nhau quá lâu, anh ấy sẽ làm gì?

Anh ấy không thể khuyên răn. Anh ấy sẽ rút gậy ra, chỉ định bắt buộc 1 chiếc xe phải lùi lại (thường là chiếc xe nhỏ hơn hoặc transaction nào tốn ít công sức hơn).

Trong Database, cảnh sát sẽ "Kill" (giết) Transaction B và văng ra lỗi khét lẹt:

```
ERROR: deadlock detected
```

Transaction B bị ép Rollback (hủy bỏ mọi thứ, hoàn tiền).

Lúc này, đường đã quang, Xe Xanh (Transaction A) vui vẻ đi tiếp và Commit thành công.

Xe Đỏ sau khi lùi ra ngoài, sẽ phải tự đề máy đi lại từ đầu (Retry transaction).

---

### 🛑 Cách lập trình viên ngăn chặn kẹt xe (Prevention)

Để cảnh sát không phải ra mặt (vì rất tốn tài nguyên hệ thống), lập trình viên thiết kế ra luật giao thông mới:

#### Giải pháp: Quy tắc "Đường một chiều" (Consistent Ordering)

Luật mới ghi rõ: Bất kể ai muốn mượn hẻm, đều phải đi từ hướng từ Đông sang Tây. Hoặc trong Database: "Luôn phải ưu tiên Lock tài khoản có ID nhỏ trước, ID lớn sau".

Áp dụng vào 2 xe: Dù ai muốn chuyển tiền cho ai, hệ thống ngầm bắt buộc phải khóa tài khoản Alice (ID 1) trước, rồi mới được khóa Bob (ID 2).

- Xe Xanh tới trước, khóa Alice.
- Xe Đỏ tới sau, muốn khóa Bob nhưng luật bắt khóa Alice trước.
- Do Alice đang bị Xe Xanh giữ, Xe Đỏ đành phải đứng ngoan ngoãn chờ ở ngoài hẻm.
- Xe Xanh đi qua trót lọt trọn vẹn. Sau đó Xe Đỏ mới được vào.

**Kẹt xe biến mất hoàn toàn!**

---

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

### Optimistic Locking (Versioning)

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

NYC Taxi Trip Data (Dữ liệu chuyến xe Taxi New York)
Đây là bộ dữ liệu "quốc dân" được giới Data Engineer và Database Admin dùng nhiều nhất để test hiệu năng hệ thống. Nó ghi lại từng chuyến xe taxi ở New York.

Quy mô: Khoảng 30 - 40 triệu dòng / năm (bạn có thể tải dữ liệu của 1 tháng là được khoảng 3 triệu dòng). File tải về định dạng CSV hoặc Parquet.

Cực kỳ phù hợp để test:

BRIN Index: Vì dữ liệu có tính chất chuỗi thời gian (time-series) tăng dần theo cột tpep_pickup_datetime (thời gian đón khách). Đánh BRIN index ở đây siêu nhỏ mà cực nhanh.

GiST Index: Tìm chuyến xe theo bán kính tọa độ địa lý (điểm đón/điểm trả).

B-Tree & Composite Index: Truy vấn các chuyến xe có passenger_count > 2 và fare_amount < 20.
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

2. eCommerce behavior data (Hành vi người dùng E-commerce)
Nếu bạn muốn thực hành bám sát vào ví dụ E-commerce trong file Bai_05_Indexing_Deep_Dive.md của bạn, đây là bộ dữ liệu hoàn hảo. Nó log lại các hành vi view, cart, purchase của người dùng trên một trang thương mại điện tử lớn.

Quy mô: Khoảng 42 triệu dòng (dung lượng cỡ vài GB).

Cực kỳ phù hợp để test:

Partial Index: Đánh index riêng cho những dòng có event_type = 'purchase' (vì lượng người mua luôn ít hơn lượng người xem).

Composite Index: Lọc dữ liệu theo (user_id, event_type) để xem lịch sử mua hàng của một khách cụ thể.

Link tải: Kaggle - eCommerce behavior data (Cần tạo tài khoản Kaggle miễn phí để tải).https://www.kaggle.com/datasets/mkechinov/ecommerce-behavior-data-from-multi-category-store

3. Amazon Product Reviews
Bộ dữ liệu chứa các đánh giá (review) thực tế của khách hàng trên Amazon.

Quy mô: Lên tới hơn 130 triệu dòng (nhưng họ chia theo từng Category, bạn có thể tải riêng mục "Electronics" hoặc "Books" cỡ 2 - 5 triệu dòng cho nhẹ máy).

Cực kỳ phù hợp để test:

GIN Index (Full-text Search): Sử dụng hàm to_tsvector để tìm kiếm các từ khóa đặc biệt nằm sâu trong nội dung đánh giá (reviewText).

Covering Index (INCLUDE): Lấy ra summary và overall (số sao) của các review mà không cần đọc lại bảng gốc.

Link tải: Amazon Reviews Data (Jianmo Ni) https://cseweb.ucsd.edu/~jmcauley/datasets/amazon_v2/