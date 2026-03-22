# Bài 19: RNN, LSTM, GRU

## 🎯 Mục tiêu
- Hiểu RNN và vấn đề vanishing gradient
- LSTM: forget gate, input gate, output gate
- Sequence-to-Sequence model

---

## 1. Recurrent Neural Network (RNN)

### 1.1 Ý tưởng
```
Neural Network thông thường: không có "bộ nhớ"
RNN: có hidden state h — nhớ thông tin từ bước trước

Tại bước t:
h_t = tanh(W_h · h_{t-1} + W_x · x_t + b)
y_t = W_y · h_t + b_y

Dùng cho: dữ liệu sequential (text, time series, audio)
```

### 1.2 PyTorch Implementation
```python
import torch
import torch.nn as nn

class SimpleRNN(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.RNN(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_classes)
    
    def forward(self, x):
        # x: (batch, seq_len)
        x = self.embedding(x)           # (batch, seq_len, embed_dim)
        output, hidden = self.rnn(x)     # output: all timesteps, hidden: last
        return self.fc(hidden.squeeze(0)) # Dùng hidden state cuối cùng

# Vấn đề: Vanishing Gradient — RNN KHÔNG nhớ được thông tin dài hạn
```

---

## 2. LSTM (Long Short-Term Memory)

### 2.1 Architecture
```
LSTM thêm "Cell State" C — đường cao tốc cho thông tin dài hạn
3 Gates kiểm soát luồng thông tin:

Forget Gate:  f_t = σ(W_f · [h_{t-1}, x_t] + b_f)    → quên gì?
Input Gate:   i_t = σ(W_i · [h_{t-1}, x_t] + b_i)    → nhớ gì mới?
Output Gate:  o_t = σ(W_o · [h_{t-1}, x_t] + b_o)    → output gì?

Cell State:   C_t = f_t ⊙ C_{t-1} + i_t ⊙ tanh(W_C · [h_{t-1}, x_t])
Hidden State: h_t = o_t ⊙ tanh(C_t)
```

### 2.2 Implementation
```python
class LSTMClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes, num_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim, 
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,    # Đọc cả 2 chiều
            dropout=0.3,
        )
        self.fc = nn.Linear(hidden_dim * 2, num_classes)  # *2 vì bidirectional
        self.dropout = nn.Dropout(0.3)
    
    def forward(self, x):
        x = self.embedding(x)
        output, (hidden, cell) = self.lstm(x)
        
        # Concat forward + backward hidden states
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)
        hidden = self.dropout(hidden)
        return self.fc(hidden)
```

---

## 3. GRU — Đơn giản hơn LSTM
```python
# GRU = LSTM đơn giản hóa: 2 gates thay vì 3, không có cell state
# Performance tương đương LSTM nhưng train nhanh hơn

class GRUClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.gru = nn.GRU(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, num_classes)
    
    def forward(self, x):
        x = self.embedding(x)
        _, hidden = self.gru(x)
        hidden = torch.cat([hidden[-2], hidden[-1]], dim=1)
        return self.fc(hidden)
```

---

## 4. Seq2Seq — Sequence to Sequence
```
Ứng dụng: dịch máy, summarization, chatbot

Encoder: đọc input sequence → context vector
Decoder: từ context vector → sinh output sequence

"Xin chào" → Encoder → [context] → Decoder → "Hello"
```

---

## 📝 Bài tập

1. **Sentiment Analysis**: Train LSTM trên IMDB dataset, đạt >85% accuracy
2. **Text Generation**: Train character-level RNN/LSTM sinh text
3. So sánh RNN vs LSTM vs GRU trên cùng task: speed, accuracy, memory
4. **Time Series**: Dự đoán giá cổ phiếu bằng LSTM

---

## 📚 Tài liệu
- *Understanding LSTM Networks* — Chris Olah (blog, MUST READ)
- *CS224n: RNNs and Language Models* — Stanford
- *Dive into Deep Learning* — Ch. RNN
