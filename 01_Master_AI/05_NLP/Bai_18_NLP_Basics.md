# Bài 18: NLP cơ bản & Word Embeddings

## 🎯 Mục tiêu
- Text preprocessing: tokenization, stemming, lemmatization
- Biểu diễn văn bản: BoW, TF-IDF
- Word Embeddings: Word2Vec, GloVe

## 📖 Câu chuyện đời thường
> Bạn vừa nhận được 1000 lá thư khiếu nại của khách hàng và cần phân loại nhanh. **Tokenization** là việc bạn tách mỗi lá thư thành từng từ riêng. **Stemming** là nhận ra "chạy", "chạy bộ" và "đang chạy" đều liên quan đến "chạy". **TF-IDF** giống như bạn tìm từ khóa quan trọng trong mỗi lá thư: từ "hoàn tiền" xuất hiện nhiều trong 1 lá thư nhưng hiếm ở các thư khác → từ này rất quan trọng. **Word2Vec** thì hay hơn: nó hiểu rằng "vua" và "hoàng hậu" gần nhau, "vua - đàn ông + phụ nữ ≈ hoàng hậu" — giống như bạn hiểu rằng các từ có "khoảng cách ý nghĩa" với nhau.

---

## 1. Text Preprocessing

```python
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

text = "I'm loving the new AI models! They're amazing in 2024."

# 1. Lowercase
text = text.lower()

# 2. Remove special characters
text = re.sub(r'[^a-zA-Z\s]', '', text)

# 3. Tokenization
from nltk.tokenize import word_tokenize
tokens = word_tokenize(text)

# 4. Remove stopwords
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
tokens = [t for t in tokens if t not in stop_words]

# 5. Lemmatization (tốt hơn stemming)
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
tokens = [lemmatizer.lemmatize(t) for t in tokens]
```

---

## 2. Bag of Words & TF-IDF

```python
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

corpus = [
    "I love machine learning",
    "Deep learning is amazing",
    "Machine learning and deep learning are related",
]

# Bag of Words: đếm tần suất từ
bow = CountVectorizer()
X_bow = bow.fit_transform(corpus)

# TF-IDF: tần suất × inverse document frequency
# Từ xuất hiện nhiều trong 1 doc NHƯNG ít trong các doc khác → score cao
tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X_tfidf = tfidf.fit_transform(corpus)
```

---

## 3. Word Embeddings

### 3.1 Tại sao cần Embeddings?
```
BoW/TF-IDF: "king" và "queen" KHÔNG liên quan (orthogonal vectors)
Embeddings:  "king" và "queen" GẦN NHAU trong vector space

Nổi tiếng: king - man + woman ≈ queen
```

### 3.2 Word2Vec
```python
from gensim.models import Word2Vec

# Training
sentences = [["i", "love", "machine", "learning"],
             ["deep", "learning", "is", "great"]]

model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, sg=1)
# sg=1: Skip-gram, sg=0: CBOW

# Sử dụng
vector = model.wv['learning']           # Vector 100 chiều
similar = model.wv.most_similar('learning')  # Từ tương tự

# Pretrained Word2Vec
import gensim.downloader
w2v = gensim.downloader.load('word2vec-google-news-300')
w2v.most_similar(positive=['king', 'woman'], negative=['man'])
# → [('queen', 0.71)]
```

### 3.3 Dùng cho Classification
```python
import numpy as np

def document_vector(doc, model, dim=300):
    """Trung bình embeddings của tất cả từ trong document"""
    words = doc.split()
    vectors = [model[w] for w in words if w in model]
    if vectors:
        return np.mean(vectors, axis=0)
    return np.zeros(dim)

X_vectors = np.array([document_vector(doc, w2v) for doc in documents])

# Sau đó dùng classifier bất kỳ
from sklearn.svm import SVC
clf = SVC().fit(X_vectors_train, y_train)
```

---

## 📝 Bài tập

1. **Sentiment Analysis**: Dataset IMDB reviews
   - Preprocessing → TF-IDF → Logistic Regression
   - So sánh BoW vs TF-IDF
2. **Text Classification** tiếng Việt (dùng underthesea cho tokenize)
3. Train Word2Vec trên corpus Wikipedia tiếng Việt, tìm từ tương tự
4. Visualize word embeddings bằng t-SNE: nhóm các từ liên quan

---

## 📚 Tài liệu
- *CS224n: Word Vectors* — Stanford (Lecture 1-2)
- *Speech and Language Processing* — Jurafsky & Martin (Ch. 6)
- [Gensim Documentation](https://radimrehurek.com/gensim/)
