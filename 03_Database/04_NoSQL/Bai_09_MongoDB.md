# Bài 09: MongoDB — Document Database

## 🎯 Mục tiêu
- Document model, BSON
- CRUD operations
- Aggregation pipeline
- Schema design patterns

## 📖 Câu chuyện đời thường
> SQL giống bảng tính Excel: cột cố định, mọi hàng phải giống nhau. **MongoDB** giống như **tủ hồ sơ linh hoạt**: mỗi hồ sơ (document) có thể chứa thông tin khác nhau. Hồ sơ nhân viên A có "kỹ năng: [Python, Java]", nhân viên B có "chứng chỉ: [AWS, K8s]" — không cần ép vào cùng khuôn. **Aggregation Pipeline** giống dây chuyền lọc: hồ sơ đi qua bước "lọc phòng ban Kỹ thuật" → "nhóm theo cấp bậc" → "đếm số người" — mỗi bước biến đổi data một chút. Phù hợp khi data không có cấu trúc cố định, thay đổi nhiều, hoặc cần tốc độ viết nhanh.

---

## 1. Document Model

```javascript
// MongoDB lưu data dạng BSON (Binary JSON)
// Không cần fixed schema — flexible structure
{
  "_id": ObjectId("65a1b2c3d4e5f6789012abcd"),
  "username": "alice",
  "email": "alice@email.com",
  "profile": {
    "full_name": "Alice Nguyen",
    "avatar_url": "https://...",
    "bio": "Software Engineer"
  },
  "skills": ["python", "mongodb", "docker"],
  "created_at": ISODate("2024-01-15T10:30:00Z")
}

// Embedded documents → denormalized
// Không cần JOIN → 1 query lấy tất cả related data

// SQL equivalent: 3 tables (users, profiles, user_skills)
// MongoDB: 1 document chứa tất cả
```

---

## 2. CRUD Operations

```javascript
// INSERT
db.users.insertOne({
  username: "alice",
  email: "alice@email.com",
  profile: { full_name: "Alice Nguyen" }
});

db.users.insertMany([
  { username: "bob", email: "bob@email.com" },
  { username: "charlie", email: "charlie@email.com" }
]);

// FIND (SELECT)
db.users.find({ username: "alice" });
db.users.find({ "profile.full_name": "Alice Nguyen" });  // nested field
db.users.find({ skills: "python" });  // array contains
db.users.find({ 
  created_at: { $gte: ISODate("2024-01-01"), $lt: ISODate("2024-02-01") }
});

// Projection (chỉ lấy fields cần)
db.users.find({}, { username: 1, email: 1, _id: 0 });

// Sort + Limit + Skip
db.users.find().sort({ created_at: -1 }).limit(20).skip(40);

// UPDATE
db.users.updateOne(
  { username: "alice" },
  { $set: { "profile.bio": "Senior Engineer" } }
);

db.users.updateMany(
  { is_active: false },
  { $set: { deleted_at: new Date() } }
);

// Atomic operations
db.products.updateOne(
  { _id: productId, stock: { $gte: 1 } },
  { $inc: { stock: -1 }, $push: { buyers: userId } }
);

// DELETE
db.users.deleteOne({ username: "alice" });
db.users.deleteMany({ created_at: { $lt: ISODate("2020-01-01") } });
```

---

## 3. Aggregation Pipeline

```javascript
// SQL GROUP BY equivalent → nhưng mạnh hơn nhiều
// Pipeline: stage 1 → stage 2 → stage 3 → result

// Doanh thu theo tháng, category
db.orders.aggregate([
  // Stage 1: Filter
  { $match: { status: "completed", created_at: { $gte: ISODate("2024-01-01") } } },
  
  // Stage 2: Unwind array
  { $unwind: "$items" },
  
  // Stage 3: Lookup (LEFT JOIN)
  { $lookup: {
      from: "products",
      localField: "items.product_id",
      foreignField: "_id",
      as: "product"
  }},
  { $unwind: "$product" },
  
  // Stage 4: Group
  { $group: {
      _id: {
        month: { $dateToString: { format: "%Y-%m", date: "$created_at" } },
        category: "$product.category"
      },
      revenue: { $sum: { $multiply: ["$items.quantity", "$items.price"] } },
      order_count: { $sum: 1 }
  }},
  
  // Stage 5: Sort
  { $sort: { "_id.month": -1, revenue: -1 } },
  
  // Stage 6: Project (reshape)
  { $project: {
      month: "$_id.month",
      category: "$_id.category",
      revenue: 1,
      order_count: 1,
      _id: 0
  }}
]);
```

---

## 4. Schema Design Patterns

### Embed vs Reference
```javascript
// EMBED khi:
//   - Data always accessed together
//   - 1:1 hoặc 1:few relationship
//   - Data không thay đổi thường xuyên

// Order with embedded items (1:few)
{
  _id: ObjectId("..."),
  user_id: ObjectId("..."),
  items: [
    { product_id: ObjectId("..."), name: "Laptop", price: 1000, qty: 1 },
    { product_id: ObjectId("..."), name: "Mouse", price: 30, qty: 2 }
  ],
  total: 1060
}

// REFERENCE khi:
//   - Many:Many relationship
//   - Data shared across documents
//   - Unbounded arrays (>100 items)

// Blog post with comment references (1:many, unbounded)
{ _id: postId, title: "...", comment_ids: [id1, id2, ...] }  // ❌ array grows forever
{ _id: commentId, post_id: postId, text: "..." }              // ✅ reference from child
```

### Bucket Pattern (time-series)
```javascript
// Thay vì 1 document per measurement
// → Bucket: 1 document per hour
{
  sensor_id: "temp-001",
  date: ISODate("2024-01-15T10:00:00Z"),
  measurements: [
    { time: ISODate("...T10:01:00Z"), value: 22.5 },
    { time: ISODate("...T10:02:00Z"), value: 22.7 },
    // ... 60 measurements per document
  ],
  count: 60,
  avg: 22.6, min: 22.1, max: 23.0
}
// Giảm 60x số documents → faster queries
```

---

## 5. Indexing

```javascript
// Single field
db.users.createIndex({ email: 1 });  // ascending

// Compound
db.orders.createIndex({ user_id: 1, created_at: -1 });

// Text index (full-text search)
db.products.createIndex({ name: "text", description: "text" });
db.products.find({ $text: { $search: "laptop gaming" } });

// TTL index (auto-delete expired documents)
db.sessions.createIndex({ created_at: 1 }, { expireAfterSeconds: 3600 });
```

---

## 📝 Bài tập

1. Model e-commerce schema trong MongoDB (embed vs reference)
2. Aggregation: top 10 products by revenue, với category info
3. Implement bucket pattern cho IoT sensor data
4. So sánh query performance: MongoDB vs PostgreSQL cho nested data

---

## 📚 Tài liệu
- [MongoDB University (free courses)](https://university.mongodb.com/)
- *MongoDB: The Definitive Guide* — Shannon Bradshaw
