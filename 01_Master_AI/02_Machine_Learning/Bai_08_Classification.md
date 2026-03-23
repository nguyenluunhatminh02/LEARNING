# Bài 08: Classification — Logistic Regression, KNN, SVM

## 🎯 Mục tiêu
- Hiểu và implement Logistic Regression
- Hiểu KNN, SVM và kernel trick
- Biết cách đánh giá classification model

## 📖 Câu chuyện đời thường
> Ngân hàng cần quyết định: cho vay hay không? Đây là bài toán **phân loại** (Yes/No). **Logistic Regression** giống như một người duyệt hồ sơ cân nhắc: thu nhập cao +10 điểm, nợ nhiều -5 điểm... rồi tổng điểm > ngưỡng thì duyệt. **KNN** là cách nghĩ đơn giản: "5 người giống bạn nhất đều trả nợ đúng hạn → bạn cũng sẽ OK". **SVM** thì giống như kẻ một đường ranh giới rõ ràng nhất giữa nhóm "tốt" và nhóm "rủi ro" — và **kernel trick** cho phép kẻ đường cong khi 2 nhóm không thể tách bằng đường thẳng.

---

## 1. Logistic Regression

### 1.1 Mô hình
```
Linear Regression:  ŷ = W @ X + b        → giá trị liên tục
Logistic Regression: ŷ = σ(W @ X + b)    → xác suất [0, 1]

σ(z) = 1 / (1 + e⁻ᶻ)  ← Sigmoid function
```

```python
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

class LogisticRegressionCustom:
    def __init__(self, lr=0.01, epochs=1000):
        self.lr = lr
        self.epochs = epochs
    
    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.W = np.zeros(n_features)
        self.b = 0
        self.losses = []
        
        for _ in range(self.epochs):
            z = X @ self.W + self.b
            y_pred = sigmoid(z)
            
            # Binary Cross-Entropy Loss
            loss = -np.mean(y * np.log(y_pred + 1e-10) + (1-y) * np.log(1-y_pred + 1e-10))
            self.losses.append(loss)
            
            # Gradients
            dW = (1/n_samples) * X.T @ (y_pred - y)
            db = (1/n_samples) * np.sum(y_pred - y)
            
            self.W -= self.lr * dW
            self.b -= self.lr * db
        return self
    
    def predict_proba(self, X):
        return sigmoid(X @ self.W + self.b)
    
    def predict(self, X, threshold=0.5):
        return (self.predict_proba(X) >= threshold).astype(int)
```

### 1.2 Multi-class: Softmax Regression
```python
def softmax(z):
    """z shape: (n_samples, n_classes)"""
    exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))  # numerical stability
    return exp_z / exp_z.sum(axis=1, keepdims=True)

# Ví dụ: 3 classes
z = np.array([[2.0, 1.0, 0.1]])
probs = softmax(z)  # [0.659, 0.242, 0.099] → class 0 xác suất cao nhất
```

---

## 2. K-Nearest Neighbors (KNN)

### 2.1 Ý tưởng
```
Để phân loại điểm mới X:
1. Tìm K điểm gần nhất trong training set
2. Đếm label phổ biến nhất trong K neighbors
3. Gán label đó cho X
```

### 2.2 Implementation
```python
class KNNClassifier:
    def __init__(self, k=5):
        self.k = k
    
    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
        return self
    
    def predict(self, X):
        predictions = []
        for x in X:
            # Tính khoảng cách đến tất cả training points
            distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
            
            # K nearest
            k_indices = np.argsort(distances)[:self.k]
            k_labels = self.y_train[k_indices]
            
            # Vote
            unique, counts = np.unique(k_labels, return_counts=True)
            predictions.append(unique[np.argmax(counts)])
        
        return np.array(predictions)

# Chọn K: thường K lẻ, thử K = 3, 5, 7, 11
# K nhỏ → overfitting, K lớn → underfitting
```

---

## 3. Support Vector Machine (SVM)

### 3.1 Ý tưởng
```
Tìm hyperplane (đường/mặt phẳng) phân cách 2 classes 
sao cho MARGIN (khoảng cách đến điểm gần nhất) LỚN NHẤT
```

### 3.2 Kernel Trick — Ánh xạ lên không gian cao hơn
```python
from sklearn.svm import SVC

# Linear SVM
svm_linear = SVC(kernel='linear', C=1.0)

# RBF kernel (phổ biến nhất) — xử lý data phi tuyến
svm_rbf = SVC(kernel='rbf', C=1.0, gamma='scale')

# Polynomial kernel
svm_poly = SVC(kernel='poly', degree=3, C=1.0)

# C: regularization. C lớn → fit sát data, C nhỏ → margin lớn hơn
```

---

## 4. Đánh giá Classification — CỰC KỲ QUAN TRỌNG

### 4.1 Confusion Matrix
```
                  Predicted
                Positive  Negative
Actual Positive    TP        FN
       Negative    FP        TN
```

```python
from sklearn.metrics import (confusion_matrix, classification_report, 
                            accuracy_score, precision_score, recall_score, 
                            f1_score, roc_auc_score, roc_curve)

y_pred = model.predict(X_test)

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)

# Metrics
accuracy  = accuracy_score(y_test, y_pred)   # (TP+TN) / Total
precision = precision_score(y_test, y_pred)  # TP / (TP+FP) — "bao nhiêu dự đoán Positive đúng?"
recall    = recall_score(y_test, y_pred)     # TP / (TP+FN) — "bao nhiêu Positive thực tế được tìm ra?"
f1        = f1_score(y_test, y_pred)         # 2 * P * R / (P + R)

print(classification_report(y_test, y_pred))
```

### 4.2 ROC-AUC
```python
# ROC curve: True Positive Rate vs False Positive Rate
y_proba = model.predict_proba(X_test)[:, 1]  # Xác suất class 1
fpr, tpr, thresholds = roc_curve(y_test, y_proba)
auc = roc_auc_score(y_test, y_proba)

import matplotlib.pyplot as plt
plt.plot(fpr, tpr, label=f'AUC = {auc:.3f}')
plt.plot([0,1], [0,1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()
```

### 4.3 Chọn metric nào?
| Tình huống | Metric ưu tiên |
|-----------|---------------|
| Balanced dataset | Accuracy, F1 |
| Imbalanced dataset | F1, Precision, Recall, AUC |
| Phát hiện bệnh (không bỏ sót) | **Recall** cao |
| Spam filter (không nhầm email quan trọng) | **Precision** cao |
| Tổng quát | **F1 score** hoặc **AUC** |

---

## 📝 Bài tập

1. Implement Logistic Regression từ đầu, test trên dataset make_classification (sklearn)
2. Dataset Breast Cancer (sklearn):
   - So sánh Logistic Regression vs KNN vs SVM
   - Tune hyperparameters (C, K, kernel) bằng GridSearchCV
   - Vẽ ROC curve cho cả 3 models
3. Dataset Titanic: predict survival
   - Xử lý missing data, encoding
   - Train nhiều models, so sánh
   - Feature importance analysis
4. Implement KNN từ đầu, thử K = 1, 3, 5, 11 → vẽ decision boundary

---

## 📚 Tài liệu
- *Hands-On ML* — Ch. 3 (Classification)
- *Andrew Ng ML* — Week 3 (Logistic Regression)
- *CS229 Stanford — SVM lecture notes*
