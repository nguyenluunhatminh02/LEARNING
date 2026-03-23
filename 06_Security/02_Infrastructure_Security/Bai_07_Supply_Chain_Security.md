# Bài 07: Supply Chain Security

## 🎯 Mục tiêu
- Dependency vulnerability scanning
- Software Bill of Materials (SBOM)
- Signed builds & verified artifacts
- Secure CI/CD pipeline

## 📖 Câu chuyện đời thường
> Bạn mở tiệm bánh và mua nguyên liệu từ nhiều nhà cung cấp. **Supply Chain Security** là kiểm tra: bột mì có tạp chất không? sữa có hết hạn không? Nếu 1 nhà cung cấp bị nhiễm độc, cả tiệm bị liên lụy. **SBOM** giống danh sách thành phần trên bao bì thực phẩm: ghi rõ dùng thư viện nào, phiên bản nào — để khi có lỗi bảo mật, biết ngay mình có bị ảnh hưởng không. **Signed builds** giống tem chống giả trên sản phẩm: bảo đảm bánh là do tiệm bạn làm, không bị ai tráo.

---

## 1. Dependency Security

```python
# Modern apps: 90%+ of code is from dependencies
# 1 vulnerable dependency = entire system compromised

# Python: pip-audit
# $ pip-audit
# Found 3 vulnerabilities:
#   numpy 1.24.0  → CVE-2023-xxxxx (HIGH)
#   requests 2.28 → CVE-2023-xxxxx (MEDIUM)

# Automated scanning tools:
# - Dependabot (GitHub) — auto PRs for vulnerable deps
# - Renovate — more configurable, multi-platform
# - Snyk — comprehensive, supports many languages
# - pip-audit / npm audit / cargo audit

# Lock files are critical:
# requirements.txt → pin exact versions
# package-lock.json / yarn.lock → deterministic installs
# poetry.lock / Pipfile.lock → hash verification
```

```toml
# pyproject.toml with version constraints
[tool.poetry.dependencies]
python = "^3.12"
fastapi = "^0.109.0"      # Updated regularly
pydantic = "^2.5.0"
sqlalchemy = "^2.0.25"
# Every dependency is a trust decision
# → Review: who maintains it? Is it actively maintained? 
#   How many downloads? Any known issues?
```

---

## 2. Software Bill of Materials (SBOM)

```
SBOM = Ingredient list for your software
Lists every component, version, license

Why SBOM matters:
- Log4Shell (2021): "Do we use Log4j? Which services?"
- Without SBOM: days to figure out → vulnerability exploited
- With SBOM: minutes to search → patch immediately

Formats:
- SPDX (ISO standard)
- CycloneDX (OWASP standard)

Generate SBOM:
$ syft myapp:latest -o cyclonedx-json > sbom.json

{
  "bomFormat": "CycloneDX",
  "components": [
    {
      "type": "library",
      "name": "fastapi",
      "version": "0.109.0",
      "purl": "pkg:pypi/fastapi@0.109.0"
    },
    ...
  ]
}

Store SBOM:
- Alongside release artifacts
- In container registry (attestation)
- Searchable database (vulnerability response)
```

---

## 3. Signed Builds & Artifact Verification

```
Problem: How do you know the artifact wasn't tampered with?

Supply Chain Attack Vectors:
1. Compromised CI/CD → attacker modifies build
2. Compromised registry → attacker replaces image
3. Typosquatting → attacker publishes similar-named package
4. Dependency confusion → attacker publishes same name to public registry

Solutions:
```

```yaml
# Container Image Signing (cosign / sigstore)
# Sign image after build
# $ cosign sign --key cosign.key myregistry/myapp:v1.2.3

# Verify before deploy (K8s admission controller)
apiVersion: policy.sigstore.dev/v1beta1
kind: ClusterImagePolicy
metadata:
  name: require-signed-images
spec:
  images:
    - glob: "myregistry/**"
  authorities:
    - key:
        data: |
          -----BEGIN PUBLIC KEY-----
          ...
          -----END PUBLIC KEY-----

# Keyless signing with Sigstore (no key management):
# $ cosign sign myregistry/myapp:v1.2.3
# Uses OIDC identity (GitHub, Google) + transparency log
```

---

## 4. Secure CI/CD Pipeline

```yaml
# Hardened GitHub Actions
name: Secure Build
on:
  push:
    branches: [main]

permissions:
  contents: read      # Minimal permissions!
  packages: write     # Only what's needed

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Pin dependencies by hash (not tag)
      - uses: actions/setup-python@39cd14951b08e74b54015e9e001cdefcf80e669f  # v5.1.0
      
      # Dependency audit
      - run: pip-audit -r requirements.txt
      
      # SAST (Static Application Security Testing)
      - uses: returntocorp/semgrep-action@v1
        with:
          config: p/owasp-top-ten
      
      # Build with SBOM
      - run: docker build -t myapp:${{ github.sha }} .
      - run: syft myapp:${{ github.sha }} -o cyclonedx-json > sbom.json
      
      # Scan image
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:${{ github.sha }}
          exit-code: 1
          severity: CRITICAL,HIGH
      
      # Sign image
      - run: cosign sign myregistry/myapp:${{ github.sha }}

# CI/CD Security Principles:
# 1. Pin action versions by SHA (not tag — can be moved)
# 2. Minimal permissions (don't use permissions: write-all)
# 3. Scan at every stage (deps, code, image)
# 4. Sign artifacts
# 5. Separate build and deploy permissions
# 6. Audit logs for all CI/CD activities
# 7. Short-lived credentials (OIDC, not static secrets)
```

---

## 5. Dependency Confusion Prevention

```
Attack: Attacker publishes "internal-utils" to pypi.org
Your CI installs from public registry instead of private

Prevention:
1. Scoped registries
   pip install --index-url https://private.registry.com/simple/
   
2. .npmrc / pip.conf — explicit registry per scope
   [global]
   index-url = https://private.registry.com/simple/
   extra-index-url = https://pypi.org/simple/

3. Namespace packages: @company/package-name

4. Lock files with hashes:
   # requirements.txt
   fastapi==0.109.0 --hash=sha256:abc123...
   # pip install --require-hashes -r requirements.txt
```

---

## 📝 Bài tập

1. Setup Dependabot / Renovate cho repository
2. Generate SBOM cho 1 project, analyze dependencies
3. Implement container image signing with cosign
4. Harden CI/CD pipeline: pin actions, add scanning, minimal permissions

---

## 📚 Tài liệu
- [SLSA Framework](https://slsa.dev/) — Supply chain Levels for Software Artifacts
- [Sigstore](https://www.sigstore.dev/)
- *Software Supply Chain Security* — Cassie Crossley
