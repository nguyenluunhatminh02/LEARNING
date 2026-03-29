# Bài 12: Relational Databases — Full Lesson

## Mục tiêu học tập
Sau bài này, bạn nên:
- hiểu relational model, schema design, SQL, indexing và transactions ở mức làm việc tốt
- biết vì sao query nhanh/chậm và bắt đầu đọc execution plan có hệ thống
- có trực giác tốt hơn khi thiết kế data model cho backend applications

## Bạn cần biết trước
- Systems section, đặc biệt là Bài 11, là nền tốt

---

## 1. Vì sao relational databases vẫn quan trọng

RDBMS tồn tại lâu và vẫn mạnh vì nó cung cấp cùng lúc:
- mô hình dữ liệu chặt chẽ
- constraints để bảo vệ tính đúng
- ngôn ngữ truy vấn mạnh
- transaction semantics rõ ràng

Rất nhiều ứng dụng nghiệp vụ cần đúng dữ liệu hơn là chỉ cần scale thô.

---

## 2. Relational model

### Thành phần cốt lõi
- table
- row
- column
- primary key
- foreign key
- constraints

### Tư duy quan trọng
Schema không chỉ là nơi cất dữ liệu. Nó là một phần của business contract.

Ví dụ:
- unique email
- foreign key từ order tới customer
- quantity không âm

Nếu constraint nằm hết ở app mà không có ở DB, lỗi dữ liệu rất dễ chui lọt.

---

## 3. Normalization và denormalization

### Normalization tốt khi
- muốn giảm duplicate data
- muốn tránh update anomalies
- domain có quan hệ rõ ràng

### Denormalization hợp lý khi
- đọc nhiều hơn ghi rất mạnh
- joins trở thành bottleneck thật
- có cơ chế đồng bộ dữ liệu duplicate rõ ràng

Điểm mấu chốt: đây là trade-off, không phải giáo điều.

---

## 4. SQL như một ngôn ngữ khai báo

Bạn mô tả dữ liệu muốn lấy, DB engine tự chọn execution strategy.

### Các khối nên nắm chắc
- SELECT / WHERE
- JOIN
- GROUP BY / HAVING
- ORDER BY
- CTE
- window functions

### Bài học lớn
Viết SQL đúng syntax chưa đủ. Bạn cần dần hiểu engine sẽ chạy nó như thế nào.

---

## 5. Indexing

Index là cấu trúc phụ giúp tìm dữ liệu nhanh hơn.

### Các ý cần nắm
- B-Tree index
- composite index
- covering index
- selectivity

### Trade-off
- đọc nhanh hơn
- ghi chậm hơn
- tốn memory/storage hơn

### Quy tắc thực dụng
Index phải đi cùng access pattern, không phải cứ thêm nhiều là tốt.

---

## 6. Transactions và isolation

Transactions giúp nhiều operations trở thành một đơn vị logic.

### ACID
- atomicity
- consistency
- isolation
- durability

### Isolation issues nên biết
- dirty read
- non-repeatable read
- phantom read

### Tại sao cực kỳ quan trọng
Payment, inventory, booking, balance updates đều phụ thuộc mạnh vào transaction semantics.

---

## 7. Query planning

Một query chậm không phải lúc nào cũng vì DB "yếu". Thường là do:
- plan không phù hợp
- cardinality estimates sai
- thiếu index hoặc index sai thứ tự
- query pattern không hợp workload

### Tối thiểu nên đọc được
- full table scan vs index scan
- join order basic intuition
- estimated rows vs actual rows

---

## 8. Data modeling cho ứng dụng thật

Những chủ đề rất đáng biết:
- audit tables
- soft delete
- multi-tenant schema patterns
- idempotent writes với unique constraints
- OLTP vs OLAP separation

Một schema đẹp là schema hỗ trợ cả correctness lẫn queries thực tế.

---

## 9. Sai lầm phổ biến
- nhét JSON vào quá nhiều chỗ rồi mất sức mạnh relational
- thiếu constraints vì nghĩ app sẽ lo
- không index foreign keys/query hot paths
- query trong loop ở tầng ứng dụng
- không test migrations và restore paths

---

## 10. Checklist sau bài
- Thiết kế được schema cơ bản cho một ứng dụng CRUD có quan hệ
- Viết được joins, aggregates, CTE và window functions cơ bản
- Hiểu index giúp gì và cost gì
- Giải thích được transaction và isolation ở mức thực dụng
- Đọc được execution plan cơ bản

## 11. Bài tập thực hành
1. Thiết kế schema cho e-commerce hoặc SaaS app.
2. Viết 10 queries quan trọng nhất cho schema đó.
3. Chọn 3 access patterns và đề xuất indexes.
4. Viết note về một transaction flow như create order hoặc payment.
5. Tự giải thích vì sao một query có thể cần full scan.

## 12. Mini deliverable
Tạo file `rdbms_design_pack.md` gồm:
- schema draft
- 5 constraints quan trọng
- 5 access patterns
- index proposals
- một transaction flow

## 13. Học tiếp
- `Bai_13_Storage_Engines_and_NoSQL_Full_Lesson.md`
- `../../08_Reference_and_Review/05_Data_and_Storage_Deep_Dive.md`