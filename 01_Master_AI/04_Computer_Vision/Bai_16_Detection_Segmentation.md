# Bài 16: Object Detection & Segmentation

## 🎯 Mục tiêu
- Hiểu Object Detection: YOLO, Faster R-CNN
- Hiểu Image Segmentation: U-Net, Mask R-CNN
- Thực hành với Ultralytics YOLOv8

---

## 1. Object Detection

### 1.1 Khác biệt với Classification
```
Classification: ảnh chứa gì?        → "cat"
Detection:      ở đâu, là gì?       → "cat at (x1,y1,x2,y2)"
Segmentation:   pixel nào thuộc gì?  → mask cho từng object
```

### 1.2 Metrics
```python
# IoU (Intersection over Union)
def iou(box1, box2):
    """box format: [x1, y1, x2, y2]"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    
    intersection = max(0, x2-x1) * max(0, y2-y1)
    area1 = (box1[2]-box1[0]) * (box1[3]-box1[1])
    area2 = (box2[2]-box2[0]) * (box2[3]-box2[1])
    union = area1 + area2 - intersection
    
    return intersection / (union + 1e-6)

# mAP (mean Average Precision): metric chính
# AP@50: IoU threshold = 0.5
# AP@75: IoU threshold = 0.75
```

### 1.3 YOLO — You Only Look Once
```python
# Cài đặt
# pip install ultralytics

from ultralytics import YOLO

# Load pretrained model
model = YOLO('yolov8n.pt')  # n=nano, s=small, m=medium, l=large, x=extra-large

# Inference
results = model('image.jpg')
results[0].show()

# Xem detections
for box in results[0].boxes:
    cls = int(box.cls)
    conf = float(box.conf)
    x1, y1, x2, y2 = box.xyxy[0].tolist()
    print(f"Class: {model.names[cls]}, Conf: {conf:.2f}, Box: [{x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f}]")

# Train custom model
model.train(
    data='dataset.yaml',   # Path to dataset config
    epochs=100,
    imgsz=640,
    batch=16,
)
```

### 1.4 Dataset YAML format (YOLO)
```yaml
# dataset.yaml
path: /path/to/dataset
train: images/train
val: images/val

names:
  0: cat
  1: dog
  2: bird
```

---

## 2. Image Segmentation

### 2.1 U-Net — Kiến trúc phổ biến nhất cho segmentation
```python
class UNet(nn.Module):
    """
    Encoder (downsampling) → Bottleneck → Decoder (upsampling)
    Skip connections giữa encoder và decoder
    """
    def __init__(self, in_channels=3, num_classes=1):
        super().__init__()
        # Encoder
        self.enc1 = self._block(in_channels, 64)
        self.enc2 = self._block(64, 128)
        self.enc3 = self._block(128, 256)
        
        self.pool = nn.MaxPool2d(2)
        
        # Bottleneck
        self.bottleneck = self._block(256, 512)
        
        # Decoder
        self.up3 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.dec3 = self._block(512, 256)  # 256 + 256 (skip)
        self.up2 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.dec2 = self._block(256, 128)
        self.up1 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.dec1 = self._block(128, 64)
        
        self.final = nn.Conv2d(64, num_classes, 1)
    
    def _block(self, in_c, out_c):
        return nn.Sequential(
            nn.Conv2d(in_c, out_c, 3, padding=1), nn.BatchNorm2d(out_c), nn.ReLU(),
            nn.Conv2d(out_c, out_c, 3, padding=1), nn.BatchNorm2d(out_c), nn.ReLU(),
        )
    
    def forward(self, x):
        # Encoder
        e1 = self.enc1(x)
        e2 = self.enc2(self.pool(e1))
        e3 = self.enc3(self.pool(e2))
        
        # Bottleneck
        b = self.bottleneck(self.pool(e3))
        
        # Decoder + skip connections
        d3 = self.dec3(torch.cat([self.up3(b), e3], dim=1))
        d2 = self.dec2(torch.cat([self.up2(d3), e2], dim=1))
        d1 = self.dec1(torch.cat([self.up1(d2), e1], dim=1))
        
        return self.final(d1)
```

---

## 3. Segmentation với YOLO
```python
# Instance segmentation
model = YOLO('yolov8n-seg.pt')
results = model('image.jpg')

# Pose estimation
model = YOLO('yolov8n-pose.pt')
results = model('image.jpg')
```

---

## 📝 Bài tập

1. **Object Detection**: Train YOLOv8 trên custom dataset (label bằng Roboflow)
2. **Semantic Segmentation**: Train U-Net trên PASCAL VOC hoặc Cityscapes
3. **Real-time Detection**: viết script detect objects từ webcam bằng YOLO
4. **Medical Imaging**: Segment tế bào/khối u từ ảnh X-ray

---

## 📚 Tài liệu
- [Ultralytics YOLOv8 Docs](https://docs.ultralytics.com/)
- Paper: *U-Net: Convolutional Networks for Biomedical Image Segmentation*
- *Dive into Deep Learning* — Object Detection chapters
