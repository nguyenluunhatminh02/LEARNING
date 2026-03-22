# Bài 13: PyTorch & TensorFlow

## 🎯 Mục tiêu
- Thành thạo PyTorch — framework DL phổ biến nhất
- Hiểu TensorFlow/Keras
- Biết khi nào dùng framework nào

---

## 1. PyTorch — Framework chính

### 1.1 Tensors (tương tự NumPy nhưng chạy trên GPU)
```python
import torch

# Tạo tensor
x = torch.tensor([1.0, 2.0, 3.0])
X = torch.randn(3, 4)                # Random normal
zeros = torch.zeros(2, 3)
ones = torch.ones(2, 3)

# Chuyển NumPy ↔ Tensor
import numpy as np
np_array = np.array([1, 2, 3])
tensor = torch.from_numpy(np_array)
back_to_np = tensor.numpy()

# GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
X_gpu = X.to(device)
```

### 1.2 Autograd — Tự động tính gradient
```python
# Autograd = backpropagation tự động!
x = torch.tensor(3.0, requires_grad=True)
y = x**2 + 2*x + 1  # y = x² + 2x + 1

y.backward()          # Tính gradient
print(x.grad)         # dy/dx = 2x + 2 = 8.0
```

### 1.3 Xây dựng Neural Network
```python
import torch.nn as nn

class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, num_classes),
        )
    
    def forward(self, x):
        return self.network(x)

model = SimpleNN(784, 128, 10).to(device)
print(model)
```

### 1.4 Training Loop — Pattern quan trọng nhất
```python
from torch.utils.data import DataLoader, TensorDataset
from torchvision import datasets, transforms

# Data
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])
train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

# Model, Loss, Optimizer
model = SimpleNN(784, 128, 10).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Training Loop
def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss = 0
    correct = 0
    total = 0
    
    for batch_X, batch_y in loader:
        batch_X = batch_X.view(-1, 784).to(device)
        batch_y = batch_y.to(device)
        
        # Forward
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        
        # Backward
        optimizer.zero_grad()  # Reset gradients
        loss.backward()        # Tính gradients
        optimizer.step()       # Cập nhật weights
        
        total_loss += loss.item() * batch_X.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(batch_y).sum().item()
        total += batch_y.size(0)
    
    return total_loss / total, correct / total

# Validation
@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0
    correct = 0
    total = 0
    
    for batch_X, batch_y in loader:
        batch_X = batch_X.view(-1, 784).to(device)
        batch_y = batch_y.to(device)
        
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        
        total_loss += loss.item() * batch_X.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(batch_y).sum().item()
        total += batch_y.size(0)
    
    return total_loss / total, correct / total

# Main training
for epoch in range(10):
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
    val_loss, val_acc = evaluate(model, val_loader, criterion, device)
    print(f"Epoch {epoch+1}: Train Loss={train_loss:.4f} Acc={train_acc:.4f} | "
          f"Val Loss={val_loss:.4f} Acc={val_acc:.4f}")
```

### 1.5 Save & Load Model
```python
# Save
torch.save(model.state_dict(), 'model.pth')

# Load
model = SimpleNN(784, 128, 10)
model.load_state_dict(torch.load('model.pth'))
model.eval()
```

---

## 2. TensorFlow / Keras

### 2.1 Keras Sequential API (nhanh nhất)
```python
import tensorflow as tf
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(10, activation='softmax'),
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.fit(X_train, y_train, 
          epochs=10, batch_size=64, 
          validation_split=0.2,
          callbacks=[keras.callbacks.EarlyStopping(patience=3)])

model.evaluate(X_test, y_test)
```

---

## 3. So sánh

| | PyTorch | TensorFlow/Keras |
|---|---------|-----------------|
| Style | Pythonic, linh hoạt | Higher-level API |
| Debug | Dễ (eager execution) | Dễ (eager default) |
| Research | ✅ Phổ biến nhất | Ít hơn |
| Production | TorchServe, ONNX | TF Serving, TFLite |
| **Khuyến nghị** | **Học PyTorch trước** | Biết cơ bản |

---

## 📝 Bài tập

1. **MNIST Classification**: train model đạt >98% accuracy bằng PyTorch
2. **Custom Dataset**: tạo Dataset class cho bộ dữ liệu ảnh của bạn
3. So sánh PyTorch vs Keras: cùng architecture, cùng hyperparameters, so kết quả
4. **Fashion-MNIST**: phân loại quần áo, thử các architectures khác nhau

---

## 📚 Tài liệu
- [PyTorch Official Tutorials](https://pytorch.org/tutorials/)
- [PyTorch Lightning](https://lightning.ai/) — simplified training
- *fast.ai — Practical Deep Learning for Coders*
