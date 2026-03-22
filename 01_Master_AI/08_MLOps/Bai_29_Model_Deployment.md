# Bài 29: Model Deployment & Monitoring

## 🎯 Mục tiêu
- Model serving strategies (REST, gRPC, batch)
- Containerized deployment (Docker, K8s)
- Model monitoring: data drift, model drift, concept drift
- A/B testing & canary deployment cho ML models
- CI/CD cho ML (CT — Continuous Training)

> **Prerequisite**: Hoàn thành Bài 28 (ML Pipeline & Experiment Tracking)

---

## 1. Model Serving Patterns

```python
# Pattern 1: REST API (FastAPI) — phổ biến nhất
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import joblib

app = FastAPI(title="ML Prediction Service")

# Load model once at startup (not per request)
model = joblib.load("models/xgboost_v2.joblib")
scaler = joblib.load("models/scaler.joblib")

class PredictionRequest(BaseModel):
    features: list[float]
    model_version: str = "v2"

class PredictionResponse(BaseModel):
    prediction: float
    confidence: float
    model_version: str

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    features = np.array(request.features).reshape(1, -1)
    scaled = scaler.transform(features)
    prediction = model.predict(scaled)[0]
    confidence = float(model.predict_proba(scaled).max())
    return PredictionResponse(
        prediction=prediction,
        confidence=confidence,
        model_version=request.model_version,
    )

@app.get("/health")
async def health():
    return {"status": "healthy", "model_version": "v2"}
```

```python
# Pattern 2: gRPC — low latency, high throughput (service-to-service)
# Proto definition:
# service ModelService {
#   rpc Predict(PredictRequest) returns (PredictResponse);
# }

# Pattern 3: Batch Prediction — large-scale offline
# Spark/Dask job chạy hàng đêm → write predictions to database
# Use case: recommendation scores cho millions of users

# Pattern 4: Edge Deployment — on device
# ONNX Runtime, TensorFlow Lite, Core ML
# Use case: mobile apps, IoT, real-time inference

# Choosing Pattern:
# ┌─────────────────┬──────────────────────────────────┐
# │ Requirement      │ Best Pattern                     │
# ├─────────────────┼──────────────────────────────────┤
# │ Real-time, <50ms│ gRPC + GPU serving               │
# │ Web API, <200ms │ REST (FastAPI/Flask)              │
# │ Millions/day    │ Batch prediction                  │
# │ Mobile/IoT      │ Edge (ONNX/TFLite)               │
# │ LLM inference   │ vLLM / TGI / Triton              │
# └─────────────────┴──────────────────────────────────┘
```

---

## 2. Containerized Deployment

```dockerfile
# Production ML Dockerfile (multi-stage, optimized)
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim
RUN groupadd -r mluser && useradd -r -g mluser mluser
WORKDIR /app

COPY --from=builder /root/.local /home/mluser/.local
COPY --chown=mluser:mluser models/ ./models/
COPY --chown=mluser:mluser src/ ./src/

ENV PATH=/home/mluser/.local/bin:$PATH
ENV MODEL_PATH=/app/models/xgboost_v2.joblib
USER mluser

EXPOSE 8000
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/health || exit 1
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```yaml
# Kubernetes Deployment cho ML Service
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ml-prediction-service
spec:
  replicas: 3
  selector:
    matchLabels: { app: ml-service }
  template:
    metadata:
      labels: { app: ml-service }
    spec:
      containers:
        - name: ml-service
          image: registry/ml-service:v2.1.0
          ports: [{ containerPort: 8000 }]
          env:
            - name: MODEL_PATH
              value: /models/xgboost_v2.joblib
          resources:
            requests: { cpu: 500m, memory: 1Gi }
            limits: { cpu: 2000m, memory: 4Gi }
          # GPU inference (nếu cần)
          # resources:
          #   limits:
          #     nvidia.com/gpu: 1
          readinessProbe:
            httpGet: { path: /health, port: 8000 }
            initialDelaySeconds: 10
          livenessProbe:
            httpGet: { path: /health, port: 8000 }
            periodSeconds: 30
      # Anti-affinity: spread across nodes
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                topologyKey: kubernetes.io/hostname
                labelSelector:
                  matchLabels: { app: ml-service }
---
# HPA: Auto-scale based on CPU/custom metrics
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ml-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ml-prediction-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target: { type: Utilization, averageUtilization: 70 }
```

---

## 3. Model Monitoring

```python
# 3 loại drift cần monitor:

# DATA DRIFT: Input distribution thay đổi
# VD: Training trên users 20-40 tuổi, production nhận users 60+
# → Model chưa từng thấy pattern này → prediction sai

# MODEL DRIFT (Performance Drift): Accuracy giảm theo thời gian
# VD: Fraud model trained tháng 1, fraudsters thay đổi tactics tháng 6

# CONCEPT DRIFT: Relationship input→output thay đổi
# VD: COVID khiến mua hàng online tăng đột biến
# → Model cũ predict sai vì "quy luật" đã thay đổi

import numpy as np
from scipy import stats

class DriftDetector:
    """Detect data drift using statistical tests."""
    
    def __init__(self, reference_data: np.ndarray):
        self.reference = reference_data
    
    def detect_drift_ks(self, current_data: np.ndarray, 
                         threshold: float = 0.05) -> dict:
        """Kolmogorov-Smirnov test per feature."""
        results = {}
        for i in range(self.reference.shape[1]):
            stat, p_value = stats.ks_2samp(
                self.reference[:, i], current_data[:, i]
            )
            results[f"feature_{i}"] = {
                "statistic": stat,
                "p_value": p_value,
                "drift_detected": p_value < threshold,
            }
        return results
    
    def detect_drift_psi(self, current_data: np.ndarray, 
                          bins: int = 10) -> dict:
        """Population Stability Index (PSI) — industry standard."""
        results = {}
        for i in range(self.reference.shape[1]):
            # Bin both distributions
            breakpoints = np.quantile(self.reference[:, i], 
                                       np.linspace(0, 1, bins + 1))
            ref_counts = np.histogram(self.reference[:, i], breakpoints)[0]
            cur_counts = np.histogram(current_data[:, i], breakpoints)[0]
            
            # Avoid division by zero
            ref_pct = (ref_counts + 1) / (len(self.reference) + bins)
            cur_pct = (cur_counts + 1) / (len(current_data) + bins)
            
            psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct))
            # PSI < 0.1: no drift | 0.1-0.2: moderate | > 0.2: significant
            results[f"feature_{i}"] = {
                "psi": psi,
                "drift_level": "none" if psi < 0.1 else "moderate" if psi < 0.2 else "significant"
            }
        return results

# Usage in production:
detector = DriftDetector(reference_data=X_train)

# Chạy daily hoặc per batch
daily_data = get_today_predictions_input()
drift_report = detector.detect_drift_psi(daily_data)

for feature, result in drift_report.items():
    if result["drift_level"] == "significant":
        alert(f"🚨 Significant drift detected in {feature}: PSI={result['psi']:.3f}")
```

---

## 4. Production Monitoring Dashboard

```python
# Metrics to track:
from prometheus_client import Counter, Histogram, Gauge

# Operational metrics
PREDICTION_COUNT = Counter('ml_predictions_total', 'Total predictions', ['model_version'])
PREDICTION_LATENCY = Histogram('ml_prediction_seconds', 'Prediction latency', ['model_version'])
PREDICTION_ERRORS = Counter('ml_prediction_errors_total', 'Failed predictions')

# Model quality metrics
CONFIDENCE_SCORE = Histogram('ml_confidence_score', 'Prediction confidence distribution')
FEATURE_DRIFT_PSI = Gauge('ml_feature_drift_psi', 'PSI drift score', ['feature_name'])
MODEL_ACCURACY = Gauge('ml_model_accuracy', 'Rolling accuracy (when ground truth available)')

@app.post("/predict")
async def predict(request: PredictionRequest):
    PREDICTION_COUNT.labels(model_version="v2").inc()
    with PREDICTION_LATENCY.labels(model_version="v2").time():
        result = model.predict(request.features)
        CONFIDENCE_SCORE.observe(result.confidence)
    return result

# Monitoring checklist:
# ┌─────────────────────────────────────────────────────────┐
# │ OPERATIONAL (real-time)                                  │
# │ • Prediction latency (p50, p95, p99)                    │
# │ • Request throughput (predictions/sec)                   │
# │ • Error rate (timeouts, invalid input, model errors)     │
# │ • CPU/Memory/GPU utilization                             │
# │                                                          │
# │ DATA QUALITY (hourly/daily)                              │
# │ • Feature drift (PSI / KS-test per feature)             │
# │ • Missing values rate                                    │
# │ • Out-of-range values                                    │
# │ • Feature correlations change                            │
# │                                                          │
# │ MODEL QUALITY (daily/weekly, needs ground truth)         │
# │ • Accuracy, precision, recall, F1                        │
# │ • AUC-ROC trend over time                                │
# │ • Prediction distribution shift                          │
# │ • Confidence score distribution                          │
# │                                                          │
# │ BUSINESS (weekly)                                        │
# │ • Conversion rate impact                                 │
# │ • Revenue impact of predictions                          │
# │ • False positive/negative business cost                  │
# └─────────────────────────────────────────────────────────┘
```

---

## 5. A/B Testing & Canary Deployment cho Models

```python
# Model A/B Testing Architecture
import hashlib

class ModelRouter:
    """Route traffic between model versions for A/B testing."""
    
    def __init__(self):
        self.models = {
            "control": load_model("models/v2_baseline.joblib"),    # 90% traffic
            "treatment": load_model("models/v3_candidate.joblib"), # 10% traffic
        }
        self.traffic_split = {"control": 90, "treatment": 10}
    
    def get_variant(self, user_id: str) -> str:
        """Deterministic assignment — same user always gets same model."""
        hash_val = int(hashlib.sha256(user_id.encode()).hexdigest(), 16)
        if hash_val % 100 < self.traffic_split["treatment"]:
            return "treatment"
        return "control"
    
    def predict(self, user_id: str, features):
        variant = self.get_variant(user_id)
        model = self.models[variant]
        prediction = model.predict(features)
        # Log for analysis
        log_prediction(user_id=user_id, variant=variant, prediction=prediction)
        return prediction, variant

# Canary Deployment Process:
# 1. Deploy new model alongside old: 5% traffic → new model
# 2. Monitor: latency, error rate, prediction distribution
# 3. Compare metrics: new vs old (statistical significance)
# 4. If OK: gradually increase → 10% → 25% → 50% → 100%
# 5. If BAD: rollback immediately (route 100% to old model)
# 6. Full rollout: remove old model

# Shadow Mode (safe testing):
# Both models run, only old model's predictions are used
# Compare outputs offline → no user impact
```

---

## 6. CI/CD for ML (MLOps Pipeline)

```yaml
# GitHub Actions — ML CI/CD Pipeline
name: ML Pipeline
on:
  push:
    paths: ['models/**', 'src/**', 'data/**']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: pytest tests/ -v
      - run: pytest tests/model_tests/ -v  # Model-specific tests
  
  train-and-evaluate:
    needs: test
    runs-on: ubuntu-latest  # or self-hosted GPU runner
    steps:
      - uses: actions/checkout@v4
      - run: python src/train.py --config configs/prod.yaml
      - run: python src/evaluate.py --model models/latest.joblib
      # Gate: model must beat current production model
      - run: python src/compare_models.py --baseline prod --candidate latest
  
  deploy:
    needs: train-and-evaluate
    if: github.ref == 'refs/heads/main'
    steps:
      - run: docker build -t ml-service:${{ github.sha }} .
      - run: docker push registry/ml-service:${{ github.sha }}
      # Canary deploy: 5% traffic to new model
      - run: kubectl set image deployment/ml-service-canary ml-service=registry/ml-service:${{ github.sha }}

# Model-specific tests:
# ✅ Prediction shape/type correct
# ✅ Latency < 100ms per prediction
# ✅ No NaN/Inf in outputs
# ✅ Known test cases produce expected output range
# ✅ Model size < threshold (can load in production memory)
# ✅ Accuracy on validation set > minimum threshold
```

```
Continuous Training (CT) Triggers:
1. SCHEDULED: Retrain weekly/monthly on latest data
2. DATA DRIFT: PSI > 0.2 → trigger retrain pipeline
3. PERFORMANCE: Accuracy drops below threshold → alert + retrain
4. NEW DATA: Significant new labeled data available

Full MLOps Maturity:
Level 0: Manual → notebook training, manual deploy
Level 1: ML Pipeline → automated training, manual deploy
Level 2: CI/CD for ML → automated training + deploy
Level 3: CT → auto-retrain on drift, auto-deploy if passes gates
```

---

## 📝 Bài tập

1. Deploy model bằng FastAPI + Docker, load test với 1000 concurrent requests
2. Implement PSI drift detection, chạy trên simulated drift data
3. Build A/B test framework: route traffic, log predictions, analyze results
4. Setup full ML CI/CD pipeline: test → train → evaluate → deploy → monitor
5. Implement shadow mode: run 2 models, compare outputs without affecting users

---

## 📚 Tài liệu
- *Designing Machine Learning Systems* — Chip Huyen
- *Reliable Machine Learning* — Cathy Chen et al.
- [MLOps Principles](https://ml-ops.org/)
- [Evidently AI — ML Monitoring](https://www.evidentlyai.com/)
- [Google MLOps Whitepaper](https://cloud.google.com/resources/mlops-whitepaper)

## 🔗 Liên kết chéo
- → **Bài 28: ML Pipeline** (cùng track) — pipeline training trước deployment
- → **Bài 30: AI Ethics** (cùng track) — monitoring bias trong production
- → **SE Bài 08: CI/CD Pipeline** — CI/CD cho model deployment
- → **SE Bài 09: Observability** — Prometheus/Grafana monitoring
- → **Security Bài 02: Authentication** — bảo vệ model serving endpoints
