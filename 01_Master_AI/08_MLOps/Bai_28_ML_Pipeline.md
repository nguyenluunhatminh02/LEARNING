# Bài 28: ML Pipeline & Experiment Tracking

## 🎯 Mục tiêu
- MLflow, Weights & Biases cho experiment tracking
- DVC cho data versioning
- Feature Store concepts
- Pipeline orchestration (Airflow, Prefect)
- End-to-end ML pipeline

> **Tiếp theo**: Bài 29 — Model Deployment & Monitoring (production serving, drift detection)

---

## 1. Experiment Tracking với MLflow

```python
import mlflow
import mlflow.sklearn
from sklearn.model_selection import cross_val_score
import numpy as np

mlflow.set_experiment("house-price-prediction")

with mlflow.start_run(run_name="xgboost-v1"):
    # Log params
    params = {"n_estimators": 200, "max_depth": 6, "learning_rate": 0.1}
    mlflow.log_params(params)
    
    # Train
    model = XGBRegressor(**params)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="r2")
    
    # Log metrics
    mlflow.log_metrics({
        "rmse": rmse,
        "r2": r2,
        "cv_mean_r2": cv_scores.mean(),
        "cv_std_r2": cv_scores.std(),
    })
    
    # Log model (with signature for validation)
    from mlflow.models import infer_signature
    signature = infer_signature(X_test, y_pred)
    mlflow.sklearn.log_model(model, "model", signature=signature)
    
    # Log artifacts
    mlflow.log_artifact("feature_importance.png")
    
    # Tag for organization
    mlflow.set_tags({"team": "data-science", "stage": "experiment"})

# UI: mlflow ui → http://localhost:5000

# Model Registry — quản lý model versions
from mlflow import MlflowClient
client = MlflowClient()
# Register best model
result = mlflow.register_model("runs:/run_id/model", "house-price-model")
# Transition to production
client.transition_model_version_stage("house-price-model", version=1, stage="Production")
# Load production model anywhere:
model = mlflow.pyfunc.load_model("models:/house-price-model/Production")
```

---

## 2. Weights & Biases (wandb)

```python
import wandb

wandb.init(project="my-ml-project", name="experiment-1",
           config={"lr": 0.001, "epochs": 100, "batch_size": 32, "model": "resnet50"})

# Training loop with rich logging
for epoch in range(wandb.config.epochs):
    train_loss, val_loss = train_one_epoch(model)
    
    wandb.log({
        "train_loss": train_loss,
        "val_loss": val_loss,
        "epoch": epoch,
        "learning_rate": scheduler.get_last_lr()[0],
    })
    
    # Log predictions visualization
    if epoch % 10 == 0:
        wandb.log({"predictions": wandb.Table(
            data=[[y_true, y_pred] for y_true, y_pred in zip(y_val[:20], preds[:20])],
            columns=["actual", "predicted"]
        )})

# Hyperparameter sweep
sweep_config = {
    "method": "bayes",   # bayesian optimization
    "metric": {"name": "val_loss", "goal": "minimize"},
    "parameters": {
        "lr": {"min": 1e-5, "max": 1e-2},
        "batch_size": {"values": [16, 32, 64]},
        "dropout": {"min": 0.1, "max": 0.5},
    }
}
sweep_id = wandb.sweep(sweep_config, project="my-ml-project")
wandb.agent(sweep_id, function=train_function, count=20)  # Run 20 trials

wandb.finish()
```

---

## 3. Data Versioning với DVC

```bash
# DVC = "Git for data" — track large files without storing in Git
pip install dvc dvc-s3  # or dvc-gcs, dvc-azure

# Initialize
dvc init
dvc remote add -d storage s3://my-bucket/dvc-store

# Track data files
dvc add data/train.csv     # Creates data/train.csv.dvc (metadata)
git add data/train.csv.dvc  # Commit metadata to git
git commit -m "Add training data v1"
dvc push                    # Upload actual data to S3

# When data changes
dvc add data/train.csv      # Update tracking
git add data/train.csv.dvc
git commit -m "Update training data v2"
dvc push

# Reproduce ANY version
git checkout v1.0           # Checkout code version
dvc checkout               # Download matching data version
# → Code + data are always in sync!
```

```yaml
# DVC Pipeline (dvc.yaml) — reproducible ML pipeline
stages:
  prepare:
    cmd: python src/prepare_data.py
    deps: [data/raw/]
    outs: [data/processed/]
  
  featurize:
    cmd: python src/featurize.py
    deps: [src/featurize.py, data/processed/]
    outs: [data/features/]
  
  train:
    cmd: python src/train.py
    deps: [src/train.py, data/features/]
    outs: [models/model.joblib]
    metrics: [metrics/scores.json]
    plots: [metrics/confusion_matrix.csv]
  
  evaluate:
    cmd: python src/evaluate.py
    deps: [src/evaluate.py, models/model.joblib, data/features/]
    metrics: [metrics/eval_scores.json]

# Run pipeline: dvc repro
# Only re-runs stages where dependencies changed
# Compare experiments: dvc metrics diff
```

---

## 4. Feature Store

```python
# Feature Store = centralized repository for ML features
# Giải quyết: feature inconsistency giữa training & serving

# Feast — open-source feature store
from feast import FeatureStore, Entity, FeatureView, Field
from feast.types import Float32, Int64

# Define entity
customer = Entity(name="customer", join_keys=["customer_id"])

# Define feature view (linked to data source)
customer_features = FeatureView(
    name="customer_features",
    entities=[customer],
    schema=[
        Field(name="total_orders", dtype=Int64),
        Field(name="avg_order_value", dtype=Float32),
        Field(name="days_since_last_order", dtype=Int64),
    ],
    source=BigQuerySource(table="project.dataset.customer_features"),
    ttl=timedelta(days=1),  # Feature freshness
)

# In training (batch):
store = FeatureStore(repo_path="feature_repo/")
training_data = store.get_historical_features(
    entity_df=entity_df,  # customer_ids + timestamps
    features=["customer_features:total_orders",
              "customer_features:avg_order_value"],
).to_df()

# In serving (online — low latency):
features = store.get_online_features(
    features=["customer_features:total_orders",
              "customer_features:avg_order_value"],
    entity_rows=[{"customer_id": "C123"}],
).to_dict()

# Benefits:
# ✅ Same features in training & serving (no training-serving skew)
# ✅ Feature reuse across teams/models
# ✅ Point-in-time correctness (prevent data leakage)
# ✅ Feature documentation & discovery
```

---

## 5. Pipeline Orchestration

```python
# Prefect — modern workflow orchestration
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta

@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def load_data(path: str):
    return pd.read_parquet(path)

@task
def preprocess(df):
    return feature_pipeline.transform(df)

@task
def train_model(X, y, params):
    model = XGBRegressor(**params)
    model.fit(X, y)
    return model

@task
def evaluate(model, X_test, y_test):
    y_pred = model.predict(X_test)
    metrics = {"rmse": rmse(y_test, y_pred), "r2": r2_score(y_test, y_pred)}
    return metrics

@task
def register_model(model, metrics, threshold=0.8):
    if metrics["r2"] > threshold:
        mlflow.sklearn.log_model(model, "production-model")
        return True
    return False

@flow(name="ml-training-pipeline")
def training_pipeline(data_path: str, params: dict):
    df = load_data(data_path)
    X, y = preprocess(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    model = train_model(X_train, y_train, params)
    metrics = evaluate(model, X_test, y_test)
    registered = register_model(model, metrics)
    return {"metrics": metrics, "registered": registered}

# Schedule: run daily at 2am
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

deployment = Deployment.build_from_flow(
    flow=training_pipeline,
    name="daily-retrain",
    schedule=CronSchedule(cron="0 2 * * *"),
    parameters={"data_path": "s3://bucket/data/latest.parquet",
                "params": {"n_estimators": 200, "max_depth": 6}},
)
```

---

## 6. MLOps Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    MLOps Architecture                            │
│                                                                  │
│  DATA LAYER          TRAINING LAYER       SERVING LAYER          │
│  ┌──────────┐       ┌──────────────┐     ┌──────────────┐      │
│  │ Data Lake │──────→│ Feature Store │────→│ Model Server │      │
│  │ (S3/GCS) │       │ (Feast)      │     │ (FastAPI)    │      │
│  └──────────┘       └──────────────┘     └──────────────┘      │
│       │                    │                     │               │
│  ┌──────────┐       ┌──────────────┐     ┌──────────────┐      │
│  │ DVC      │       │ MLflow       │     │ Monitoring   │      │
│  │ (version)│       │ (tracking)   │     │ (Evidently)  │      │
│  └──────────┘       └──────────────┘     └──────────────┘      │
│                           │                     │               │
│                    ┌──────────────┐              │               │
│                    │ Prefect      │──────────────┘               │
│                    │ (orchestrate)│ retrain trigger               │
│                    └──────────────┘                               │
│                                                                  │
│  CI/CD: GitHub Actions → test → train → evaluate → deploy       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📝 Bài tập

1. Setup MLflow: track 5 experiments, use Model Registry to promote best model
2. Setup DVC: version 3 iterations of a dataset, reproduce pipeline
3. Build end-to-end pipeline với Prefect: load → preprocess → train → evaluate → register
4. Implement hyperparameter sweep với W&B Sweeps (20+ trials, bayesian)
5. Compare MLflow vs W&B: which fits your workflow better?

---

## 📚 Tài liệu
- *Designing Machine Learning Systems* — Chip Huyen
- *Reliable Machine Learning* — Cathy Chen et al.
- [MLflow Documentation](https://mlflow.org/)
- [Weights & Biases Docs](https://docs.wandb.ai/)
- [DVC Documentation](https://dvc.org/doc)
- [Feast Feature Store](https://feast.dev/)
- *Made With ML — MLOps Course* (miễn phí)

## 🔗 Liên kết chéo
- → **Bài 29: Model Deployment** (cùng track) — triển khai model sau khi pipeline hoàn chỉnh
- → **Bài 30: AI Ethics** (cùng track) — fairness testing trong pipeline
- → **SE Bài 08: CI/CD Pipeline** — áp dụng CI/CD principles cho ML
- → **SE Bài 09: Observability** — monitoring infrastructure cho ML systems
- → **System Design Bài 08: Database Scaling** — data storage cho feature store & model artifacts
