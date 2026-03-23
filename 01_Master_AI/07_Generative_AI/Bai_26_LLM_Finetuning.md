# Bài 26: LLM Fine-tuning — LoRA, QLoRA, RLHF

## 🎯 Mục tiêu
- Supervised Fine-Tuning (SFT)
- Parameter-Efficient Fine-Tuning: LoRA, QLoRA
- RLHF & DPO alignment

## 📖 Câu chuyện đời thường
> Bạn thuê một nhân viên mới đã có kinh nghiệm 10 năm (pretrained model). Bạn không cần dạy họ lập trình từ đầu, chỉ cần hướng dẫn văn hóa công ty và quy trình riêng — đó là **SFT** (Supervised Fine-Tuning). **LoRA** giống như bạn chỉ dán thêm vài tờ note nhỏ lên cuốn sách giáo khoa cũ — không viết lại cả cuốn, chỉ thêm bổ sung thông tin mới (rất tiết kiệm bộ nhớ). **QLoRA** là dùng cuốn sách phiên bản rút gọn + note nhỏ — tiết kiệm hơn nữa. **RLHF** là giai đoạn "dạy văn phòng" — người dùng nói câu trả lời nào hay hơn, AI tự điều chỉnh phong cách.

---

## 1. Supervised Fine-Tuning (SFT)

### 1.1 Instruction Tuning
```
Base model (pre-trained) → biết ngôn ngữ, NHƯNG không biết follow instructions
SFT: train trên (instruction, response) pairs → model biết trả lời câu hỏi

Ví dụ training data:
{
  "instruction": "Dịch sang tiếng Anh",
  "input": "Xin chào",
  "output": "Hello"
}
```

---

## 2. LoRA (Low-Rank Adaptation) — PHƯƠNG PHÁP PHỔ BIẾN NHẤT

### 2.1 Ý tưởng
```
Full fine-tuning: update TẤT CẢ weights → tốn RAM, chậm
LoRA: chỉ thêm 2 ma trận nhỏ A, B vào mỗi layer

W_new = W_original + A × B   (A: d×r, B: r×d, r << d)

Model 7B params → LoRA chỉ train ~0.1% params (vài MB thay vì vài GB)
```

### 2.2 Fine-tune với QLoRA
```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer
from datasets import load_dataset
import torch

# Load model 4-bit quantized (QLoRA)
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    load_in_4bit=True,
    torch_dtype=torch.float16,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B")
tokenizer.pad_token = tokenizer.eos_token

# LoRA config
lora_config = LoraConfig(
    r=16,                  # Rank — càng cao → càng mạnh nhưng tốn RAM
    lora_alpha=32,         # Scaling factor
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # Layers to adapt
    lora_dropout=0.05,
    task_type="CAUSAL_LM",
)

model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# → ~0.1% trainable params

# Dataset
dataset = load_dataset("your_dataset")

# Training
training_args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch",
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    tokenizer=tokenizer,
    max_seq_length=2048,
)

trainer.train()

# Save LoRA weights (chỉ vài MB!)
model.save_pretrained("./lora_adapter")
```

### 2.3 Merge LoRA & Inference
```python
from peft import PeftModel

# Load base model + LoRA adapter
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
model = PeftModel.from_pretrained(base_model, "./lora_adapter")

# Merge → model đơn lẻ (optional)
model = model.merge_and_unload()
```

---

## 3. Quantization — Chạy LLM trên hardware nhỏ

```python
# GPTQ: post-training quantization
# AWQ: activation-aware quantization
# GGUF: format cho llama.cpp (chạy trên CPU!)

# Ví dụ: load model 4-bit
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    quantization_config=bnb_config,
)
# 8B model: ~16GB (FP16) → ~4GB (4-bit) → chạy được trên RTX 3060!
```

---

## 4. RLHF & DPO

```
RLHF Pipeline:
1. SFT model → base chat model
2. Reward Model: train trên human preferences (A > B)
3. PPO: optimize model to maximize reward

DPO (Direct Preference Optimization):
- Đơn giản hơn: KHÔNG cần reward model riêng
- Train trực tiếp trên preference pairs
- Kết quả tương đương RLHF
```

```python
from trl import DPOTrainer

# DPO dataset format: (prompt, chosen_response, rejected_response)
dpo_trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    args=training_args,
    train_dataset=dpo_dataset,
    tokenizer=tokenizer,
    beta=0.1,  # Temperature for DPO
)
dpo_trainer.train()
```

---

## 📝 Bài tập

1. Fine-tune LLaMA 3 8B bằng QLoRA cho task tiếng Việt (chatbot, translation)
2. Tạo dataset instruction-following tiếng Việt (100+ examples), fine-tune
3. Quantize model và so sánh quality vs speed ở các mức: FP16, 8-bit, 4-bit
4. Implement DPO training trên preference dataset đơn giản

---

## 📚 Tài liệu
- [Hugging Face PEFT Documentation](https://huggingface.co/docs/peft/)
- [TRL (Transformer Reinforcement Learning)](https://huggingface.co/docs/trl/)
- Paper: *LoRA: Low-Rank Adaptation of Large Language Models*
- Paper: *Direct Preference Optimization* (DPO)
