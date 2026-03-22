# Bài 12: Neural Network từ đầu

## 🎯 Mục tiêu
- Hiểu cấu trúc Neural Network
- Implement forward & backward propagation bằng NumPy
- Hiểu activation functions & loss functions

---

## 1. Perceptron → Multi-Layer Perceptron

### 1.1 Neuron đơn lẻ
```
Input: x₁, x₂, ..., xₙ
Output: y = activation(w₁x₁ + w₂x₂ + ... + wₙxₙ + b)
       = activation(W · X + b)
```

### 1.2 Activation Functions
```python
import numpy as np

# Sigmoid: output ∈ (0, 1) — dùng cho binary output
def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

# Tanh: output ∈ (-1, 1) — centered ở 0
def tanh(z):
    return np.tanh(z)

# ReLU: output ∈ [0, ∞) — PHỔ BIẾN NHẤT
def relu(z):
    return np.maximum(0, z)

# Leaky ReLU: tránh "dying ReLU"
def leaky_relu(z, alpha=0.01):
    return np.where(z > 0, z, alpha * z)

# Đạo hàm
def sigmoid_derivative(z):
    s = sigmoid(z)
    return s * (1 - s)

def relu_derivative(z):
    return (z > 0).astype(float)
```

---

## 2. Neural Network từ đầu

```python
class NeuralNetwork:
    """
    2-layer neural network: Input → Hidden → Output
    """
    def __init__(self, input_size, hidden_size, output_size, lr=0.01):
        self.lr = lr
        # Xavier initialization
        self.W1 = np.random.randn(input_size, hidden_size) * np.sqrt(2.0 / input_size)
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * np.sqrt(2.0 / hidden_size)
        self.b2 = np.zeros((1, output_size))
    
    def forward(self, X):
        """Forward propagation"""
        # Layer 1
        self.Z1 = X @ self.W1 + self.b1       # Linear
        self.A1 = np.maximum(0, self.Z1)        # ReLU
        
        # Layer 2 (output)
        self.Z2 = self.A1 @ self.W2 + self.b2  # Linear
        self.A2 = sigmoid(self.Z2)               # Sigmoid (binary classification)
        
        return self.A2
    
    def compute_loss(self, y_true, y_pred):
        """Binary Cross-Entropy Loss"""
        m = len(y_true)
        loss = -np.mean(y_true * np.log(y_pred + 1e-10) + 
                       (1 - y_true) * np.log(1 - y_pred + 1e-10))
        return loss
    
    def backward(self, X, y_true):
        """Backpropagation — tính gradient bằng chain rule"""
        m = X.shape[0]
        
        # Output layer gradients
        dZ2 = self.A2 - y_true                     # ∂L/∂Z2
        dW2 = (1/m) * self.A1.T @ dZ2              # ∂L/∂W2
        db2 = (1/m) * np.sum(dZ2, axis=0, keepdims=True)  # ∂L/∂b2
        
        # Hidden layer gradients (chain rule!)
        dA1 = dZ2 @ self.W2.T                      # ∂L/∂A1
        dZ1 = dA1 * (self.Z1 > 0)                  # ∂L/∂Z1 (ReLU derivative)
        dW1 = (1/m) * X.T @ dZ1                    # ∂L/∂W1
        db1 = (1/m) * np.sum(dZ1, axis=0, keepdims=True)  # ∂L/∂b1
        
        # Update weights
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1
    
    def train(self, X, y, epochs=1000, verbose=True):
        losses = []
        for epoch in range(epochs):
            # Forward
            y_pred = self.forward(X)
            loss = self.compute_loss(y, y_pred)
            losses.append(loss)
            
            # Backward
            self.backward(X, y)
            
            if verbose and epoch % 100 == 0:
                acc = np.mean((y_pred > 0.5).astype(int) == y)
                print(f"Epoch {epoch}: Loss={loss:.4f}, Accuracy={acc:.4f}")
        return losses
    
    def predict(self, X):
        return (self.forward(X) > 0.5).astype(int)

# === TEST ===
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split

X, y = make_moons(n_samples=1000, noise=0.2, random_state=42)
y = y.reshape(-1, 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

nn = NeuralNetwork(input_size=2, hidden_size=16, output_size=1, lr=0.1)
losses = nn.train(X_train, y_train, epochs=1000)

y_pred = nn.predict(X_test)
accuracy = np.mean(y_pred == y_test)
print(f"Test Accuracy: {accuracy:.4f}")
```

---

## 3. Backpropagation — Giải thích chi tiết

```
FORWARD:  X → Z1 = XW1+b1 → A1 = relu(Z1) → Z2 = A1W2+b2 → A2 = σ(Z2) → Loss

BACKWARD (Chain Rule):
∂Loss/∂W2 = ∂Loss/∂A2 × ∂A2/∂Z2 × ∂Z2/∂W2
∂Loss/∂W1 = ∂Loss/∂A2 × ∂A2/∂Z2 × ∂Z2/∂A1 × ∂A1/∂Z1 × ∂Z1/∂W1

Mỗi layer: gradient "chảy ngược" qua chain rule
```

---

## 4. Vanishing / Exploding Gradient

```
Vấn đề: gradient nhân qua nhiều layers
- Sigmoid: derivative max = 0.25 → gradient shrinks exponentially
- Deep network: gradient ≈ 0 ở layers đầu → KHÔNG HỌC ĐƯỢC

Giải pháp:
1. Dùng ReLU (derivative = 1 cho z > 0)
2. Proper initialization (Xavier/He)
3. Batch Normalization
4. Residual connections (skip connections)
```

---

## 📝 Bài tập

1. Thêm 1 hidden layer nữa (3-layer NN), test trên make_circles
2. Implement softmax output cho multi-class (MNIST digits)
3. Thêm L2 regularization vào loss và gradient
4. Plot decision boundary của neural network
5. So sánh Sigmoid vs ReLU activation: vẽ loss curve, accuracy

---

## 📚 Tài liệu
- *3Blue1Brown: Neural Networks* — 4 videos (MUST WATCH)
- *CS231n: Backpropagation* — Stanford
- *Michael Nielsen: Neural Networks and Deep Learning* (online book, miễn phí)
