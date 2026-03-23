# Bài 17: Vision Transformers (ViT)

## 🎯 Mục tiêu
- Hiểu ViT architecture: ảnh → patches → transformer
- So sánh CNN vs ViT
- Sử dụng pretrained ViT

## 📖 Câu chuyện đời thường
> Trước đây, để đọc một bức tranh lớn, bạn dùng kính lúp quét từ trái sang phải (CNN). Nhưng **ViT** làm khác: nó **cắt bức tranh thành nhiều mảnh nhỏ** (patches), rồi nhìn tất cả các mảnh cùng lúc và tự hỏi: "mảnh nào liên quan đến mảnh nào?" (self-attention). Giống như khi bạn xem một bản đồ thành phố — bạn không đọc từ góc trái sang phải, mà mắt bạn nhảy giữa các khu vực để hiểu mối quan hệ: "bệnh viện gần trường học, công viên xa khu công nghiệp". ViT làm được điều này vì nó kế thừa sức mạnh từ Transformer — công nghệ đã cách mạng NLP.

---

## 1. Vision Transformer Architecture

### 1.1 Ý tưởng
```
CNN: dùng convolution filters trượt qua ảnh
ViT: chia ảnh thành patches, xem mỗi patch như 1 "token" (giống NLP)
     → đưa vào Transformer encoder

Ảnh 224×224 → 196 patches (16×16 mỗi patch) → Transformer → Classification
```

### 1.2 Implementation đơn giản
```python
import torch
import torch.nn as nn

class VisionTransformer(nn.Module):
    def __init__(self, img_size=224, patch_size=16, in_channels=3,
                 embed_dim=768, num_heads=12, num_layers=12, num_classes=1000):
        super().__init__()
        num_patches = (img_size // patch_size) ** 2  # 196
        
        # Patch Embedding: flatten patches → linear projection
        self.patch_embed = nn.Conv2d(in_channels, embed_dim, 
                                     kernel_size=patch_size, stride=patch_size)
        
        # CLS token + Position embeddings
        self.cls_token = nn.Parameter(torch.randn(1, 1, embed_dim))
        self.pos_embed = nn.Parameter(torch.randn(1, num_patches + 1, embed_dim))
        
        # Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim, nhead=num_heads,
            dim_feedforward=embed_dim * 4, activation='gelu',
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Classification head
        self.head = nn.Linear(embed_dim, num_classes)
    
    def forward(self, x):
        B = x.shape[0]
        
        # Patch embedding: (B, 3, 224, 224) → (B, 768, 14, 14) → (B, 196, 768)
        x = self.patch_embed(x).flatten(2).transpose(1, 2)
        
        # Prepend CLS token
        cls = self.cls_token.expand(B, -1, -1)
        x = torch.cat([cls, x], dim=1)  # (B, 197, 768)
        
        # Add position embeddings
        x = x + self.pos_embed
        
        # Transformer
        x = self.transformer(x)
        
        # CLS token output → classification
        return self.head(x[:, 0])
```

---

## 2. Sử dụng Pretrained ViT

```python
import timm

# Load pretrained ViT
model = timm.create_model('vit_base_patch16_224', pretrained=True, num_classes=10)

# Hoặc Swin Transformer (hierarchical, hiệu quả hơn)
model = timm.create_model('swin_base_patch4_window7_224', pretrained=True, num_classes=10)

# Hugging Face
from transformers import ViTForImageClassification
model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')
```

---

## 3. CNN vs ViT

| | CNN | ViT |
|---|-----|-----|
| Inductive bias | Locality, translation invariance | Global attention |
| Data cần | Ít hơn | CẦN RẤT NHIỀU data |
| Small dataset | ✅ Tốt hơn | Kém (trừ khi pretrained) |
| Large dataset | Tốt | ✅ Tốt hơn |
| Khuyến nghị | Data < 100K ảnh | Data > 1M hoặc pretrained |

---

## 📝 Bài tập

1. Fine-tune ViT pretrained trên dataset nhỏ (Flowers102), so sánh với ResNet50
2. Visualize attention maps: ViT "nhìn" vào đâu khi phân loại?
3. Thử Swin Transformer, so sánh với ViT vanilla

---

## 📚 Tài liệu
- Paper: *An Image is Worth 16x16 Words: Transformers for Image Recognition*
- Paper: *Swin Transformer: Hierarchical Vision Transformer*
- [timm library documentation](https://huggingface.co/docs/timm/)
