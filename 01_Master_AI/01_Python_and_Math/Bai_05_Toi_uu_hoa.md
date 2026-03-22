# Bài 05: Tối ưu hóa (Optimization) cho AI

## 🎯 Mục tiêu
- Hiểu Gradient Descent và các biến thể
- Implement optimizer từ đầu
- Biết cách chọn optimizer phù hợp

---

## 1. Gradient Descent

### 1.1 Ý tưởng cốt lõi
```
Training AI = Tìm weights W để minimize Loss function L(W)

Công thức cập nhật:
W_new = W_old - learning_rate × ∇L(W)
        ↓           ↓              ↓
    weights mới   bước nhảy    hướng giảm nhanh nhất
```

### 1.2 Batch Gradient Descent
```python
import numpy as np

def batch_gradient_descent(X, y, lr=0.01, epochs=1000):
    """Dùng TOÀN BỘ dataset để tính gradient mỗi bước"""
    n_samples, n_features = X.shape
    W = np.zeros(n_features)
    b = 0
    losses = []
    
    for epoch in range(epochs):
        # Forward
        y_pred = X @ W + b
        
        # Loss (MSE)
        loss = np.mean((y_pred - y) ** 2)
        losses.append(loss)
        
        # Gradient
        dW = (2/n_samples) * X.T @ (y_pred - y)
        db = (2/n_samples) * np.sum(y_pred - y)
        
        # Update
        W -= lr * dW
        b -= lr * db
    
    return W, b, losses

# Ưu: ổn định, hội tụ mượt
# Nhược: CHẬM khi dataset lớn (tính gradient trên toàn bộ data)
```

### 1.3 Stochastic Gradient Descent (SGD)
```python
def sgd(X, y, lr=0.01, epochs=100):
    """Dùng 1 SAMPLE để tính gradient mỗi bước"""
    n_samples, n_features = X.shape
    W = np.zeros(n_features)
    b = 0
    
    for epoch in range(epochs):
        # Shuffle data
        indices = np.random.permutation(n_samples)
        
        for i in indices:
            xi = X[i:i+1]
            yi = y[i:i+1]
            
            y_pred = xi @ W + b
            dW = 2 * xi.T @ (y_pred - yi)
            db = 2 * (y_pred - yi)
            
            W -= lr * dW.flatten()
            b -= lr * db.item()
    
    return W, b

# Ưu: nhanh, thoát local minima nhờ noise
# Nhược: dao động nhiều, khó hội tụ chính xác
```

### 1.4 Mini-Batch Gradient Descent — ĐƯỢC DÙNG NHIỀU NHẤT
```python
def mini_batch_gd(X, y, lr=0.01, epochs=100, batch_size=32):
    """Dùng batch_size samples để tính gradient"""
    n_samples, n_features = X.shape
    W = np.zeros(n_features)
    b = 0
    
    for epoch in range(epochs):
        indices = np.random.permutation(n_samples)
        
        for start in range(0, n_samples, batch_size):
            end = min(start + batch_size, n_samples)
            batch_idx = indices[start:end]
            
            X_batch = X[batch_idx]
            y_batch = y[batch_idx]
            
            y_pred = X_batch @ W + b
            dW = (2/len(batch_idx)) * X_batch.T @ (y_pred - y_batch)
            db = (2/len(batch_idx)) * np.sum(y_pred - y_batch)
            
            W -= lr * dW
            b -= lr * db
    
    return W, b

# Cân bằng giữa Batch GD và SGD
# batch_size phổ biến: 32, 64, 128, 256
```

---

## 2. Các Optimizer nâng cao

### 2.1 SGD with Momentum
```python
# Ý tưởng: thêm "quán tính" → vượt qua local minima, hội tụ nhanh hơn
# v = β * v + (1-β) * gradient
# W = W - lr * v

class SGDMomentum:
    def __init__(self, lr=0.01, momentum=0.9):
        self.lr = lr
        self.momentum = momentum
        self.velocity = {}
    
    def update(self, params, grads):
        for key in params:
            if key not in self.velocity:
                self.velocity[key] = np.zeros_like(params[key])
            
            self.velocity[key] = (self.momentum * self.velocity[key] + 
                                  (1 - self.momentum) * grads[key])
            params[key] -= self.lr * self.velocity[key]
```

### 2.2 RMSProp
```python
# Ý tưởng: adaptive learning rate cho mỗi parameter
# Scale gradient theo lịch sử: parameters có gradient lớn → lr nhỏ hơn

class RMSProp:
    def __init__(self, lr=0.001, decay=0.99, epsilon=1e-8):
        self.lr = lr
        self.decay = decay
        self.epsilon = epsilon
        self.cache = {}
    
    def update(self, params, grads):
        for key in params:
            if key not in self.cache:
                self.cache[key] = np.zeros_like(params[key])
            
            # Running average of squared gradients
            self.cache[key] = (self.decay * self.cache[key] + 
                              (1 - self.decay) * grads[key]**2)
            
            # Adaptive update
            params[key] -= self.lr * grads[key] / (np.sqrt(self.cache[key]) + self.epsilon)
```

### 2.3 Adam — OPTIMIZER PHỔ BIẾN NHẤT
```python
# Kết hợp Momentum + RMSProp
# = Adaptive learning rate + Momentum

class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.lr = lr
        self.beta1 = beta1    # Momentum decay
        self.beta2 = beta2    # RMSProp decay
        self.epsilon = epsilon
        self.m = {}  # First moment (mean of gradients)
        self.v = {}  # Second moment (mean of squared gradients)
        self.t = 0   # Timestep
    
    def update(self, params, grads):
        self.t += 1
        
        for key in params:
            if key not in self.m:
                self.m[key] = np.zeros_like(params[key])
                self.v[key] = np.zeros_like(params[key])
            
            # Update moments
            self.m[key] = self.beta1 * self.m[key] + (1 - self.beta1) * grads[key]
            self.v[key] = self.beta2 * self.v[key] + (1 - self.beta2) * grads[key]**2
            
            # Bias correction (quan trọng ở bước đầu)
            m_hat = self.m[key] / (1 - self.beta1**self.t)
            v_hat = self.v[key] / (1 - self.beta2**self.t)
            
            # Update params
            params[key] -= self.lr * m_hat / (np.sqrt(v_hat) + self.epsilon)
```

### 2.4 So sánh Optimizers

| Optimizer | Learning Rate | Khi nào dùng |
|-----------|--------------|-------------|
| SGD | Cần tune cẩn thận | Khi muốn generalize tốt (training lâu) |
| SGD + Momentum | Cần tune | CV tasks, khi SGD quá chậm |
| RMSProp | Adaptive | RNN, non-stationary problems |
| **Adam** | **Adaptive** | **Default choice cho hầu hết tasks** |
| AdamW | Adaptive + weight decay | Transformer, LLM training |

---

## 3. Learning Rate — Hyperparameter quan trọng nhất

### 3.1 Learning Rate Scheduling
```python
# 1. Step Decay
def step_decay(epoch, initial_lr=0.1, drop=0.5, epochs_drop=10):
    return initial_lr * (drop ** (epoch // epochs_drop))

# 2. Cosine Annealing — phổ biến nhất
def cosine_annealing(epoch, max_epochs, initial_lr=0.1, min_lr=1e-6):
    return min_lr + 0.5 * (initial_lr - min_lr) * (1 + np.cos(np.pi * epoch / max_epochs))

# 3. Warmup + Cosine (dùng cho Transformer)
def warmup_cosine(epoch, warmup_epochs=5, max_epochs=100, max_lr=0.001):
    if epoch < warmup_epochs:
        return max_lr * epoch / warmup_epochs  # Linear warmup
    else:
        return cosine_annealing(epoch - warmup_epochs, max_epochs - warmup_epochs, max_lr)
```

### 3.2 Learning Rate quá lớn vs quá nhỏ
```
lr quá lớn  → loss dao động, diverge (phát tán)
lr quá nhỏ  → hội tụ rất chậm, stuck ở local minimum
lr vừa phải → hội tụ ổn định đến global minimum
```

---

## 📝 Bài tập

1. Implement Linear Regression bằng Gradient Descent từ đầu, plot loss curve
2. So sánh SGD vs Momentum vs Adam trên cùng 1 bài toán, vẽ trajectory trên contour plot
3. Implement learning rate finder: tăng lr từ nhỏ→lớn, plot loss vs lr để tìm lr tối ưu
4. Tìm minimum của Rosenbrock function: f(x,y) = (1-x)² + 100(y-x²)² bằng Adam

---

## 📚 Tài liệu
- *An overview of gradient descent optimization algorithms* — Sebastian Ruder (blog)
- *CS231n: Optimization* — Stanford
- *Adam: A Method for Stochastic Optimization* — Kingma & Ba (paper gốc)
