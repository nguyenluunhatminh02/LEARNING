# Bài 23: Deep Reinforcement Learning

## 🎯 Mục tiêu
- Policy Gradient methods: REINFORCE, Actor-Critic
- PPO — thuật toán phổ biến nhất
- RLHF — dùng trong LLM alignment

---

## 1. Policy Gradient

### 1.1 REINFORCE
```python
import torch
import torch.nn as nn
import torch.optim as optim

class PolicyNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 128), nn.ReLU(),
            nn.Linear(128, action_dim), nn.Softmax(dim=-1),
        )
    
    def forward(self, state):
        return self.network(state)

# REINFORCE: update policy theo hướng tăng expected reward
# Loss = -log(π(a|s)) * G_t    (G_t = discounted return)
```

---

## 2. Actor-Critic
```
Actor:  chọn action (policy network)
Critic: đánh giá action tốt/xấu (value network)

Actor học từ feedback của Critic → ổn định hơn REINFORCE
```

---

## 3. PPO (Proximal Policy Optimization)
```python
# PPO = Actor-Critic + clipping → stable training
# Thuật toán RL phổ biến nhất trong production

# Dùng Stable Baselines3
from stable_baselines3 import PPO

model = PPO('MlpPolicy', 'CartPole-v1', verbose=1)
model.learn(total_timesteps=100000)

# Test
obs, _ = env.reset()
for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, _ = env.step(action)
    if terminated or truncated:
        obs, _ = env.reset()
```

---

## 4. RLHF — RL from Human Feedback
```
Dùng trong: GPT-4, Claude, LLaMA-chat

Pipeline:
1. Supervised Fine-Tuning (SFT): train trên human demonstrations
2. Reward Model: human đánh giá output A > B → train reward model
3. PPO: optimize policy to maximize reward model
   → LLM sinh output mà con người thích

Thay thế mới: DPO (Direct Preference Optimization) — đơn giản hơn RLHF
```

---

## 📝 Bài tập

1. Train PPO agent cho CartPole, LunarLander bằng Stable Baselines3
2. Giải Atari game (Pong hoặc Breakout) bằng DQN
3. Đọc paper DPO, so sánh lý thuyết DPO vs RLHF
4. Train multi-agent: 2 agents chơi game đơn giản với nhau

---

## 📚 Tài liệu
- *CS285: Deep RL* — UC Berkeley
- *Spinning Up in Deep RL* — OpenAI
- Paper: *Proximal Policy Optimization* — Schulman et al.
- Paper: *Training language models to follow instructions with human feedback* (InstructGPT)
