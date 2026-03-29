# Bài 12: Relational Databases

## 🎯 Mục tiêu
- Hiểu relational model và vì sao SQL vẫn là ngôn ngữ quan trọng nhất cho dữ liệu nghiệp vụ
- Nắm schema design, normalization, indexes, transactions, query planning và operational basics
- Có khả năng đọc một query chậm và suy nghĩ đúng hướng để tối ưu

## 📖 Bức tranh lớn
Relational databases là một trong những abstraction thành công nhất của Computer Science: dữ liệu được mô hình hóa bằng bảng, ràng buộc và ngôn ngữ khai báo. Bạn nói "mình muốn gì", optimizer sẽ tìm cách thực hiện. Hiểu tốt RDBMS giúp bạn viết backend tốt hơn, thiết kế data model rõ hơn và tránh vô số lỗi dữ liệu trong production.

---

## 1. Relational model và schema design

### Chủ đề cần nắm
- Table, row, column
- Primary key, foreign key
- Constraints: unique, not null, check
- Normalization và khi nào denormalize

### Tư duy quan trọng
- Schema là contract nghiệp vụ, không chỉ là chỗ nhét data
- Mỗi bảng nên phản ánh một thực thể hoặc quan hệ rõ ràng
- Naming, keys và constraints giúp giảm bug logic rất nhiều

---

## 2. SQL như một ngôn ngữ khai báo

### Phải nắm
- SELECT, WHERE, JOIN, GROUP BY, ORDER BY
- Subquery, CTE
- Aggregate functions
- Window functions
- INSERT, UPDATE, DELETE

### Khái niệm nền tảng
- SQL mô tả kết quả mong muốn, không mô tả chi tiết từng bước như code imperative
- Cùng một query logic có thể có nhiều execution plan khác nhau

---

## 3. Indexing

### Chủ đề cần nắm
- B-Tree index
- Composite index
- Covering index
- Selectivity
- Clustered vs secondary index ở mức overview

### Quy tắc thực dụng
- Index tăng tốc đọc nhưng làm write tốn hơn
- Không phải query nào cũng cần index riêng
- Thứ tự cột trong composite index rất quan trọng
- Over-indexing gây tốn memory, storage và write amplification

---

## 4. Transactions và isolation

### Chủ đề cần nắm
- ACID
- Transaction boundaries
- Dirty read, non-repeatable read, phantom read
- Isolation levels
- Locking và deadlocks
- MVCC ở mức trực giác

### Vì sao quan trọng
- Đúng dữ liệu quan trọng hơn nhanh trong rất nhiều nghiệp vụ
- Payment, inventory, booking, account balance đều phụ thuộc nặng vào transaction semantics

---

## 5. Query planning và optimization

### Phải hiểu
- Full table scan vs index scan
- Join algorithms ở mức overview
- Cardinality estimation ở mức trực giác
- `EXPLAIN` / `EXPLAIN ANALYZE`

### Hướng tối ưu chuẩn
- Đảm bảo filter/join predicates hợp lý
- Thêm hoặc sửa index đúng chỗ
- Tránh query trong loop ở tầng ứng dụng
- Giảm data transfer không cần thiết
- Xem lại schema và access pattern

---

## 6. Data modeling cho ứng dụng thực tế

### Chủ đề cần nắm
- OLTP vs OLAP
- Audit trail
- Soft delete
- Multi-tenant design ở mức overview
- Idempotent writes và unique constraints

### Sai lầm phổ biến
- Nhét quá nhiều JSON vào cột quan trọng rồi mất lợi ích relational
- Không đặt constraints vì "app sẽ tự đảm bảo"
- Thiếu index cho foreign keys và truy vấn thường xuyên

---

## 7. Operational basics

### Tối thiểu nên biết
- Backup/restore
- Replication
- Connection pooling
- Migration strategy
- Monitoring: slow queries, locks, CPU, IOPS, cache hit ratio

---

## ✅ Checklist ôn tập
- Viết được query với joins, aggregates, window functions cơ bản
- Giải thích được vì sao một index giúp hoặc không giúp query
- Hiểu transaction, isolation và deadlock ở mức làm việc được
- Đọc `EXPLAIN` ở mức cơ bản
- Biết các nguyên tắc data modeling cho backend service

## 📝 Bài tập
1. Thiết kế schema cho e-commerce hoặc task management app.
2. Viết 10 queries từ cơ bản đến nâng cao cho schema đó.
3. Tạo ví dụ deadlock hoặc lost update trên DB local nếu có điều kiện.
4. Giải thích bằng lời một execution plan đơn giản.
5. Tự làm checklist review schema cho dự án của bạn.

## 📚 Tài liệu
- *Database System Concepts* — Silberschatz, Korth, Sudarshan
- *SQL Performance Explained* — Markus Winand
- Track đào sâu: `../../03_Database/`