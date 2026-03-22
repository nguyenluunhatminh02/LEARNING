# Bài 09: Tree-based Models & Ensemble Methods

## 🎯 Mục tiêu
- Hiểu Decision Tree, Random Forest
- Hiểu Gradient Boosting: XGBoost, LightGBM
- Ensemble methods: Bagging, Boosting, Stacking

---

## 1. Decision Tree

### 1.1 Cách hoạt động
```
Chia dữ liệu dựa trên câu hỏi Yes/No:

                    [Tuổi > 30?]
                   /            \
              Yes /              \ No
        [Thu nhập > 50K?]    [Sinh viên?]
         /         \           /        \
       Yes         No       Yes         No
    [Mua: Yes]  [Mua: No] [Mua: Yes] [Mua: No]
```

### 1.2 Criteria phân chia
```python
import numpy as np

# Gini Impurity (dùng trong CART — sklearn mặc định)
def gini(y):
    classes, counts = np.unique(y, return_counts=True)
    probs = counts / len(y)
    return 1 - np.sum(probs ** 2)

# Entropy (dùng trong C4.5, ID3)
def entropy(y):
    classes, counts = np.unique(y, return_counts=True)
    probs = counts / len(y)
    return -np.sum(probs * np.log2(probs + 1e-10))

# Information Gain = Entropy(parent) - weighted_avg(Entropy(children))
```

### 1.3 Sử dụng với sklearn
```python
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
tree = DecisionTreeClassifier(max_depth=3, min_samples_leaf=5, random_state=42)
tree.fit(X, y)

# Xem cấu trúc cây
print(export_text(tree, feature_names=load_iris().feature_names))

# Feature importance
for name, imp in zip(load_iris().feature_names, tree.feature_importances_):
    print(f"{name}: {imp:.4f}")
```

### 1.4 Hyperparameters chống Overfitting
```python
tree = DecisionTreeClassifier(
    max_depth=5,          # Giới hạn độ sâu cây
    min_samples_split=10, # Tối thiểu samples để split
    min_samples_leaf=5,   # Tối thiểu samples ở leaf
    max_features='sqrt',  # Số features xem xét mỗi split
)
```

---

## 2. Ensemble Methods

### 2.1 Bagging → Random Forest
```
Bagging = Bootstrap Aggregating
1. Tạo N bộ dữ liệu con (bootstrap sampling — lấy có hoàn lại)
2. Train N models trên N bộ dữ liệu
3. Kết hợp kết quả: voting (classification) hoặc trung bình (regression)
→ Giảm Variance → Giảm Overfitting
```

```python
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(
    n_estimators=100,      # Số cây
    max_depth=10,
    min_samples_leaf=5,
    max_features='sqrt',   # Random subspace — mỗi cây chỉ xem sqrt(n_features)
    n_jobs=-1,             # Parallel training
    random_state=42
)
rf.fit(X_train, y_train)

# Feature Importance
importances = rf.feature_importances_
sorted_idx = np.argsort(importances)[::-1]
for i in sorted_idx[:10]:
    print(f"{feature_names[i]}: {importances[i]:.4f}")
```

### 2.2 Boosting → Gradient Boosting
```
Boosting: train models TUẦN TỰ, mỗi model sửa lỗi của model trước

1. Train model₁ → lỗi e₁
2. Train model₂ tập trung vào e₁ → lỗi e₂
3. Train model₃ tập trung vào e₂ → ...
4. Final = model₁ + model₂ + model₃ + ...
→ Giảm Bias → Fit tốt hơn
```

### 2.3 XGBoost — THƯ VIỆN MẠNH NHẤT cho tabular data
```python
from xgboost import XGBClassifier

xgb = XGBClassifier(
    n_estimators=200,     # Số cây
    max_depth=6,          # Độ sâu mỗi cây
    learning_rate=0.1,    # Shrinkage — bước học
    subsample=0.8,        # % dữ liệu cho mỗi cây
    colsample_bytree=0.8, # % features cho mỗi cây
    reg_alpha=0.1,        # L1 regularization
    reg_lambda=1.0,       # L2 regularization
    use_label_encoder=False,
    eval_metric='logloss',
    early_stopping_rounds=20,
    random_state=42
)

xgb.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    verbose=10
)
```

### 2.4 LightGBM — NHANH hơn XGBoost
```python
from lightgbm import LGBMClassifier

lgbm = LGBMClassifier(
    n_estimators=200,
    max_depth=-1,         # Không giới hạn (leaf-wise growth)
    learning_rate=0.1,
    num_leaves=31,        # Quan trọng nhất — thay vì max_depth
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42
)
lgbm.fit(X_train, y_train, eval_set=[(X_val, y_val)])
```

### 2.5 Stacking
```python
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression

stack = StackingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n_estimators=100)),
        ('xgb', XGBClassifier(n_estimators=100)),
        ('lgbm', LGBMClassifier(n_estimators=100)),
    ],
    final_estimator=LogisticRegression(),
    cv=5
)
stack.fit(X_train, y_train)
```

---

## 3. So sánh

| Model | Ưu điểm | Nhược điểm | Khi nào dùng |
|-------|---------|-----------|-------------|
| Decision Tree | Dễ hiểu, interpretable | Overfitting | Khi cần giải thích |
| Random Forest | Robust, ít tune | Chậm inference | Default cho tabular |
| **XGBoost** | **Mạnh nhất** | Cần tune nhiều | **Kaggle, production** |
| **LightGBM** | **Nhanh, ít RAM** | Overfitting nếu data nhỏ | **Data lớn** |

---

## 📝 Bài tập

1. Dataset: Heart Disease (sklearn/Kaggle)
   - So sánh: Decision Tree vs Random Forest vs XGBoost vs LightGBM
   - Tune hyperparameters bằng Optuna hoặc GridSearchCV
2. Kaggle: House Prices competition
   - Feature engineering + XGBoost/LightGBM
   - Submit và xem leaderboard rank
3. Implement một Decision Tree classifier đơn giản từ đầu
4. Thử Stacking: combine RF + XGB + LightGBM → so sánh với standalone models

---

## 📚 Tài liệu
- *Hands-On ML* — Ch. 6-7 (Trees & Ensembles)
- XGBoost Documentation
- LightGBM Documentation
