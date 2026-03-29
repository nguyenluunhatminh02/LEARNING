# Python Exercises 201-210: Advanced Level
# Bài tập Python 201-210: Nâng cao

# Bài 201: Sắp xếp nhanh (Quick Sort)
print("Bài 201: Sắp xếp nhanh (Quick Sort)")
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

danh_sach = [3, 6, 8, 10, 1, 2, 1]
print(f"Danh sách gốc: {danh_sach}")
print(f"Sau khi Quick Sort: {quick_sort(danh_sach)}")
print("=" * 50)
print()

# Bài 202: Sắp xếp trộn (Merge Sort)
print("Bài 202: Sắp xếp trộn (Merge Sort)")
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    ket_qua = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            ket_qua.append(left[i])
            i += 1
        else:
            ket_qua.append(right[j])
            j += 1
    
    ket_qua.extend(left[i:])
    ket_qua.extend(right[j:])
    return ket_qua

danh_sach = [38, 27, 43, 3, 9, 82, 10]
print(f"Danh sách gốc: {danh_sach}")
print(f"Sau khi Merge Sort: {merge_sort(danh_sach)}")
print("=" * 50)
print()

# Bài 203: Tìm kiếm nhị phân (Binary Search)
print("Bài 203: Tìm kiếm nhị phân (Binary Search)")
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

danh_sach = [1, 3, 5, 7, 9, 11, 13, 15]
target = 7
print(f"Danh sách: {danh_sach}")
print(f"Tìm {target}: Vị trí {binary_search(danh_sach, target)}")
target = 8
print(f"Tìm {target}: Vị trí {binary_search(danh_sach, target)}")
print("=" * 50)
print()

# Bài 204: Tìm kiếm tuyến tính (Linear Search)
print("Bài 204: Tìm kiếm tuyến tính (Linear Search)")
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1

danh_sach = [5, 3, 8, 4, 2]
target = 8
print(f"Danh sách: {danh_sach}")
print(f"Tìm {target}: Vị trí {linear_search(danh_sach, target)}")
target = 6
print(f"Tìm {target}: Vị trí {linear_search(danh_sach, target)}")
print("=" * 50)
print()

# Bài 205: Tìm đường đi ngắn nhất trong đồ thị (Dijkstra)
print("Bài 205: Tìm đường đi ngắn nhất trong đồ thị (Dijkstra)")
import heapq

def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

graph = {
    'A': {'B': 5, 'C': 1},
    'B': {'A': 5, 'C': 2, 'D': 1},
    'C': {'A': 1, 'B': 2, 'D': 4, 'E': 8},
    'D': {'B': 1, 'C': 4, 'E': 3, 'F': 6},
    'E': {'C': 8, 'D': 3},
    'F': {'D': 6}
}

print("Đồ thị:", graph)
print("Khoảng cách từ A:", dijkstra(graph, 'A'))
print("=" * 50)
print()

# Bài 206: Tìm đường đi ngắn nhất (BFS)
print("Bài 206: Tìm đường đi ngắn nhất (BFS)")
from collections import deque

def bfs_shortest_path(graph, start, end):
    queue = deque([(start, [start])])
    visited = set([start])
    
    while queue:
        node, path = queue.popleft()
        if node == end:
            return path
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print("Đồ thị:", graph)
print("Đường đi từ A đến F:", bfs_shortest_path(graph, 'A', 'F'))
print("=" * 50)
print()

# Bài 207: DFS (Depth-First Search)
print("Bài 207: DFS (Depth-First Search)")
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    
    visited.add(start)
    ket_qua = [start]
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            ket_qua.extend(dfs(graph, neighbor, visited))
    
    return ket_qua

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print("Đồ thị:", graph)
print("DFS từ A:", dfs(graph, 'A'))
print("=" * 50)
print()

# Bài 208: Tìm cây bao trùm nhỏ nhất (Prim's Algorithm)
print("Bài 208: Tìm cây bao trùm nhỏ nhất (Prim's Algorithm)")
def prim_mst(graph):
    if not graph:
        return []
    
    start_node = next(iter(graph))
    visited = set([start_node])
    mst = []
    edges = []
    
    for neighbor, weight in graph[start_node].items():
        edges.append((weight, start_node, neighbor))
    
    heapq.heapify(edges)
    
    while edges and len(visited) < len(graph):
        weight, node1, node2 = heapq.heappop(edges)
        
        if node2 in visited:
            continue
        
        visited.add(node2)
        mst.append((node1, node2, weight))
        
        for neighbor, w in graph[node2].items():
            if neighbor not in visited:
                heapq.heappush(edges, (w, node2, neighbor))
    
    return mst

graph = {
    'A': {'B': 4, 'C': 1},
    'B': {'A': 4, 'C': 2, 'D': 1},
    'C': {'A': 1, 'B': 2, 'D': 5},
    'D': {'B': 1, 'C': 5}
}

print("Đồ thị:", graph)
print("Cây bao trùm nhỏ nhất:", prim_mst(graph))
print("=" * 50)
print()

# Bài 209: Tìm đường đi ngắn nhất (Floyd-Warshall)
print("Bài 209: Tìm đường đi ngắn nhất (Floyd-Warshall)")
def floyd_warshall(graph):
    nodes = list(graph.keys())
    n = len(nodes)
    dist = [[float('infinity')] * n for _ in range(n)]
    
    for i in range(n):
        dist[i][i] = 0
    
    for i, node in enumerate(nodes):
        for j, neighbor in enumerate(nodes):
            if neighbor in graph[node]:
                dist[i][j] = graph[node][neighbor]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return {nodes[i]: {nodes[j]: dist[i][j] for j in range(n)} for i in range(n)}

graph = {
    'A': {'B': 3, 'C': 8, 'D': -4},
    'B': {'D': 1, 'E': 7},
    'C': {'B': 4},
    'D': {'C': -5, 'E': 2},
    'E': {'A': 2}
}

print("Đồ thị:", graph)
print("Ma trận khoảng cách:", floyd_warshall(graph))
print("=" * 50)
print()

# Bài 210: Kiểm tra đồ thị có chu trình không (Union-Find)
print("Bài 210: Kiểm tra đồ thị có chu trình không (Union-Find)")
class UnionFind:
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}
    
    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]
    
    def union(self, set1, set2):
        root1 = self.find(set1)
        root2 = self.find(set2)
        
        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1
            return False
        return True

def has_cycle(graph):
    vertices = list(graph.keys())
    uf = UnionFind(vertices)
    
    for u in vertices:
        for v in graph[u]:
            if uf.union(u, v):
                return True
    return False

graph1 = {
    'A': ['B'],
    'B': ['C'],
    'C': ['A']
}

graph2 = {
    'A': ['B'],
    'B': ['C'],
    'C': []
}

print("Đồ thị 1:", graph1)
print("Có chu trình:", has_cycle(graph1))
print("Đồ thị 2:", graph2)
print("Có chu trình:", has_cycle(graph2))
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập nâng cao!")
