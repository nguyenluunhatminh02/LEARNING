# Bài 01: Python cho AI

## 🎯 Mục tiêu
- Nắm vững Python cơ bản đến nâng cao
- Viết code Python clean, hiệu quả cho AI/ML

## 📖 Câu chuyện đời thường
> Hãy tưởng tượng bạn muốn mở một nhà hàng. Trước khi nấu bất kỳ món ăn cao cấp nào, bạn cần thành thạo các kỹ năng cơ bản: cầm dao đúng cách, biết các loại gia vị, biết điều chỉnh lửa. Python chính là "bộ dao và bếp" của AI Engineer — nếu bạn không thành thạo công cụ cơ bản, thì dù có công thức (thuật toán) hay đến đâu, bạn cũng không nấu được món ngon (model tốt). List comprehension giống như kỹ thuật cắt nhanh của đầu bếp chuyên nghiệp — cùng một việc nhưng nhanh gọn hơn hẳn.

---

## 1. Python cơ bản — Ôn tập nhanh

### 1.1 Biến & Kiểu dữ liệu
```python
# Kiểu số
x = 10          # int
y = 3.14        # float
z = 2 + 3j      # complex

# Kiểu chuỗi
name = "AI Engineer"
multi_line = """
Dòng 1
Dòng 2
"""

# Boolean
is_active = True

# None
result = None
```

### 1.2 Collections
```python
# List — mutable, ordered
numbers = [1, 2, 3, 4, 5]
numbers.append(6)
numbers[0]  # 1

# Tuple — immutable, ordered
point = (3, 4)
x, y = point  # unpacking

# Dictionary — key-value pairs
student = {
    "name": "Minh",
    "age": 25,
    "scores": [90, 85, 92]
}
student["name"]  # "Minh"
student.get("email", "N/A")  # "N/A"

# Set — unique, unordered
unique_nums = {1, 2, 3, 2, 1}  # {1, 2, 3}
```

### 1.3 Control Flow
```python
# If-elif-else
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"

# For loop
for i in range(5):      # 0, 1, 2, 3, 4
    print(i)

for name, score in student_scores.items():
    print(f"{name}: {score}")

# While loop
count = 0
while count < 5:
    count += 1

# Comprehensions — QUAN TRỌNG cho AI
squares = [x**2 for x in range(10)]
even_squares = [x**2 for x in range(10) if x % 2 == 0]
word_lengths = {word: len(word) for word in ["hello", "world", "AI"]}
```

### 1.4 Functions
```python
# Basic function
def calculate_mse(y_true, y_pred):
    """Tính Mean Squared Error"""
    n = len(y_true)
    mse = sum((yt - yp)**2 for yt, yp in zip(y_true, y_pred)) / n
    return mse

# Default arguments
def train(model, epochs=10, lr=0.001):
    pass

# *args và **kwargs
def flexible_function(*args, **kwargs):
    print(f"Positional: {args}")
    print(f"Keyword: {kwargs}")

# Lambda
square = lambda x: x**2
sorted_data = sorted(data, key=lambda x: x["score"], reverse=True)
```

---

## 2. Python nâng cao cho AI

### 2.1 Generators — Xử lý dữ liệu lớn
```python
# Generator function — tiết kiệm RAM
def data_loader(file_path, batch_size=32):
    """Load dữ liệu theo batch, không load toàn bộ vào RAM"""
    batch = []
    with open(file_path, 'r') as f:
        for line in f:
            batch.append(line.strip())
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch

# Sử dụng
for batch in data_loader("data.txt", batch_size=64):
    process(batch)

# Generator expression
sum_squares = sum(x**2 for x in range(1_000_000))  # không tạo list
```

### 2.2 Decorators — Dùng nhiều trong ML frameworks
```python
import time
import functools

# Timer decorator — đo thời gian training
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.2f}s")
        return result
    return wrapper

@timer
def train_model(data, epochs=10):
    # training code...
    pass

# Decorator with arguments
def retry(max_attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"Retry {attempt + 1}/{max_attempts}: {e}")
        return wrapper
    return decorator

@retry(max_attempts=3)
def download_data(url):
    pass
```

### 2.3 Context Manager
```python
# Sử dụng with statement
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Custom context manager
from contextlib import contextmanager

@contextmanager
def gpu_memory_tracker():
    """Theo dõi GPU memory usage"""
    import torch
    torch.cuda.reset_peak_memory_stats()
    yield
    peak_memory = torch.cuda.max_memory_allocated() / 1e9
    print(f"Peak GPU memory: {peak_memory:.2f} GB")

with gpu_memory_tracker():
    # training code
    pass
```

### 2.4 Classes — OOP cho ML
```python
class NeuralNetwork:
    def __init__(self, layers):
        self.layers = layers
        self.weights = self._initialize_weights()
        self.history = {"loss": [], "accuracy": []}
    
    def _initialize_weights(self):
        """Khởi tạo weights ngẫu nhiên"""
        import numpy as np
        weights = []
        for i in range(len(self.layers) - 1):
            w = np.random.randn(self.layers[i], self.layers[i+1]) * 0.01
            weights.append(w)
        return weights
    
    def forward(self, X):
        """Forward propagation"""
        activation = X
        for w in self.weights:
            activation = self._sigmoid(activation @ w)
        return activation
    
    @staticmethod
    def _sigmoid(z):
        import numpy as np
        return 1 / (1 + np.exp(-z))
    
    def __repr__(self):
        return f"NeuralNetwork(layers={self.layers})"

# Sử dụng
nn = NeuralNetwork([784, 128, 64, 10])
print(nn)  # NeuralNetwork(layers=[784, 128, 64, 10])
```

### 2.5 Type Hints — Clean code
```python
from typing import List, Dict, Tuple, Optional, Union
import numpy as np

def preprocess_data(
    data: List[Dict[str, float]],
    normalize: bool = True,
    fill_value: Optional[float] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Tiền xử lý dữ liệu.
    
    Args:
        data: List các dictionary chứa features
        normalize: Có normalize hay không
        fill_value: Giá trị thay thế missing data
    
    Returns:
        Tuple (X_features, y_labels)
    """
    pass
```

---

## 3. Thư viện Python quan trọng cho AI

### Tổng quan
| Thư viện | Mục đích | Cài đặt |
|----------|---------|---------|
| NumPy | Tính toán ma trận | `pip install numpy` |
| Pandas | Xử lý dữ liệu bảng | `pip install pandas` |
| Matplotlib/Seaborn | Trực quan hóa | `pip install matplotlib seaborn` |
| Scikit-learn | ML cơ bản | `pip install scikit-learn` |
| PyTorch | Deep Learning | `pip install torch` |
| Hugging Face | NLP/LLM | `pip install transformers` |

### Setup môi trường
```bash
# Tạo virtual environment
python -m venv ai_env

# Activate (Windows)
ai_env\Scripts\activate

# Activate (Linux/Mac)
source ai_env/bin/activate

# Cài packages
pip install numpy pandas matplotlib seaborn scikit-learn jupyter

# HOẶC dùng conda
conda create -n ai_env python=3.11
conda activate ai_env
conda install numpy pandas matplotlib seaborn scikit-learn jupyter
```

---

## 📝 Bài tập

### Bài 1: Python cơ bản
1. Viết function `flatten(nested_list)` biến list lồng nhau thành list phẳng
2. Viết generator `fibonacci(n)` tạo n số Fibonacci
3. Viết decorator `@cache` lưu kết quả function (memoization)

### Bài 2: Data Processing
1. Đọc file CSV chứa dữ liệu sinh viên, tính điểm trung bình mỗi lớp
2. Viết class `DataPipeline` với các method: `load()`, `clean()`, `transform()`, `save()`
3. Xử lý file JSON chứa 1 triệu records — dùng generator để không hết RAM

### Bài 3: Mini Project
Viết chương trình phân tích văn bản:
- Đếm tần suất từ
- Tìm top 10 từ phổ biến nhất
- Tính TF-IDF đơn giản (không dùng thư viện)

---

## 📚 Tài liệu
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- *Fluent Python* — Luciano Ramalho
- *Python Cookbook* — David Beazley
