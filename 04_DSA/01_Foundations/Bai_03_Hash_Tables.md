# Bài 03: Hash Tables & Sets

## 🎯 Mục tiêu
- Hash function, collision handling
- HashMap/HashSet patterns
- Frequency counting, grouping

---

## 1. Hash Table Internals

```
Hash Function: key → integer → index in array
  hash("alice") → 1234567 → 1234567 % 16 = 7 → bucket[7]

Collision Resolution:
  Chaining: bucket[7] → LinkedList [("alice",1), ("bob",2)]
  Open Addressing: probe next empty slot (linear/quadratic)

Load Factor = items / buckets
  > 0.75 → resize (double buckets, rehash all)
  
Time Complexity:
  Average: O(1) get/put/delete
  Worst:   O(N) if many collisions (bad hash function)
```

---

## 2. HashMap Patterns

```python
# Two Sum (classic)
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

# Group Anagrams
def group_anagrams(strs):
    groups = {}
    for s in strs:
        key = tuple(sorted(s))
        groups.setdefault(key, []).append(s)
    return list(groups.values())

# Frequency Counter
from collections import Counter
def top_k_frequent(nums, k):
    count = Counter(nums)
    return [x for x, _ in count.most_common(k)]

# Longest Consecutive Sequence — O(N)
def longest_consecutive(nums):
    num_set = set(nums)
    max_len = 0
    for num in num_set:
        if num - 1 not in num_set:  # start of sequence
            length = 1
            while num + length in num_set:
                length += 1
            max_len = max(max_len, length)
    return max_len
```

---

## 3. HashSet Patterns

```python
# Contains Duplicate
def contains_duplicate(nums):
    return len(nums) != len(set(nums))

# Intersection of Two Arrays
def intersection(nums1, nums2):
    return list(set(nums1) & set(nums2))

# Happy Number (detect cycle with set)
def is_happy(n):
    seen = set()
    while n != 1:
        n = sum(int(d) ** 2 for d in str(n))
        if n in seen:
            return False
        seen.add(n)
    return True
```

---

## 4. Advanced: LRU Cache

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # remove oldest
```

---

## 📝 Bài tập
1. Valid Anagram
2. Encode and Decode TinyURL
3. Design HashMap from scratch
4. Minimum Window Substring (HashMap + Sliding Window)

## 🎯 LeetCode Practice List

**HashMap Basics:**
- #1 Two Sum (Easy) → classic hash lookup
- #242 Valid Anagram (Easy)
- #49 Group Anagrams (Medium)
- #128 Longest Consecutive Sequence (Medium)

**HashMap + Pattern:**
- #560 Subarray Sum Equals K (Medium) → prefix sum + hash
- #347 Top K Frequent Elements (Medium) → hash + bucket sort
- #438 Find All Anagrams in String (Medium)
- #76 Minimum Window Substring (Hard)

**HashSet:**
- #217 Contains Duplicate (Easy)
- #36 Valid Sudoku (Medium)
- #705 Design HashSet (Easy)
- #706 Design HashMap (Easy) → implement from scratch

> Mục tiêu: Giải ≥ 10/12 bài.

## 📚 Tài liệu
- [NeetCode — Arrays & Hashing](https://neetcode.io/roadmap)
