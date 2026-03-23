# Bài 20: Transformer — Attention Is All You Need

## 🎯 Mục tiêu
- Hiểu Self-Attention, Multi-Head Attention
- Hiểu kiến trúc Transformer đầy đủ
- Implement Transformer encoder từ đầu

## 📖 Câu chuyện đời thường
> Bạn đang học bài trong một cuốn sách dày. **RNN** đọc từ từ từ đầu đến cuối — đến trang 100 thì quên mất trang 1. **Self-Attention** thì khác: giống như bạn đọc một câu và mắt bạn tự động nhảy đến những từ liên quan. Ví dụ: "Con **mèo** ngồi trên bàn, **nó** rất lười" — mắt bạn tự nối "nó" với "mèo" dù cách xa nhau. **Multi-Head Attention** giống như đọc cùng một câu nhưng từ nhiều góc nhìn: head 1 nhìn ngữ pháp, head 2 nhìn ngữ nghĩa, head 3 nhìn cảm xúc. Transformer = nhiều người đọc song song, mỗi người chú ý một khía cạnh — nhanh và hiểu sâu hơn đọc tuần tự.

---

## 1. Self-Attention — Cơ chế cốt lõi

### 1.1 Ý tưởng
```
RNN: xử lý tuần tự, token 1 → token 2 → ... → token n (CHẬM)
Attention: MỌI token nhìn MỌI token khác ĐỒNG THỜI (song song)

"The cat sat on the mat because it was tired"
→ "it" attend vào "cat" (không phải "mat") → hiểu ngữ cảnh
```

### 1.2 Scaled Dot-Product Attention
```
Attention(Q, K, V) = softmax(Q @ Kᵀ / √d_k) @ V

Q (Query):  "tôi đang tìm gì?"
K (Key):    "tôi chứa thông tin gì?"
V (Value):  "thông tin thực tế của tôi"
```

```python
import torch
import torch.nn as nn
import math

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q, K, V: (batch, num_heads, seq_len, d_k)
    """
    d_k = Q.size(-1)
    
    # Attention scores: (batch, heads, seq_len, seq_len)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))
    
    attention_weights = torch.softmax(scores, dim=-1)
    output = torch.matmul(attention_weights, V)
    
    return output, attention_weights
```

### 1.3 Multi-Head Attention
```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=512, num_heads=8):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
    
    def forward(self, Q, K, V, mask=None):
        batch_size = Q.size(0)
        
        # Linear projections → split into heads
        Q = self.W_q(Q).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(K).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(V).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # Attention
        attn_output, _ = scaled_dot_product_attention(Q, K, V, mask)
        
        # Concat heads
        attn_output = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.num_heads * self.d_k)
        
        return self.W_o(attn_output)
```

---

## 2. Transformer Architecture

### 2.1 Positional Encoding
```python
class PositionalEncoding(nn.Module):
    """Thêm thông tin vị trí vào embeddings (vì attention không biết thứ tự)"""
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        
        pe[:, 0::2] = torch.sin(position * div_term)  # Even indices
        pe[:, 1::2] = torch.cos(position * div_term)  # Odd indices
        
        self.register_buffer('pe', pe.unsqueeze(0))
    
    def forward(self, x):
        return x + self.pe[:, :x.size(1)]
```

### 2.2 Transformer Encoder Layer
```python
class TransformerEncoderLayer(nn.Module):
    def __init__(self, d_model=512, num_heads=8, d_ff=2048, dropout=0.1):
        super().__init__()
        # Multi-Head Attention
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.norm1 = nn.LayerNorm(d_model)
        
        # Feed-Forward Network
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
        )
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # Self-Attention + Residual + LayerNorm
        attn_out = self.attention(x, x, x, mask)
        x = self.norm1(x + self.dropout(attn_out))
        
        # FFN + Residual + LayerNorm
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_out))
        
        return x
```

### 2.3 Full Transformer Encoder (cho classification)
```python
class TransformerClassifier(nn.Module):
    def __init__(self, vocab_size, d_model=256, num_heads=8, 
                 num_layers=6, num_classes=2, max_len=512):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_encoding = PositionalEncoding(d_model, max_len)
        
        self.layers = nn.ModuleList([
            TransformerEncoderLayer(d_model, num_heads)
            for _ in range(num_layers)
        ])
        
        self.classifier = nn.Linear(d_model, num_classes)
        self.dropout = nn.Dropout(0.1)
    
    def forward(self, x, mask=None):
        x = self.dropout(self.pos_encoding(self.embedding(x)))
        
        for layer in self.layers:
            x = layer(x, mask)
        
        # CLS token (first token) hoặc mean pooling
        x = x.mean(dim=1)  # Mean pooling
        return self.classifier(x)
```

---

## 3. Encoder vs Decoder
```
Encoder (BERT-style):
- Bidirectional: nhìn cả trái + phải
- Dùng cho: classification, NER, QA

Decoder (GPT-style):
- Causal/Autoregressive: chỉ nhìn trái
- Causal mask: token i chỉ attend token 1..i
- Dùng cho: text generation

Encoder-Decoder (T5, BART):
- Encoder đọc input, Decoder sinh output
- Dùng cho: translation, summarization
```

---

## 📝 Bài tập

1. **Implement Transformer Encoder** từ đầu, train text classification trên IMDB
2. **Visualize Attention**: plot attention weights, xem model chú ý từ nào
3. **Implement Causal Mask** cho decoder (Left-to-right attention)
4. So sánh Transformer vs Bi-LSTM trên cùng task: accuracy, training time

---

## 📚 Tài liệu
- *The Illustrated Transformer* — Jay Alammar (MUST READ blog)
- Paper: *Attention Is All You Need* — Vaswani et al. (2017)
- *CS224n: Transformers* — Stanford (Lecture 9-10)
- *The Annotated Transformer* — Harvard NLP (code walkthrough)
