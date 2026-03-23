# Bài 05: Heaps & Priority Queues

## 🎯 Mục tiêu
- Min/Max Heap operations
- Top-K problems
- Median of stream

## 📖 Câu chuyện đời thường
> Bạn là bác sĩ phòng cấp cứu. Bệnh nhân không được khám theo thứ tự đến mà theo mức độ nguy kịch — ai nặng nhất khám trước. Đó chính là **Heap** (Priority Queue). **Min Heap** = luôn lấy ra phần tử nhỏ nhất. **Max Heap** = luôn lấy ra lớn nhất. **Top-K** giống như bảng xếp hạng: "Top 10 bài hát tuần này" — heap giúp luôn biết top 10 mà không cần sắp xếp lại toàn bộ mỗi lần có bài mới. **Median of stream** giống giữa 2 nhóm học sinh giỏi và khá — giá trị giữa luôn cập nhật khi có học sinh mới.

---

## 1. Heap Basics

```python
import heapq

# Min Heap (default in Python)
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 1)
heapq.heappush(heap, 3)
heapq.heappop(heap)  # 1 (smallest)

# Max Heap (negate values)
max_heap = []
heapq.heappush(max_heap, -5)
heapq.heappush(max_heap, -1)
-heapq.heappop(max_heap)  # 5 (largest)

# Heapify array → O(N)
nums = [3, 1, 4, 1, 5, 9]
heapq.heapify(nums)  # [1, 1, 4, 3, 5, 9]

# Top K Largest → O(N log K)
def top_k_largest(nums, k):
    return heapq.nlargest(k, nums)

# Top K Frequent Elements
from collections import Counter
def top_k_frequent(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)
```

---

## 2. Two Heaps — Median of Stream

```python
class MedianFinder:
    def __init__(self):
        self.small = []  # max heap (left half, negated)
        self.large = []  # min heap (right half)
    
    def addNum(self, num):
        heapq.heappush(self.small, -num)
        # Ensure small's max <= large's min
        if self.small and self.large and -self.small[0] > self.large[0]:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        # Balance sizes
        if len(self.small) > len(self.large) + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small) + 1:
            heapq.heappush(self.small, -heapq.heappop(self.large))
    
    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        if len(self.large) > len(self.small):
            return self.large[0]
        return (-self.small[0] + self.large[0]) / 2
```

---

## 3. Merge K Sorted Lists

```python
def merge_k_lists(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst.val, i, lst))
    
    dummy = ListNode(0)
    curr = dummy
    while heap:
        val, i, node = heapq.heappop(heap)
        curr.next = node
        curr = curr.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

---

## 📝 Bài tập
1. Kth Largest Element in Array
2. Task Scheduler (greedy + heap)
3. Reorganize String (max heap)
4. Find Median from Data Stream

## 🎯 LeetCode Practice List

**Min/Max Heap Basics:**
- #703 Kth Largest Element in a Stream (Easy)
- #1046 Last Stone Weight (Easy)
- #215 Kth Largest Element in Array (Medium) ⭐
- #347 Top K Frequent Elements (Medium)
- #973 K Closest Points to Origin (Medium)

**Heap + Greedy:**
- #621 Task Scheduler (Medium)
- #767 Reorganize String (Medium)
- #1337 K Weakest Rows in Matrix (Easy)

**Two Heaps / Advanced:**
- #295 Find Median from Data Stream (Hard) ⭐
- #355 Design Twitter (Medium)
- #23 Merge K Sorted Lists (Hard)
- #778 Swim in Rising Water (Hard)

> Mục tiêu: Giải ≥ 9/12 bài.

## 📚 Tài liệu
- *Introduction to Algorithms* — CLRS (Ch.6: Heapsort)
