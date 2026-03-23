# Bài 25: Large Language Models (LLM)

## 🎯 Mục tiêu
- Hiểu LLM architecture: GPT, LLaMA
- Tokenization: BPE, SentencePiece
- Train mini-GPT từ đầu (nanoGPT)

## 📖 Câu chuyện đời thường
> Hãy tưởng tượng một người đã đọc **toàn bộ internet** — mọi cuốn sách, mọi bài báo, mọi cuộc trò chuyện. Giờ bạn nói một nửa câu, họ đoán từ tiếp theo dựa trên tất cả những gì đã đọc. Đó là bản chất của **LLM** — dự đoán từ tiếp theo, nhưng vì đã đọc quá nhiều nên có vẻ "hiểu" mọi thứ. **Tokenization** giống như cách bạn bày chữ trong Scrabble: không phải mỗi ô là 1 chữ cái mà có thể là cả một từ hoặc một phần từ (sub-word). Tham số của LLM giống như số synapse trong não — GPT-4 có hàng tỷ "kết nối", nên nó có thể xử lý rất nhiều loại câu hỏi.

---

## 1. LLM Architecture

### 1.1 GPT = Decoder-only Transformer
```
Input tokens → Token Embedding + Position Embedding
→ N × [Masked Self-Attention → Feed-Forward]
→ Output: probability distribution over vocabulary

Pre-training: Next Token Prediction
"The cat sat on the" → "mat"
```

### 1.2 Scaling Laws
```
Performance ∝ f(Model Size, Data Size, Compute)

GPT-2:  1.5B params, 40GB text
GPT-3:  175B params, 570GB text
GPT-4:  ~1.7T params (ước tính), massive data
LLaMA 3: 8B, 70B, 405B params
```

---

## 2. Tokenization

```python
# BPE (Byte-Pair Encoding) — thuật toán chính
# "unhappiness" → ["un", "happiness"] → ["un", "happ", "iness"]

# tiktoken (OpenAI)
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")  # GPT-4 tokenizer
tokens = enc.encode("Hello, how are you?")
print(tokens)       # [9906, 11, 1268, 527, 499, 30]
print(len(tokens))  # 6 tokens

# Hugging Face tokenizer
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")
tokens = tokenizer("Xin chào Việt Nam", return_tensors="pt")
```

---

## 3. Mini-GPT từ đầu (nanoGPT style)

```python
import torch
import torch.nn as nn

class GPTBlock(nn.Module):
    def __init__(self, d_model, num_heads, dropout=0.1):
        super().__init__()
        self.ln1 = nn.LayerNorm(d_model)
        self.attn = nn.MultiheadAttention(d_model, num_heads, dropout=dropout, batch_first=True)
        self.ln2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.GELU(),
            nn.Linear(d_model * 4, d_model),
            nn.Dropout(dropout),
        )
    
    def forward(self, x, mask):
        # Pre-norm style (GPT-2+)
        h = self.ln1(x)
        h, _ = self.attn(h, h, h, attn_mask=mask)
        x = x + h
        x = x + self.ffn(self.ln2(x))
        return x

class MiniGPT(nn.Module):
    def __init__(self, vocab_size, d_model=256, num_heads=8, 
                 num_layers=6, max_len=512, dropout=0.1):
        super().__init__()
        self.token_emb = nn.Embedding(vocab_size, d_model)
        self.pos_emb = nn.Embedding(max_len, d_model)
        self.blocks = nn.ModuleList([
            GPTBlock(d_model, num_heads, dropout) for _ in range(num_layers)
        ])
        self.ln_f = nn.LayerNorm(d_model)
        self.head = nn.Linear(d_model, vocab_size, bias=False)
        self.max_len = max_len
    
    def forward(self, idx):
        B, T = idx.shape
        
        # Embeddings
        tok_emb = self.token_emb(idx)
        pos_emb = self.pos_emb(torch.arange(T, device=idx.device))
        x = tok_emb + pos_emb
        
        # Causal mask
        mask = torch.triu(torch.ones(T, T, device=idx.device), diagonal=1).bool()
        
        # Transformer blocks
        for block in self.blocks:
            x = block(x, mask)
        
        x = self.ln_f(x)
        logits = self.head(x)  # (B, T, vocab_size)
        return logits
    
    @torch.no_grad()
    def generate(self, idx, max_new_tokens, temperature=1.0, top_k=50):
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -self.max_len:]
            logits = self(idx_cond)[:, -1, :]  # Last token
            logits = logits / temperature
            
            # Top-k sampling
            if top_k > 0:
                v, _ = torch.topk(logits, top_k)
                logits[logits < v[:, [-1]]] = float('-inf')
            
            probs = torch.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            idx = torch.cat([idx, next_token], dim=1)
        return idx
```

---

## 4. Open-Source LLMs

| Model | Params | Đặc điểm |
|-------|--------|----------|
| LLaMA 3 | 8B, 70B, 405B | Meta, mạnh nhất open-source |
| Mistral | 7B, 8x7B | Hiệu quả, MoE variant |
| Phi-3 | 3.8B | Microsoft, nhỏ nhưng mạnh |
| Gemma 2 | 2B, 9B, 27B | Google |
| Qwen 2.5 | 0.5B–72B | Alibaba, tốt cho tiếng Việt |

```python
# Chạy local với Ollama
# ollama run llama3.1:8b

# Hoặc Hugging Face
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
```

---

## 📝 Bài tập

1. Train character-level GPT trên Shakespeare text (nanoGPT)
2. Chạy LLaMA 3 8B local bằng Ollama, thử các prompt khác nhau
3. So sánh output của GPT-4 vs LLaMA 3 vs Mistral trên cùng prompt
4. Implement BPE tokenizer từ đầu

---

## 📚 Tài liệu
- *Andrej Karpathy: Let's build GPT from scratch* (YouTube, MUST WATCH)
- *Andrej Karpathy: nanoGPT* (GitHub)
- Paper: *LLaMA: Open and Efficient Foundation Language Models*
- *Lilian Weng: Large Language Model (LLM) blog*
