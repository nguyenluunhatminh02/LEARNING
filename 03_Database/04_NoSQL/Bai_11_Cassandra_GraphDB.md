# Bài 11: Cassandra & Graph Database (Neo4j)

## 🎯 Mục tiêu
- Cassandra: wide-column model, CQL, partition design
- Neo4j: graph model, Cypher queries
- Khi nào dùng từng loại

## 📖 Câu chuyện đời thường
> **Cassandra** giống như hệ thống ghi chép của một mạng lưới cảm biến: hàng triệu thiết bị gửi data liên tục, chỉ cần ghi nhanh và đọc theo thời gian. Không cần JOIN phức tạp, chỉ cần: "lấy data cảm biến X từ 9h-10h hôm nay". **Neo4j** (Graph DB) thì hoàn toàn khác: giống mạng xã hội. Mỗi người là một điểm (node), mối quan hệ là đường nối (edge). Bạn có thể hỏi: "Bạn của bạn tôi là ai?" hoặc "Từ người này đến người kia qua mấy lần giới thiệu?" — các câu hỏi mà SQL phải viết 10 dòng JOIN, Graph DB trả lời trong 1 dòng.

---

## PART A: Apache Cassandra

### Data Model
```
Cassandra = Wide-Column Store, distributed, highly available

Keyspace → Table → Partition → Row → Column

Table: user_events
┌────────────────┬──────────────┬──────────┬──────────┐
│ user_id (PK)   │ event_time   │ event    │ data     │
├────────────────┼──────────────┼──────────┼──────────┤
│ user_1         │ 2024-01-15   │ login    │ {...}    │ ← Partition 1
│ user_1         │ 2024-01-15   │ click    │ {...}    │
│ user_1         │ 2024-01-16   │ purchase │ {...}    │
├────────────────┼──────────────┼──────────┼──────────┤
│ user_2         │ 2024-01-15   │ login    │ {...}    │ ← Partition 2
│ user_2         │ 2024-01-16   │ login    │ {...}    │
└────────────────┴──────────────┴──────────┴──────────┘

Partition Key (user_id) → determines which node stores data
Clustering Key (event_time) → sorts rows within partition
```

### CQL (Cassandra Query Language)
```sql
CREATE KEYSPACE myapp WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'dc1': 3, 'dc2': 3
};

CREATE TABLE user_events (
    user_id UUID,
    event_time TIMESTAMP,
    event_type TEXT,
    data MAP<TEXT, TEXT>,
    PRIMARY KEY (user_id, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);

-- Insert
INSERT INTO user_events (user_id, event_time, event_type, data)
VALUES (uuid(), toTimestamp(now()), 'login', {'ip': '1.2.3.4'});

-- Query (MUST include partition key)
SELECT * FROM user_events WHERE user_id = ? AND event_time > '2024-01-01';

-- ❌ CANNOT do:
-- SELECT * FROM user_events WHERE event_type = 'login'  (no partition key!)
-- SELECT * FROM user_events ORDER BY event_time (cross-partition)
```

### When to use Cassandra?
```
✅ High write throughput (100K+ writes/sec)
✅ Time-series data, IoT, logs, events
✅ Multi-datacenter replication
✅ Known query patterns (design table per query)
❌ No JOINs, no ad-hoc queries, no strong consistency
```

---

## PART B: Neo4j (Graph Database)

### Graph Model
```
(Nodes) -[:RELATIONSHIPS]-> (Nodes)

(:User {name: "Alice"}) -[:FOLLOWS]-> (:User {name: "Bob"})
(:User {name: "Alice"}) -[:LIKES]-> (:Post {title: "GraphDB"})
(:Post {title: "GraphDB"}) -[:TAGGED]-> (:Tag {name: "database"})
```

### Cypher Query Language
```cypher
// Create
CREATE (alice:User {name: "Alice", age: 30})
CREATE (bob:User {name: "Bob", age: 25})
CREATE (alice)-[:FOLLOWS]->(bob)
CREATE (alice)-[:LIKES]->(post:Post {title: "Learn Neo4j"})

// Find friends of friends
MATCH (user:User {name: "Alice"})-[:FOLLOWS]->()-[:FOLLOWS]->(fof:User)
WHERE NOT (user)-[:FOLLOWS]->(fof) AND user <> fof
RETURN fof.name

// Shortest path between 2 users
MATCH path = shortestPath(
  (a:User {name: "Alice"})-[:FOLLOWS*..6]-(b:User {name: "Charlie"})
)
RETURN path

// Recommendation: users who like same posts as me
MATCH (me:User {name: "Alice"})-[:LIKES]->(post)<-[:LIKES]-(other:User)
WHERE me <> other
WITH other, COUNT(post) AS common_likes
ORDER BY common_likes DESC LIMIT 10
RETURN other.name, common_likes
```

### When to use Graph DB?
```
✅ Social networks (friends, followers)
✅ Recommendation engines
✅ Fraud detection (find suspicious patterns)
✅ Knowledge graphs
✅ Queries: "find all paths", "shortest path", "connected components"
❌ Simple CRUD, bulk analytics, time-series
```

---

## So sánh tổng hợp NoSQL

| | MongoDB | Redis | Cassandra | Neo4j |
|---|---|---|---|---|
| Model | Document | Key-Value | Wide-Column | Graph |
| Best for | Flexible schema | Cache, RT | Write-heavy | Relationships |
| Scale | Sharding | Cluster | **Linear scale** | Limited |
| Consistency | Tunable | Strong | Tunable | ACID |
| Query | Rich | Simple | Limited | Graph traversal |

---

## 📝 Bài tập

1. Design Cassandra table cho chat messages (partition by chat_id)
2. Model social network trong Neo4j, query mutual friends
3. So sánh: PostgreSQL vs Cassandra cho time-series data
4. Implement recommendation engine bằng Neo4j Cypher

---

## 📚 Tài liệu
- *Cassandra: The Definitive Guide* — Jeff Carpenter
- [Neo4j GraphAcademy (free)](https://graphacademy.neo4j.com/)
