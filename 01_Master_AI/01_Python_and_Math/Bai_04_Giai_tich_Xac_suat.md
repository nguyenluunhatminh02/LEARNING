# Bài 04: Giải tích & Xác suất Thống kê cho AI

## 🎯 Mục tiêu
- Hiểu đạo hàm, gradient — nền tảng của backpropagation
- Hiểu xác suất, phân phối — nền tảng của nhiều thuật toán ML
- Liên kết toán học với ứng dụng thực tế trong AI

---

## PHẦN 1: Giải tích (Calculus)

### 1.1 Đạo hàm — Tốc độ thay đổi
```
f'(x) = lim[h→0] (f(x+h) - f(x)) / h
```

**Tại sao cần trong AI?**
- Đạo hàm = hướng thay đổi nhanh nhất của hàm
- Training AI = tìm minimum của loss function = đi ngược hướng đạo hàm

```python
import numpy as np

# Đạo hàm số (numerical derivative)
def numerical_derivative(f, x, h=1e-7):
    return (f(x + h) - f(x - h)) / (2 * h)

# Ví dụ
f = lambda x: x**2 + 3*x + 1
print(numerical_derivative(f, 2))  # ≈ 7.0 (f'(x) = 2x + 3, f'(2) = 7)
```

### 1.2 Đạo hàm riêng (Partial Derivative)
Khi hàm có nhiều biến, đạo hàm theo từng biến:

```
f(x, y) = x² + 2xy + y²
∂f/∂x = 2x + 2y    (giữ y cố định)
∂f/∂y = 2x + 2y    (giữ x cố định)
```

**Trong ML**: Loss function phụ thuộc vào NHIỀU weights → đạo hàm riêng theo mỗi weight.

### 1.3 Gradient — Vector đạo hàm riêng
```
∇f = [∂f/∂w₁, ∂f/∂w₂, ..., ∂f/∂wₙ]
```

Gradient chỉ **hướng tăng nhanh nhất** → đi ngược gradient = **giảm nhanh nhất**.

```python
# Gradient descent đơn giản
def gradient_descent(f_grad, x_init, lr=0.01, epochs=100):
    """
    f_grad: function trả về gradient tại x
    x_init: điểm bắt đầu
    lr: learning rate
    """
    x = x_init.copy()
    history = [x.copy()]
    
    for _ in range(epochs):
        grad = f_grad(x)
        x = x - lr * grad  # CẬP NHẬT: đi ngược gradient
        history.append(x.copy())
    
    return x, history

# Ví dụ: minimize f(x,y) = x² + y²
f_grad = lambda x: 2 * x  # gradient = [2x, 2y]
x_optimal, history = gradient_descent(f_grad, np.array([5.0, 3.0]), lr=0.1)
print(f"Optimal: {x_optimal}")  # ≈ [0, 0]
```

### 1.4 Chain Rule — Nền tảng của Backpropagation
```
Nếu y = f(g(x)), thì dy/dx = f'(g(x)) * g'(x)
```

**Neural network**: output = f₃(f₂(f₁(x)))
Backpropagation dùng Chain Rule để tính gradient qua nhiều layers.

```python
# Ví dụ chain rule trong neural network
# Forward: z = w*x + b → a = sigmoid(z) → loss = (a - y)²

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sigmoid_derivative(z):
    s = sigmoid(z)
    return s * (1 - s)

# Forward pass
x, y = 2.0, 1.0
w, b = 0.5, 0.1

z = w * x + b           # z = 1.1
a = sigmoid(z)           # a ≈ 0.75
loss = (a - y) ** 2      # loss ≈ 0.063

# Backward pass (Chain Rule)
dloss_da = 2 * (a - y)                    # ∂loss/∂a
da_dz = sigmoid_derivative(z)              # ∂a/∂z
dz_dw = x                                  # ∂z/∂w
dz_db = 1                                  # ∂z/∂b

dloss_dw = dloss_da * da_dz * dz_dw       # ∂loss/∂w (chain rule!)
dloss_db = dloss_da * da_dz * dz_db       # ∂loss/∂b

# Update weights
lr = 0.1
w -= lr * dloss_dw
b -= lr * dloss_db
```

---

## PHẦN 2: Xác suất & Thống kê

### 2.1 Xác suất cơ bản
```
P(A) ∈ [0, 1]
P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
P(A|B) = P(A ∩ B) / P(B)    ← Xác suất có điều kiện
```

### 2.2 Định lý Bayes — Cốt lõi của nhiều thuật toán ML
```
P(A|B) = P(B|A) * P(A) / P(B)

Trong ML:
P(class|data) = P(data|class) * P(class) / P(data)
  posterior    =  likelihood  *   prior   / evidence
```

```python
# Ví dụ: Spam filter (Naive Bayes)
# P(spam|"free money") = P("free money"|spam) * P(spam) / P("free money")

# Giả sử:
P_spam = 0.3                    # 30% email là spam
P_free_money_given_spam = 0.8   # 80% spam chứa "free money"
P_free_money_given_ham = 0.05   # 5% email thường chứa "free money"

P_free_money = P_free_money_given_spam * P_spam + P_free_money_given_ham * (1 - P_spam)
P_spam_given_free_money = P_free_money_given_spam * P_spam / P_free_money
print(f"P(spam|'free money') = {P_spam_given_free_money:.2%}")  # ~87%
```

### 2.3 Phân phối xác suất phổ biến

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# 1. Phân phối Bernoulli: thành công/thất bại
# Ứng dụng: binary classification output
bernoulli = np.random.binomial(1, p=0.7, size=1000)

# 2. Phân phối Gaussian (Normal) — QUAN TRỌNG NHẤT
# Ứng dụng: weight initialization, noise, data distribution
mu, sigma = 0, 1
gaussian = np.random.normal(mu, sigma, size=10000)

# 3. Phân phối Uniform
# Ứng dụng: random initialization, data augmentation
uniform = np.random.uniform(low=0, high=1, size=1000)

# 4. Phân phối Poisson
# Ứng dụng: đếm sự kiện (clicks/second, errors/day)
poisson = np.random.poisson(lam=5, size=1000)

# Plot
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0,0].hist(bernoulli, bins=3, edgecolor='black'); axes[0,0].set_title('Bernoulli')
axes[0,1].hist(gaussian, bins=50, edgecolor='black'); axes[0,1].set_title('Gaussian')
axes[1,0].hist(uniform, bins=30, edgecolor='black');  axes[1,0].set_title('Uniform')
axes[1,1].hist(poisson, bins=20, edgecolor='black');  axes[1,1].set_title('Poisson')
plt.tight_layout()
plt.show()
```

### 2.4 Kỳ vọng, Phương sai, Hiệp phương sai

```python
data = np.random.randn(1000)

# Kỳ vọng (Mean): giá trị trung bình
E_X = np.mean(data)

# Phương sai (Variance): mức độ phân tán
Var_X = np.var(data)    # E[(X - μ)²]

# Độ lệch chuẩn (Standard Deviation)
Std_X = np.std(data)    # sqrt(Var)

# Hiệp phương sai (Covariance): mối quan hệ giữa 2 biến
X = np.random.randn(1000)
Y = 2 * X + np.random.randn(1000) * 0.5  # Y phụ thuộc X
Cov_XY = np.cov(X, Y)  # Ma trận hiệp phương sai

# Hệ số tương quan (Correlation): [-1, 1]
Corr_XY = np.corrcoef(X, Y)  # Gần 1 → tương quan dương mạnh
```

### 2.5 Maximum Likelihood Estimation (MLE)

```python
# MLE: tìm tham số θ sao cho P(data|θ) lớn nhất
# Log-likelihood: log P(data|θ) → maximize

# Ví dụ: ước lượng μ, σ của phân phối Gaussian
data = np.random.normal(loc=5, scale=2, size=1000)

# MLE cho Gaussian
mu_mle = np.mean(data)      # MLE of μ = sample mean
sigma_mle = np.std(data)    # MLE of σ = sample std

print(f"True: μ=5, σ=2")
print(f"MLE:  μ={mu_mle:.2f}, σ={sigma_mle:.2f}")
```

### 2.6 Entropy & Cross-Entropy — Dùng trong Loss Function

```python
# Entropy: đo lượng thông tin / sự không chắc chắn
# H(p) = -Σ p(x) * log(p(x))
def entropy(probs):
    return -np.sum(probs * np.log(probs + 1e-10))

# Cross-Entropy: đo khoảng cách giữa 2 phân phối
# H(p, q) = -Σ p(x) * log(q(x))
# → Loss function cho classification!
def cross_entropy(y_true, y_pred):
    return -np.sum(y_true * np.log(y_pred + 1e-10))

# Binary Cross-Entropy
def binary_cross_entropy(y_true, y_pred):
    return -np.mean(y_true * np.log(y_pred + 1e-10) + 
                    (1 - y_true) * np.log(1 - y_pred + 1e-10))
```

---

## 📝 Bài tập

1. Implement gradient descent cho f(x,y) = (x-3)² + (y-2)², vẽ trajectory
2. Implement Naive Bayes classifier từ đầu cho spam detection
3. Generate 1000 data points từ Gaussian mixture (2 clusters), vẽ histogram
4. Implement binary cross-entropy loss, so sánh kết quả với sklearn
5. Chứng minh MLE cho Gaussian distribution cho ra μ = sample mean

---

## 📚 Tài liệu
- *3Blue1Brown: Essence of Calculus* — Video series
- *Khan Academy: Statistics & Probability* — Khóa học miễn phí
- *Mathematics for Machine Learning* — Ch. 5-6 (Probability)
- *Information Theory, Inference, and Learning Algorithms* — David MacKay
