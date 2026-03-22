# 🎓 GIÁO TRÌNH MASTER AI — TỪ CƠ BẢN ĐẾN NÂNG CAO

> Lộ trình toàn diện để trở thành AI Engineer / ML Engineer / AI Researcher
> Thời lượng ước tính: 12–18 tháng (tự học toàn thời gian)

---

## 📋 MỤC LỤC

- [Phase 0: Nền tảng Toán học & Lập trình](#phase-0-nền-tảng-toán-học--lập-trình)
- [Phase 1: Machine Learning cơ bản](#phase-1-machine-learning-cơ-bản)
- [Phase 2: Deep Learning](#phase-2-deep-learning)
- [Phase 3: Computer Vision](#phase-3-computer-vision)
- [Phase 4: Natural Language Processing](#phase-4-natural-language-processing)
- [Phase 5: Reinforcement Learning](#phase-5-reinforcement-learning)
- [Phase 6: Generative AI & Large Language Models](#phase-6-generative-ai--large-language-models)
- [Phase 7: MLOps & Production AI](#phase-7-mlops--production-ai)
- [Phase 8: Chuyên sâu & Nghiên cứu](#phase-8-chuyên-sâu--nghiên-cứu)

---

## Phase 0: Nền tảng Toán học & Lập trình
**Thời lượng: 4–6 tuần**

### 0.1 Python cho AI
- **Cơ bản Python**: biến, kiểu dữ liệu, vòng lặp, hàm, class, module
- **Python nâng cao**: decorator, generator, context manager, comprehension
- **Thư viện quan trọng**:
  - `NumPy` — tính toán ma trận, mảng đa chiều
  - `Pandas` — xử lý dữ liệu dạng bảng
  - `Matplotlib` / `Seaborn` — trực quan hóa dữ liệu
  - `Scikit-learn` — thư viện ML cơ bản
- **Bài tập**: phân tích bộ dữ liệu Titanic, trực quan hóa dữ liệu COVID-19

### 0.2 Đại số tuyến tính (Linear Algebra)
- Vector, ma trận, phép nhân ma trận
- Không gian vector, cơ sở, hạng ma trận
- Trị riêng (eigenvalue) và vector riêng (eigenvector)
- Phân rã ma trận: SVD, PCA
- **Ứng dụng**: nén ảnh bằng SVD, giảm chiều dữ liệu bằng PCA

### 0.3 Giải tích (Calculus)
- Đạo hàm, đạo hàm riêng (partial derivative)
- Gradient, Jacobian, Hessian
- Quy tắc chuỗi (Chain Rule) — nền tảng của backpropagation
- Tối ưu hóa: cực trị, điểm yên ngựa (saddle point)
- **Ứng dụng**: hiểu gradient descent từ góc nhìn toán học

### 0.4 Xác suất & Thống kê (Probability & Statistics)
- Biến ngẫu nhiên, phân phối xác suất (Bernoulli, Gaussian, Poisson...)
- Kỳ vọng, phương sai, hiệp phương sai
- Định lý Bayes — nền tảng của nhiều thuật toán ML
- Kiểm định giả thuyết (hypothesis testing)
- MLE (Maximum Likelihood Estimation) và MAP
- **Ứng dụng**: Naive Bayes spam filter

### 0.5 Tối ưu hóa (Optimization)
- Gradient Descent, Stochastic Gradient Descent (SGD)
- Momentum, Adam, RMSProp
- Convex vs Non-convex optimization
- Learning rate scheduling
- **Bài tập**: implement gradient descent từ đầu bằng NumPy

### 📚 Tài liệu tham khảo Phase 0
| Tài liệu | Loại |
|-----------|------|
| *Mathematics for Machine Learning* — Deisenroth et al. | Sách (miễn phí) |
| *3Blue1Brown — Essence of Linear Algebra* | Video |
| *Khan Academy — Statistics & Probability* | Khóa học |
| *Python for Data Analysis* — Wes McKinney | Sách |

---

## Phase 1: Machine Learning cơ bản
**Thời lượng: 6–8 tuần**

### 1.1 Tổng quan về Machine Learning
- Định nghĩa ML: học từ dữ liệu
- 3 loại học: Supervised, Unsupervised, Reinforcement Learning
- Quy trình ML pipeline: thu thập dữ liệu → tiền xử lý → huấn luyện → đánh giá → triển khai
- Bias-Variance tradeoff
- Overfitting vs Underfitting

### 1.2 Supervised Learning — Hồi quy (Regression)
- **Linear Regression**: mô hình, hàm mất mát MSE, Normal Equation, Gradient Descent
- **Polynomial Regression**: mở rộng đặc trưng
- **Ridge Regression (L2)** và **Lasso Regression (L1)**: regularization
- **Elastic Net**: kết hợp L1 và L2
- **Đánh giá**: MSE, RMSE, MAE, R²
- **Bài tập**: dự đoán giá nhà (Boston Housing / California Housing)

### 1.3 Supervised Learning — Phân loại (Classification)
- **Logistic Regression**: sigmoid, cross-entropy loss
- **K-Nearest Neighbors (KNN)**
- **Decision Tree**: entropy, information gain, Gini impurity
- **Random Forest**: bagging, feature importance
- **Support Vector Machine (SVM)**: margin, kernel trick
- **Gradient Boosting**: XGBoost, LightGBM, CatBoost
- **Đánh giá**: accuracy, precision, recall, F1-score, ROC-AUC, confusion matrix
- **Bài tập**: phân loại email spam, phát hiện bệnh tiểu đường

### 1.4 Unsupervised Learning
- **K-Means Clustering**: thuật toán, elbow method
- **Hierarchical Clustering**: agglomerative, dendrogram
- **DBSCAN**: density-based clustering
- **PCA (Principal Component Analysis)**: giảm chiều dữ liệu
- **t-SNE** và **UMAP**: trực quan hóa dữ liệu nhiều chiều
- **Bài tập**: phân nhóm khách hàng (customer segmentation)

### 1.5 Feature Engineering
- Xử lý missing data (imputation)
- Encoding biến phân loại: one-hot, label, target encoding
- Scaling: StandardScaler, MinMaxScaler, RobustScaler
- Feature selection: correlation, mutual information, recursive feature elimination
- Feature creation: domain-specific features
- **Bài tập**: Kaggle competition — Tabular Playground Series

### 1.6 Model Selection & Evaluation
- Train / Validation / Test split
- K-Fold Cross Validation, Stratified K-Fold
- Hyperparameter tuning: Grid Search, Random Search, Bayesian Optimization
- Learning curves
- Ensemble methods: Voting, Stacking, Blending

### 📚 Tài liệu Phase 1
| Tài liệu | Loại |
|-----------|------|
| *Hands-On Machine Learning* — Aurélien Géron | Sách |
| *Andrew Ng — Machine Learning Specialization (Coursera)* | Khóa học |
| *Scikit-learn Documentation* | Tài liệu |
| *Kaggle Learn — Intro to ML* | Khóa học |

---

## Phase 2: Deep Learning
**Thời lượng: 6–8 tuần**

### 2.1 Neural Network cơ bản
- Perceptron, Multi-Layer Perceptron (MLP)
- Activation functions: Sigmoid, Tanh, ReLU, Leaky ReLU, GELU, Swish
- Forward propagation và Backpropagation
- Hàm mất mát: MSE, Cross-Entropy, Binary Cross-Entropy
- **Bài tập**: code neural network từ đầu bằng NumPy

### 2.2 Framework Deep Learning
- **PyTorch**: tensor, autograd, nn.Module, DataLoader
- **TensorFlow / Keras**: Sequential API, Functional API
- So sánh PyTorch vs TensorFlow
- GPU computing: CUDA basics
- **Bài tập**: phân loại MNIST bằng cả PyTorch và TensorFlow

### 2.3 Kỹ thuật huấn luyện
- **Optimizer**: SGD, Adam, AdamW, LAMB
- **Learning Rate**: warmup, cosine annealing, OneCycleLR
- **Regularization**: Dropout, Batch Normalization, Layer Normalization, Weight Decay
- **Data Augmentation**: random crop, flip, color jitter, mixup, cutout
- Gradient clipping, gradient accumulation
- Mixed precision training (FP16/BF16)

### 2.4 Kiến trúc mạng nổi bật
- **Fully Connected Network**
- **AutoEncoder**: encoding, bottleneck, decoding
- **Variational AutoEncoder (VAE)**: latent space, reparameterization trick
- Residual connections (skip connections)
- Attention mechanism (overview trước khi đi sâu ở phase sau)

### 2.5 Practical Deep Learning
- Debugging neural networks: loss không giảm, gradient vanishing/exploding
- Hyperparameter tuning cho DL: Weights & Biases (wandb)
- Transfer learning: pretrained models, fine-tuning
- Model interpretability: Grad-CAM, SHAP, LIME
- **Project**: phân loại ảnh thực phẩm Việt Nam

### 📚 Tài liệu Phase 2
| Tài liệu | Loại |
|-----------|------|
| *Deep Learning* — Goodfellow, Bengio, Courville | Sách (miễn phí) |
| *fast.ai — Practical Deep Learning* | Khóa học |
| *PyTorch Official Tutorials* | Tài liệu |
| *CS231n — Stanford (YouTube)* | Bài giảng |

---

## Phase 3: Computer Vision
**Thời lượng: 4–6 tuần**

### 3.1 Convolutional Neural Networks (CNN)
- Convolution layer, pooling layer, stride, padding
- Kiến trúc kinh điển: LeNet → AlexNet → VGGNet → GoogLeNet → ResNet → DenseNet
- Depthwise separable convolution (MobileNet)
- EfficientNet: compound scaling
- **Bài tập**: implement ResNet từ đầu

### 3.2 Object Detection
- Two-stage detectors: R-CNN → Fast R-CNN → Faster R-CNN
- One-stage detectors: YOLO (v1→v8+), SSD, RetinaNet
- Anchor-free detectors: CenterNet, FCOS
- Loss functions: IoU, GIoU, DIoU, CIoU
- Non-Maximum Suppression (NMS)
- Đánh giá: mAP, AP@50, AP@75
- **Project**: xây dựng hệ thống phát hiện biển báo giao thông

### 3.3 Image Segmentation
- **Semantic Segmentation**: FCN, U-Net, DeepLab v3+
- **Instance Segmentation**: Mask R-CNN
- **Panoptic Segmentation**
- **Bài tập**: segment ảnh y khoa (Medical Image Segmentation)

### 3.4 Vision Transformers (ViT)
- Patch embedding
- ViT architecture: image → patches → transformer encoder
- DeiT, Swin Transformer, BEiT
- Hybrid CNN-Transformer models
- **So sánh**: CNN vs ViT — khi nào dùng gì?

### 3.5 Advanced CV Tasks
- **Image Generation**: GAN, StyleGAN, Diffusion Models
- **Video Understanding**: 3D CNN, SlowFast, VideoMAE
- **3D Vision**: NeRF, Point Cloud processing
- **OCR**: text detection + text recognition
- **Face Recognition**: ArcFace, CosFace
- **Project**: xây dựng hệ thống nhận diện khuôn mặt real-time

### 📚 Tài liệu Phase 3
| Tài liệu | Loại |
|-----------|------|
| *CS231n — Stanford* | Bài giảng |
| *Dive into Deep Learning — d2l.ai* | Sách (miễn phí) |
| *Papers With Code — Computer Vision* | Tổng hợp paper |
| *Ultralytics YOLOv8 Docs* | Tài liệu |

---

## Phase 4: Natural Language Processing
**Thời lượng: 6–8 tuần**

### 4.1 NLP cơ bản
- Text preprocessing: tokenization, stemming, lemmatization, stopwords
- Biểu diễn văn bản: Bag of Words, TF-IDF
- Word Embeddings: Word2Vec (CBOW, Skip-gram), GloVe, FastText
- **Bài tập**: phân tích sentiment bình luận tiếng Việt

### 4.2 Recurrent Neural Networks
- RNN: cấu trúc, vanishing gradient problem
- LSTM (Long Short-Term Memory): forget gate, input gate, output gate
- GRU (Gated Recurrent Unit)
- Bidirectional RNN
- Seq2Seq model
- **Bài tập**: generation văn bản, dịch máy đơn giản

### 4.3 Attention Mechanism & Transformer
- Attention: Bahdanau attention, Luong attention
- **Transformer** (chi tiết):
  - Self-Attention, Multi-Head Attention
  - Positional Encoding
  - Encoder-Decoder architecture
  - Layer Normalization, Residual Connection
- **Bài tập**: implement Transformer từ đầu bằng PyTorch ("Attention Is All You Need")

### 4.4 Pre-trained Language Models
- **BERT**: Masked Language Model, Next Sentence Prediction
- **GPT series**: GPT-1 → GPT-2 → GPT-3 → GPT-4
- **T5**: Text-to-Text framework
- **RoBERTa, ALBERT, DistilBERT, DeBERTa**
- Hugging Face `transformers` library
- Fine-tuning BERT cho downstream tasks
- **Bài tập**: fine-tune BERT cho Named Entity Recognition tiếng Việt

### 4.5 Advanced NLP Tasks
- **Text Classification**: single-label, multi-label
- **Named Entity Recognition (NER)**
- **Question Answering**: extractive, generative
- **Text Summarization**: extractive vs abstractive
- **Machine Translation**
- **Semantic Search**: dense retrieval, sentence embeddings
- **Project**: xây dựng chatbot hỏi đáp bằng BERT/GPT

### 📚 Tài liệu Phase 4
| Tài liệu | Loại |
|-----------|------|
| *CS224n — Stanford NLP (YouTube)* | Bài giảng |
| *Speech and Language Processing* — Jurafsky & Martin | Sách (miễn phí) |
| *Hugging Face Course* | Khóa học (miễn phí) |
| *The Illustrated Transformer* — Jay Alammar | Blog |

---

## Phase 5: Reinforcement Learning
**Thời lượng: 4–6 tuần**

### 5.1 RL cơ bản
- Markov Decision Process (MDP)
- State, Action, Reward, Policy, Value Function
- Bellman Equation
- Dynamic Programming: Policy Iteration, Value Iteration

### 5.2 Model-Free RL
- **Monte Carlo Methods**
- **Temporal Difference (TD) Learning**: TD(0), TD(λ)
- **Q-Learning**: off-policy, ε-greedy
- **SARSA**: on-policy
- **Bài tập**: giải quyết FrozenLake, CartPole bằng Q-learning

### 5.3 Deep Reinforcement Learning
- **Deep Q-Network (DQN)**: experience replay, target network
- **Double DQN, Dueling DQN, Prioritized Experience Replay**
- **Policy Gradient**: REINFORCE
- **Actor-Critic**: A2C, A3C
- **PPO (Proximal Policy Optimization)** — thuật toán phổ biến nhất
- **SAC (Soft Actor-Critic)**
- **Bài tập**: train agent chơi Atari games

### 5.4 Advanced RL
- Multi-Agent RL (MARL)
- Model-Based RL: World Models, MuZero
- Offline RL / Batch RL
- Inverse RL, Imitation Learning
- RLHF (RL from Human Feedback) — dùng trong LLM alignment
- **Project**: train robot ảo trong MuJoCo/Isaac Gym

### 📚 Tài liệu Phase 5
| Tài liệu | Loại |
|-----------|------|
| *Reinforcement Learning: An Introduction* — Sutton & Barto | Sách (miễn phí) |
| *CS285 — UC Berkeley Deep RL* | Bài giảng |
| *Spinning Up in Deep RL — OpenAI* | Tài liệu |
| *Stable Baselines3* | Thư viện |

---

## Phase 6: Generative AI & Large Language Models
**Thời lượng: 6–8 tuần**

### 6.1 Generative Adversarial Networks (GAN)
- GAN cơ bản: Generator vs Discriminator
- Training dynamics, mode collapse, Nash equilibrium
- DCGAN, WGAN, WGAN-GP
- Conditional GAN, Pix2Pix, CycleGAN
- StyleGAN, StyleGAN2, StyleGAN3
- **Bài tập**: generate khuôn mặt bằng DCGAN

### 6.2 Diffusion Models
- Denoising Diffusion Probabilistic Models (DDPM)
- Score-based models
- DDIM: faster sampling
- **Stable Diffusion**: U-Net, CLIP, VAE
- ControlNet, LoRA cho Stable Diffusion
- **Bài tập**: fine-tune Stable Diffusion cho style riêng

### 6.3 Large Language Models (LLMs)
- Scaling laws: model size, data, compute
- **GPT architecture** chi tiết: causal attention, BPE tokenizer
- **LLaMA, Mistral, Phi, Gemma** — open-source LLMs
- Tokenization: BPE, SentencePiece, tiktoken
- **Bài tập**: train GPT-2 nhỏ từ đầu (nanoGPT)

### 6.4 LLM Training & Fine-tuning
- **Pre-training**: next token prediction, masked language modeling
- **Supervised Fine-Tuning (SFT)**: instruction tuning
- **RLHF**: reward model → PPO alignment
- **DPO (Direct Preference Optimization)**
- **Parameter-Efficient Fine-Tuning**: LoRA, QLoRA, Adapters, Prefix Tuning
- Quantization: GPTQ, AWQ, GGUF (llama.cpp)
- **Bài tập**: fine-tune LLaMA 3 bằng QLoRA cho tiếng Việt

### 6.5 LLM Applications & Engineering
- **Prompt Engineering**: zero-shot, few-shot, chain-of-thought, tree-of-thought
- **RAG (Retrieval-Augmented Generation)**:
  - Vector databases: Chroma, Pinecone, Weaviate, Milvus
  - Embedding models: OpenAI, Cohere, Sentence-BERT
  - Chunking strategies, reranking
- **LLM Agents**: ReAct, tool use, function calling
- **Frameworks**: LangChain, LlamaIndex, CrewAI, AutoGen
- **Evaluation**: BLEU, ROUGE, perplexity, human eval, LLM-as-judge
- **Project**: xây dựng RAG chatbot cho tài liệu pháp luật Việt Nam

### 6.6 Multimodal AI
- Vision-Language Models: CLIP, BLIP, LLaVA
- GPT-4V, Gemini — multimodal LLMs
- Text-to-Image: DALL-E, Midjourney, Stable Diffusion
- Text-to-Video: Sora, Runway Gen-2
- Text-to-Audio: MusicGen, AudioLM
- **Project**: xây dựng ứng dụng mô tả ảnh bằng LLaVA

### 📚 Tài liệu Phase 6
| Tài liệu | Loại |
|-----------|------|
| *Andrej Karpathy — Let's build GPT (YouTube)* | Video |
| *Hugging Face PEFT Documentation* | Tài liệu |
| *LangChain Documentation* | Tài liệu |
| *Lilian Weng's Blog (lilianweng.github.io)* | Blog |
| *Chip Huyen — Building LLM Applications* | Sách |

---

## Phase 7: MLOps & Production AI
**Thời lượng: 4–6 tuần**

### 7.1 ML Pipeline & Experiment Tracking
- MLflow: experiment tracking, model registry
- Weights & Biases (wandb)
- DVC (Data Version Control)
- Feature Store: Feast

### 7.2 Model Serving & Deployment
- **REST API**: FastAPI, Flask
- **Model Serving**: TorchServe, TF Serving, Triton Inference Server
- **Containerization**: Docker, Docker Compose
- **Orchestration**: Kubernetes basics
- **Serverless**: AWS Lambda, Google Cloud Functions
- **Edge Deployment**: ONNX, TensorRT, CoreML, TFLite
- **Bài tập**: deploy model phân loại ảnh lên AWS với Docker + FastAPI

### 7.3 Model Optimization
- Pruning: structured vs unstructured
- Quantization: post-training quantization, quantization-aware training
- Knowledge Distillation
- Model compression
- Inference optimization: batching, caching, speculative decoding

### 7.4 Monitoring & CI/CD
- Data drift detection, model drift
- A/B testing cho ML models
- CI/CD pipeline: GitHub Actions, Jenkins
- Model retraining strategies
- Observability: logging, metrics, alerting

### 7.5 Cloud & Infrastructure
- **AWS**: SageMaker, EC2, S3, Lambda
- **GCP**: Vertex AI, Cloud Run, BigQuery
- **Azure**: Azure ML, Cognitive Services
- GPU cloud: RunPod, Lambda, Vast.ai
- Cost optimization strategies
- **Project**: end-to-end ML pipeline trên cloud

### 📚 Tài liệu Phase 7
| Tài liệu | Loại |
|-----------|------|
| *Designing Machine Learning Systems* — Chip Huyen | Sách |
| *Made With ML — MLOps Course* | Khóa học (miễn phí) |
| *Full Stack Deep Learning* | Khóa học |
| *MLflow Documentation* | Tài liệu |

---

## Phase 8: Chuyên sâu & Nghiên cứu
**Thời lượng: ongoing**

### 8.1 Đọc Paper & Nghiên cứu
- Cách đọc paper hiệu quả (3-pass method)
- Nguồn paper: arXiv, Papers With Code, Semantic Scholar
- Reproduce paper kết quả
- Viết paper / technical report

### 8.2 Các hướng nghiên cứu hot (2024–2026)
- **Efficient AI**: smaller models, faster inference
- **AI Agents**: autonomous agents, multi-agent systems
- **AI Safety & Alignment**: constitutional AI, interpretability
- **Neuro-Symbolic AI**: kết hợp neural networks + logic programming
- **AI for Science**: protein folding (AlphaFold), drug discovery, weather prediction
- **Embodied AI**: robotics + AI
- **Graph Neural Networks (GNN)**: ứng dụng trong molecular, social network
- **Federated Learning**: privacy-preserving ML
- **Continual Learning**: học liên tục không quên kiến thức cũ

### 8.3 Cộng đồng & Phát triển sự nghiệp
- Contribute to open-source: Hugging Face, PyTorch, LangChain
- Kaggle competitions (target: Expert → Master → Grandmaster)
- Viết blog kỹ thuật (Medium, dev.to, personal blog)
- Build portfolio: GitHub projects
- Networking: AI conferences (NeurIPS, ICML, ICLR, CVPR, ACL)

---

## 🗺️ LỘ TRÌNH TỔNG QUAN

```
Phase 0 ─── Toán + Python (4-6 tuần)
   │
Phase 1 ─── Machine Learning (6-8 tuần)
   │
Phase 2 ─── Deep Learning (6-8 tuần)
   │
   ├── Phase 3 ─── Computer Vision (4-6 tuần)
   │
   ├── Phase 4 ─── NLP (6-8 tuần)
   │
   └── Phase 5 ─── RL (4-6 tuần)
         │
Phase 6 ─── Generative AI & LLM (6-8 tuần)
   │
Phase 7 ─── MLOps (4-6 tuần)
   │
Phase 8 ─── Chuyên sâu & Nghiên cứu (ongoing)
```

> **Ghi chú**: Phase 3, 4, 5 có thể học song song. Chọn hướng phù hợp với mục tiêu nghề nghiệp.

---

## 💡 LỜI KHUYÊN

1. **Thực hành > Lý thuyết**: code ít nhất 70% thời gian học
2. **Build projects**: mỗi phase nên có 1-2 project hoàn chỉnh
3. **Kaggle**: tham gia competition để rèn skill thực chiến
4. **Đọc paper**: bắt đầu từ phase 3-4, đọc ít nhất 2 paper/tuần
5. **Cộng đồng**: tham gia Discord, Reddit (r/MachineLearning), Twitter/X AI community
6. **Kiên nhẫn**: AI là marathon, không phải sprint. Consistency > intensity.
