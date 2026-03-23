# Bài 30: AI Ethics & Responsible AI

## 🎯 Mục tiêu
- Hiểu các vấn đề đạo đức trong AI: bias, fairness, transparency
- Nắm vững Explainable AI (XAI) với SHAP và LIME
- Hiểu EU AI Act và các framework quản lý AI
- Xây dựng quy trình Responsible AI trong tổ chức

## 📖 Câu chuyện đời thường
> Một ngân hàng dùng AI để duyệt hồ sơ vay. Bất ngờ, hệ thống từ chối gần hết hồ sơ từ một khu vực nhất định — không phải vì họ không đủ điều kiện, mà vì data huấn luyện có **bias** từ lịch sử. Đó là vấn đề **fairness**. **Explainable AI** giống như bạn yêu cầu ngân hàng giải thích: "Tại sao từ chối tôi?" — thay vì chỉ nói "AI quyết định", họ phải chỉ ra lý do cụ thể (SHAP: thu nhập thấp chiếm 40%, tuổi chiếm 20%...). **EU AI Act** giống như luật an toàn thực phẩm với AI — bắt buộc "ghi rõ thành phần" và đảm bảo không gây hại.

---

## 1. Bias trong AI

### 1.1 Các loại Bias

```
Data Bias:
├── Selection Bias      → Dữ liệu không đại diện cho toàn bộ population
├── Historical Bias     → Dữ liệu phản ánh bất công xã hội quá khứ
├── Measurement Bias    → Cách thu thập dữ liệu không chính xác
├── Label Bias          → Annotator có sai lệch chủ quan
└── Survivor Bias       → Chỉ có data từ nhóm "sống sót"

Algorithmic Bias:
├── Representation Bias → Model thiếu features quan trọng
├── Aggregation Bias    → 1 model cho nhiều nhóm khác nhau
└── Evaluation Bias     → Benchmark không reflect real-world
```

### 1.2 Case Studies nổi tiếng

| Case | Vấn đề | Root Cause |
|------|--------|------------|
| COMPAS (recidivism) | Bias chủng tộc trong dự đoán tái phạm | Historical bias trong criminal justice data |
| Amazon Hiring AI | Phân biệt giới tính | Training data 10 năm, chủ yếu nam |
| Google Photos | Gán nhãn sai cho người da màu | Thiếu diversity trong training data |
| Healthcare Algorithm | Ưu tiên bệnh nhân da trắng | Dùng chi phí y tế làm proxy cho mức độ bệnh |

### 1.3 Phát hiện và giảm Bias

```python
# === Fairness Metrics ===
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.algorithms.preprocessing import Reweighing

# Demographic Parity: P(Ŷ=1|A=0) = P(Ŷ=1|A=1)
# Equal Opportunity: P(Ŷ=1|Y=1,A=0) = P(Ŷ=1|Y=1,A=1)
# Equalized Odds: cả TP rate và FP rate bằng nhau giữa groups

# Đo Disparate Impact
def disparate_impact(y_pred, sensitive_attr):
    """DI = P(Ŷ=1|unprivileged) / P(Ŷ=1|privileged)
    Hợp lệ nếu 0.8 ≤ DI ≤ 1.25 (80% rule)"""
    priv_mask = sensitive_attr == 1
    unpriv_mask = sensitive_attr == 0
    
    p_priv = y_pred[priv_mask].mean()
    p_unpriv = y_pred[unpriv_mask].mean()
    
    return p_unpriv / p_priv if p_priv > 0 else 0

# Pre-processing: Reweighing
reweigher = Reweighing(
    unprivileged_groups=[{'race': 0}],
    privileged_groups=[{'race': 1}]
)
dataset_reweighed = reweigher.fit_transform(dataset)

# Post-processing: Equalized Odds
from aif360.algorithms.postprocessing import EqOddsPostprocessing
eqodds = EqOddsPostprocessing(
    unprivileged_groups=[{'race': 0}],
    privileged_groups=[{'race': 1}]
)
dataset_debiased = eqodds.fit_predict(dataset_true, dataset_pred)
```

**3 giai đoạn giảm bias:**
| Giai đoạn | Kỹ thuật | Ví dụ |
|-----------|----------|-------|
| Pre-processing | Reweighing, Disparate Impact Remover | Cân bằng trọng số samples |
| In-processing | Adversarial Debiasing, Fairness Constraints | Thêm fairness term vào loss function |
| Post-processing | Equalized Odds, Calibrated EqOdds | Điều chỉnh threshold per group |

---

## 2. Explainable AI (XAI)

### 2.1 Tại sao cần XAI?

```
Stakeholders cần giải thích:
├── End Users       → "Tại sao tôi bị từ chối vay?"
├── Regulators      → "Model có phân biệt đối xử không?"
├── Data Scientists → "Model đang học gì? Có đúng pattern không?"
├── Business        → "Insight nào từ model giúp ra quyết định?"
└── Legal           → "Có thể chứng minh quyết định hợp lý không?"
```

### 2.2 SHAP (SHapley Additive exPlanations)

Dựa trên Shapley values từ game theory — phân bổ "đóng góp" của mỗi feature.

```python
import shap

# === Global Explanation ===
model = xgboost.XGBClassifier().fit(X_train, y_train)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot: feature importance trung bình
shap.summary_plot(shap_values, X_test)

# Dependence plot: relationship giữa 1 feature và SHAP value
shap.dependence_plot("age", shap_values, X_test)

# === Local Explanation (1 prediction) ===
# Giải thích tại sao sample[0] được predict positive
shap.force_plot(
    explainer.expected_value, 
    shap_values[0], 
    X_test.iloc[0]
)

# Waterfall cho 1 prediction
shap.waterfall_plot(
    shap.Explanation(
        values=shap_values[0],
        base_values=explainer.expected_value,
        data=X_test.iloc[0]
    )
)
```

### 2.3 LIME (Local Interpretable Model-agnostic Explanations)

Giải thích từng prediction bằng cách tạo linear model cục bộ.

```python
from lime.lime_tabular import LimeTabularExplainer

explainer = LimeTabularExplainer(
    X_train.values,
    feature_names=X_train.columns,
    class_names=['rejected', 'approved'],
    mode='classification'
)

# Giải thích 1 prediction
explanation = explainer.explain_instance(
    X_test.iloc[0].values,
    model.predict_proba,
    num_features=10
)
explanation.show_in_notebook()

# Output dạng:
# income > 50000        → +0.35 (approved)
# debt_ratio > 0.4      → -0.22 (rejected)
# employment_years > 5   → +0.18 (approved)
```

### 2.4 So sánh SHAP vs LIME

| Tiêu chí | SHAP | LIME |
|-----------|------|------|
| Lý thuyết | Shapley values (game theory) | Local linear approximation |
| Scope | Global + Local | Local only |
| Consistency | Đảm bảo mathematical consistency | Không guarantee |
| Tốc độ | Chậm hơn (exponential features) | Nhanh hơn |
| Model-agnostic | Có (KernelSHAP) | Có |
| Ưu điểm | Chính xác, có theoretical guarantee | Nhanh, dễ hiểu |

---

## 3. EU AI Act & Quy định AI

### 3.1 EU AI Act — Risk-Based Framework

```
╔══════════════════════════════════════════════╗
║           EU AI Act Risk Levels              ║
╠══════════════════════════════════════════════╣
║                                              ║
║  🔴 UNACCEPTABLE RISK → BẤM CẤM             ║
║     - Social scoring bởi chính phủ           ║
║     - Real-time biometric surveillance       ║
║     - Manipulative AI (exploit vulnerable)   ║
║                                              ║
║  🟠 HIGH RISK → QUY ĐỊNH NGHIÊM NGẶT        ║
║     - Healthcare diagnosis                   ║
║     - Credit scoring                         ║
║     - Recruitment/HR AI                      ║
║     - Law enforcement                        ║
║     - Yêu cầu: conformity assessment,        ║
║       risk management, logging, transparency ║
║                                              ║
║  🟡 LIMITED RISK → MINH BẠCH                 ║
║     - Chatbots → phải thông báo là AI        ║
║     - Deepfakes → phải gắn label             ║
║     - Emotion recognition → thông báo user   ║
║                                              ║
║  🟢 MINIMAL RISK → TỰ DO                     ║
║     - Spam filters                           ║
║     - Game AI                                ║
║     - Recommendation systems (cơ bản)        ║
╚══════════════════════════════════════════════╝
```

### 3.2 Yêu cầu cho High-Risk AI

```
Checklist cho High-Risk AI System:
□ Risk Management System → đánh giá rủi ro liên tục
□ Data Governance → data quality, bias testing
□ Technical Documentation → mô tả chi tiết system
□ Record Keeping → logging predictions + inputs
□ Transparency → user biết đang interact với AI
□ Human Oversight → human-in-the-loop mechanism
□ Accuracy & Robustness → testing standards
□ Cybersecurity → bảo vệ khỏi adversarial attacks
```

### 3.3 Các framework khác

| Framework | Tổ chức | Focus |
|-----------|---------|-------|
| EU AI Act | European Union | Legal compliance, risk-based |
| NIST AI RMF | US NIST | Risk management, voluntary |
| IEEE 7000 | IEEE | Ethical design process |
| Singapore FEAT | MAS | Fairness, Ethics, Accountability, Transparency |
| China AI Regulations | CAC | Content generation, deepfakes, recommendation |

---

## 4. Responsible AI Framework

### 4.1 Principles

```
Microsoft Responsible AI:
├── Fairness        → Treat all people fairly
├── Reliability     → Operate reliably and safely
├── Privacy         → Respect privacy
├── Inclusiveness   → Empower everyone
├── Transparency    → Be understandable
└── Accountability  → People accountable for AI systems

Google AI Principles:
├── Be socially beneficial
├── Avoid creating or reinforcing unfair bias
├── Be built and tested for safety
├── Be accountable to people
├── Incorporate privacy design principles
├── Uphold high standards of scientific excellence
└── Be made available for uses accord with these principles
```

### 4.2 Responsible AI Workflow

```python
# === Model Card Template ===
"""
MODEL CARD: Credit Scoring Model v2.1
=====================================
1. Model Details
   - Type: XGBoost classifier
   - Version: 2.1 (2024-01)
   - Owner: ML Team, Credit Department
   
2. Intended Use
   - Primary: Assist credit officers in loan decisions
   - Out-of-scope: Automated decisions without human review
   
3. Training Data
   - Source: Internal loan applications (2019-2023)
   - Size: 500K samples
   - Demographics: Age 18-75, all races, both genders
   
4. Evaluation Metrics
   - AUC: 0.87, F1: 0.82
   - Disparate Impact (race): 0.91 ✅ (>0.8)
   - Disparate Impact (gender): 0.88 ✅ (>0.8)
   - Equal Opportunity gap: 0.03 ✅ (<0.05)
   
5. Limitations
   - May underperform for applicants < 21 (small sample)
   - Not validated for commercial loans
   
6. Ethical Considerations
   - Race/gender NOT used as features
   - Proxy features (zip code) monitored for indirect bias
   - Quarterly fairness audit scheduled
"""
```

### 4.3 AI Governance trong tổ chức

```
AI Governance Structure:
├── AI Ethics Board (cross-functional)
│   ├── Review high-risk use cases
│   ├── Set policies & guidelines
│   └── Audit compliance
├── ML Engineering Standards
│   ├── Model Card required for production models
│   ├── Fairness testing in CI/CD pipeline
│   ├── Explainability report for each model
│   └── Data lineage tracking
├── Monitoring & Audit
│   ├── Quarterly bias audit
│   ├── Drift detection (data + concept)
│   ├── Performance by demographic group
│   └── Incident response plan
└── Training & Culture
    ├── Ethics training cho tất cả ML engineers
    ├── Bias awareness workshops
    └── Ethical review checklist trước deploy
```

---

## 5. AI Safety & Adversarial Robustness

### 5.1 Adversarial Attacks

```python
# === FGSM Attack (Fast Gradient Sign Method) ===
import torch

def fgsm_attack(model, image, label, epsilon=0.03):
    """Tạo adversarial example bằng cách thêm noise nhỏ"""
    image.requires_grad = True
    output = model(image)
    loss = torch.nn.functional.cross_entropy(output, label)
    model.zero_grad()
    loss.backward()
    
    # Tạo perturbation
    perturbation = epsilon * image.grad.sign()
    adversarial_image = image + perturbation
    adversarial_image = torch.clamp(adversarial_image, 0, 1)
    
    return adversarial_image

# === Defense: Adversarial Training ===
def adversarial_training(model, dataloader, epsilon=0.03):
    for images, labels in dataloader:
        # Train trên cả clean và adversarial examples
        adv_images = fgsm_attack(model, images, labels, epsilon)
        
        # Loss = clean_loss + adversarial_loss
        clean_output = model(images)
        adv_output = model(adv_images)
        loss = (
            F.cross_entropy(clean_output, labels) + 
            F.cross_entropy(adv_output, labels)
        ) / 2
        loss.backward()
        optimizer.step()
```

### 5.2 LLM Safety

```
LLM Risks:
├── Hallucination     → Generate thông tin sai nhưng tự tin
├── Prompt Injection  → User manipulate behavior qua input
├── Data Leakage      → Model tiết lộ training data
├── Toxic Output      → Hate speech, harmful content
└── Misuse            → Phishing, malware generation, fraud

Mitigations:
├── RLHF (Reinforcement Learning from Human Feedback)
├── Constitutional AI → self-critique framework
├── Guardrails       → input/output filtering
├── Red Teaming      → systematic adversarial testing
└── RAG              → ground responses in factual data
```

---

## 6. Privacy-Preserving AI

### 6.1 Các kỹ thuật

| Kỹ thuật | Mô tả | Use Case |
|----------|--------|----------|
| Differential Privacy | Thêm noise vào data/model để protect individuals | Census data, analytics |
| Federated Learning | Train model trên device, không gửi raw data | Mobile keyboards, healthcare |
| Homomorphic Encryption | Compute trên encrypted data | Financial AI, cloud ML |
| Secure Multi-Party Computation | Nhiều bên tính toán chung mà không reveal data | Cross-org ML |

```python
# === Differential Privacy với PyTorch (Opacus) ===
from opacus import PrivacyEngine

model = Net()
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

privacy_engine = PrivacyEngine()
model, optimizer, dataloader = privacy_engine.make_private(
    module=model,
    optimizer=optimizer,
    data_loader=dataloader,
    noise_multiplier=1.1,    # Noise level
    max_grad_norm=1.0,       # Gradient clipping
)

# Training như bình thường
for batch in dataloader:
    loss = train_step(model, batch)
    loss.backward()
    optimizer.step()

# Kiểm tra privacy budget
epsilon = privacy_engine.get_epsilon(delta=1e-5)
print(f"ε = {epsilon:.2f}")  # Thấp hơn = private hơn
```

---

## 📝 Bài tập

1. **Bias Analysis**: Lấy dataset Adult Income (UCI), train model, đo Disparate Impact theo race và gender. Áp dụng Reweighing và so sánh kết quả.
2. **XAI Report**: Train model bất kỳ, tạo SHAP summary plot + waterfall plot cho 3 predictions. Viết giải thích bằng ngôn ngữ phi kỹ thuật.
3. **Model Card**: Viết Model Card đầy đủ cho 1 model đã train từ các bài trước.
4. **EU AI Act Classification**: Liệt kê 10 AI applications trong cuộc sống, phân loại theo risk level của EU AI Act.
5. **Adversarial Testing**: Implement FGSM attack trên model image classification, measure accuracy drop. Thử adversarial training để defend.

---

## 📚 Tài liệu

- [Fairness and Machine Learning](https://fairmlbook.org/) — Barocas, Hardt, Narayanan (free textbook)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [EU AI Act Full Text](https://artificialintelligenceact.eu/)
- [Google Model Cards](https://modelcards.withgoogle.com/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [Responsible AI Practices — Google](https://ai.google/responsibility/responsible-ai-practices/)
- *Weapons of Math Destruction* — Cathy O'Neil
- *Atlas of AI* — Kate Crawford
