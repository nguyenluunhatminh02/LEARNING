# Python Exercises 251-260: Advanced Level
# Bài tập Python 251-260: Nâng cao

# Bài 251: Tìm cây bao trùm nhỏ nhất (Kruskal's Algorithm)
print("Bài 251: Tìm cây bao trùm nhỏ nhất (Kruskal's Algorithm)")
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
            return True
        return False

def kruskal_mst(graph):
    edges = []
    for u in graph:
        for v, weight in graph[u].items():
            edges.append((weight, u, v))
    
    edges.sort()
    vertices = list(graph.keys())
    uf = UnionFind(vertices)
    mst = []
    
    for weight, u, v in edges:
        if uf.union(u, v):
            mst.append((u, v, weight))
            if len(mst) == len(vertices) - 1:
                break
    
    return mst

graph = {
    'A': {'B': 4, 'C': 1},
    'B': {'A': 4, 'C': 2, 'D': 1},
    'C': {'A': 1, 'B': 2, 'D': 5},
    'D': {'B': 1, 'C': 5}
}

print("Đồ thị:", graph)
print("Cây bao trùm nhỏ nhất:", kruskal_mst(graph))
print("=" * 50)
print()

# Bài 252: Tìm đường đi ngắn nhất (A* Algorithm)
print("Bài 252: Tìm đường đi ngắn nhất (A* Algorithm)")
import heapq

def a_star(graph, start, goal, heuristic):
    open_set = [(0, start)]
    came_from = {}
    g_score = {node: float('infinity') for node in graph}
    g_score[start] = 0
    f_score = {node: float('infinity') for node in graph}
    f_score[start] = heuristic[start]
    
    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for neighbor, weight in graph[current].items():
            tentative_g_score = g_score[current] + weight
            
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic[neighbor]
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None

graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

heuristic = {'A': 7, 'B': 6, 'C': 2, 'D': 0}
print("Đồ thị:", graph)
print("Đường đi từ A đến D:", a_star(graph, 'A', 'D', heuristic))
print("=" * 50)
print()

# Bài 253: Tìm đường đi ngắn nhất (Dijkstra với Priority Queue)
print("Bài 253: Tìm đường đi ngắn nhất (Dijkstra với Priority Queue)")
def dijkstra_with_path(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, previous

graph = {
    'A': {'B': 5, 'C': 1},
    'B': {'A': 5, 'C': 2, 'D': 1},
    'C': {'A': 1, 'B': 2, 'D': 4, 'E': 8},
    'D': {'B': 1, 'C': 4, 'E': 3, 'F': 6},
    'E': {'C': 8, 'D': 3},
    'F': {'D': 6}
}

print("Đồ thị:", graph)
distances, previous = dijkstra_with_path(graph, 'A')
print("Khoảng cách từ A:", distances)
print("=" * 50)
print()

# Bài 254: Tìm luồng cực đại (Edmonds-Karp)
print("Bài 254: Tìm luồng cực đại (Edmonds-Karp)")
def bfs_edmonds_karp(graph, source, sink, parent):
    visited = {node: False for node in graph}
    queue = [source]
    visited[source] = True
    
    while queue:
        u = queue.pop(0)
        
        for v, capacity in graph[u].items():
            if not visited[v] and capacity > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
    
    return visited[sink]

def edmonds_karp(graph, source, sink):
    parent = {}
    max_flow = 0
    
    while bfs_edmonds_karp(graph, source, sink, parent):
        path_flow = float('infinity')
        v = sink
        
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, graph[u][v])
            v = u
        
        max_flow += path_flow
        
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] = graph.get(v, {}).get(u, 0) + path_flow
            v = u
    
    return max_flow

graph = {
    'S': {'A': 3, 'B': 2},
    'A': {'B': 5, 'T': 2},
    'B': {'T': 3},
    'T': {}
}

print("Đồ thị:", graph)
print("Luồng cực đại từ S đến T:", edmonds_karp(graph, 'S', 'T'))
print("=" * 50)
print()

# Bài 255: Tìm đường đi ngắn nhất (Bellman-Ford với đường đi)
print("Bài 255: Tìm đường đi ngắn nhất (Bellman-Ford với đường đi)")
def bellman_ford_with_path(graph, start):
    vertices = list(graph.keys())
    distances = {v: float('infinity') for v in vertices}
    distances[start] = 0
    previous = {v: None for v in vertices}
    
    for _ in range(len(vertices) - 1):
        for u in vertices:
            for v, weight in graph[u].items():
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    previous[v] = u
    
    # Kiểm tra chu trình âm
    for u in vertices:
        for v, weight in graph[u].items():
            if distances[u] + weight < distances[v]:
                return None, None  # Có chu trình âm
    
    return distances, previous

graph = {
    'A': {'B': -1, 'C': 4},
    'B': {'C': 3, 'D': 2, 'E': 2},
    'C': {},
    'D': {'B': 1, 'C': 5},
    'E': {'D': -3}
}

print("Đồ thị:", graph)
distances, previous = bellman_ford_with_path(graph, 'A')
print("Khoảng cách từ A:", distances)
print("=" * 50)
print()

# Bài 256: Tìm đường đi ngắn nhất (Floyd-Warshall với đường đi)
print("Bài 256: Tìm đường đi ngắn nhất (Floyd-Warshall với đường đi)")
def floyd_warshall_with_path(graph):
    nodes = list(graph.keys())
    n = len(nodes)
    dist = [[float('infinity')] * n for _ in range(n)]
    next_node = [[None] * n for _ in range(n)]
    
    for i in range(n):
        dist[i][i] = 0
        for j in range(n):
            if nodes[j] in graph[nodes[i]]:
                dist[i][j] = graph[nodes[i]][nodes[j]]
                next_node[i][j] = j
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]
    
    return dist, next_node

graph = {
    'A': {'B': 3, 'C': 8, 'D': -4},
    'B': {'D': 1, 'E': 7},
    'C': {'B': 4},
    'D': {'C': -5, 'E': 2},
    'E': {'A': 2}
}

print("Đồ thị:", graph)
dist, next_node = floyd_warshall_with_path(graph)
print("Ma trận khoảng cách:", dist)
print("=" * 50)
print()

# Bài 257: Tìm đường đi Euler (Hierholzer's Algorithm)
print("Bài 257: Tìm đường đi Euler (Hierholzer's Algorithm)")
def find_eulerian_path_hierholzer(graph):
    if not graph:
        return []
    
    # Tìm điểm bắt đầu
    start = next(iter(graph))
    for node in graph:
        if len(graph[node]) % 2 != 0:
            start = node
            break
    
    stack = [start]
    path = []
    
    while stack:
        current = stack[-1]
        if graph[current]:
            next_node = graph[current].pop()
            graph[next_node].remove(current)
            stack.append(next_node)
        else:
            path.append(stack.pop())
    
    return path[::-1]

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C']
}

print("Đồ thị:", graph)
print("Đường đi Euler:", find_eulerian_path_hierholzer(graph))
print("=" * 50)
print()

# Bài 258: Tìm đường đi Hamilton (Backtracking)
print("Bài 258: Tìm đường đi Hamilton (Backtracking)")
def hamiltonian_path_backtracking(graph, path, visited):
    if len(path) == len(graph):
        return path
    
    current = path[-1]
    for neighbor in graph[current]:
        if neighbor not in visited:
            visited.add(neighbor)
            path.append(neighbor)
            ket_qua = hamiltonian_path_backtracking(graph, path, visited)
            if ket_qua:
                return ket_qua
            path.pop()
            visited.remove(neighbor)
    
    return None

def find_hamiltonian_path_bt(graph):
    for start in graph:
        visited = {start}
        path = [start]
        ket_qua = hamiltonian_path_backtracking(graph, path, visited)
        if ket_qua:
            return ket_qua
    return None

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
}

print("Đồ thị:", graph)
print("Đường đi Hamilton:", find_hamiltonian_path_bt(graph))
print("=" * 50)
print()

# Bài 259: Tìm cây bao trùm nhỏ nhất (Borůvka's Algorithm)
print("Bài 259: Tìm cây bao trùm nhỏ nhất (Borůvka's Algorithm)")
def boruvka_mst(graph):
    if not graph:
        return []
    
    vertices = list(graph.keys())
    components = [{v} for v in vertices]
    mst = []
    
    while len(components) > 1:
        min_edges = {}
        
        for comp in components:
            min_edge = None
            min_weight = float('infinity')
            
            for u in comp:
                for v, weight in graph[u].items():
                    if v not in comp:
                        if weight < min_weight:
                            min_weight = weight
                            min_edge = (u, v, weight)
            
            if min_edge:
                min_edges[frozenset(comp)] = min_edge
        
        # Gộp các thành phần
        new_components = []
        used = set()
        
        for comp in components:
            if frozenset(comp) in used:
                continue
            
            edge = min_edges.get(frozenset(comp))
            if edge:
                mst.append(edge)
                u, v, weight = edge
                
                # Tìm thành phần chứa v
                v_comp = None
                for c in components:
                    if v in c:
                        v_comp = c
                        break
                
                # Gộp hai thành phần
                new_comp = comp.union(v_comp)
                new_components.append(new_comp)
                used.add(frozenset(comp))
                used.add(frozenset(v_comp))
        
        components = new_components
    
    return mst

graph = {
    'A': {'B': 4, 'C': 1},
    'B': {'A': 4, 'C': 2, 'D': 1},
    'C': {'A': 1, 'B': 2, 'D': 5},
    'D': {'B': 1, 'C': 5}
}

print("Đồ thị:", graph)
print("Cây bao trùm nhỏ nhất:", boruvka_mst(graph))
print("=" * 50)
print()

# Bài 260: Tìm đường đi ngắn nhất (Bidirectional Search)
print("Bài 260: Tìm đường đi ngắn nhất (Bidirectional Search)")
from collections import deque

def bidirectional_search(graph, start, goal):
    if start == goal:
        return [start]
    
    queue_start = deque([start])
    queue_goal = deque([goal])
    
    visited_start = {start: None}
    visited_goal = {goal: None}
    
    meeting_point = None
    
    while queue_start and queue_goal:
        # Mở rộng từ start
        for _ in range(len(queue_start)):
            current = queue_start.popleft()
            
            for neighbor in graph[current]:
                if neighbor not in visited_start:
                    visited_start[neighbor] = current
                    queue_start.append(neighbor)
                    
                    if neighbor in visited_goal:
                        meeting_point = neighbor
                        break
        
        if meeting_point:
            break
        
        # Mở rộng từ goal
        for _ in range(len(queue_goal)):
            current = queue_goal.popleft()
            
            for neighbor in graph[current]:
                if neighbor not in visited_goal:
                    visited_goal[neighbor] = current
                    queue_goal.append(neighbor)
                    
                    if neighbor in visited_start:
                        meeting_point = neighbor
                        break
        
        if meeting_point:
            break
    
    if not meeting_point:
        return None
    
    # Tạo đường đi
    path_start = []
    current = meeting_point
    while current is not None:
        path_start.append(current)
        current = visited_start[current]
    
    path_goal = []
    current = visited_goal[meeting_point]
    while current is not None:
        path_goal.append(current)
        current = visited_goal[current]
    
    return path_start[::-1] + path_goal

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print("Đồ thị:", graph)
print("Đường đi từ A đến F:", bidirectional_search(graph, 'A', 'F'))
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập nâng cao!")
