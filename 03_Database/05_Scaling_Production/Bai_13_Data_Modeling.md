# Bài 13: Data Modeling & Schema Design

## 🎯 Mục tiêu
- Normalization (1NF → 3NF → BCNF)
- Denormalization strategies
- Schema patterns cho real-world systems

---

## 1. Normalization

### 1NF: Atomic values, no repeating groups
```sql
-- ❌ Violates 1NF
-- | id | name  | phones              |
-- | 1  | Alice | 0901234567,0912345678|

-- ✅ 1NF
CREATE TABLE user_phones (
    user_id BIGINT REFERENCES users(id),
    phone VARCHAR(20),
    PRIMARY KEY (user_id, phone)
);
```

### 2NF: No partial dependencies (on part of composite key)
```sql
-- ❌ Violates 2NF (order_id alone determines customer_name)
-- PK: (order_id, product_id)
-- | order_id | product_id | customer_name | quantity |

-- ✅ 2NF: separate tables
-- orders: (order_id PK, customer_name)
-- order_items: (order_id, product_id PK, quantity)
```

### 3NF: No transitive dependencies
```sql
-- ❌ Violates 3NF (zip_code → city, transitive via student)
-- | student_id | name | zip_code | city    |

-- ✅ 3NF
-- students: (student_id, name, zip_code FK)
-- locations: (zip_code PK, city)
```

### When to Normalize vs Denormalize
```
Normalize (3NF):
  ✅ Write-heavy systems (less update anomalies)
  ✅ Data integrity critical
  ✅ Storage efficiency

Denormalize:
  ✅ Read-heavy systems (avoid expensive JOINs)
  ✅ Reporting / analytics
  ❌ Update anomalies (data inconsistency risk)
  ❌ More storage
```

---

## 2. Schema Design Patterns

### Polymorphic Associations
```sql
-- Single Table Inheritance
CREATE TABLE notifications (
    id BIGSERIAL PRIMARY KEY,
    type VARCHAR(20) NOT NULL,  -- 'email', 'sms', 'push'
    recipient TEXT NOT NULL,
    subject TEXT,    -- only for email
    body TEXT,
    phone TEXT,      -- only for sms
    device_token TEXT -- only for push
);
-- ✅ Simple queries, ❌ sparse columns (NULL)

-- Class Table Inheritance
CREATE TABLE notifications (id BIGSERIAL PRIMARY KEY, type VARCHAR(20), body TEXT);
CREATE TABLE email_notifications (notification_id BIGINT PK REFERENCES notifications, subject TEXT, recipient TEXT);
CREATE TABLE sms_notifications (notification_id BIGINT PK REFERENCES notifications, phone TEXT);
-- ✅ Clean, ❌ needs JOINs
```

### Audit Trail / History Table
```sql
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    name TEXT, price NUMERIC, updated_at TIMESTAMPTZ
);

CREATE TABLE products_history (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT,
    name TEXT, price NUMERIC,
    changed_at TIMESTAMPTZ DEFAULT NOW(),
    changed_by BIGINT,
    operation VARCHAR(10)  -- INSERT, UPDATE, DELETE
);

-- Trigger auto-log changes
CREATE FUNCTION log_product_changes() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO products_history (product_id, name, price, changed_by, operation)
    VALUES (OLD.id, OLD.name, OLD.price, current_setting('app.user_id')::bigint, TG_OP);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_products_history
AFTER UPDATE OR DELETE ON products
FOR EACH ROW EXECUTE FUNCTION log_product_changes();
```

### Soft Delete
```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;
CREATE INDEX idx_users_active ON users(id) WHERE deleted_at IS NULL;

-- All queries add: WHERE deleted_at IS NULL
-- Or use VIEW:
CREATE VIEW active_users AS SELECT * FROM users WHERE deleted_at IS NULL;
```

---

## 3. Real-World Schema Examples

### E-commerce
```sql
-- Core tables
users → addresses (1:N)
products → categories (N:1), product_images (1:N)
orders → order_items → products
orders → payments, shipments
products → reviews (1:N) → users

-- Denormalized fields for performance:
-- orders.total (calculated from items)
-- products.avg_rating (calculated from reviews)
-- products.sold_count (calculated from order_items)
```

### Multi-tenant SaaS
```sql
-- Shared schema approach
CREATE TABLE tenants (id UUID PRIMARY KEY, name TEXT, plan TEXT);

-- All tables have tenant_id
CREATE TABLE users (
    id UUID PRIMARY KEY,
    tenant_id UUID NOT NULL REFERENCES tenants(id),
    email TEXT NOT NULL,
    UNIQUE (tenant_id, email)  -- unique within tenant
);

-- Row Level Security (PostgreSQL)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON users
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

---

## 📝 Bài tập

1. Design normalized schema cho hospital system (patients, doctors, appointments, prescriptions)
2. Implement audit trail trigger cho orders table
3. Design multi-tenant SaaS schema với Row Level Security
4. Denormalize e-commerce schema cho analytics dashboard

---

## 📚 Tài liệu
- *SQL Antipatterns* — Bill Karwin
- *Database Design for Mere Mortals* — Michael Hernandez
