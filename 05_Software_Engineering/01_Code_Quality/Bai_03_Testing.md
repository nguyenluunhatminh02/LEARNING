# Bài 03: Testing Strategy

## 🎯 Mục tiêu
- Test Pyramid: Unit → Integration → E2E
- TDD (Test-Driven Development)
- Mocking, fixtures, test patterns

---

## 1. Test Pyramid

```
        /  E2E  \         Slow, expensive, few
       / Integration \     Medium speed, moderate
      /    Unit Tests  \   Fast, cheap, many
     ──────────────────

Unit:        70% of tests — test single function/class, no dependencies
Integration: 20% — test modules working together, real DB/API
E2E:         10% — test full user flow, browser/UI
```

---

## 2. Unit Testing (pytest)

```python
# src/services/pricing.py
class PricingService:
    def calculate_discount(self, price, discount_pct):
        if discount_pct < 0 or discount_pct > 100:
            raise ValueError("Discount must be 0–100")
        return price * (1 - discount_pct / 100)
    
    def calculate_total(self, items, tax_rate=0.1):
        subtotal = sum(item.price * item.quantity for item in items)
        return subtotal * (1 + tax_rate)

# tests/test_pricing.py
import pytest
from services.pricing import PricingService

class TestPricingService:
    def setup_method(self):
        self.service = PricingService()
    
    def test_calculate_discount_normal(self):
        assert self.service.calculate_discount(100, 20) == 80.0
    
    def test_calculate_discount_zero(self):
        assert self.service.calculate_discount(100, 0) == 100.0
    
    def test_calculate_discount_invalid_raises(self):
        with pytest.raises(ValueError):
            self.service.calculate_discount(100, -10)
    
    @pytest.mark.parametrize("price,discount,expected", [
        (100, 10, 90), (200, 50, 100), (50, 0, 50), (100, 100, 0)
    ])
    def test_calculate_discount_parametrized(self, price, discount, expected):
        assert self.service.calculate_discount(price, discount) == expected
```

---

## 3. Mocking

```python
from unittest.mock import Mock, patch, MagicMock

# Mock external dependency
class OrderService:
    def __init__(self, payment_gateway, email_service):
        self.payment = payment_gateway
        self.email = email_service
    
    def place_order(self, order):
        receipt = self.payment.charge(order.total)
        self.email.send_confirmation(order.user_email, receipt)
        return receipt

def test_place_order():
    mock_payment = Mock()
    mock_payment.charge.return_value = {"id": "pay_123", "status": "success"}
    mock_email = Mock()
    
    service = OrderService(mock_payment, mock_email)
    result = service.place_order(order)
    
    mock_payment.charge.assert_called_once_with(order.total)
    mock_email.send_confirmation.assert_called_once()
    assert result["status"] == "success"

# Patch external module
@patch('services.order.requests.post')
def test_webhook(mock_post):
    mock_post.return_value.status_code = 200
    result = send_webhook("https://example.com", data)
    assert result == True
```

---

## 4. Integration Testing

```python
import pytest
from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def db():
    with PostgresContainer("postgres:16") as postgres:
        engine = create_engine(postgres.get_connection_url())
        create_tables(engine)
        yield engine

def test_user_repository_save(db):
    repo = UserRepository(db)
    user = User(name="Alice", email="alice@test.com")
    
    saved = repo.save(user)
    found = repo.find_by_id(saved.id)
    
    assert found.name == "Alice"
    assert found.email == "alice@test.com"

def test_user_repository_unique_email(db):
    repo = UserRepository(db)
    repo.save(User(name="Alice", email="alice@test.com"))
    
    with pytest.raises(IntegrityError):
        repo.save(User(name="Bob", email="alice@test.com"))
```

---

## 5. TDD — Red → Green → Refactor

```
1. RED:    Write failing test
2. GREEN:  Write minimum code to pass
3. REFACTOR: Improve code, keep tests green

# Step 1: RED
def test_fizzbuzz_3():
    assert fizzbuzz(3) == "Fizz"
# → NameError: fizzbuzz not defined

# Step 2: GREEN
def fizzbuzz(n):
    if n % 3 == 0: return "Fizz"
    return str(n)
# → test passes

# Step 3: Add more tests → extend code
def test_fizzbuzz_5():
    assert fizzbuzz(5) == "Buzz"

def test_fizzbuzz_15():
    assert fizzbuzz(15) == "FizzBuzz"
```

---

## 6. What NOT to Test

```
❌ Private methods (test via public interface)
❌ Framework code (Django ORM, FastAPI routing)
❌ Simple getters/setters
❌ Third-party libraries
❌ Implementation details (test behavior, not structure)
```

---

## 📝 Bài tập

1. Viết unit tests cho PricingService (>90% coverage)
2. TDD: build FizzBuzz → Calculator → Stack from scratch
3. Integration test với real PostgreSQL (testcontainers)
4. Mock external API, test error handling scenarios

---

## 📚 Tài liệu
- *Test-Driven Development* — Kent Beck
- *Unit Testing* — Vladimir Khorikov
- [pytest Documentation](https://docs.pytest.org/)
