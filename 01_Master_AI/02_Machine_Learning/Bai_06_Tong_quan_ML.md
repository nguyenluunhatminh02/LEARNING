# Bài 06: Tổng quan Machine Learning

## 🎯 Mục tiêu
- Hiểu ML là gì, các loại ML
- Nắm ML pipeline từ đầu đến cuối
- Hiểu Bias-Variance tradeoff, Overfitting/Underfitting

---

## 1. Machine Learning là gì?

### 1.1 Định nghĩa
> "A computer program is said to **learn** from experience E with respect to task T and performance measure P, if its performance at T improves with E." — Tom Mitchell

**Nói đơn giản**: ML = máy tính học patterns từ dữ liệu, thay vì được lập trình cụ thể.

### 1.2 Traditional Programming vs ML
```
Traditional: INPUT + RULES  → OUTPUT
ML:          INPUT + OUTPUT → RULES (model)
```

---

## 2. Ba loại Machine Learning

### 2.1 Supervised Learning (Học có giám sát)
- Có **label** (đáp án) cho training data
- **Regression**: dự đoán giá trị liên tục (giá nhà, nhiệt độ)
- **Classification**: dự đoán nhãn rời rạc (spam/not spam, mèo/chó)

```python
# Ví dụ
X = [[180, 80], [160, 55], [170, 65]]  # [chiều cao, cân nặng]
y = ["nam", "nữ", "nam"]                # label
# → Học: chiều cao & cân nặng → giới tính
```

### 2.2 Unsupervised Learning (Học không giám sát)
- **KHÔNG có label**
- **Clustering**: nhóm dữ liệu tương tự (phân nhóm khách hàng)
- **Dimensionality Reduction**: giảm chiều (PCA, t-SNE)
- **Anomaly Detection**: phát hiện bất thường

### 2.3 Reinforcement Learning (Học tăng cường)
- Agent tương tác với môi trường, nhận reward/punishment
- Học qua thử và sai
- Ví dụ: AlphaGo, self-driving cars, game AI

---

## 3. ML Pipeline

```
1. Define Problem    → Bài toán gì? Metric nào?
2. Collect Data      → Thu thập dữ liệu
3. EDA               → Khám phá, trực quan hóa
4. Preprocess        → Xử lý missing, encoding, scaling
5. Feature Engineer  → Tạo features mới
6. Train Model       → Chọn thuật toán, huấn luyện
7. Evaluate          → Đánh giá trên test set
8. Tune              → Tối ưu hyperparameters
9. Deploy            → Triển khai production
10. Monitor          → Theo dõi performance
```

---

## 4. Bias-Variance Tradeoff

### 4.1 Khái niệm
```
Total Error = Bias² + Variance + Irreducible Noise

Bias cao    → Underfitting: model quá ĐƠN GIẢN, không capture được pattern
Variance cao → Overfitting: model quá PHỨC TẠP, memorize noise trong training data
```

### 4.2 Overfitting vs Underfitting
```python
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Tạo dữ liệu
np.random.seed(42)
X = np.sort(np.random.rand(30, 1) * 10, axis=0)
y = np.sin(X).ravel() + np.random.randn(30) * 0.3

# Underfitting: degree=1 (đường thẳng cho dữ liệu cong)
# Vừa phải:    degree=3
# Overfitting:  degree=15 (quá phức tạp, fit cả noise)

for degree in [1, 3, 15]:
    poly = PolynomialFeatures(degree)
    X_poly = poly.fit_transform(X)
    model = LinearRegression().fit(X_poly, y)
    y_pred = model.predict(X_poly)
    print(f"Degree {degree}: Train MSE = {mean_squared_error(y, y_pred):.4f}")
```

### 4.3 Cách phát hiện & xử lý
| Vấn đề | Dấu hiệu | Giải pháp |
|--------|----------|-----------|
| **Underfitting** | Train error cao, Test error cao | Model phức tạp hơn, thêm features |
| **Overfitting** | Train error thấp, Test error CAO | Regularization, thêm data, dropout |

---

## 5. Train/Validation/Test Split

```python
from sklearn.model_selection import train_test_split

# Split: 60% train, 20% validation, 20% test
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.25, random_state=42)

# Train set:      huấn luyện model
# Validation set:  tune hyperparameters
# Test set:        đánh giá CUỐI CÙNG (chỉ dùng 1 lần!)
```

### Cross-Validation
```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
print(f"CV Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
# Chia data thành 5 fold
# Train 5 lần, mỗi lần 1 fold khác nhau làm validation
# → Đánh giá ổn định hơn
```

---

## 📝 Bài tập

1. Lấy dataset Iris (sklearn), chia train/test, train model đơn giản, đánh giá accuracy
2. Tạo dữ liệu polynomial, fit các model degree khác nhau, vẽ underfitting/overfitting
3. Implement K-Fold Cross Validation từ đầu (không dùng sklearn)
4. Với dataset Titanic: xác định đây là bài toán gì? Metric nào phù hợp? Tại sao?

---

## 📚 Tài liệu
- *Andrew Ng — Machine Learning Specialization* (Coursera) — Week 1-2
- *Hands-On Machine Learning* — Aurélien Géron — Ch. 1-2
