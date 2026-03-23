# Bài 02: NumPy & Pandas — Xử lý dữ liệu cho AI

## 🎯 Mục tiêu
- Thành thạo NumPy cho tính toán ma trận
- Thành thạo Pandas cho phân tích dữ liệu bảng
- Trực quan hóa dữ liệu với Matplotlib & Seaborn

## 📖 Câu chuyện đời thường
> Bạn là quản lý của một chuỗi siêu thị có 100 chi nhánh. Mỗi ngày bạn nhận được bảng doanh thu khổng lồ. Nếu dùng tay (Python thuần) để cộng từng ô một thì mất cả ngày. NumPy giống như máy tính Casio — bấm một phát ra kết quả cho cả bảng số. Còn Pandas giống như Excel thông minh — bạn có thể lọc "chi nhánh nào lỗ tháng này?", nhóm theo khu vực, tính trung bình... chỉ bằng 1 dòng lệnh. Matplotlib thì giống như khi bạn vẽ biểu đồ lên bảng trắng để trình bày cho sếp — hình ảnh nói lên nhiều hơn ngàn con số.

---

## PHẦN 1: NumPy — Nền tảng tính toán AI

### 1.1 Tạo Array
```python
import numpy as np

# Từ list
a = np.array([1, 2, 3, 4, 5])
b = np.array([[1, 2, 3], [4, 5, 6]])  # 2D array (ma trận)

# Các hàm tạo nhanh
zeros = np.zeros((3, 4))          # Ma trận 0, shape (3,4)
ones = np.ones((2, 3))            # Ma trận 1
identity = np.eye(4)              # Ma trận đơn vị 4x4
random_arr = np.random.randn(3, 4)  # Phân phối chuẩn
uniform = np.random.rand(3, 4)      # Phân phối đều [0,1)
range_arr = np.arange(0, 10, 0.5)   # Tương tự range()
linspace = np.linspace(0, 1, 100)   # 100 điểm đều từ 0→1

# Thuộc tính
print(b.shape)   # (2, 3)
print(b.dtype)   # int64
print(b.ndim)    # 2
print(b.size)    # 6
```

### 1.2 Indexing & Slicing
```python
a = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12]])

# Truy cập phần tử
a[0, 0]     # 1
a[2, 3]     # 12
a[-1, -1]   # 12

# Slicing: array[row_start:row_end, col_start:col_end]
a[0:2, 1:3]    # [[2,3], [6,7]]
a[:, 0]         # Cột đầu tiên: [1, 5, 9]
a[1, :]         # Hàng thứ 2: [5, 6, 7, 8]

# Boolean indexing — RẤT QUAN TRỌNG trong ML
mask = a > 5
print(a[mask])  # [6, 7, 8, 9, 10, 11, 12]

# Fancy indexing
rows = [0, 2]
cols = [1, 3]
a[rows, cols]   # [2, 12]
```

### 1.3 Phép toán trên Array (Vectorization)
```python
# Phép toán element-wise — NHANH hơn loop rất nhiều
a = np.array([1, 2, 3, 4])
b = np.array([5, 6, 7, 8])

a + b      # [6, 8, 10, 12]
a * b      # [5, 12, 21, 32]
a ** 2     # [1, 4, 9, 16]
np.sqrt(a) # [1., 1.41, 1.73, 2.]
np.exp(a)  # e^a cho mỗi phần tử

# So sánh tốc độ: loop vs vectorized
import time

size = 1_000_000
a = np.random.randn(size)
b = np.random.randn(size)

# Loop Python — CHẬM
start = time.time()
result = [a[i] + b[i] for i in range(size)]
print(f"Loop: {time.time() - start:.3f}s")

# Vectorized NumPy — NHANH gấp 100x+
start = time.time()
result = a + b
print(f"NumPy: {time.time() - start:.3f}s")
```

### 1.4 Phép toán ma trận — Cốt lõi của Deep Learning
```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Nhân ma trận
C = A @ B          # hoặc np.dot(A, B)
# C = [[1*5+2*7, 1*6+2*8], [3*5+4*7, 3*6+4*8]]
# C = [[19, 22], [43, 50]]

# Transpose
A.T     # [[1,3], [2,4]]

# Determinant, Inverse
np.linalg.det(A)     # -2.0
np.linalg.inv(A)     # Ma trận nghịch đảo

# Eigenvalues & Eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)

# Norm (sẽ dùng trong regularization)
np.linalg.norm(A)         # Frobenius norm
np.linalg.norm(A, axis=1) # L2 norm mỗi hàng
```

### 1.5 Broadcasting — Kỹ thuật quan trọng
```python
# Broadcasting cho phép tính toán giữa arrays khác shape
X = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])  # (3, 3)

mean = X.mean(axis=0)   # [4, 5, 6] — shape (3,)
X_centered = X - mean   # Broadcasting: (3,3) - (3,) → (3,3)

# Ví dụ thực tế: normalize features
X = np.random.randn(1000, 5)  # 1000 samples, 5 features
mean = X.mean(axis=0)          # mean mỗi feature
std = X.std(axis=0)            # std mỗi feature
X_normalized = (X - mean) / std  # Standardization
```

### 1.6 Các hàm thống kê
```python
data = np.random.randn(1000)

np.mean(data)       # Trung bình
np.median(data)     # Trung vị
np.std(data)        # Độ lệch chuẩn
np.var(data)        # Phương sai
np.min(data), np.max(data)
np.percentile(data, [25, 50, 75])  # Quartiles
np.corrcoef(x, y)  # Hệ số tương quan

# Aggregation theo trục
X = np.random.randn(100, 5)
X.sum(axis=0)    # Tổng mỗi cột (100 rows → 1 row)
X.mean(axis=1)   # Trung bình mỗi hàng (5 cols → 1 col)
```

---

## PHẦN 2: Pandas — Phân tích dữ liệu

### 2.1 Series & DataFrame
```python
import pandas as pd

# Series
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
s['a']  # 10

# DataFrame — bảng dữ liệu 2D
df = pd.DataFrame({
    'name': ['Minh', 'Lan', 'Hùng', 'Mai'],
    'age': [25, 30, 22, 28],
    'salary': [1000, 1500, 800, 1200],
    'department': ['IT', 'HR', 'IT', 'Marketing']
})

# Đọc/ghi dữ liệu
df = pd.read_csv('data.csv')
df = pd.read_excel('data.xlsx')
df = pd.read_json('data.json')
df.to_csv('output.csv', index=False)
```

### 2.2 Khám phá dữ liệu (EDA)
```python
# Thông tin tổng quan
df.head(10)        # 10 dòng đầu
df.tail(5)         # 5 dòng cuối
df.shape           # (rows, cols)
df.info()          # Kiểu dữ liệu, null count
df.describe()      # Thống kê: mean, std, min, max, quartiles
df.dtypes          # Kiểu mỗi cột

# Missing data
df.isnull().sum()           # Đếm null mỗi cột
df.isnull().sum() / len(df) # Tỷ lệ null
df.dropna()                 # Xóa rows có null
df.fillna(0)                # Điền null bằng 0
df['age'].fillna(df['age'].median(), inplace=True)  # Điền bằng median

# Unique values
df['department'].nunique()       # Số giá trị unique
df['department'].value_counts()  # Đếm mỗi giá trị
```

### 2.3 Truy vấn & Lọc dữ liệu
```python
# Chọn cột
df['name']                  # 1 cột → Series
df[['name', 'salary']]     # Nhiều cột → DataFrame

# Lọc theo điều kiện
df[df['age'] > 25]
df[(df['age'] > 25) & (df['department'] == 'IT')]
df[df['name'].str.contains('M')]
df.query('age > 25 and salary > 1000')

# loc (label-based) vs iloc (integer-based)
df.loc[0:2, 'name':'salary']    # Rows 0-2, columns name→salary
df.iloc[0:2, 0:3]               # Rows 0-1, columns 0-2
```

### 2.4 Biến đổi dữ liệu
```python
# Tạo cột mới
df['bonus'] = df['salary'] * 0.1
df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 100], labels=['Young', 'Mid', 'Senior'])

# Apply function
df['name_upper'] = df['name'].apply(lambda x: x.upper())
df['salary_rank'] = df['salary'].rank(ascending=False)

# Map values
df['dept_code'] = df['department'].map({'IT': 1, 'HR': 2, 'Marketing': 3})

# Replace
df['department'].replace({'IT': 'Technology'}, inplace=True)

# Sort
df.sort_values('salary', ascending=False)
df.sort_values(['department', 'salary'], ascending=[True, False])
```

### 2.5 GroupBy & Aggregation
```python
# Nhóm và tính thống kê
dept_stats = df.groupby('department').agg({
    'salary': ['mean', 'median', 'max', 'min'],
    'age': 'mean',
    'name': 'count'
})

# Pivot table
pivot = df.pivot_table(
    values='salary',
    index='department',
    columns='age_group',
    aggfunc='mean',
    fill_value=0
)

# Crosstab
pd.crosstab(df['department'], df['age_group'])
```

### 2.6 Merge / Join
```python
# Merge (giống SQL JOIN)
orders = pd.DataFrame({'user_id': [1, 2, 3], 'product': ['A', 'B', 'C']})
users = pd.DataFrame({'user_id': [1, 2, 4], 'name': ['Minh', 'Lan', 'Hùng']})

# Inner join
pd.merge(orders, users, on='user_id', how='inner')

# Left join
pd.merge(orders, users, on='user_id', how='left')

# Concat
pd.concat([df1, df2], axis=0)  # Stack theo hàng
pd.concat([df1, df2], axis=1)  # Stack theo cột
```

---

## PHẦN 3: Trực quan hóa dữ liệu

### 3.1 Matplotlib
```python
import matplotlib.pyplot as plt

# Line plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, label='Training Loss', color='blue', linewidth=2)
ax.plot(x, y2, label='Validation Loss', color='red', linestyle='--')
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
ax.set_title('Training Progress')
ax.legend()
plt.tight_layout()
plt.savefig('loss_curve.png', dpi=150)
plt.show()

# Subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes[0, 0].hist(data, bins=30)
axes[0, 1].scatter(x, y, alpha=0.5)
axes[1, 0].bar(categories, values)
axes[1, 1].boxplot([data1, data2, data3])
plt.tight_layout()
plt.show()
```

### 3.2 Seaborn — Statistical Visualization
```python
import seaborn as sns

# Distribution
sns.histplot(df['salary'], kde=True)
sns.boxplot(x='department', y='salary', data=df)

# Relationships
sns.scatterplot(x='age', y='salary', hue='department', data=df)
sns.pairplot(df[['age', 'salary', 'experience']], hue='department')

# Correlation heatmap — RẤT HỮU ÍCH cho EDA
correlation = df[numeric_cols].corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
```

---

## 📝 Bài tập

### Bài tập NumPy
1. Tạo 2 ma trận 3x3 ngẫu nhiên, tính tích ma trận, transpose, determinant
2. Implement hàm `softmax(x)` bằng NumPy (dùng trong neural network)
3. Tạo 1000 điểm dữ liệu 2D theo phân phối Gaussian, tính mean, std, normalize

### Bài tập Pandas
1. Tải dataset Titanic từ Kaggle, thực hiện EDA đầy đủ:
   - Bao nhiêu missing values mỗi cột?
   - Tỷ lệ sống sót theo giới tính, hạng vé?
   - Phân phối tuổi theo class?
2. Tải dataset World Happiness Report, tìm top 10 quốc gia hạnh phúc nhất, vẽ biểu đồ
3. Merge 2 dataset: orders + products, tính tổng doanh thu theo category

### Mini Project: Phân tích dữ liệu COVID-19
- Tải dữ liệu COVID-19 (Our World in Data)
- Vẽ biểu đồ số ca nhiễm theo thời gian cho 5 quốc gia
- So sánh tỷ lệ tiêm vaccine
- Tạo dashboard đơn giản với matplotlib subplots

---

## 📚 Tài liệu
- [NumPy User Guide](https://numpy.org/doc/stable/user/)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/)
- *Python for Data Analysis* — Wes McKinney (tác giả Pandas)
