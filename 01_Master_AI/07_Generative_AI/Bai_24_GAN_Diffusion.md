# Bài 24: GAN & Diffusion Models

## 🎯 Mục tiêu
- Hiểu GAN: Generator vs Discriminator
- Hiểu Diffusion Models & Stable Diffusion
- Sinh ảnh bằng cả 2 phương pháp

---

## 1. GAN (Generative Adversarial Network)

### 1.1 Ý tưởng
```
Generator (G):     tạo fake data từ noise → cố gắng lừa Discriminator
Discriminator (D): phân biệt real vs fake → cố gắng "bắt" Generator

G và D "đấu" với nhau → cả 2 ngày càng giỏi hơn
→ Cuối cùng G tạo data gần như thật
```

### 1.2 DCGAN Implementation
```python
import torch
import torch.nn as nn

class Generator(nn.Module):
    def __init__(self, latent_dim=100, img_channels=1):
        super().__init__()
        self.net = nn.Sequential(
            # latent_dim → 7×7×256
            nn.Linear(latent_dim, 256 * 7 * 7),
            nn.BatchNorm1d(256 * 7 * 7),
            nn.ReLU(),
            nn.Unflatten(1, (256, 7, 7)),
            
            # 7×7 → 14×14
            nn.ConvTranspose2d(256, 128, 4, 2, 1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            
            # 14×14 → 28×28
            nn.ConvTranspose2d(128, img_channels, 4, 2, 1),
            nn.Tanh(),  # Output ∈ [-1, 1]
        )
    
    def forward(self, z):
        return self.net(z)

class Discriminator(nn.Module):
    def __init__(self, img_channels=1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(img_channels, 64, 4, 2, 1),
            nn.LeakyReLU(0.2),
            nn.Conv2d(64, 128, 4, 2, 1),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2),
            nn.Flatten(),
            nn.Linear(128 * 7 * 7, 1),
            nn.Sigmoid(),
        )
    
    def forward(self, x):
        return self.net(x)

# Training loop
G = Generator().to(device)
D = Discriminator().to(device)
criterion = nn.BCELoss()
opt_G = torch.optim.Adam(G.parameters(), lr=0.0002, betas=(0.5, 0.999))
opt_D = torch.optim.Adam(D.parameters(), lr=0.0002, betas=(0.5, 0.999))

for epoch in range(epochs):
    for real_images, _ in dataloader:
        batch_size = real_images.size(0)
        real_images = real_images.to(device)
        
        # Train Discriminator
        z = torch.randn(batch_size, 100).to(device)
        fake_images = G(z)
        
        real_loss = criterion(D(real_images), torch.ones(batch_size, 1).to(device))
        fake_loss = criterion(D(fake_images.detach()), torch.zeros(batch_size, 1).to(device))
        d_loss = (real_loss + fake_loss) / 2
        
        opt_D.zero_grad()
        d_loss.backward()
        opt_D.step()
        
        # Train Generator
        z = torch.randn(batch_size, 100).to(device)
        fake_images = G(z)
        g_loss = criterion(D(fake_images), torch.ones(batch_size, 1).to(device))
        
        opt_G.zero_grad()
        g_loss.backward()
        opt_G.step()
```

---

## 2. Diffusion Models

### 2.1 Ý tưởng
```
Forward process:  ảnh gốc → thêm noise dần dần → noise thuần
Reverse process:  noise thuần → denoise dần dần → ảnh mới

Model học cách "khử noise" → từ random noise → sinh ảnh mới
Ưu: chất lượng tốt hơn GAN, training ổn định hơn
```

### 2.2 Stable Diffusion
```python
from diffusers import StableDiffusionPipeline
import torch

# Load model
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
).to("cuda")

# Generate
image = pipe(
    prompt="A beautiful sunset over mountains, oil painting style",
    num_inference_steps=50,
    guidance_scale=7.5,  # CFG: higher = closer to prompt
).images[0]

image.save("generated.png")
```

### 2.3 ControlNet — Kiểm soát output
```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel

# Dùng edge map để kiểm soát layout
controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny")
pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", controlnet=controlnet
)
```

---

## 📝 Bài tập

1. Train DCGAN generate MNIST digits
2. Dùng Stable Diffusion sinh ảnh theo prompts khác nhau
3. Fine-tune Stable Diffusion với LoRA cho style riêng (5-10 ảnh)
4. So sánh GAN vs Diffusion: chất lượng, tốc độ, diversity

---

## 📚 Tài liệu
- *Lilian Weng: What are Diffusion Models?* (blog)
- Paper: *Denoising Diffusion Probabilistic Models* (DDPM)
- [Hugging Face Diffusers Documentation](https://huggingface.co/docs/diffusers/)
