# Bài 08: Dynamic Programming

## 🎯 Mục tiêu
- Memoization (top-down) vs Tabulation (bottom-up)
- Classic DP patterns
- Multi-dimensional DP

## 📖 Câu chuyện đời thường
> Bạn leo cầu thang 100 bậc. Mỗi lần bước được 1 hoặc 2 bậc. "Có bao nhiêu cách leo?". Nếu tính brute force, bạn thử tất cả tổ hợp — vũ trụ huỷ diệt vẫn chưa xong. **Dynamic Programming** là nhận ra: số cách đến bậc 10 = số cách đến bậc 9 + số cách đến bậc 8 (vì từ 9 bước 1, từ 8 bước 2). Bạn ghi chép kết quả đã tính (**memoization**) để không tính lại. Giống như khi tính tiền đi chợ: thay vì cộng lại từ đầu mỗi lần thêm món, bạn ghi tổng hiện tại và chỉ cộng thêm món mới.

---

## 1. DP Framework

```
1. Define state: dp[i] = ?
2. Recurrence: dp[i] = f(dp[i-1], dp[i-2], ...)
3. Base case: dp[0] = ?
4. Order: fill dp from base case
5. Answer: dp[n] or max(dp)
```

---

## 2. 1D DP

```python
# Fibonacci
def fib(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Climbing Stairs (n ways to climb n steps, 1 or 2 at a time)
# Same as fibonacci: dp[i] = dp[i-1] + dp[i-2]

# House Robber (max money, can't rob adjacent houses)
def rob(nums):
    if len(nums) <= 2: return max(nums)
    dp = [0] * len(nums)
    dp[0], dp[1] = nums[0], max(nums[0], nums[1])
    for i in range(2, len(nums)):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    return dp[-1]

# Longest Increasing Subsequence — O(N log N)
from bisect import bisect_left
def length_of_lis(nums):
    tails = []
    for num in nums:
        pos = bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)

# Coin Change (min coins to make amount)
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for coin in coins:
            if coin <= a:
                dp[a] = min(dp[a], dp[a - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
```

---

## 3. 2D DP

```python
# Longest Common Subsequence
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# 0/1 Knapsack
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i-1][w]  # don't take item i
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i][w], dp[i-1][w - weights[i-1]] + values[i-1])
    return dp[n][capacity]

# Unique Paths (grid)
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i-1][j] + dp[i][j-1]
    return dp[m-1][n-1]

# Edit Distance
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]
```

---

## 📝 Bài tập
1. Word Break, Decode Ways
2. Longest Palindromic Subsequence
3. Partition Equal Subset Sum
4. Maximum Product Subarray

## 🎯 LeetCode Practice List

**1D DP (start here):**
- #70 Climbing Stairs (Easy)
- #198 House Robber (Medium)
- #213 House Robber II (Medium)
- #5 Longest Palindromic Substring (Medium)
- #647 Palindromic Substrings (Medium)
- #91 Decode Ways (Medium) ⭐
- #139 Word Break (Medium) ⭐
- #152 Maximum Product Subarray (Medium)
- #300 Longest Increasing Subsequence (Medium) ⭐

**2D DP (intermediate):**
- #62 Unique Paths (Medium)
- #1143 Longest Common Subsequence (Medium)
- #72 Edit Distance (Medium) ⭐
- #97 Interleaving String (Medium)
- #329 Longest Increasing Path in Matrix (Hard)

**Knapsack Pattern:**
- #416 Partition Equal Subset Sum (Medium)
- #494 Target Sum (Medium)
- #322 Coin Change (Medium) ⭐
- #518 Coin Change II (Medium)

**DP on Intervals/Trees:**
- #312 Burst Balloons (Hard)
- #1235 Maximum Profit in Job Scheduling (Hard)

> Mục tiêu: Giải ≥ 15/20 bài. DP cần nhiều luyện tập nhất — mỗi bài làm 2-3 lần cho quen pattern.

## 📚 Tài liệu
- [NeetCode DP Patterns](https://neetcode.io/roadmap)
- *Introduction to Algorithms* — CLRS (Ch.15)
