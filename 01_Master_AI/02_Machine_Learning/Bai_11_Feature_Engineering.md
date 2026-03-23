# Bài 11: Feature Engineering & Model Evaluation

## 🎯 Mục tiêu
- Xử lý dữ liệu thực tế: missing values, encoding, scaling
- Tạo features tốt — kỹ năng quan trọng nhất của ML Engineer
- Hyperparameter tuning chiến lược

## 📖 Câu chuyện đời thường
> Bạn nấu phở. Nguyên liệu thô (data thô) là xương, thịt, hành, gừng. Nhưng đầu bếp giỏi không chỉ cho vào nồi — họ biết **chế biến**: hầm xương 6 tiếng, nướng hành cho thơm, thái thịt đúng độ dày. Đó chính là **Feature Engineering** — biến dữ liệu thô thành "nguyên liệu đã sơ chế" để model học tốt hơn. Missing values giống như hết hành → thay bằng hành tây (imputation). Scaling giống như đoạn "cân lại gia vị" — không để một vị nào lấn át. Hyperparameter tuning là chỉnh lửa to nhỏ cho đến khi nước dùng hoàn hảo.

---

## 1. Xử lý Missing Data

```python
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer

# Kiểm tra
df.isnull().sum()

# Chiến lược xử lý
# 1. Xóa (khi tỷ lệ missing < 5%)
df.dropna(subset=['important_col'])

# 2. Điền giá trị
df['age'].fillna(df['age'].median(), inplace=True)        # Numeric: median
df['city'].fillna(df['city'].mode()[0], inplace=True)      # Categorical: mode

# 3. KNN Imputer (thông minh hơn)
imputer = KNNImputer(n_neighbors=5)
X_imputed = imputer.fit_transform(X)

# 4. Tạo feature "is_missing"
df['age_missing'] = df['age'].isnull().astype(int)
```

---

## 2. Encoding biến phân loại

```python
# 1. Label Encoding (ordinal data: thấp < trung bình < cao)
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['size_encoded'] = le.fit_transform(df['size'])  # S→0, M→1, L→2

# 2. One-Hot Encoding (nominal data: không có thứ tự)
df_encoded = pd.get_dummies(df, columns=['color'], drop_first=True)

# 3. Target Encoding (high cardinality)
# Thay category bằng mean(target) của category đó
target_means = df.groupby('city')['price'].mean()
df['city_encoded'] = df['city'].map(target_means)

# 4. Frequency Encoding
freq = df['city'].value_counts(normalize=True)
df['city_freq'] = df['city'].map(freq)
```

---

## 3. Feature Scaling

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# StandardScaler: z = (x - μ) / σ → mean=0, std=1
# Dùng cho: hầu hết algorithms (SVM, KNN, Neural Networks)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # DÙNG fit_transform CHỈ TRÊN TRAIN!

# MinMaxScaler: x' = (x - min) / (max - min) → [0, 1]
# Ảnh hưởng bởi outliers

# RobustScaler: dùng median và IQR → robust với outliers
robust = RobustScaler()
X_robust = robust.fit_transform(X_train)
```

> ⚠️ **Quan trọng**: LUÔN fit scaler trên training set, rồi transform cả train + test

---

## 4. Feature Creation

```python
# 1. Interaction features
df['area'] = df['length'] * df['width']

# 2. Polynomial features
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=2, interaction_only=True)
X_poly = poly.fit_transform(X)

# 3. Date features
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

# 4. Text features
df['text_length'] = df['text'].str.len()
df['word_count'] = df['text'].str.split().str.len()
df['has_exclamation'] = df['text'].str.contains('!').astype(int)

# 5. Aggregation features
df['user_avg_spend'] = df.groupby('user_id')['amount'].transform('mean')
df['user_total_orders'] = df.groupby('user_id')['order_id'].transform('count')

# 6. Binning
df['age_group'] = pd.cut(df['age'], bins=[0, 18, 35, 55, 100],
                         labels=['young', 'adult', 'middle', 'senior'])
```

---

## 5. Feature Selection

```python
# 1. Correlation matrix — loại features tương quan cao với nhau
corr = df[numeric_cols].corr()
# Nếu corr(A, B) > 0.9 → giữ 1, loại 1

# 2. Feature Importance từ tree-based models
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier().fit(X_train, y_train)
importances = pd.Series(rf.feature_importances_, index=feature_names)
importances.nlargest(10).plot(kind='barh')

# 3. Recursive Feature Elimination (RFE)
from sklearn.feature_selection import RFE
rfe = RFE(estimator=rf, n_features_to_select=10)
rfe.fit(X_train, y_train)
selected = np.array(feature_names)[rfe.support_]
```

---

## 6. Hyperparameter Tuning

```python
# 1. GridSearchCV — exhaustive search
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15],
    'learning_rate': [0.01, 0.05, 0.1],
}
grid = GridSearchCV(xgb, param_grid, cv=5, scoring='f1', n_jobs=-1)
grid.fit(X_train, y_train)
print(f"Best params: {grid.best_params_}")
print(f"Best F1: {grid.best_score_:.4f}")

# 2. Optuna — Bayesian optimization (THÔNG MINH HƠN)
import optuna

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 15),
        'learning_rate': trial.suggest_float('learning_rate', 0.001, 0.3, log=True),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
    }
    model = XGBClassifier(**params, random_state=42)
    score = cross_val_score(model, X_train, y_train, cv=5, scoring='f1').mean()
    return score

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
print(f"Best params: {study.best_params}")
```

---

## 7. Pipeline hoàn chỉnh

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Tách numeric và categorical
numeric_features = ['age', 'income', 'credit_score']
categorical_features = ['gender', 'city', 'education']

# Preprocessing pipeline
preprocessor = ColumnTransformer([
    ('num', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
    ]), numeric_features),
    ('cat', Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore')),
    ]), categorical_features),
])

# Full pipeline
full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', XGBClassifier(random_state=42)),
])

full_pipeline.fit(X_train, y_train)
y_pred = full_pipeline.predict(X_test)
```

---

## 📝 Bài tập

1. **Kaggle: Spaceship Titanic** — full pipeline:
   - EDA → Feature Engineering → Model → Tune → Submit
2. Tạo ít nhất 10 features mới từ dataset House Prices, so sánh score trước/sau
3. Implement complete sklearn Pipeline với ColumnTransformer cho dataset có cả numeric + categorical

---

## 📚 Tài liệu
- *Feature Engineering for Machine Learning* — Alice Zheng
- *Kaggle Learn: Feature Engineering*
- Optuna Documentation
