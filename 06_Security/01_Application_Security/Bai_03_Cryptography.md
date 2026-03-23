# Bài 03: Cryptography Fundamentals

## 🎯 Mục tiêu
- Hashing, symmetric & asymmetric encryption
- TLS/HTTPS
- Key management & secrets handling

## 📖 Câu chuyện đời thường
> **Hashing** giống dấu vân tay: từ vân tay suy ra được người nhưng không thể từ người suy ra vân tay (một chiều). Dùng để lưu mật khẩu: không lưu "abc123" mà lưu vân tay của nó. **Symmetric encryption** giống hộp khóa chung: bạn và người nhận dùng cùng 1 chìa khóa — nhanh nhưng phải tìm cách trao chìa khóa an toàn. **Asymmetric** giống hòm thư công cộng: ai cũng bỏ thư vào được (public key) nhưng chỉ bạn mới mở ra đọc (private key). **TLS** là việc 2 người bắt tay nhau và thỏa thuận cách mã hóa trước khi nói chuyện bí mật.

---

## 1. Hashing

```python
import hashlib
import bcrypt

# Hash = one-way function, same input → same output, irreversible
# Use cases: password storage, data integrity, deduplication

# ❌ NEVER use for passwords:
md5 = hashlib.md5(b"password").hexdigest()     # Fast, broken
sha256 = hashlib.sha256(b"password").hexdigest() # Fast, not for passwords

# ✅ Password hashing (slow by design, with salt)
password = "user_password_123"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
# → $2b$12$LJ3m4ys3Lk0dXqLGJEMULOxGxb... (includes salt)

# Verify
is_valid = bcrypt.checkpw(password.encode(), hashed)

# Why bcrypt/argon2?
# - SLOW: ~100ms per hash (vs nanoseconds for SHA256)
# - Salt: random per-password, prevents rainbow tables
# - Cost factor: adjustable (rounds=12 → 2^12 iterations)

# Even better: Argon2 (winner of Password Hashing Competition)
from argon2 import PasswordHasher
ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)
hash_val = ph.hash(password)
ph.verify(hash_val, password)  # Raises exception if invalid
```

---

## 2. Symmetric Encryption

```python
# Same key for encrypt & decrypt
# Fast, for large data
# AES-256-GCM (authenticated encryption — ensures integrity + confidentiality)

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

# Simple: Fernet (AES-CBC + HMAC, good default)
key = Fernet.generate_key()  # Store securely!
cipher = Fernet(key)
encrypted = cipher.encrypt(b"sensitive data")
decrypted = cipher.decrypt(encrypted)

# Advanced: AES-256-GCM (for custom needs)
key = AESGCM.generate_key(bit_length=256)
nonce = os.urandom(12)  # MUST be unique per encryption
aesgcm = AESGCM(key)
encrypted = aesgcm.encrypt(nonce, b"sensitive data", b"additional_auth_data")
decrypted = aesgcm.decrypt(nonce, encrypted, b"additional_auth_data")

# Key points:
# - Never reuse nonce with same key
# - Use authenticated encryption (GCM, not ECB/CBC without HMAC)
# - Key rotation: encrypt with new key, keep old key for decryption
```

---

## 3. Asymmetric Encryption

```python
# Public key (share) + Private key (secret)
# Slow, for small data / key exchange / signatures

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

# Generate key pair
private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
public_key = private_key.public_key()

# Encrypt with public key (anyone can encrypt)
ciphertext = public_key.encrypt(
    b"secret message",
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# Decrypt with private key (only key owner)
plaintext = private_key.decrypt(ciphertext, padding.OAEP(...))

# Digital Signatures (prove authenticity)
signature = private_key.sign(
    b"document content",
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)
# Anyone with public key can verify
public_key.verify(signature, b"document content", padding.PSS(...), hashes.SHA256())

# Use cases:
# RSA: key exchange, digital signatures, JWT signing
# In practice: RSA encrypts AES key → AES encrypts data (hybrid)
```

---

## 4. TLS/HTTPS

```
TLS Handshake (simplified):
1. Client → Server: "Hello, I support TLS 1.3, these cipher suites"
2. Server → Client: "Let's use TLS 1.3 + AES-256-GCM, here's my certificate"
3. Client verifies certificate chain (CA → Intermediate → Server cert)
4. Key exchange (ECDHE): both derive shared secret
5. Encrypted communication begins

Certificate chain:
  Root CA (trusted, in OS/browser)
    → Intermediate CA
      → Your server certificate (domain-specific)

Best practices:
- TLS 1.3 only (disable 1.0, 1.1, 1.2 if possible)
- HSTS header: Strict-Transport-Security: max-age=31536000; includeSubDomains
- Certificate: use Let's Encrypt (free, automated)
- Perfect Forward Secrecy (ECDHE): compromise of server key 
  doesn't decrypt past sessions
```

---

## 5. Secrets Management

```python
# ❌ NEVER: hardcode secrets
API_KEY = "sk-1234567890abcdef"  # In source code → leaked in git

# ❌ AVOID: .env files in production (ok for local dev)

# ✅ GOOD: Environment variables (basic)
import os
api_key = os.environ["API_KEY"]  # Set by deployment platform

# ✅ BETTER: Secrets manager (production)
# AWS Secrets Manager / HashiCorp Vault / GCP Secret Manager
import boto3

def get_secret(secret_name: str) -> str:
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    return response["SecretString"]

db_password = get_secret("prod/database/password")

# Key Management Best Practices:
# 1. Rotate secrets regularly (automated)
# 2. Least privilege: each service gets only secrets it needs
# 3. Audit access: who accessed what secret when
# 4. Never log secrets (mask in logs)
# 5. Use short-lived credentials (IAM roles, not static keys)
# 6. Encrypt at rest AND in transit

# Git protection: pre-commit hooks
# pip install detect-secrets
# detect-secrets scan → finds hardcoded secrets
```

---

## 6. Encryption at Rest & in Transit

```
Data States:
┌────────────────────────────────────────────────────────┐
│ At Rest     → AES-256 encryption (disk, DB, backups)   │
│ In Transit  → TLS 1.3 (network)                        │
│ In Use      → Application-level encryption (specific)   │
└────────────────────────────────────────────────────────┘

Database encryption:
  - Transparent Data Encryption (TDE): entire DB encrypted
  - Column-level encryption: encrypt specific sensitive columns
  - Application-level: encrypt before storing (you control keys)

Choose based on threat model:
  TDE: protects against stolen disks/backups
  Column-level: protects against DB admin access
  App-level: protects against everything except app compromise
```

---

## 📝 Bài tập

1. Implement password hashing with Argon2 + login verification
2. Build encrypt/decrypt utility using AES-256-GCM
3. Setup TLS cho local development (mkcert)
4. Migrate hardcoded secrets to environment variables + secrets manager

---

## 📚 Tài liệu
- *Serious Cryptography* — Jean-Philippe Aumasson
- *Designing Secure Software* — Loren Kohnfelder
- [cryptography.io docs](https://cryptography.io/)
