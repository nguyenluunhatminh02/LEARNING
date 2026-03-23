# Bài 14: Data Engineering Basics — ETL, Data Warehouse, OLAP

## 🎯 Mục tiêu
- OLTP vs OLAP
- ETL/ELT pipelines
- Data Warehouse, Data Lake
- Star Schema, dbt

## 📖 Câu chuyện đời thường
> **OLTP** giống quầy thu ngân siêu thị: xử lý từng giao dịch nhanh, mỗi lần 1 khách. **OLAP** giống phòng phân tích của giám đốc: xem báo cáo tổng hợp "doanh thu theo tháng, theo khu vực, so với năm ngoái". **ETL** giống dây chuyền chế biến thực phẩm: nhập nguyên liệu từ nhiều nơi (Extract), rửa sạch + cắt gọt (Transform), bày vào tủ đông lạnh (Load vào warehouse). **Data Lake** giống kho chứa mọi thứ chưa qua chế biến (raw data). **Star Schema** giống ngôi sao: giữa là bảng doanh thu (fact), xung quanh là các chiều: thời gian, sản phẩm, khu vực (dimensions).

---

## 1. OLTP vs OLAP

| | OLTP | OLAP |
|---|---|---|
| Purpose | Transaction processing | Analytics & reporting |
| Queries | Simple CRUD, short | Complex aggregations, long |
| Data | Current, normalized | Historical, denormalized |
| Users | Application, end-users | Analysts, data scientists |
| Rows per query | ~1-100 | Millions |
| Examples | PostgreSQL, MySQL | BigQuery, Redshift, Snowflake |

---

## 2. ETL / ELT

```
ETL (Extract → Transform → Load):
  Source DBs → [Transform in staging] → Data Warehouse
  Traditional approach

ELT (Extract → Load → Transform): ⭐ Modern
  Source DBs → Data Warehouse → [Transform in DW]
  DW powerful enough to transform (BigQuery, Snowflake)

Pipeline:
  ┌──────────┐    ┌───────────┐    ┌──────────────┐
  │ PostgreSQL│    │           │    │              │
  │ MongoDB   │──→ │  Staging  │──→ │  Data        │──→ BI Tools
  │ APIs      │    │  (S3)     │    │  Warehouse   │   (Tableau, Looker)
  │ Logs      │    │           │    │  (Snowflake) │
  └──────────┘    └───────────┘    └──────────────┘

Tools:
  Extract: Fivetran, Airbyte, Singer
  Transform: dbt ⭐ (SQL-based)
  Orchestration: Airflow, Dagster, Prefect
```

---

## 3. Star Schema (Dimensional Modeling)

```
Fact Table (measurements/metrics):
  fact_sales: sale_id, date_id, product_id, store_id, quantity, revenue

Dimension Tables (descriptive attributes):
  dim_date:    date_id, year, quarter, month, day, is_weekend
  dim_product: product_id, name, category, brand
  dim_store:   store_id, name, city, country

        dim_date
           ↑
dim_product → fact_sales ← dim_store
           ↑
       dim_customer

Star shape: fact in center, dimensions around it
```

```sql
-- Analytics query on star schema
SELECT 
    d.year, d.quarter,
    p.category,
    s.country,
    SUM(f.revenue) AS total_revenue,
    COUNT(DISTINCT f.sale_id) AS num_sales
FROM fact_sales f
JOIN dim_date d ON f.date_id = d.date_id
JOIN dim_product p ON f.product_id = p.product_id
JOIN dim_store s ON f.store_id = s.store_id
WHERE d.year = 2024
GROUP BY d.year, d.quarter, p.category, s.country
ORDER BY total_revenue DESC;
```

---

## 4. dbt (Data Build Tool)

```sql
-- models/staging/stg_orders.sql
SELECT 
    id AS order_id,
    user_id,
    status,
    total_amount,
    created_at
FROM {{ source('raw', 'orders') }}
WHERE status != 'cancelled'

-- models/marts/fct_daily_revenue.sql
SELECT 
    DATE_TRUNC('day', o.created_at) AS date,
    COUNT(DISTINCT o.order_id) AS num_orders,
    SUM(o.total_amount) AS revenue
FROM {{ ref('stg_orders') }} o
WHERE o.status = 'completed'
GROUP BY 1
```

```yaml
# dbt_project.yml
# dbt run        → execute all models
# dbt test       → run data tests
# dbt docs generate → documentation
```

---

## 5. Data Lake vs Data Warehouse

```
Data Lake:
  Raw data, any format (JSON, CSV, Parquet, images)
  Storage: S3, GCS, ADLS
  Schema-on-read
  Cheap storage
  Tools: Spark, Presto, Trino

Data Warehouse:
  Structured, transformed data
  Schema-on-write
  Optimized for SQL queries
  Tools: Snowflake, BigQuery, Redshift

Data Lakehouse (modern):
  Combine both: raw storage + SQL engine
  Tools: Databricks (Delta Lake), Apache Iceberg
```

---

## 📝 Bài tập

1. Design star schema cho e-commerce analytics
2. Setup dbt project, transform raw orders → daily revenue
3. Build ETL pipeline: PostgreSQL → S3 → BigQuery
4. So sánh: Snowflake vs BigQuery cho analytics workload

---

## 📚 Tài liệu
- *The Data Warehouse Toolkit* — Ralph Kimball
- [dbt Documentation](https://docs.getdbt.com/)
- *Fundamentals of Data Engineering* — Joe Reis
