# Bài 15: CNN & Kiến trúc kinh điển

## 🎯 Mục tiêu
- Hiểu Convolution, Pooling — cơ chế cốt lõi của CNN
- Biết các kiến trúc: LeNet → AlexNet → VGG → ResNet → EfficientNet
- Implement CNN trong PyTorch

## 📖 Câu chuyện đời thường
> Hãy tưởng tượng bạn là thám tử xem ảnh hiện trường. Bạn không nhìn cả bức ảnh cùng lúc mà dùng một **kính lúp** (filter/kernel) quét từ góc này sang góc khác: đầu tiên tìm cạnh viền (edges), rồi nhận ra hình dạng (shapes), cuối cùng mới kết luận "có một chiếc xe" — đó chính là cách **CNN** hoạt động: các layer đầu tìm cạnh, layer giữa tìm hình dạng, layer cuối nhận vật thể. **Pooling** giống như bạn lùi ra xa để nhìn bức ảnh nhỏ lại — bỏ bớt chi tiết vụn nhưng vẫn nhận ra đối tượng chính. **ResNet** giải quyết vấn đề "nhìn quá sâu thì quên mất bức tranh tổng thể" bằng cách luôn giữ một bản sao gốc để so sánh.

---

## 1. Convolution Layer

### 1.1 Ý tưởng
```
Ảnh = ma trận pixel. Convolution = trượt filter (kernel) qua ảnh.
Filter phát hiện patterns: edges, textures, shapes → objects

Input (6×6) * Filter (3×3) → Output (4×4)

Filter ví dụ (edge detection):
[-1  0  1]
[-1  0  1]
[-1  0  1]
```

### 1.2 Parameters
```python
import torch.nn as nn

# Conv2D(in_channels, out_channels, kernel_size, stride, padding)
conv = nn.Conv2d(
    in_channels=3,      # RGB ảnh: 3 channels
    out_channels=32,     # 32 filters → 32 feature maps
    kernel_size=3,       # Filter 3×3
    stride=1,            # Bước trượt
    padding=1,           # Padding để giữ kích thước
)
# Output size = (input_size - kernel + 2*padding) / stride + 1

# Pooling — giảm kích thước
pool = nn.MaxPool2d(kernel_size=2, stride=2)  # Giảm 1/2
```

---

## 2. CNN cơ bản cho CIFAR-10
```python
class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            # Block 1: 3→32 channels, 32×32→16×16
            nn.Conv2d(3, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            # Block 2: 32→64 channels, 16×16→8×8
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.Conv2d(64, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2),
            
            # Block 3: 64→128, 8×8→4×4
            nn.Conv2d(64, 128, 3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes),
        )
    
    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x
```

---

## 3. Kiến trúc kinh điển

### 3.1 Tiến hóa
```
LeNet (1998) → AlexNet (2012) → VGGNet (2014) → GoogLeNet (2014)
→ ResNet (2015) → DenseNet (2016) → EfficientNet (2019)
```

### 3.2 ResNet — Kiến trúc quan trọng nhất
```python
# Skip Connection (Residual Connection):
# output = F(x) + x    ← thêm input vào output
# → Giải quyết vanishing gradient, train được mạng rất sâu (152+ layers)

class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.block = nn.Sequential(
            nn.Conv2d(channels, channels, 3, padding=1),
            nn.BatchNorm2d(channels),
            nn.ReLU(),
            nn.Conv2d(channels, channels, 3, padding=1),
            nn.BatchNorm2d(channels),
        )
        self.relu = nn.ReLU()
    
    def forward(self, x):
        residual = x
        out = self.block(x)
        out += residual    # ← SKIP CONNECTION
        return self.relu(out)
```

### 3.3 Sử dụng pretrained models
```python
import torchvision.models as models

# ResNet50 pretrained trên ImageNet
model = models.resnet50(weights='IMAGENET1K_V2')

# EfficientNet B0
model = models.efficientnet_b0(weights='IMAGENET1K_V1')

# Thay classifier cho task của bạn
model.fc = nn.Linear(model.fc.in_features, num_classes)
```

---

## 📝 Bài tập

1. Train CNN từ đầu trên CIFAR-10, đạt >85% accuracy
2. Implement ResidualBlock, xây ResNet-18 mini
3. Transfer learning: Fine-tune ResNet50 cho phân loại hoa (Flowers102)
4. Visualize feature maps/filters của CNN: layer đầu phát hiện gì? layer cuối?

---

## 📚 Tài liệu
- *CS231n: Convolutional Neural Networks* — Stanford
- Paper: *Deep Residual Learning* — He et al. (2015)
- *Dive into Deep Learning* — d2l.ai (Ch. CNN)
