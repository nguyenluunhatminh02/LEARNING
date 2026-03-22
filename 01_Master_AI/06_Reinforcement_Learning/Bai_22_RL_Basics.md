# Bài 22: Reinforcement Learning cơ bản

## 🎯 Mục tiêu
- Hiểu MDP, Policy, Value Function
- Q-Learning & SARSA
- Giải quyết bài toán đơn giản với RL

---

## 1. Khái niệm cốt lõi

```
Agent (AI) tương tác với Environment (môi trường):
1. Agent quan sát State (trạng thái)
2. Agent chọn Action (hành động) theo Policy
3. Environment trả về Reward + State mới
4. Mục tiêu: maximize tổng Reward dài hạn

State (s) → Action (a) → Reward (r) → New State (s')
```

### Bellman Equation
```
V(s) = max_a [R(s,a) + γ * V(s')]

Q(s,a) = R(s,a) + γ * max_a' Q(s', a')

γ (gamma): discount factor ∈ [0,1] — cân bằng reward ngắn hạn vs dài hạn
```

---

## 2. Q-Learning

```python
import numpy as np
import gymnasium as gym

# Môi trường FrozenLake
env = gym.make('FrozenLake-v1', is_slippery=False)
n_states = env.observation_space.n    # 16
n_actions = env.action_space.n        # 4

# Q-table: Q[state, action] = expected reward
Q = np.zeros((n_states, n_actions))

# Hyperparameters
lr = 0.8            # Learning rate
gamma = 0.95        # Discount factor
epsilon = 1.0       # Exploration rate
epsilon_decay = 0.999
episodes = 10000

for episode in range(episodes):
    state, _ = env.reset()
    done = False
    
    while not done:
        # Epsilon-greedy: explore vs exploit
        if np.random.random() < epsilon:
            action = env.action_space.sample()   # Random (explore)
        else:
            action = np.argmax(Q[state])          # Best known (exploit)
        
        next_state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
        
        # Q-Learning update (off-policy)
        Q[state, action] += lr * (
            reward + gamma * np.max(Q[next_state]) - Q[state, action]
        )
        
        state = next_state
    
    epsilon *= epsilon_decay

# Test
wins = 0
for _ in range(100):
    state, _ = env.reset()
    done = False
    while not done:
        action = np.argmax(Q[state])
        state, reward, terminated, truncated, _ = env.step(action)
        done = terminated or truncated
    wins += reward
print(f"Win rate: {wins}%")
```

---

## 3. Deep Q-Network (DQN)
```python
import torch
import torch.nn as nn

class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim),
        )
    
    def forward(self, x):
        return self.network(x)

# Key techniques:
# 1. Experience Replay: lưu (s, a, r, s') vào buffer, sample random batch
# 2. Target Network: copy model mỗi N steps → stabilize training
```

---

## 📝 Bài tập

1. Implement Q-Learning cho FrozenLake, đạt >90% win rate
2. Implement DQN cho CartPole-v1 (OpenAI Gym), đạt 500 steps
3. So sánh Q-Learning vs SARSA trên cùng environment
4. Visualize Q-table: vẽ heatmap optimal actions

---

## 📚 Tài liệu
- *Reinforcement Learning: An Introduction* — Sutton & Barto (Ch. 1-6)
- *Spinning Up in Deep RL* — OpenAI (miễn phí)
- [Gymnasium Documentation](https://gymnasium.farama.org/)
