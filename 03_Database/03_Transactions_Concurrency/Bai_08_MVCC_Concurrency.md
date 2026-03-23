# Bài 08: MVCC & Concurrency Control

## 🎯 Mục tiêu

- MVCC (Multi-Version Concurrency Control)
- PostgreSQL MVCC implementation
- VACUUM & bloat
- Lock types

---

## 📖 Câu chuyện đời thường

> Bạn làm việc trên Google Docs cùng đồng nghiệp. **MVCC** giống như mỗi người được nhìn thấy một "phiên bản tại thời điểm họ mở file" — dù người khác đang sửa, bạn vẫn đọc được phiên bản cũ mà không bị chặn. PostgreSQL không xóa data cũ ngay mà giữ lại nhiều phiên bản. Vấn đề: phiên bản cũ chất đống như giấy vụn chưa vứt (**bloat**). **VACUUM** giống người dọn vệ sinh văn phòng — gốm giấy cũ đi. Nếu không dọn thường xuyên, văn phòng ngày càng chật và chậm. **Lock** giống biển "do not disturb" trên phòng khách sạn: "tôi đang sửa dòng này, xin chờ".

---

## 1. MVCC — Multi-Version Concurrency Control

### 🎬 Kịch bản: Quán phở muốn tăng giá

Giả sử Phở bò đang có giá là 40.000đ. Hôm nay thịt bò lên giá, bà Ba (chủ quán) quyết định tăng giá lên 50.000đ.

#### 1. Nếu KHÔNG CÓ MVCC (Dùng Lock - Khóa truyền thống)

Bà Ba cầm bút xóa ra giữa quán và hô to: "Tất cả dừng lại! Không ai được nhìn menu hay gọi món nữa!".

Bà chạy đến từng bàn, giật lại cuốn menu mà khách đang cầm trên tay (Lock).

Bà cặm cụi dùng bút xóa bôi số 40k, viết đè số 50k lên. Đợi mực khô xong, bà mới trả lại menu cho khách.

**Hậu quả:** Trong lúc bà Ba sửa giá (Writer), tất cả khách hàng (Readers) phải ngồi ngáp ruồi chờ đợi. Hệ thống bị treo, trải nghiệm cực kỳ tệ. (Writer block Reader).

---

#### 2. Nếu CÓ MVCC (Đa phiên bản - Cách Database hiện đại làm)

Bà Ba thông minh hơn, bà áp dụng nguyên lý MVCC:

Bà vào trong quầy, âm thầm in một xấp menu MỚI tinh với giá Phở 50.000đ. Menu cũ (40k) bà KHÔNG hề lấy bút xóa sửa đè lên.

- **Với khách cũ (Anh A):** Anh A vào quán từ sớm và đang cầm cuốn menu 40k. Bà Ba cứ để yên cho anh A xem và gọi món với giá 40k. (Hệ thống tạo một Snapshot - ảnh chụp thời điểm anh A bước vào).
- **Với khách mới (Chị B):** Chị B vừa bước qua cửa, nhân viên lập tức phát cho chị cuốn menu MỚI giá 50k. Chị B sẽ gọi món theo giá mới.

**Kết quả:** Quán phở vẫn hoạt động trơn tru. Bà Ba cứ việc cập nhật giá (Write), khách cứ việc xem giá (Read). Không ai phải chờ ai! (Writer NEVER blocks Reader, Reader NEVER blocks Writer).

---

### 💻 Áp chiếu vào ngôn ngữ Database

Từ câu chuyện trên, chúng ta rút ra các thuật ngữ cốt lõi của MVCC trong PostgreSQL:

#### Tạo phiên bản mới thay vì ghi đè (Multi-Version)

Khi bạn chạy lệnh `UPDATE price = 50`, Database không sửa trực tiếp vào dòng cũ. Nó gạch bỏ (đánh dấu) dòng cũ là đã hết hạn, và TẠO RA MỘT DÒNG HOÀN TOÀN MỚI mang giá trị 50. Lúc này trong ổ cứng tồn tại song song 2 phiên bản của cùng 1 tô phở.

#### Tính cô lập (Snapshot Isolation)

Anh A bước vào quán lúc nào thì sẽ chốt với bảng giá của lúc đó. Trong Database, mỗi Transaction khi BEGIN sẽ được cấp một "bức ảnh chụp" toàn bộ dữ liệu ngay khoảnh khắc đó. Những biến động xảy ra sau đó bởi người khác sẽ bị "tàng hình" đối với Transaction này.

#### Cô lao công dọn rác (VACUUM)

Khi anh khách A (người cuối cùng cầm cuốn menu 40k) ăn xong và tính tiền ra về. Cuốn menu 40k bị bỏ lại trên bàn và chính thức vô dụng (không còn Transaction nào cần đọc nó nữa). Lúc này, Database sẽ cử một tiến trình ngầm tên là Autovacuum đi thu gom những "cuốn menu cũ" này ném vào thùng rác, trả lại dung lượng cho ổ cứng (chống Bloat).

---

### MVCC Technical Details

```
Problem: Readers block writers, writers block readers → low concurrency
Solution: MVCC — keep multiple versions of each row

Rule: Readers NEVER block writers, writers NEVER block readers!

Mỗi row có hidden columns:
  xmin: Transaction ID that inserted this row
  xmax: Transaction ID that deleted/updated this row (0 = still valid)

INSERT id=1 (xid=100):
  → (xmin=100, xmax=0, id=1, name='Alice')

UPDATE name='Bob' (xid=200):
  → (xmin=100, xmax=200, id=1, name='Alice')  ← old version (dead)
  → (xmin=200, xmax=0,   id=1, name='Bob')    ← new version (live)

DELETE (xid=300):
  → (xmin=200, xmax=300, id=1, name='Bob')    ← marked as dead
```

---

### Snapshot Isolation

```
Transaction 500 starts:
  → Takes snapshot: "I can see rows where xmin < 500 AND committed"
  → Cannot see rows with xmin ≥ 500 (future transactions)
  → Cannot see rows with xmax < 500 AND committed (deleted)

Tx 500 reads table:
  (xmin=100, xmax=200) → xmax committed & < 500 → INVISIBLE (deleted)
  (xmin=200, xmax=0)   → xmin committed & < 500 → VISIBLE ✅
  (xmin=501, xmax=0)   → xmin > 500 → INVISIBLE (future)
```

---

## 2. VACUUM — Cleanup Dead Tuples

### 🎬 Kịch bản: Bãi rác Menu trong quán phở

Nhờ áp dụng MVCC, quán phở của bà Ba hoạt động rất trơn tru. Mỗi khi đổi giá món ăn (ví dụ: Phở 40k lên 50k, Trà đá 2k lên 5k), bà không giật lại menu của khách đang ăn, mà chỉ in menu mới cho khách vào sau.

Nhưng một tuần trôi qua, một vấn đề lớn xuất hiện:

#### Vấn đề (Dead Tuples)

Những vị khách cầm menu cũ (40k) sau khi ăn xong đã đi về. Tuy nhiên, cuốn menu cũ đó vẫn nằm chỏng chơ trên bàn. Không ai dọn nó đi cả!

#### Hậu quả (Table Bloat - Trương phình dữ liệu)

Càng ngày, bà Ba càng update nhiều món. Lượng menu cũ hết hạn (giấy vụn) chất thành đống trên bàn, dưới sàn nhà. Khách mới bước vào không còn chỗ để ngồi, quán phở rộng 100m2 nhưng ngập ngụa trong rác.

Trong Database, ổ cứng của bạn y hệt như quán phở này. Dù dữ liệu thực tế (menu đang dùng) chỉ có 1GB, nhưng file cơ sở dữ liệu lại phình to lên tận 10GB vì chứa toàn rác (những dòng dữ liệu cũ đã bị update/delete).

---

### 🧹 Vị cứu tinh: Cô lao công VACUUM

Để giải quyết đống rác này, bà Ba quyết định thuê một cô lao công tên là VACUUM (Tiếng Anh nghĩa là máy hút bụi).

Cô lao công này hoạt động như sau:

- **Đi tuần tra:** Cô đi quanh quán và chỉ nhìn vào những cuốn menu cũ.
- **Kiểm tra an toàn:** Cô sẽ hỏi một câu cực kỳ quan trọng: "Có vị khách nào (Transaction) trong quán CÒN ĐANG dùng cuốn menu cũ này không?"
- **Dọn dẹp:** Nếu vẫn còn người đang ăn và xem menu đó → Cô để yên (MVCC). Nhưng nếu người khách cuối cùng dùng menu đó đã ra về → Cô lập tức hốt cuốn menu quăng vào thùng rác.
- **Tái sử dụng (Reusable Space):** Chỗ trống mà cuốn menu cũ vừa để lại trên bàn sẽ được cô đánh dấu là "Bàn trống". Khi bà Ba in menu mới, bà sẽ đặt đúng vào cái chỗ trống đó thay vì phải mua thêm bàn mới (không tốn thêm dung lượng ổ cứng).

**Lưu ý:** PostgreSQL rất thông minh, nó có một tính năng gọi là Autovacuum – tức là cô lao công này được lập trình để tự động đi dọn rác ngầm mỗi khi rác đến một mức độ nhất định, bạn không cần phải tự tay gọi cô ấy.

---

### 🛑 Trùm cuối: VACUUM FULL (Tổng vệ sinh cuối năm)

Đôi khi, quán phở quá bừa bộn. Rác nằm xen kẽ với chỗ khách ngồi lởm chởm. Dù cô lao công có dọn đi những cuốn menu, các khoảng trống bị vỡ vụn (phân mảnh) khiến bà Ba không thể kê thêm một cái bàn lớn nào vào được.

Lúc này, bà Ba đành phải dùng tuyệt chiêu VACUUM FULL:

- Bà treo biển "ĐÓNG CỬA TỔNG VỆ SINH" (Lock Table).
- Bà đuổi tất cả khách ra ngoài, không cho ai vào ăn, không cho ai gọi món (Block toàn bộ các lệnh SELECT, INSERT, UPDATE).
- Bà gom toàn bộ bàn ghế, menu mới xếp lại gọn gàng tắp lự vào một góc. Quán trở nên rộng rãi y như lúc mới khai trương (Thu hồi lại toàn bộ dung lượng ổ cứng về mức tối ưu nhất).

**Hậu quả:** Ứng dụng của bạn sẽ bị "chết đứng" trong suốt quá trình chạy VACUUM FULL. Do đó, người ta rất hiếm khi chạy lệnh này trên hệ thống đang hoạt động (Production), mà thường dùng các công cụ dọn rác online không cần khóa cửa như pg_repack.

---

### 💻 Tóm tắt lại bằng ngôn ngữ Database

- **Dead Tuples:** Là những dòng dữ liệu cũ (bản nháp) sinh ra do lệnh UPDATE hoặc DELETE, hiện tại không còn giao dịch (Transaction) nào cần đọc nó nữa.
- **Table Bloat:** Hiện tượng bảng dữ liệu phình to chiếm hết ổ cứng do chứa quá nhiều Dead Tuples.
- **VACUUM:** Lệnh dọn dẹp Dead Tuples, biến không gian đó thành khoảng trống để các lệnh INSERT/UPDATE sau này ghi đè lên (Không trả lại dung lượng cho hệ điều hành, nhưng ngăn database phình to thêm).
- **VACUUM FULL:** Lệnh nén và sắp xếp lại toàn bộ dữ liệu, trả lại dung lượng ổ cứng cho hệ điều hành. Tuy nhiên, nó sẽ khóa chết bảng (Lock) cho đến khi chạy xong.

---

### VACUUM Technical Details

```
MVCC creates dead tuples (old versions)
Without VACUUM → table grows forever (bloat)

VACUUM does:
1. Mark dead tuples as reusable space
2. Update visibility map
3. Update free space map
4. Freeze old transaction IDs (prevent wraparound)

VACUUM FULL:
  Rewrites entire table → reclaims disk space
  ❌ LOCKS TABLE (exclusive access required)
  → Dùng pg_repack thay thế (online, no lock)
```

---

### Monitoring Dead Tuples

```sql
-- Check dead tuples
SELECT 
    relname AS table,
    n_dead_tup AS dead_tuples,
    n_live_tup AS live_tuples,
    ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
    last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Autovacuum config
autovacuum = on
autovacuum_vacuum_threshold = 50         -- min dead tuples before vacuum
autovacuum_vacuum_scale_factor = 0.1     -- vacuum when 10% dead tuples
autovacuum_analyze_threshold = 50
autovacuum_analyze_scale_factor = 0.05
```

---

### Table Bloat

```sql
-- Check bloat ratio
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(tablename::regclass)) AS total_size,
    pg_size_pretty(pg_relation_size(tablename::regclass)) AS table_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename::regclass) DESC;

-- Fix bloat without locking (pg_repack extension)
-- pg_repack --table=orders --jobs=4 mydb
```

---

## 3. Lock Types

### Table-Level Locks

```
ACCESS SHARE          → SELECT (weakest, compatible with most)
ROW SHARE             → SELECT FOR UPDATE
ROW EXCLUSIVE         → INSERT, UPDATE, DELETE
SHARE                 → CREATE INDEX (blocks writes)
EXCLUSIVE             → VACUUM FULL, some ALTER TABLE
ACCESS EXCLUSIVE      → DROP TABLE, ALTER TABLE (strongest, blocks all)

Compatibility matrix:
  SELECT + SELECT = OK ✅
  SELECT + INSERT = OK ✅ (MVCC!)
  INSERT + INSERT = OK ✅ (different rows)
  UPDATE same row = WAIT (row-level lock)
  DDL + anything = WAIT
```

---

### Row-Level Locks

```sql
-- FOR UPDATE: exclusive lock on selected rows
SELECT * FROM products WHERE id = 1 FOR UPDATE;

-- FOR SHARE: shared lock (others can read, not modify)
SELECT * FROM products WHERE id = 1 FOR SHARE;

-- FOR UPDATE SKIP LOCKED: job queue pattern
-- Worker 1 and Worker 2 both try to get tasks:
BEGIN;
SELECT * FROM tasks 
WHERE status = 'pending' 
ORDER BY created_at 
LIMIT 1 
FOR UPDATE SKIP LOCKED;
-- Each worker gets a DIFFERENT task (no contention!)
UPDATE tasks SET status = 'processing' WHERE id = ?;
COMMIT;
```

---

## 4. Transaction ID Wraparound

### 🎬 Kịch bản: Sự cố "Xuyên không" tại Phòng Khám

Giả sử phòng khám có một nguyên tắc làm việc (giống như MVCC) rất rõ ràng:

**Luật MVCC:** "Bác sĩ đang khám đến số hiện tại là bao nhiêu, thì chỉ những hồ sơ có số thứ tự nhỏ hơn hoặc bằng số hiện tại mới là hồ sơ hợp lệ (dữ liệu trong quá khứ). Những hồ sơ mang số lớn hơn là của bệnh nhân chưa tới lượt (dữ liệu của tương lai), tuyệt đối không được mở ra xem."

Chuyện gì sẽ xảy ra nếu máy phát số bị giới hạn?

Cái máy phát số của phòng khám chỉ in được tối đa 3 chữ số: từ 001 đến 999.

Buổi sáng, bệnh nhân số 005 vào khám, để lại hồ sơ lưu trữ bình thường. Hệ thống hiểu số 005 < số hiện tại, nên hồ sơ này hoàn toàn hợp lệ.

Phòng khám quá đông. Đến chiều tối, máy phát đến số 999. Lúc này bệnh nhân thứ 1000 bước qua cửa, cái máy không thể in số 1000 được nữa, nó quay vòng (wraparound) và phát ra tấm vé số 001.

Số hiện tại của phòng khám bị reset về 001.

---

### 💥 Thảm họa bùng nổ

Ngay khoảnh khắc số thứ tự quay về 001, hệ thống nhìn lại đống hồ sơ buổi sáng (số 005, số 999).

Nó đối chiếu với luật MVCC và tá hỏa: "Chết cha, hiện tại mới là số 001, tại sao lại có những hồ sơ mang số 005 hay 999 ở đây? Đây chắc chắn là dữ liệu của tương lai chưa hề tồn tại!"

**Hậu quả:** Hệ thống lập tức tàng hình (ẩn đi) toàn bộ hồ sơ của ngày hôm đó. Toàn bộ dữ liệu tự nhiên "bốc hơi" trắng xóa trên màn hình dù không ai bấm nút Delete!

---

### 💻 Áp chiếu vào PostgreSQL

Chuyện ở phòng khám y hệt như cách PostgreSQL hoạt động:

- **Máy phát số bị giới hạn:** PostgreSQL sử dụng số nguyên 32-bit để đánh mã Transaction ID (XID). Con số này chứa được tối đa khoảng 4,2 tỷ giao dịch. Khi xài hết 4,2 tỷ, nó sẽ quay vòng về số 0.
- **Luật 2 tỷ ranh giới:** PostgreSQL chia 4,2 tỷ ra làm đôi. Nó quy định: 2 tỷ ID nằm trước số hiện tại là "Quá khứ" (được phép đọc), 2 tỷ ID nằm sau số hiện tại là "Tương lai" (tàng hình).
- **Data Disappears (Mất dữ liệu):** Khi ID quay vòng vượt quá ranh giới 2 tỷ, những dữ liệu cũ (những bài viết, user, hóa đơn) được tạo ra từ rất lâu bỗng nhiên bị hệ thống lầm tưởng là "dữ liệu của tương lai". PostgreSQL sẽ ẩn chúng đi. Database của bạn bỗng nhiên trống trơn!

---

### 🦸‍♂️ Cách giải cứu: Đóng mộc "FROZEN" (VACUUM FREEZE)

Để thảm họa này không xảy ra, PostgreSQL có một cơ chế tuyệt đỉnh mang tên VACUUM FREEZE (Đóng băng).

Quay lại phòng khám:

Nhận thức được cái máy phát số bị lỗi, cô y tá trưởng (chính là tiến trình Autovacuum) sẽ rình lúc phòng khám vắng vẻ để đi tuần.

Cô lôi những hồ sơ đã khám xong từ lâu (ví dụ hồ sơ số 005) ra, lấy một con dấu đỏ chót đóng cái rầm lên dòng số thứ tự: "FROZEN" (ĐÃ ĐÓNG BĂNG).

Luật mới được ban hành: "Bất kể cái máy phát số đang nhảy ở số bao nhiêu, hễ hồ sơ nào có đóng mộc FROZEN thì hồ sơ đó được coi là cựu chiến binh, miễn nhiễm với thời gian và luôn luôn được phép hiển thị."

Trong Database, khi Autovacuum chạy, nó sẽ đổi Transaction ID của các dòng dữ liệu cũ thành một ID đặc biệt (FrozenTransactionId = 2). Mọi ID này luôn được hệ thống hiểu là "cũ hơn mọi ID khác", nên dữ liệu sẽ vĩnh viễn không bao giờ bị tàng hình.

---

### 🚨 Lưu ý "Sống còn" khi đi làm thực tế

PostgreSQL có cơ chế Autovacuum ngầm để tự đi "đóng mộc" Frozen. Nhưng nếu server của bạn có lưu lượng ghi (Write/Update) quá khủng khiếp, cô y tá Autovacuum dọn dẹp không kịp, ID sẽ tiến dần đến ngưỡng tử thần.

Nếu Transaction ID chạm mốc cách sự cố quay vòng 1 triệu ID, PostgreSQL sẽ tự động TẮT CẢ HỆ THỐNG (Shut down), từ chối mọi kết nối thêm/sửa/xóa để bảo vệ dữ liệu. Bạn sẽ phải có một đêm thức trắng để chạy lệnh VACUUM bằng tay.

---

### Transaction ID Wraparound Technical Details

```
PostgreSQL uses 32-bit transaction IDs → 4 billion
After 2 billion transactions → wraparound risk

If not vacuumed:
  Old data with txid=100 → after wraparound, 100 looks "future"
  → Data DISAPPEARS!

Prevention: VACUUM freezes old txids
  → Replace xmin with FrozenTransactionId
  → Autovacuum does this automatically
  → Monitor: age(datfrozenxid) should be < 1 billion

-- Check
SELECT datname, age(datfrozenxid) FROM pg_database ORDER BY age DESC;
-- If age > 1 billion → URGENT: manual VACUUM FREEZE
```

---

## 5. Connection Pooling (PgBouncer)

### 🎬 Kịch bản: Bờm mở quán lẩu nướng

#### 1. Thời kỳ đầu (Khi chưa có PgBouncer): Mô hình "1 kèm 1" tốn kém

Quán lẩu của Bờm (Database PostgreSQL) bắt đầu nổi tiếng. App điện thoại (Client) gửi khách tới nườm nượp.

Bờm áp dụng chính sách chăm sóc tận răng: Cứ 1 khách bước vào quán, Bờm sẽ tuyển nóng 1 nhân viên phục vụ (Database Connection) đứng túc trực riêng cho khách đó.

**Thực tế đau lòng:** Khách vào quán xem menu mất 15 phút, nướng thịt ăn mất 1 tiếng, đi vệ sinh mất 10 phút. Trong suốt thời gian đó, nhân viên phục vụ chỉ đứng ngáp ruồi chờ đợi.

**Hậu quả (Out of Memory/Kết nối chậm):** Quán có 1000 khách, Bờm phải nuôi 1000 nhân viên. Mỗi nhân viên (Process của PostgreSQL) chiếm khoảng 10MB RAM. 1000 nhân viên ăn đứt 10GB RAM của máy chủ. Quán sập tiệm vì... hết tiền trả lương (quá tải RAM và CPU), chưa kể thời gian làm thủ tục tuyển dụng/sa thải (Mở/đóng connection) quá lâu!

---

#### 2. Kỷ nguyên ánh sáng (Có PgBouncer): Cô Lễ tân siêu đẳng

Bờm sa thải hết, chỉ giữ lại một đội ngũ tinh nhuệ gồm 20 nhân viên phục vụ siêu tốc (Server Connections).

Đồng thời, Bờm thuê một cô Lễ tân cực kỳ nhanh nhẹn tên là PgBouncer đứng ở cửa.

App điện thoại lại gửi 1000 khách tới. Cô Lễ tân PgBouncer vẫn tươi cười mở cửa đón nhận toàn bộ 1000 người vào trong (Mở 1000 Client Connections rất nhẹ nhàng, chỉ tốn vài MB RAM cho cả ngàn người).

**Tuyệt chiêu điều phối:** Cô Lễ tân dặn 20 nhân viên phục vụ cứ đứng ở quầy. Chỉ khi nào có bàn thực sự bấm chuông gọi món (Bắt đầu 1 Transaction), cô mới điều 1 nhân viên chạy ra ghi order và bưng đồ ăn.

Bưng đồ ra xong (Kết thúc Transaction), nhân viên lập tức quay về quầy để phục vụ bàn khác, không đứng chờ bàn đó ăn nữa.

**Kết quả:** Chỉ với 20 nhân viên (Connections), Bờm phục vụ trơn tru 1000 khách hàng cùng lúc mà máy chủ chạy êm ru mát mẻ!

---

### 🧠 3 Chế độ điều phối của PgBouncer (Pool Modes)

Để hiểu sâu hơn, hãy xem cô Lễ tân (PgBouncer) có 3 cách điều phối nhân viên như thế nào:

#### Session Pooling (Bao trọn gói)

Khách bước vào quán, cô Lễ tân cử 1 nhân viên đi theo khách từ lúc ngồi xuống đến khi thanh toán đi về (Disconnect).

**Đánh giá:** Ít dùng, vì nhân viên vẫn phải đứng chờ lúc khách ăn. Chỉ dùng cho các ứng dụng cũ không hỗ trợ tốt.

---

#### Transaction Pooling (Gói theo món) - ⭐ Tuyệt chiêu hay dùng nhất!

Khách bấm chuông gọi "Cho 1 đĩa bò và 1 đĩa mực" (Bắt đầu giao dịch - BEGIN).

Nhân viên tới ghi nhận, mang bò và mực ra bàn, khách xác nhận đủ món (Kết thúc giao dịch - COMMIT). Xong là nhân viên té luôn sang bàn khác.

Lát sau khách gọi tính tiền, có thể là một nhân viên hoàn toàn khác chạy ra xử lý.

**Đánh giá:** Hoàn hảo cho các ứng dụng web/API hiện đại (Spring Boot, NestJS). Tối ưu 100% công suất nhân viên.

---

#### Statement Pooling (Gói theo từng câu nói)

- Khách nói: "Cho 1 đĩa bò" → 1 nhân viên chạy ra lấy bò.
- Khách nói: "Cho 1 đĩa mực" → 1 nhân viên khác chạy ra lấy mực.

**Đánh giá:** Quá manh mún. Không hỗ trợ các giao dịch (Transactions) gồm nhiều bước liên hoàn. Rất hiếm khi sử dụng.

---

### 💻 Áp chiếu vào Cấu hình Thực tế

Khi bạn cấu hình file pgbouncer.ini, nó sẽ trông hệt như cách Bờm tổ chức quán lẩu:

```ini
# pgbouncer.ini
[databases]
mydb = host=127.0.0.1 port=5432 dbname=mydb

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
min_pool_size = 5
```

---

### 💡 Bài học rút ra khi đi làm

Nếu bạn viết một API bằng Node.js/Java và kết nối thẳng vào database PostgreSQL, mỗi lần có request tới, app của bạn có thể sẽ mở 1 connection. Traffic tăng đột biến (ví dụ: Sale 11/11), số lượng connection tăng vọt lên 500, 1000... Database của bạn sẽ chết cứng vì kiệt sức (Connection Exhaustion).

**Giải pháp:** Luôn luôn đặt một cái PgBouncer ở giữa ứng dụng và Database trên môi trường Production!

---

### Connection Pooling Technical Details

```
Problem: PostgreSQL fork process per connection (~10MB each)
  500 connections = 5GB RAM just for connections!
  Connection setup = ~50ms

Solution: Connection pool
  Application → PgBouncer (100 connections) → PostgreSQL (20 connections)

PgBouncer modes:
  Session:     1 client = 1 server conn (until disconnect)
  Transaction: 1 client = 1 server conn (per transaction) ⭐
  Statement:   1 client = 1 server conn (per statement) — risky
```

---

## 📝 Bài tập

1. Demo MVCC: 2 concurrent transactions, show xmin/xmax
2. Monitor dead tuples, trigger VACUUM, observe cleanup
3. Implement job queue bằng FOR UPDATE SKIP LOCKED
4. Setup PgBouncer với transaction pooling mode

---

## 📚 Tài liệu

- *PostgreSQL 14 Internals* — Egor Rogov
- [PostgreSQL MVCC Explained](https://www.interdb.jp/pg/pgsql05.html)
- [PgBouncer Documentation](https://www.pgbouncer.org/)
