# Bài 01: Clean Code & SOLID Principles

## 🎯 Mục tiêu
- Viết code readable, maintainable
- SOLID principles
- Code smells & refactoring

---

## 1. Clean Code Rules

### Naming
```python
# ❌ Bad
d = 86400
def calc(a, b, c): ...
lst = get_them()

# ✅ Good
SECONDS_PER_DAY = 86400
def calculate_shipping_cost(weight, distance, priority): ...
active_users = get_active_users()

# Rules:
# - Variables: nouns (user_count, order_status)
# - Functions: verbs (get_user, calculate_total, validate_email)
# - Booleans: is/has/can (is_active, has_permission, can_delete)
# - Classes: nouns (UserService, OrderRepository)
# - Constants: UPPER_SNAKE (MAX_RETRY_COUNT)
```

### Functions
```python
# ❌ Bad: does too many things
def process_order(order):
    validate_order(order)
    charge_payment(order)
    update_inventory(order)
    send_email(order)
    update_analytics(order)

# ✅ Good: single responsibility, small, do one thing
def process_order(order):
    validated_order = validate_order(order)
    payment = charge_payment(validated_order)
    update_inventory(validated_order)
    notify_customer(validated_order, payment)

# Rules:
# - Max 20 lines per function
# - Max 3 parameters (use object if more)
# - No side effects (or name them clearly)
# - One level of abstraction per function
```

---

## 2. SOLID Principles

### S — Single Responsibility
```python
# ❌ One class does everything
class User:
    def save_to_db(self): ...
    def send_email(self): ...
    def generate_report(self): ...

# ✅ Each class = one reason to change
class User:
    def __init__(self, name, email): ...

class UserRepository:
    def save(self, user): ...

class EmailService:
    def send_welcome(self, user): ...
```

### O — Open/Closed (open for extension, closed for modification)
```python
# ❌ Modify existing code for each new type
def calculate_area(shape):
    if shape.type == "circle":
        return 3.14 * shape.radius ** 2
    elif shape.type == "rectangle":
        return shape.width * shape.height
    # Add new elif for each shape...

# ✅ Extend via new classes
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...

class Circle(Shape):
    def __init__(self, radius): self.radius = radius
    def area(self): return 3.14 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h
# Add Triangle without touching existing code
```

### L — Liskov Substitution
```python
# Child must be substitutable for parent
# ❌ Square violates Rectangle contract
class Rectangle:
    def set_width(self, w): self.width = w
    def set_height(self, h): self.height = h

class Square(Rectangle):
    def set_width(self, w): self.width = self.height = w  # ❌ breaks expectations

# ✅ Separate abstractions
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
```

### I — Interface Segregation
```python
# ❌ Fat interface forces unnecessary implementations
class Worker(ABC):
    @abstractmethod
    def work(self): ...
    @abstractmethod
    def eat(self): ...  # Robot doesn't eat!

# ✅ Small, focused interfaces
class Workable(ABC):
    @abstractmethod
    def work(self): ...

class Feedable(ABC):
    @abstractmethod
    def eat(self): ...

class Human(Workable, Feedable): ...
class Robot(Workable): ...
```

### D — Dependency Inversion
```python
# ❌ High-level depends on low-level
class OrderService:
    def __init__(self):
        self.db = PostgresDB()  # tightly coupled
        self.mailer = SmtpMailer()  # tightly coupled

# ✅ Depend on abstractions
class OrderService:
    def __init__(self, db: DatabasePort, mailer: MailerPort):
        self.db = db
        self.mailer = mailer

# Inject at runtime
service = OrderService(db=PostgresDB(), mailer=SmtpMailer())
# Test with mocks
service = OrderService(db=InMemoryDB(), mailer=MockMailer())
```

---

## 3. Code Smells

```
Long Method:       >20 lines → extract methods
God Class:         >300 lines, does everything → split
Feature Envy:      Method uses another class's data more → move it
Primitive Obsession: Use domain types (Money, Email) instead of string/int
Magic Numbers:     42 → MAX_CONNECTIONS = 42
Deep Nesting:      if → if → if → guard clause / early return
Shotgun Surgery:   1 change requires editing 10 files → consolidate
```

---

## 📝 Bài tập

1. Refactor a 200-line function into clean, SOLID code
2. Áp dụng SOLID cho e-commerce: OrderService, PaymentService, NotificationService
3. Identify 10 code smells trong codebase thực tế, refactor
4. Viết code review checklist dựa trên Clean Code principles

---

## 📚 Tài liệu
- *Clean Code* — Robert C. Martin ⭐
- *Refactoring* — Martin Fowler ⭐
- *A Philosophy of Software Design* — John Ousterhout
