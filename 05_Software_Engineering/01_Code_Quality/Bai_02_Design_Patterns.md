# Bài 02: Design Patterns

## 🎯 Mục tiêu
- Creational, Structural, Behavioral patterns
- Khi nào dùng pattern nào
- Anti-patterns to avoid

## 📖 Câu chuyện đời thường
> Design Patterns giống như **công thức nấu ăn đã được chứng minh**. Bạn không cần phát minh lại cách nấu phở — có công thức sẵn rồi. **Singleton** giống giám đốc công ty — chỉ có duy nhất 1 người. **Factory** giống tiệm bánh: nói "cho 1 bánh chocolate", tiệm tự biết cách làm. **Observer** giống đăng ký nhận thông báo YouTube: khi có video mới, tất cả subscriber đều được báo. **Strategy** giống chọn cách đi làm: hôm nay xe máy, mai trời mưa đi Grab, mốt đi bus — cùng mục đích (di chuyển) nhưng chiến lược khác nhau. **Anti-pattern** = công thức sai mà nhiều người hay mắc.

---

## 1. Creational Patterns

### Factory Method
```python
class NotificationFactory:
    @staticmethod
    def create(channel: str) -> Notification:
        if channel == "email": return EmailNotification()
        if channel == "sms": return SmsNotification()
        if channel == "push": return PushNotification()
        raise ValueError(f"Unknown channel: {channel}")

# Usage: notification = NotificationFactory.create("email")
```

### Singleton
```python
class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = create_connection()
        return cls._instance

# Better: dependency injection thay vì singleton (testable)
```

### Builder
```python
class QueryBuilder:
    def __init__(self):
        self._table = None
        self._conditions = []
        self._order = None
        self._limit = None
    
    def table(self, name):
        self._table = name; return self
    
    def where(self, condition):
        self._conditions.append(condition); return self
    
    def order_by(self, field):
        self._order = field; return self
    
    def limit(self, n):
        self._limit = n; return self
    
    def build(self):
        query = f"SELECT * FROM {self._table}"
        if self._conditions:
            query += " WHERE " + " AND ".join(self._conditions)
        if self._order: query += f" ORDER BY {self._order}"
        if self._limit: query += f" LIMIT {self._limit}"
        return query

# Usage
query = (QueryBuilder()
    .table("users")
    .where("age > 18")
    .where("is_active = true")
    .order_by("created_at DESC")
    .limit(10)
    .build())
```

---

## 2. Structural Patterns

### Adapter
```python
# Adapt external payment API to our interface
class StripeAdapter(PaymentGateway):
    def __init__(self):
        self.stripe = StripeAPI()
    
    def charge(self, amount, currency, card_token):
        # Adapt our interface to Stripe's API
        return self.stripe.create_charge(
            amount_cents=int(amount * 100),
            currency=currency.lower(),
            source=card_token
        )
```

### Decorator
```python
# Add behavior without modifying existing code
import functools, time

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(delay * (2 ** attempt))
        return wrapper
    return decorator

@retry(max_attempts=3)
def call_external_api():
    return requests.get("https://api.example.com/data")
```

### Repository Pattern
```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, id: int) -> User: ...
    @abstractmethod
    def find_by_email(self, email: str) -> User: ...
    @abstractmethod
    def save(self, user: User) -> User: ...

class PostgresUserRepository(UserRepository):
    def find_by_id(self, id):
        row = self.db.execute("SELECT * FROM users WHERE id = %s", id)
        return User.from_row(row)

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
    def find_by_id(self, id):
        return self.users.get(id)
```

---

## 3. Behavioral Patterns

### Strategy
```python
class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, base_price: float) -> float: ...

class RegularPricing(PricingStrategy):
    def calculate(self, base_price): return base_price

class PremiumPricing(PricingStrategy):
    def calculate(self, base_price): return base_price * 0.9  # 10% off

class OrderService:
    def __init__(self, pricing: PricingStrategy):
        self.pricing = pricing
    
    def total(self, items):
        return sum(self.pricing.calculate(item.price) for item in items)
```

### Observer (Event System)
```python
class EventBus:
    def __init__(self):
        self._handlers = {}
    
    def subscribe(self, event_type, handler):
        self._handlers.setdefault(event_type, []).append(handler)
    
    def publish(self, event_type, data):
        for handler in self._handlers.get(event_type, []):
            handler(data)

bus = EventBus()
bus.subscribe("order_created", send_confirmation_email)
bus.subscribe("order_created", update_inventory)
bus.subscribe("order_created", notify_warehouse)
bus.publish("order_created", order)
```

### Chain of Responsibility
```python
class Handler(ABC):
    def __init__(self, next_handler=None):
        self._next = next_handler
    
    def handle(self, request):
        if self.can_handle(request):
            return self.process(request)
        if self._next:
            return self._next.handle(request)
        raise Exception("No handler found")

class AuthHandler(Handler):
    def can_handle(self, req): return 'auth' not in req
    def process(self, req): ...

class RateLimitHandler(Handler):
    def can_handle(self, req): return req.get('rate_exceeded')
    def process(self, req): ...

# Chain: Auth → RateLimit → Validation → Business Logic
pipeline = AuthHandler(RateLimitHandler(ValidationHandler(BusinessHandler())))
```

---

## 📝 Bài tập

1. Implement Strategy pattern cho discount calculation
2. Build plugin system bằng Factory + Registry pattern
3. Refactor if/else chain thành Strategy hoặc Chain of Responsibility
4. Implement Event Bus cho order processing pipeline

---

## 📚 Tài liệu
- *Design Patterns* — GoF (Gang of Four)
- *Head First Design Patterns*
- [Refactoring Guru](https://refactoring.guru/design-patterns)
