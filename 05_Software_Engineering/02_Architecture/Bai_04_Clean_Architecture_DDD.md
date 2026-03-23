# Bài 04: Clean Architecture & Domain-Driven Design

## 🎯 Mục tiêu
- Layered, Hexagonal, Clean Architecture
- DDD: Entities, Value Objects, Aggregates, Bounded Contexts
- Dependency rule

## 📖 Câu chuyện đời thường
> **Clean Architecture** giống như bệnh viện được thiết kế tốt. Vùng lõi là phòng mổ (business logic) — không phụ thuộc vào loại máy móc bên ngoài. Lớp ngoài là quầy lễ tân, hệ thống đặt lịch — thay đổi được mà không ảnh hưởng phòng mổ. **DDD** giống như việc bác sĩ và lập trình viên nói chung ngôn ngữ: khi nói "bệnh nhân", cả 2 hiểu giống nhau (ubiquitous language). **Bounded Context** = phòng Khám và phòng Thuán có thể dùng từ "bệnh nhân" khác nghĩa (người đến khám vs người đang nằm viện) — mỗi phòng là một "thế giới" riêng.

---

## 1. Clean Architecture

```
┌──────────────────────────────────────────┐
│              Frameworks & Drivers        │  FastAPI, PostgreSQL, Redis
│  ┌────────────────────────────────────┐  │
│  │          Interface Adapters        │  │  Controllers, Repos, Presenters
│  │  ┌──────────────────────────────┐  │  │
│  │  │      Application Layer       │  │  │  Use Cases, DTOs, Services
│  │  │  ┌────────────────────────┐  │  │  │
│  │  │  │    Domain Layer        │  │  │  │  Entities, Value Objects, Rules
│  │  │  └────────────────────────┘  │  │  │
│  │  └──────────────────────────────┘  │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘

DEPENDENCY RULE: Dependencies point INWARD only
  Frameworks → Adapters → Application → Domain
  Domain NEVER imports from outer layers
```

### Project Structure
```
src/
├── domain/              # Pure business logic, no frameworks
│   ├── entities/
│   │   ├── order.py     # Order entity with business rules
│   │   └── user.py
│   ├── value_objects/
│   │   ├── money.py
│   │   └── email.py
│   ├── repositories/    # Abstract interfaces (ports)
│   │   └── order_repo.py
│   └── services/
│       └── pricing.py   # Domain service
├── application/         # Use cases, orchestration
│   ├── use_cases/
│   │   ├── create_order.py
│   │   └── cancel_order.py
│   └── dtos/
│       └── order_dto.py
├── infrastructure/      # External implementations (adapters)
│   ├── persistence/
│   │   └── postgres_order_repo.py
│   ├── messaging/
│   │   └── kafka_publisher.py
│   └── external/
│       └── stripe_payment.py
└── api/                 # Framework layer
    ├── routes/
    │   └── order_routes.py
    └── main.py
```

---

## 2. Domain-Driven Design

### Entity (has identity)
```python
class Order:
    def __init__(self, id, user_id, items, status="pending"):
        self.id = id
        self.user_id = user_id
        self.items = items
        self.status = status
    
    def add_item(self, item):
        if self.status != "pending":
            raise DomainError("Cannot modify confirmed order")
        self.items.append(item)
    
    def confirm(self):
        if not self.items:
            raise DomainError("Cannot confirm empty order")
        self.status = "confirmed"
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.items)
```

### Value Object (no identity, immutable)
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str
    
    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __mul__(self, factor):
        return Money(self.amount * factor, self.currency)

@dataclass(frozen=True)
class Email:
    value: str
    
    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError(f"Invalid email: {self.value}")
```

### Aggregate Root
```python
# Order is an Aggregate Root
# → All modifications to OrderItems go THROUGH Order
# → External code never directly modifies OrderItem

class Order:  # Aggregate Root
    def add_item(self, product_id, quantity, price):
        item = OrderItem(product_id, quantity, Money(price, "USD"))
        self._items.append(item)
        self._raise_event(ItemAddedEvent(self.id, item))

class OrderItem:  # Part of Order aggregate
    # Never accessed directly from outside
    pass
```

### Bounded Context
```
E-commerce system:
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │   Ordering   │  │   Payment    │  │   Shipping   │
  │  Context     │  │  Context     │  │  Context     │
  │              │  │              │  │              │
  │ Order        │  │ Payment      │  │ Shipment     │
  │ OrderItem    │  │ Transaction  │  │ Address      │
  │ Customer     │  │ Customer     │  │ Package      │
  │ (id, name)   │  │ (id, card)   │  │ (id, addr)   │
  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
         │                 │                 │
         └─── Events ──────┴─── Events ──────┘

Same "Customer" concept, different representations per context
Integration via Domain Events (not shared DB!)
```

---

## 3. Use Case Layer

```python
class CreateOrderUseCase:
    def __init__(self, order_repo: OrderRepository, 
                 payment: PaymentGateway, publisher: EventPublisher):
        self.order_repo = order_repo
        self.payment = payment
        self.publisher = publisher
    
    def execute(self, request: CreateOrderRequest) -> CreateOrderResponse:
        order = Order.create(request.user_id, request.items)
        
        payment_result = self.payment.charge(order.total)
        if not payment_result.success:
            raise PaymentFailedError(payment_result.error)
        
        order.confirm()
        self.order_repo.save(order)
        
        self.publisher.publish(OrderCreatedEvent(order.id))
        
        return CreateOrderResponse(order_id=order.id, status=order.status)
```

---

## 📝 Bài tập

1. Refactor monolith endpoint thành Clean Architecture layers
2. Model e-commerce domain: Order, Product, Inventory aggregates
3. Implement Value Objects: Money, Email, Address
4. Define Bounded Contexts cho food delivery system

---

## 📚 Tài liệu
- *Clean Architecture* — Robert C. Martin
- *Domain-Driven Design* — Eric Evans
- *Implementing Domain-Driven Design* — Vaughn Vernon
