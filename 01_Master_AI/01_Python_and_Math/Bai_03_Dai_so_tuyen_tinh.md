# Bài 03: Đại số tuyến tính cho AI

## 🎯 Mục tiêu
- Hiểu vector, ma trận và các phép toán cơ bản
- Hiểu eigenvalue, eigenvector, SVD — nền tảng của PCA, recommendation
- Ứng dụng đại số tuyến tính vào AI/ML

---

## 1. Vector

### 1.1 Khái niệm
Vector là mảng 1 chiều các số, biểu diễn một **điểm** hoặc **hướng** trong không gian.

Trong ML, **mỗi sample** là một vector:
- Ảnh 28x28 pixel → vector 784 chiều
- Text embedding → vector 768 chiều (BERT)
- Dữ liệu khách hàng: [tuổi, thu_nhập, số_đơn_hàng] → vector 3 chiều

```python
import numpy as np

# Vector trong Python
v = np.array([3, 4])         # vector 2D
w = np.array([1, 2, 3, 4])   # vector 4D
```

### 1.2 Phép toán vector
```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Cộng, trừ
a + b  # [5, 7, 9]
a - b  # [-3, -3, -3]

# Nhân scalar
3 * a  # [3, 6, 9]

# Dot product (tích vô hướng) — CỰC KỲ QUAN TRỌNG
# Đo "sự tương tự" giữa 2 vector
dot = np.dot(a, b)  # 1*4 + 2*5 + 3*6 = 32

# Norm (độ dài vector)
# L2 norm (Euclidean): ||a|| = sqrt(a1² + a2² + ...)
l2 = np.linalg.norm(a)  # sqrt(1+4+9) = sqrt(14) ≈ 3.74

# L1 norm (Manhattan): |a1| + |a2| + ...
l1 = np.linalg.norm(a, ord=1)  # 1+2+3 = 6
```

### 1.3 Cosine Similarity — Dùng rất nhiều trong NLP
```python
def cosine_similarity(a, b):
    """Đo góc giữa 2 vector. Giá trị [-1, 1]"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Ví dụ: so sánh embeddings
doc1 = np.array([0.8, 0.2, 0.5])  # embedding "Mua laptop"
doc2 = np.array([0.7, 0.3, 0.6])  # embedding "Mua máy tính"
doc3 = np.array([0.1, 0.9, 0.1])  # embedding "Nấu ăn"

print(cosine_similarity(doc1, doc2))  # ~0.98 → rất giống
print(cosine_similarity(doc1, doc3))  # ~0.35 → khác nhau
```

---

## 2. Ma trận (Matrix)

### 2.1 Khái niệm
Ma trận là mảng 2D, shape (m × n) với m hàng, n cột.

Trong ML:
- **Bảng dữ liệu**: ma trận X (n_samples × n_features)
- **Weights trong neural network**: ma trận W (input_dim × output_dim)
- **Ảnh xám**: ma trận (height × width)

### 2.2 Phép toán ma trận
```python
A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Nhân ma trận — phép toán CƠ BẢN nhất trong Deep Learning
# C = A @ B: C[i,j] = sum(A[i,k] * B[k,j])
C = A @ B  # [[19, 22], [43, 50]]

# Transpose (chuyển vị)
A.T  # [[1, 3], [2, 4]]

# Ma trận đơn vị
I = np.eye(3)  # A @ I = A

# Ma trận nghịch đảo: A @ A_inv = I
A_inv = np.linalg.inv(A)

# Determinant (định thức)
det = np.linalg.det(A)  # 1*4 - 2*3 = -2

# Rank (hạng)
rank = np.linalg.matrix_rank(A)
```

### 2.3 Nhân ma trận trong Neural Network
```python
# Forward pass trong neural network thực chất là nhân ma trận!
# y = X @ W + b

X = np.random.randn(32, 784)    # 32 images, 784 pixels mỗi ảnh
W1 = np.random.randn(784, 128)  # Weight layer 1
b1 = np.zeros(128)               # Bias layer 1

# Layer 1: (32, 784) @ (784, 128) = (32, 128)
Z1 = X @ W1 + b1

# Activation
A1 = np.maximum(0, Z1)  # ReLU

W2 = np.random.randn(128, 10)  # Weight layer 2
b2 = np.zeros(10)

# Layer 2: (32, 128) @ (128, 10) = (32, 10)
Z2 = A1 @ W2 + b2  # Output: 32 images × 10 classes
```

---

## 3. Eigenvalue & Eigenvector

### 3.1 Khái niệm
Cho ma trận A, nếu: **A @ v = λ * v**
- v là **eigenvector** (vector riêng) — hướng không thay đổi khi nhân A
- λ là **eigenvalue** (trị riêng) — hệ số scale

```python
A = np.array([[4, 2], [1, 3]])
eigenvalues, eigenvectors = np.linalg.eig(A)

print(f"Eigenvalues: {eigenvalues}")    # [5, 2]
print(f"Eigenvectors:\n{eigenvectors}") # Mỗi cột là 1 eigenvector
```

### 3.2 Ứng dụng: PCA (Principal Component Analysis)
```python
# PCA = tìm eigenvectors của ma trận hiệp phương sai
# → Giảm chiều dữ liệu, giữ lại variance lớn nhất

from sklearn.decomposition import PCA

# Dữ liệu 100 chiều → giảm còn 2 chiều
X = np.random.randn(1000, 100)

pca = PCA(n_components=2)
X_reduced = pca.fit_transform(X)

print(X_reduced.shape)  # (1000, 2)
print(f"Variance explained: {pca.explained_variance_ratio_.sum():.2%}")
```

---

## 4. Singular Value Decomposition (SVD)

### 4.1 Khái niệm
Phân rã ma trận: **A = U @ Σ @ Vᵀ**
- U: ma trận trực giao (left singular vectors)
- Σ: ma trận đường chéo (singular values, giảm dần)
- Vᵀ: ma trận trực giao (right singular vectors)

```python
A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

U, S, Vt = np.linalg.svd(A)
```

### 4.2 Ứng dụng: Nén ảnh
```python
from PIL import Image

# Đọc ảnh grayscale
img = np.array(Image.open('photo.jpg').convert('L'))  # (H, W)

U, S, Vt = np.linalg.svd(img, full_matrices=False)

# Giữ k singular values đầu tiên → nén ảnh
k = 50
img_compressed = U[:, :k] @ np.diag(S[:k]) @ Vt[:k, :]

# Tỷ lệ nén: thay vì lưu H×W values
# chỉ cần lưu H×k + k + k×W values
```

### 4.3 Ứng dụng: Recommendation System
```python
# Ma trận user-item ratings
# Rows = users, Columns = movies
R = np.array([
    [5, 3, 0, 1],
    [4, 0, 0, 1],
    [1, 1, 0, 5],
    [0, 0, 5, 4],
])

U, S, Vt = np.linalg.svd(R, full_matrices=False)

# Giảm chiều → tìm latent factors
k = 2
U_k = U[:, :k]
S_k = np.diag(S[:k])
Vt_k = Vt[:k, :]

# Reconstruct → predict missing ratings (giá trị 0)
R_predicted = U_k @ S_k @ Vt_k
```

---

## 5. Tóm tắt ứng dụng trong AI

| Khái niệm | Ứng dụng trong AI |
|-----------|-------------------|
| Vector operations | Feature representation, embeddings |
| Dot product | Similarity, attention mechanism |
| Cosine similarity | Semantic search, recommendation |
| Matrix multiplication | Forward pass in neural networks |
| Transpose | Backpropagation |
| Inverse | Linear regression (Normal Equation) |
| Eigendecomposition | PCA, spectral clustering |
| SVD | Dimensionality reduction, recommendation, LoRA |
| Norms (L1, L2) | Regularization, loss functions |

---

## 📝 Bài tập

1. **Vector operations**: Implement cosine similarity, euclidean distance từ đầu (không dùng thư viện)
2. **Ma trận**: Implement phép nhân ma trận bằng 3 vòng for, so sánh thời gian với NumPy
3. **PCA**: Implement PCA từ đầu bằng eigendecomposition, kiểm tra với sklearn
4. **Nén ảnh**: Dùng SVD nén ảnh với k = 5, 20, 50, 100, so sánh chất lượng
5. **Mini project**: Xây dựng hệ thống recommendation đơn giản bằng SVD

---

## 📚 Tài liệu
- *3Blue1Brown: Essence of Linear Algebra* — 16 video (MUST WATCH)
- *Mathematics for Machine Learning* — Deisenroth et al. (Ch. 2-4)
- *Linear Algebra and Its Applications* — Gilbert Strang
