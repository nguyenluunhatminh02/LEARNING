# Bài 06: Container & Kubernetes Security

## 🎯 Mục tiêu
- Docker security best practices
- Kubernetes RBAC & Pod Security
- Secrets management trong K8s
- Image scanning & runtime security

## 📖 Câu chuyện đời thường
> **Container** giống như căn hộ trong chung cư. Mỗi ứng dụng sống trong căn hộ riêng, không nhìn thấy căn khác. **Docker security** = không cho người thuê khóa mỗi căn chạy bằng quyền admin (root), chỉ cho vào các tầng được phép. **K8s RBAC** = quản lý ai được vào tầng nào: nhân viên bảo trì vào hầm xe, cư dân vào căn mình, quản lý vào mọi nơi. **Image scanning** giống kiểm tra an ninh trước khi dọn vào: xem căn hộ có vấn đề gì không (vulnerabilities). **Secrets management** = không dán mật khẩu WiFi lên tường mà cất trong két sắt.

---

## 1. Docker Security

```dockerfile
# ❌ BAD Dockerfile
FROM ubuntu:latest            # Unversioned, large attack surface
RUN apt-get update && apt-get install -y python3 curl wget vim
COPY . /app                   # Copies secrets, .git, everything
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]     # Runs as root!

# ✅ SECURE Dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim
# Non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser src/ ./src/
ENV PATH=/home/appuser/.local/bin:$PATH
USER appuser
# Read-only filesystem
EXPOSE 8000
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```
Docker Security Checklist:
✅ Use specific base image tags (python:3.12-slim, NOT :latest)
✅ Multi-stage builds (minimize final image size & attack surface)
✅ Non-root user (USER appuser)
✅ .dockerignore (exclude .git, .env, secrets, tests)
✅ No secrets in image (use runtime env vars / secrets manager)
✅ Minimal packages (slim/alpine, no curl/wget/vim in prod)
✅ Read-only root filesystem (--read-only flag)
✅ Health checks
```

---

## 2. Image Scanning

```bash
# Scan for known CVEs in container images
# Tools: Trivy, Snyk, Grype, AWS ECR scanning

# Trivy (most popular, free)
trivy image myapp:latest
# → CVE-2024-1234 HIGH python3.12 numpy < 1.26.4
# → CVE-2024-5678 CRITICAL openssl < 3.2.1

# In CI/CD pipeline:
# - Scan on every build
# - Block deployment if CRITICAL or HIGH CVEs
# - Auto-create issues for MEDIUM vulnerabilities
```

```yaml
# GitHub Actions — image scanning
- name: Scan image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    severity: CRITICAL,HIGH
    exit-code: 1  # Fail pipeline if vulnerabilities found
```

---

## 3. Kubernetes RBAC

```yaml
# Principle of Least Privilege
# Each service account gets ONLY what it needs

# ServiceAccount for the app
apiVersion: v1
kind: ServiceAccount
metadata:
  name: order-service
  namespace: production

---
# Role: what permissions?
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: order-service-role
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["configmaps"]
    verbs: ["get", "list"]         # Read-only configmaps
  - apiGroups: [""]
    resources: ["secrets"]
    resourceNames: ["order-db-credentials"]  # Only specific secret
    verbs: ["get"]

---
# RoleBinding: attach role to service account
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: order-service-binding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: order-service
roleRef:
  kind: Role
  name: order-service-role
  apiGroup: rbac.authorization.k8s.io
```

---

## 4. Pod Security

```yaml
# Pod Security Standards: Restricted (most secure)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  template:
    spec:
      serviceAccountName: order-service
      automountServiceAccountToken: false  # Don't auto-mount unless needed
      
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      
      containers:
        - name: app
          image: myapp:v1.2.3@sha256:abc123...  # Pin by digest
          
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: ["ALL"]
          
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      
      volumes:
        - name: tmp
          emptyDir: {}  # Writable temp dir (root FS is read-only)
```

---

## 5. Network Policies

```yaml
# Default: deny all ingress (zero trust)
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes: ["Ingress", "Egress"]

---
# Allow specific traffic: order-service ← only from API gateway
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: order-service-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: order-service
  policyTypes: ["Ingress"]
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: api-gateway
      ports:
        - port: 8000
          protocol: TCP
```

---

## 6. Secrets in Kubernetes

```yaml
# ❌ Basic K8s Secrets (base64 encoded, NOT encrypted)
# Anyone with RBAC access can read them

# ✅ External Secrets Operator — sync from Vault/AWS SM
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: order-db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: order-db-credentials
  data:
    - secretKey: password
      remoteRef:
        key: prod/order-service/db
        property: password

# ✅ Enable encryption at rest for K8s secrets
# etcd encryption configuration on cluster level
# ✅ Use Sealed Secrets for GitOps (encrypted in git, decrypted in cluster)
```

---

## 📝 Bài tập

1. Harden Dockerfile: multi-stage, non-root, read-only
2. Setup Trivy scanning trong CI pipeline
3. Configure K8s RBAC cho 3 services với least privilege
4. Implement NetworkPolicies: default deny + explicit allow

---

## 📚 Tài liệu
- *Kubernetes Security* — Liz Rice
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
