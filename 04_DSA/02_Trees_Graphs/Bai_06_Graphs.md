# Bài 06: Graphs — BFS, DFS, Dijkstra, Topological Sort

## 🎯 Mục tiêu
- Graph representation
- BFS, DFS traversal
- Shortest path (Dijkstra)
- Topological Sort, Union-Find

---

## 1. Graph Representation

```python
# Adjacency List (preferred)
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C']
}

# Adjacency Matrix
#     A  B  C  D
# A [[0, 1, 1, 0],
# B  [1, 0, 0, 1],
# C  [1, 0, 0, 1],
# D  [0, 1, 1, 0]]
```

---

## 2. BFS & DFS

```python
from collections import deque

# BFS — shortest path in unweighted graph
def bfs(graph, start, target):
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        node, path = queue.popleft()
        if node == target:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None

# DFS — explore all paths, detect cycles
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited

# Number of Islands (grid BFS/DFS)
def num_islands(grid):
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        grid[r][c] = '0'  # mark visited
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            dfs(r + dr, c + dc)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count
```

---

## 3. Dijkstra — Shortest Path (Weighted)

```python
import heapq

def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    heap = [(0, start)]
    
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for neighbor, weight in graph[node]:
            new_dist = d + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    
    return dist
```

---

## 4. Topological Sort (DAG)

```python
# Course Schedule — can finish all courses?
def can_finish(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque(i for i in range(num_courses) if in_degree[i] == 0)
    completed = 0
    
    while queue:
        course = queue.popleft()
        completed += 1
        for next_course in graph[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return completed == num_courses
```

---

## 5. Union-Find (Disjoint Set)

```python
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py: return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True
```

---

## 📝 Bài tập
1. Clone Graph, Pacific Atlantic Water Flow
2. Network Delay Time (Dijkstra)
3. Course Schedule II (Topological Sort order)
4. Number of Connected Components (Union-Find)

## 🎯 LeetCode Practice List

**BFS/DFS on Graphs:**
- #200 Number of Islands (Medium) ⭐
- #133 Clone Graph (Medium)
- #695 Max Area of Island (Medium)
- #417 Pacific Atlantic Water Flow (Medium)
- #994 Rotting Oranges (Medium) → BFS
- #127 Word Ladder (Hard)

**Topological Sort:**
- #207 Course Schedule (Medium)
- #210 Course Schedule II (Medium) ⭐
- #269 Alien Dictionary (Hard)

**Dijkstra / Shortest Path:**
- #743 Network Delay Time (Medium) ⭐
- #1631 Path With Minimum Effort (Medium)
- #787 Cheapest Flights Within K Stops (Medium)

**Union-Find:**
- #323 Number of Connected Components (Medium)
- #684 Redundant Connection (Medium)
- #721 Accounts Merge (Medium)

> Mục tiêu: Giải ≥ 12/15 bài.

## 📚 Tài liệu
- *Introduction to Algorithms* — CLRS (Ch.22-25)
- [NeetCode — Graphs](https://neetcode.io/roadmap)
