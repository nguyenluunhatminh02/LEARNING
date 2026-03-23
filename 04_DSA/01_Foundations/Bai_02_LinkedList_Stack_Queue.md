# Bài 02: Linked Lists, Stacks & Queues

## 🎯 Mục tiêu
- Linked List operations & patterns
- Stack & Queue applications
- Monotonic Stack

## 📖 Câu chuyện đời thường
> **Linked List** giống đoàn tàu hỏa: mỗi toa biết toa kế tiếp là gì nhưng không biết toa số 10 ở đâu. Muốn thêm toa giữa đoàn tàu? Dễ! Chỉ cần nối lại 2 móc (con trỏ). **Stack** giống chồng đĩa: đĩa đặt sau cùng lấy ra trước (LIFO). Khi bạn bấm Ctrl+Z, chất Undo stack lấy hành động gần nhất ra hủy. **Queue** giống hàng đợi mua vé xem phim: ai đến trước mua trước (FIFO). **Monotonic Stack** giống như đứng trên mái nhà nhìn về phía trước: bạn chỉ thấy tòa nhà tiếp theo cao hơn bạn, các tòa thấp hơn bị che khuất.

---

## 1. Linked List

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Reverse linked list
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev

# Detect cycle (Floyd's Tortoise & Hare)
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Merge two sorted lists
def merge_two_lists(l1, l2):
    dummy = ListNode(0)
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next
    curr.next = l1 or l2
    return dummy.next

# Find middle node
def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

---

## 2. Stack

```python
# Valid parentheses
def is_valid(s):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    for char in s:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            stack.append(char)
    return len(stack) == 0

# Min Stack — O(1) getMin
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val):
        self.stack.append(val)
        min_val = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(min_val)
    
    def pop(self):
        self.stack.pop()
        self.min_stack.pop()
    
    def getMin(self):
        return self.min_stack[-1]
```

---

## 3. Monotonic Stack

```python
# Next Greater Element — cho mỗi element, tìm element lớn hơn tiếp theo
def next_greater(nums):
    result = [-1] * len(nums)
    stack = []  # indices, decreasing order
    for i, num in enumerate(nums):
        while stack and nums[stack[-1]] < num:
            idx = stack.pop()
            result[idx] = num
        stack.append(i)
    return result

# Daily Temperatures — bao nhiêu ngày đợi để có nhiệt độ cao hơn
def daily_temperatures(temps):
    result = [0] * len(temps)
    stack = []
    for i, temp in enumerate(temps):
        while stack and temps[stack[-1]] < temp:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)
    return result

# Largest Rectangle in Histogram
def largest_rectangle(heights):
    stack = []
    max_area = 0
    for i, h in enumerate(heights + [0]):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area
```

---

## 4. Queue — BFS Pattern

```python
from collections import deque

# BFS level-order traversal
def level_order(root):
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

---

## 📝 Bài tập
1. Reverse Linked List II (reverse from position m to n)
2. LRU Cache (HashMap + Doubly Linked List)
3. Evaluate Reverse Polish Notation (Stack)
4. Sliding Window Maximum (Monotonic Deque)

## 🎯 LeetCode Practice List

**Linked List:**
- #206 Reverse Linked List (Easy)
- #21 Merge Two Sorted Lists (Easy)
- #141 Linked List Cycle (Easy)
- #19 Remove Nth Node From End (Medium)
- #143 Reorder List (Medium)
- #146 LRU Cache (Medium) ⭐ must-do

**Stack:**
- #20 Valid Parentheses (Easy)
- #155 Min Stack (Medium)
- #150 Evaluate Reverse Polish Notation (Medium)
- #739 Daily Temperatures (Medium) → monotonic stack
- #84 Largest Rectangle in Histogram (Hard)

**Queue/Deque:**
- #225 Implement Stack using Queues (Easy)
- #239 Sliding Window Maximum (Hard) → monotonic deque

> Mục tiêu: Giải ≥ 10/13 bài.

## 📚 Tài liệu
- [LeetCode Stack Problems](https://leetcode.com/tag/stack/)
- *Elements of Programming Interviews* — Aziz, Lee, Prakash
