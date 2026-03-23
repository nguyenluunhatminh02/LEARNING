# Bài 02: Authentication & Authorization

## 🎯 Mục tiêu
- OAuth 2.0, OpenID Connect flows
- JWT best practices & pitfalls
- RBAC vs ABAC
- Session management & multi-factor auth

## 📖 Câu chuyện đời thường
> **Authentication** = xác minh "bạn là ai" (như xuất trình CMND ở cửa). **Authorization** = xác minh "bạn được làm gì" (nhân viên vào phòng làm việc OK, nhưng không vào phòng giám đốc). **OAuth 2.0** giống như bạn để người giúp việc dùng chung WiFi nhưng không đưa mật khẩu router — bạn tạo một "token tạm" có giới hạn. **JWT** giống vé xem phim: ghi rõ tên, phòng, gió, ghế — nhân viên chỉ cần xem vé không cần gọi lại quầy. **MFA** là "khóa 2 lới": có chìa khóa (password) còn cần mã OTP trên điện thoại nữa.

---

## 1. Authentication vs Authorization

```
Authentication (AuthN): WHO are you?
  → Login, password, MFA, biometrics
  → "Prove your identity"

Authorization (AuthZ): WHAT can you do?
  → Permissions, roles, policies
  → "You're allowed to access X but not Y"

Flow:
  User → AuthN (login) → Get token → Request resource → AuthZ (check permission) → Allow/Deny
```

---

## 2. OAuth 2.0 & OpenID Connect

```
OAuth 2.0 = Authorization framework (delegate access)
OIDC = Identity layer on top of OAuth (authentication)

Authorization Code Flow (most secure, for web apps):
┌──────┐     ┌───────────┐     ┌──────────────┐
│ User │ ──→ │ Your App  │ ──→ │ Auth Server  │
│      │     │ (Client)  │     │ (Google/Auth0)│
└──────┘     └───────────┘     └──────────────┘
  1. User clicks "Login with Google"
  2. App redirects to Auth Server with client_id, redirect_uri, scope
  3. User authenticates with Auth Server
  4. Auth Server redirects back with authorization_code
  5. App exchanges code for tokens (server-side, secure)
  6. App gets: access_token + id_token + refresh_token

PKCE Extension (for mobile/SPA):
  + code_verifier (random string)
  + code_challenge = SHA256(code_verifier)
  Prevents authorization code interception
```

---

## 3. JWT (JSON Web Token)

```python
# Structure: header.payload.signature
# eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ1MTIzIiwiZXhwIjoxNzA5MjAwMDAwfQ.signature

import jwt
from datetime import datetime, timedelta, timezone

# ✅ GOOD: Use RS256 (asymmetric) for distributed systems
PRIVATE_KEY = load_private_key()  # Only auth server has this
PUBLIC_KEY = load_public_key()    # All services can verify

def create_token(user_id: str, roles: list[str]) -> str:
    payload = {
        "sub": user_id,
        "roles": roles,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),  # Short-lived!
        "iss": "auth.myapp.com",
        "aud": "api.myapp.com",
    }
    return jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")

def verify_token(token: str) -> dict:
    return jwt.decode(
        token, PUBLIC_KEY, 
        algorithms=["RS256"],          # Explicit algorithm!
        audience="api.myapp.com",      # Verify audience
        issuer="auth.myapp.com",       # Verify issuer
    )

# JWT Pitfalls:
# ❌ algorithm="none" → disable signature verification
# ❌ Long expiry (hours/days) → can't revoke
# ❌ Storing sensitive data in payload (it's base64, not encrypted)
# ❌ Using HS256 with shared secret in microservices

# ✅ Best Practices:
# - Access token: 15min expiry
# - Refresh token: 7 days, stored securely, rotated on use
# - Always verify: exp, iss, aud, algorithm
# - Use RS256 for services, HS256 only for single server
```

---

## 4. RBAC vs ABAC

```python
# RBAC (Role-Based Access Control)
# Simple, works for most applications
ROLES = {
    "admin":   ["read", "write", "delete", "manage_users"],
    "editor":  ["read", "write"],
    "viewer":  ["read"],
}

def check_permission(user, action):
    return action in ROLES.get(user.role, [])

# ABAC (Attribute-Based Access Control)
# Fine-grained, policy-based
# "User can edit document IF user.department == doc.department 
#  AND doc.status != 'published' AND current_time is business_hours"

def check_policy(user, action, resource, context):
    policies = [
        # Owner can always edit their own resources
        lambda: action == "edit" and resource.owner_id == user.id,
        # Department managers can approve within their department
        lambda: (action == "approve" 
                 and user.role == "manager" 
                 and user.department == resource.department),
        # Only during business hours
        lambda: (action in ["write", "delete"] 
                 and 9 <= context["hour"] <= 17),
    ]
    return any(p() for p in policies)

# When to use which:
# RBAC: Simple apps, < 10 roles, permission is role-based
# ABAC: Complex orgs, dynamic rules, context-dependent access
# Hybrid: RBAC for basic structure + ABAC for edge cases
```

---

## 5. Session Management

```python
# Server-side sessions (stateful — more secure)
import secrets
from redis import Redis

redis = Redis()

def create_session(user_id: str) -> str:
    session_id = secrets.token_urlsafe(32)  # Cryptographically secure
    redis.setex(
        f"session:{session_id}", 
        3600,  # 1 hour TTL
        json.dumps({"user_id": user_id, "created": time.time()})
    )
    return session_id

# Set-Cookie: session_id=abc123; 
#   HttpOnly;    ← JS cannot access (prevents XSS theft)
#   Secure;      ← Only sent over HTTPS
#   SameSite=Lax; ← CSRF protection
#   Path=/;
#   Max-Age=3600

# Session security:
# - Regenerate session ID after login (prevent fixation)
# - Invalidate on logout (delete from Redis)
# - Absolute timeout: max 8 hours regardless of activity
# - Idle timeout: expire after 30min of inactivity
# - Bind to IP/User-Agent (optional, may break on mobile)
```

---

## 6. Multi-Factor Authentication (MFA)

```
Factors:
1. Something you KNOW     — password, PIN
2. Something you HAVE     — phone (TOTP), hardware key (YubiKey)
3. Something you ARE      — fingerprint, face ID

TOTP (Time-based One-Time Password):
  Shared secret + current time → 6-digit code
  Changes every 30 seconds
  Apps: Google Authenticator, Authy

WebAuthn/FIDO2 (strongest):
  Hardware security key or biometrics
  Public key cryptography — no shared secret
  Phishing-resistant — bound to specific domain

Implementation priority:
  1. Password + TOTP (good)
  2. Password + WebAuthn (better)
  3. Passkeys — passwordless WebAuthn (best)
```

---

## 📝 Bài tập

1. Implement OAuth 2.0 Authorization Code + PKCE flow
2. Build JWT auth system: access token (15min) + refresh token rotation
3. Implement RBAC middleware cho FastAPI
4. Add TOTP-based MFA to login flow

---

## 📚 Tài liệu
- [OAuth 2.0 RFC 6749](https://tools.ietf.org/html/rfc6749)
- [JWT Best Practices RFC 8725](https://tools.ietf.org/html/rfc8725)
- *OAuth 2 in Action* — Justin Richer

## 🔗 Liên kết chéo
- → **SE Bài 06: API Design** — implement auth cho REST/GraphQL APIs
- → **AI Bài 29: Model Deployment** — protect ML serving endpoints
- → **System Design Bài 14-15: Security Design** — auth trong distributed systems
- → **DB Bài 10: Security & Encryption** — database-level access control
