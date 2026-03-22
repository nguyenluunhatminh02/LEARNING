# Bài 01: Complexity Analysis, Arrays & Strings

## 🎯 Mục tiêu
- Big-O notation
- Array/String manipulation
- Two Pointers, Sliding Window patterns

---

## 1. Big-O Complexity

```
O(1)       — Constant:   hash lookup, array access
O(log N)   — Logarithmic: binary search, balanced BST
O(N)       — Linear:     iterate array, linear search
O(N log N) — Log-linear: merge sort, quick sort (avg)
O(N²)      — Quadratic:  nested loops, bubble sort
O(2^N)     — Exponential: subsets, recursive fibonacci
O(N!)      — Factorial:   permutations

Space complexity: bao nhiêu extra memory dùng thêm
  In-place algorithm → O(1) space
  Copy array → O(N) space
```

---

## 2. Arrays

```python
# Two Pointers: sorted array → find pair with target sum
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []

# Remove duplicates in-place (sorted array)
def remove_duplicates(nums):
    if not nums:
        return 0
    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    return write
```

---

## 3. Sliding Window

```python
# Max sum subarray of size K
def max_sum_subarray(nums, k):
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum

# Longest substring without repeating characters
def length_of_longest_substring(s):
    char_index = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        char_index[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len

# Minimum window substring (contains all chars of t)
def min_window(s, t):
    from collections import Counter
    need = Counter(t)
    missing = len(t)
    left = start = 0
    min_len = float('inf')
    
    for right, char in enumerate(s):
        if need[char] > 0:
            missing -= 1
        need[char] -= 1
        
        while missing == 0:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                start = left
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    
    return s[start:start + min_len] if min_len != float('inf') else ""
```

---

## 4. Prefix Sum

```python
# Range sum query O(1) after O(N) preprocessing
class PrefixSum:
    def __init__(self, nums):
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)
    
    def range_sum(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]

# Subarray sum equals K
def subarray_sum(nums, k):
    prefix_count = {0: 1}
    current_sum = 0
    count = 0
    for num in nums:
        current_sum += num
        count += prefix_count.get(current_sum - k, 0)
        prefix_count[current_sum] = prefix_count.get(current_sum, 0) + 1
    return count
```

---

## 📝 Bài tập
1. Container With Most Water (Two Pointers)
2. Longest Repeating Character Replacement (Sliding Window)
3. Product of Array Except Self (Prefix)
4. Trapping Rain Water

## 🎯 LeetCode Practice List

**Two Pointers:**
- #167 Two Sum II (Easy) → warm-up
- #15 3Sum (Medium) → classic
- #11 Container With Most Water (Medium)
- #42 Trapping Rain Water (Hard)

**Sliding Window:**
- #209 Minimum Size Subarray Sum (Medium)
- #3 Longest Substring Without Repeating (Medium)
- #424 Longest Repeating Character Replacement (Medium)
- #76 Minimum Window Substring (Hard)

**Prefix/Arrays:**
- #238 Product of Array Except Self (Medium)
- #53 Maximum Subarray (Kadane's) (Medium)
- #560 Subarray Sum Equals K (Medium)
- #41 First Missing Positive (Hard)

> Mục tiêu: Giải ≥ 10/12 bài. Mỗi bài nên tự code trước khi xem solution.

## 📚 Tài liệu
- [NeetCode Roadmap](https://neetcode.io/roadmap)
- *Cracking the Coding Interview* — Gayle McDowell
