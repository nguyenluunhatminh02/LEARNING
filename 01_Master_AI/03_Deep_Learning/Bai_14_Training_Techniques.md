# Bài 14: Kỹ thuật huấn luyện nâng cao

## 🎯 Mục tiêu
- Regularization: Dropout, Batch Norm, Weight Decay
- Data Augmentation
- Transfer Learning
- Mixed Precision Training

---

## 1. Regularization

### 1.1 Dropout
```python
import torch.nn as nn

# Randomly "tắt" neurons khi training → giảm overfitting
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(0.5),    # 50% neurons bị tắt mỗi forward pass
    nn.Linear(256, 128),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(128, 10),
)

# QUAN TRỌNG: tắt dropout khi inference
model.train()   # Dropout active
model.eval()    # Dropout OFF
```

### 1.2 Batch Normalization
```python
# Normalize activation ở mỗi layer → training ổn định, nhanh hơn
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.BatchNorm1d(256),  # Normalize → learn scale & shift
    nn.ReLU(),
    nn.Linear(256, 128),
    nn.BatchNorm1d(128),
    nn.ReLU(),
    nn.Linear(128, 10),
)
# BatchNorm1d cho fully connected
# BatchNorm2d cho CNN
```

### 1.3 Weight Decay (L2 Regularization)
```python
# Thêm penalty cho weights lớn
optimizer = torch.optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
# AdamW > Adam khi dùng weight decay
```

---

## 2. Data Augmentation
```python
from torchvision import transforms

# Tạo variations của ảnh → tăng data, giảm overfitting
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(15),
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

# Validation: KHÔNG augment, chỉ resize + normalize
val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])
```

---

## 3. Learning Rate Scheduling
```python
from torch.optim.lr_scheduler import CosineAnnealingLR, OneCycleLR, StepLR

optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Cosine Annealing: lr giảm dần theo cosine
scheduler = CosineAnnealingLR(optimizer, T_max=100, eta_min=1e-6)

# OneCycleLR: warmup → max → anneal (phổ biến cho super-convergence)
scheduler = OneCycleLR(optimizer, max_lr=0.01, total_steps=num_epochs * len(train_loader))

# Trong training loop:
for epoch in range(num_epochs):
    for batch in train_loader:
        # ... train step ...
        scheduler.step()  # Cập nhật lr sau mỗi batch (OneCycleLR)
    # scheduler.step()    # Hoặc sau mỗi epoch (CosineAnnealing)
```

---

## 4. Transfer Learning — KỸ THUẬT MẠNH NHẤT

```python
import torchvision.models as models

# Load pretrained model (đã train trên ImageNet)
model = models.resnet50(pretrained=True)

# Freeze tất cả layers
for param in model.parameters():
    param.requires_grad = False

# Thay thế classifier cuối
model.fc = nn.Sequential(
    nn.Linear(2048, 256),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(256, num_classes),  # Số classes của bạn
)

# Chỉ train classifier mới
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)

# Fine-tuning: unfreeze một số layers cuối sau vài epochs
for param in model.layer4.parameters():
    param.requires_grad = True
```

---

## 5. Gradient Clipping & Accumulation
```python
# Gradient Clipping: tránh exploding gradients
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)

# Gradient Accumulation: simulate batch lớn hơn
accumulation_steps = 4
for i, (X, y) in enumerate(train_loader):
    loss = criterion(model(X), y) / accumulation_steps
    loss.backward()
    
    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

---

## 6. Early Stopping
```python
class EarlyStopping:
    def __init__(self, patience=5, min_delta=0):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_loss = None
    
    def __call__(self, val_loss):
        if self.best_loss is None:
            self.best_loss = val_loss
        elif val_loss > self.best_loss - self.min_delta:
            self.counter += 1
            if self.counter >= self.patience:
                return True  # Stop training
        else:
            self.best_loss = val_loss
            self.counter = 0
        return False

early_stop = EarlyStopping(patience=5)
for epoch in range(100):
    val_loss = evaluate(model, val_loader)
    if early_stop(val_loss):
        print(f"Early stopping at epoch {epoch}")
        break
```

---

## 📝 Bài tập

1. **CIFAR-10 Classification**:
   - Train from scratch vs Transfer Learning (ResNet18)
   - So sánh accuracy, thời gian training
2. **Flowers102 Dataset**: Fine-tune pretrained model đạt >90% accuracy
3. Thử các augmentation strategies khác nhau, đo impact lên accuracy
4. Implement training loop hoàn chỉnh với: scheduler, early stopping, best model saving

---

## 📚 Tài liệu
- *fast.ai — Practical Deep Learning*
- *PyTorch Lightning Documentation*
- *Weights & Biases (wandb) — Experiment Tracking*
