# Bài 07: Linear & Polynomial Regression

## 🎯 Mục tiêu
- Implement Linear Regression từ đầu
- Hiểu Loss function, Normal Equation, Gradient Descent
- Regularization: Ridge, Lasso, Elastic Net

## 📖 Câu chuyện đời thường
> Bạn muốn dự đoán giá nhà ở Quận 7. Bạn biết rằng diện tích càng lớn thì giá càng cao, nhưng bao nhiêu? Bạn lấy dữ liệu 50 căn nhà đã bán, vẽ lên giấy: trục x là diện tích, trục y là giá. Rồi kẻ một đường thẳng "vừa vặn nhất" xuyên qua các điểm — đó chính là **Linear Regression**. Đường thẳng này cho bạn biết: "căn nhà 80m² có lẽ giá khoảng 5 tỷ". **Regularization** giống như bạn tự nhắc mình: "đừng tin quá vào dữ liệu, có căn nào giá bất thường do chủ nhà nóng vội bán" — giúp đường dự đoán không bị "ngoằn nghoèo" vì dữ liệu nhiễu.

---

## 1. Linear Regression

### 1.1 Mô hình
```
ŷ = w₁x₁ + w₂x₂ + ... + wₙxₙ + b
ŷ = X @ W + b    (dạng ma trận)

Mục tiêu: tìm W, b sao cho ŷ gần y nhất
```

### 1.2 Loss Function — Mean Squared Error
```python
# MSE = (1/n) * Σ(yᵢ - ŷᵢ)²
def mse_loss(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)
```

### 1.3 Cách 1: Normal Equation (Closed-form solution)
```python
import numpy as np

class LinearRegressionNormal:
    """Linear Regression bằng Normal Equation: W = (XᵀX)⁻¹Xᵀy"""
    
    def fit(self, X, y):
        # Thêm cột 1 cho bias
        X_b = np.c_[np.ones(len(X)), X]
        # W = (XᵀX)⁻¹ Xᵀ y
        self.W = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y
        return self
    
    def predict(self, X):
        X_b = np.c_[np.ones(len(X)), X]
        return X_b @ self.W

# Test
np.random.seed(42)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X.ravel() + np.random.randn(100) * 0.5  # y = 4 + 3x + noise

model = LinearRegressionNormal().fit(X, y)
print(f"Intercept ≈ {model.W[0]:.2f}, Slope ≈ {model.W[1]:.2f}")
# → Intercept ≈ 4.0, Slope ≈ 3.0
```

### 1.4 Cách 2: Gradient Descent
```python
class LinearRegressionGD:
    def __init__(self, lr=0.01, epochs=1000):
        self.lr = lr
        self.epochs = epochs
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.W = np.zeros(n_features)
        self.b = 0
        self.losses = []
        
        for _ in range(self.epochs):
            y_pred = X @ self.W + self.b
            
            # Gradients
            dW = (2/n_samples) * X.T @ (y_pred - y)
            db = (2/n_samples) * np.sum(y_pred - y)
            
            # Update
            self.W -= self.lr * dW
            self.b -= self.lr * db
            
            self.losses.append(mse_loss(y, y_pred))
        return self
    
    def predict(self, X):
        return X @ self.W + self.b
```

---

## 2. Polynomial Regression
```python
from sklearn.preprocessing import PolynomialFeatures

# Dữ liệu phi tuyến
X = np.sort(np.random.rand(50, 1) * 6, axis=0)
y = np.sin(X).ravel() + np.random.randn(50) * 0.2

# Mở rộng features: x → [1, x, x², x³]
poly = PolynomialFeatures(degree=3)
X_poly = poly.fit_transform(X)  # shape: (50, 4)

# Fit Linear Regression trên features mới
from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X_poly, y)
```

---

## 3. Regularization — Chống Overfitting

### 3.1 Ridge Regression (L2)
```python
# Loss = MSE + α * Σwᵢ²
# → Giảm magnitude của weights, KHÔNG đưa về 0

from sklearn.linear_model import Ridge

ridge = Ridge(alpha=1.0)  # alpha = strength of regularization
ridge.fit(X_train, y_train)
```

### 3.2 Lasso Regression (L1)
```python
# Loss = MSE + α * Σ|wᵢ|
# → Có thể đưa weights về 0 → Feature selection!

from sklearn.linear_model import Lasso

lasso = Lasso(alpha=0.1)
lasso.fit(X_train, y_train)
print(f"Non-zero features: {np.sum(lasso.coef_ != 0)} / {len(lasso.coef_)}")
```

### 3.3 Elastic Net (L1 + L2)
```python
from sklearn.linear_model import ElasticNet

elastic = ElasticNet(alpha=0.1, l1_ratio=0.5)  # 50% L1 + 50% L2
elastic.fit(X_train, y_train)
```

---

## 4. Đánh giá Regression

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)          # Mean Squared Error
rmse = np.sqrt(mse)                                # Root MSE (cùng đơn vị với y)
mae = mean_absolute_error(y_test, y_pred)          # Mean Absolute Error
r2 = r2_score(y_test, y_pred)                      # R² ∈ [0,1], 1 = perfect

print(f"RMSE: {rmse:.4f}")
print(f"MAE:  {mae:.4f}")
print(f"R²:   {r2:.4f}")
```

---

## 📝 Bài tập

1. Implement Linear Regression bằng GD từ đầu, vẽ loss curve
2. Dataset California Housing (sklearn): dự đoán giá nhà
   - EDA, xử lý missing data
   - So sánh Linear vs Ridge vs Lasso
   - Tìm alpha tốt nhất bằng Cross Validation
3. Với Polynomial Regression: vẽ đồ thị degree 1, 3, 5, 10, 20 → thấy overfitting
4. Implement Ridge Regression từ đầu bằng Normal Equation có regularization

---

## 📚 Tài liệu
- *Andrew Ng ML Specialization* — Week 1-2 (Regression)
- *Hands-On ML* — Ch. 4 (Training Models)
