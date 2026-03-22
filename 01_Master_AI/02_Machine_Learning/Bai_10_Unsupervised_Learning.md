# Bài 10: Unsupervised Learning

## 🎯 Mục tiêu
- Clustering: K-Means, DBSCAN, Hierarchical
- Dimensionality Reduction: PCA, t-SNE, UMAP
- Anomaly Detection

---

## 1. K-Means Clustering

### 1.1 Thuật toán
```
1. Chọn K centroids ngẫu nhiên
2. Gán mỗi điểm vào centroid gần nhất
3. Tính lại centroid = trung bình các điểm trong cluster
4. Lặp lại 2-3 đến khi hội tụ
```

```python
import numpy as np

class KMeansCustom:
    def __init__(self, k=3, max_iters=100):
        self.k = k
        self.max_iters = max_iters
    
    def fit(self, X):
        n_samples = X.shape[0]
        # Random init
        idx = np.random.choice(n_samples, self.k, replace=False)
        self.centroids = X[idx]
        
        for _ in range(self.max_iters):
            # Assign clusters
            distances = np.sqrt(((X[:, np.newaxis] - self.centroids) ** 2).sum(axis=2))
            self.labels = np.argmin(distances, axis=1)
            
            # Update centroids
            new_centroids = np.array([X[self.labels == i].mean(axis=0) for i in range(self.k)])
            
            if np.allclose(self.centroids, new_centroids):
                break
            self.centroids = new_centroids
        return self

# Sklearn
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(X)
```

### 1.2 Chọn K — Elbow Method
```python
inertias = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, random_state=42).fit(X)
    inertias.append(km.inertia_)

plt.plot(range(1, 11), inertias, 'bo-')
plt.xlabel('K')
plt.ylabel('Inertia')
plt.title('Elbow Method')
# → Chọn K tại "khuỷu tay" — nơi inertia giảm chậm lại
```

### 1.3 Silhouette Score
```python
from sklearn.metrics import silhouette_score

for k in range(2, 11):
    km = KMeans(n_clusters=k, random_state=42).fit(X)
    score = silhouette_score(X, km.labels_)
    print(f"K={k}: Silhouette = {score:.3f}")
# Silhouette ∈ [-1, 1], càng gần 1 càng tốt
```

---

## 2. DBSCAN — Density-based Clustering

```python
from sklearn.cluster import DBSCAN

# Ưu điểm: không cần chọn K, tìm được cluster hình dạng bất kỳ, phát hiện noise
db = DBSCAN(
    eps=0.5,           # Bán kính lân cận
    min_samples=5,      # Tối thiểu points trong eps để tạo cluster
)
labels = db.fit_predict(X)

n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
n_noise = (labels == -1).sum()
print(f"Clusters: {n_clusters}, Noise points: {n_noise}")
```

---

## 3. Dimensionality Reduction

### 3.1 PCA
```python
from sklearn.decomposition import PCA

# Giảm 100 features → 2 (để visualization)
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X)

print(f"Explained variance: {pca.explained_variance_ratio_}")
print(f"Total: {pca.explained_variance_ratio_.sum():.2%}")

# Chọn số components giữ lại 95% variance
pca_95 = PCA(n_components=0.95)
X_reduced = pca_95.fit_transform(X)
print(f"Components needed: {pca_95.n_components_}")
```

### 3.2 t-SNE — Visualization
```python
from sklearn.manifold import TSNE

tsne = TSNE(n_components=2, perplexity=30, random_state=42)
X_tsne = tsne.fit_transform(X)

plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=labels, cmap='viridis', alpha=0.5)
plt.title('t-SNE Visualization')
# t-SNE tốt cho visualization nhưng KHÔNG dùng cho downstream tasks
```

### 3.3 UMAP — Tốt hơn t-SNE
```python
import umap

reducer = umap.UMAP(n_components=2, random_state=42)
X_umap = reducer.fit_transform(X)
# Nhanh hơn, giữ cấu trúc global tốt hơn t-SNE
```

---

## 📝 Bài tập

1. Customer Segmentation: Dataset Mall Customers (Kaggle)
   - Áp dụng K-Means, DBSCAN
   - Chọn K tốt nhất, phân tích từng cluster
2. MNIST digits: dùng PCA giảm từ 784 xuống 50 features, sau đó K-Means
3. Phát hiện anomaly trong credit card transactions bằng Isolation Forest
4. So sánh t-SNE vs UMAP trên MNIST, Fashion-MNIST

---

## 📚 Tài liệu
- *Hands-On ML* — Ch. 8-9 (Unsupervised Learning)
- *Scikit-learn Clustering Documentation*
