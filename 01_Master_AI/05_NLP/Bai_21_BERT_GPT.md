# Bài 21: BERT, GPT & Fine-tuning

## 🎯 Mục tiêu
- Hiểu BERT, GPT — 2 paradigm chính của NLP hiện đại
- Fine-tune pretrained models với Hugging Face
- Áp dụng cho classification, NER, QA

---

## 1. BERT (Bidirectional Encoder Representations from Transformers)

### 1.1 Pre-training Tasks
```
1. Masked Language Model (MLM): che random 15% tokens, dự đoán lại
   Input:  "The [MASK] sat on the mat"
   Output: "The cat sat on the mat"

2. Next Sentence Prediction (NSP): 2 câu có liên tiếp không?
   → Học hiểu ngữ cảnh giữa các câu
```

### 1.2 Fine-tuning BERT với Hugging Face
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import Trainer, TrainingArguments
from datasets import load_dataset

# Load dataset
dataset = load_dataset('imdb')

# Load pretrained BERT
model_name = 'bert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# Tokenize
def tokenize(examples):
    return tokenizer(examples['text'], truncation=True, padding='max_length', max_length=256)

tokenized = dataset.map(tokenize, batched=True)

# Training
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    learning_rate=2e-5,
    weight_decay=0.01,
    eval_strategy='epoch',
    save_strategy='epoch',
    load_best_model_at_end=True,
    fp16=True,  # Mixed precision
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized['train'],
    eval_dataset=tokenized['test'],
)

trainer.train()
```

---

## 2. GPT (Generative Pre-trained Transformer)

### 2.1 Khác biệt BERT vs GPT
```
BERT (Encoder):
- Bidirectional: nhìn cả trái + phải
- Pre-train: MLM (đoán từ bị che)
- Dùng cho: classification, NER, QA, embedding

GPT (Decoder):
- Autoregressive: chỉ nhìn trái
- Pre-train: next token prediction
- Dùng cho: text generation, chatbot, code generation
```

### 2.2 Text Generation với GPT-2
```python
from transformers import GPT2LMHeadModel, GPT2Tokenizer

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

prompt = "Artificial intelligence will"
inputs = tokenizer.encode(prompt, return_tensors='pt')

outputs = model.generate(
    inputs,
    max_length=100,
    temperature=0.7,       # Creativity: 0=deterministic, 1=random
    top_p=0.9,             # Nucleus sampling
    do_sample=True,
    no_repeat_ngram_size=2,
)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

---

## 3. NLP Tasks với Hugging Face

### 3.1 Named Entity Recognition (NER)
```python
from transformers import pipeline

ner = pipeline('ner', model='dslim/bert-base-NER', aggregation_strategy='simple')
result = ner("Elon Musk is the CEO of Tesla in California")
for entity in result:
    print(f"{entity['word']}: {entity['entity_group']} ({entity['score']:.2f})")
# Elon Musk: PER (0.99)
# Tesla: ORG (0.98)
# California: LOC (0.99)
```

### 3.2 Question Answering
```python
qa = pipeline('question-answering', model='deepset/roberta-base-squad2')

result = qa(
    question="What is the capital of France?",
    context="France is a country in Europe. Its capital is Paris, known for the Eiffel Tower."
)
print(f"Answer: {result['answer']} (score: {result['score']:.3f})")
```

### 3.3 Semantic Similarity / Embeddings
```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

sentences = [
    "How to learn Python?",
    "Best way to study Python programming",
    "Recipe for chocolate cake",
]

embeddings = model.encode(sentences)
sim_matrix = cosine_similarity(embeddings)
# sentences[0] vs [1]: ~0.85 (similar)
# sentences[0] vs [2]: ~0.10 (different)
```

---

## 📝 Bài tập

1. **Sentiment Analysis**: Fine-tune BERT trên dataset tiếng Việt (VLSP, UIT-VSFC)
2. **NER tiếng Việt**: Fine-tune BERT cho nhận dạng thực thể
3. **Semantic Search**: Dùng Sentence-BERT tìm câu hỏi tương tự trong FAQ database
4. **Text Summarization**: Dùng T5/BART summary tin tức

---

## 📚 Tài liệu
- [Hugging Face Course](https://huggingface.co/learn/nlp-course) — MIỄN PHÍ
- *The Illustrated BERT* — Jay Alammar
- Paper: *BERT: Pre-training of Deep Bidirectional Transformers*
- Paper: *Language Models are Few-Shot Learners* (GPT-3)
