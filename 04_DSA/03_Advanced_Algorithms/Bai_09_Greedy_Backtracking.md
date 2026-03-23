# Bài 09: Greedy & Backtracking

## 🎯 Mục tiêu
- Greedy algorithms
- Backtracking template
- When Greedy vs DP vs Backtracking

## 📖 Câu chuyện đời thường
> **Greedy** giống như đi chợ với ngân sách hạn chế: luôn chọn món rẻ nhất mà vẫn đủ dinh dưỡng — mỗi bước chọn cái tốt nhất tại thời điểm đó. Không phải lúc nào cũng cho kết quả tối ưu toàn cục, nhưng rất nhanh. **Backtracking** giống tìm đường trong mê cung: đi thử một hướng, nếu vào ngõ cụt thì quay lại thử hướng khác. Bạn không đi mò toàn bộ mê cung — khi biết rõ hướng này sai, bạn cắt bỏ luôn (pruning). Greedy cho bài đơn giản, DP cho bài tối ưu, Backtracking cho bài "liệt kê tất cả cách".

---

## 1. Greedy

```python
# Jump Game — can reach last index?
def can_jump(nums):
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach: return False
        max_reach = max(max_reach, i + jump)
    return True

# Merge Intervals
def merge_intervals(intervals):
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged

# Meeting Rooms II — min rooms needed
import heapq
def min_meeting_rooms(intervals):
    intervals.sort()
    heap = []  # end times
    for start, end in intervals:
        if heap and heap[0] <= start:
            heapq.heappop(heap)
        heapq.heappush(heap, end)
    return len(heap)
```

---

## 2. Backtracking Template

```python
def backtrack(candidates, path, result):
    if is_solution(path):
        result.append(path[:])
        return
    for candidate in get_candidates(path):
        if is_valid(candidate, path):
            path.append(candidate)
            backtrack(candidates, path, result)
            path.pop()  # undo choice

# Subsets
def subsets(nums):
    result = []
    def bt(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            bt(i + 1, path)
            path.pop()
    bt(0, [])
    return result

# Permutations
def permutations(nums):
    result = []
    def bt(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        for i in range(len(remaining)):
            path.append(remaining[i])
            bt(path, remaining[:i] + remaining[i+1:])
            path.pop()
    bt([], nums)
    return result

# N-Queens
def solve_nqueens(n):
    result = []
    cols, diag1, diag2 = set(), set(), set()
    
    def bt(row, board):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row-col) in diag1 or (row+col) in diag2:
                continue
            cols.add(col); diag1.add(row-col); diag2.add(row+col)
            board[row][col] = 'Q'
            bt(row + 1, board)
            board[row][col] = '.'
            cols.remove(col); diag1.remove(row-col); diag2.remove(row+col)
    
    bt(0, [['.' for _ in range(n)] for _ in range(n)])
    return result
```

---

## 3. When to use what?

```
Greedy:   Local optimal → global optimal. Fast O(N log N).
  → Intervals, scheduling, Huffman encoding

DP:       Overlapping subproblems + optimal substructure.
  → Sequence problems, knapsack, counting paths

Backtracking: Explore all possibilities with pruning.
  → Permutations, combinations, constraint satisfaction
```

---

## 📝 Bài tập
1. Combination Sum, Letter Combinations of Phone Number
2. Palindrome Partitioning (Backtracking)
3. Gas Station, Hand of Straights (Greedy)
4. Word Search (Grid Backtracking)

## 🎯 LeetCode Practice List

**Backtracking:**
- #78 Subsets (Medium)
- #90 Subsets II (Medium)
- #46 Permutations (Medium)
- #39 Combination Sum (Medium) ⭐
- #40 Combination Sum II (Medium)
- #17 Letter Combinations of Phone Number (Medium)
- #131 Palindrome Partitioning (Medium)
- #79 Word Search (Medium) ⭐
- #51 N-Queens (Hard)

**Greedy:**
- #53 Maximum Subarray (Kadane) (Medium)
- #55 Jump Game (Medium)
- #45 Jump Game II (Medium)
- #134 Gas Station (Medium) ⭐
- #763 Partition Labels (Medium)
- #846 Hand of Straights (Medium)

> Mục tiêu: Giải ≥ 12/15 bài.

## 📚 Tài liệu
- *Algorithm Design Manual* — Steven Skiena
