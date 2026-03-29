# Python Exercises 281-290: Advanced Level
# Bài tập Python 281-290: Nâng cao

# Bài 281: Tìm đường đi ngắn nhất trong 3D
print("Bài 281: Tìm đường đi ngắn nhất trong 3D")
import heapq

def shortest_path_3d(grid):
    if not grid or not grid[0] or not grid[0][0]:
        return 0
    
    rows, cols, depth = len(grid), len(grid[0]), len(grid[0][0])
    directions = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    
    heap = [(grid[0][0][0], 0, 0, 0)]
    visited = set()
    
    while heap:
        cost, x, y, z = heapq.heappop(heap)
        
        if (x, y, z) in visited:
            continue
        visited.add((x, y, z))
        
        if x == rows - 1 and y == cols - 1 and z == depth - 1:
            return cost
        
        for dx, dy, dz in directions:
            nx, ny, nz = x + dx, y + dy, z + dz
            
            if 0 <= nx < rows and 0 <= ny < cols and 0 <= nz < depth:
                heapq.heappush(heap, (cost + grid[nx][ny][nz], nx, ny, nz))
    
    return -1

grid_3d = [
    [
        [1, 2, 3],
        [4, 5, 6]
    ],
    [
        [7, 8, 9],
        [10, 11, 12]
    ]
]

print("Lưới 3D:", grid_3d)
print(f"Đường đi ngắn nhất: {shortest_path_3d(grid_3d)}")
print("=" * 50)
print()

# Bài 282: Tìm đường đi trong mê cung
print("Bài 282: Tìm đường đi trong mê cung")
def maze_solver(maze):
    if not maze or not maze[0]:
        return None
    
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def bfs(start, end):
        queue = [(start, [start])]
        visited = {start}
        
        while queue:
            (x, y), path = queue.pop(0)
            
            if (x, y) == end:
                return path
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if (0 <= nx < rows and 0 <= ny < cols and 
                    maze[nx][ny] == 0 and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        
        return None
    
    start = (0, 0)
    end = (rows - 1, cols - 1)
    return bfs(start, end)

maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

print("Mê cung (0: đi được, 1: tường):", maze)
print(f"Đường đi từ góc trên trái sang góc dưới phải: {maze_solver(maze)}")
print("=" * 50)
print()

# Bài 283: Tìm đường đi trong mê cung với DFS
print("Bài 283: Tìm đường đi trong mê cung với DFS")
def maze_solver_dfs(maze):
    if not maze or not maze[0]:
        return None
    
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def dfs(x, y, path, visited):
        if x == rows - 1 and y == cols - 1:
            return path + [(x, y)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            if (0 <= nx < rows and 0 <= ny < cols and 
                maze[nx][ny] == 0 and (nx, ny) not in visited):
                visited.add((nx, ny))
                ket_qua = dfs(nx, ny, path + [(x, y)], visited)
                if ket_qua:
                    return ket_qua
                visited.remove((nx, ny))
        
        return None
    
    return dfs(0, 0, [], {(0, 0)})

maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

print("Mê cung (0: đi được, 1: tường):", maze)
print(f"Đường đi DFS: {maze_solver_dfs(maze)}")
print("=" * 50)
print()

# Bài 284: Tìm đường đi trong mê cung với A*
print("Bài 284: Tìm đường đi trong mê cung với A*")
def maze_solver_astar(maze):
    if not maze or not maze[0]:
        return None
    
    rows, cols = len(maze), len(maze[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    def heuristic(x, y):
        return abs(rows - 1 - x) + abs(cols - 1 - y)
    
    def a_star():
        start = (0, 0)
        goal = (rows - 1, cols - 1)
        
        open_set = [(heuristic(0, 0), 0, start, [start])]
        visited = set()
        
        while open_set:
            f, g, (x, y), path = heapq.heappop(open_set)
            
            if (x, y) in visited:
                continue
            visited.add((x, y))
            
            if (x, y) == goal:
                return path
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                if (0 <= nx < rows and 0 <= ny < cols and 
                    maze[nx][ny] == 0 and (nx, ny) not in visited):
                    new_g = g + 1
                    new_f = new_g + heuristic(nx, ny)
                    heapq.heappush(open_set, (new_f, new_g, (nx, ny), path + [(nx, ny)]))
        
        return None
    
    return a_star()

maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

print("Mê cung (0: đi được, 1: tường):", maze)
print(f"Đường đi A*: {maze_solver_astar(maze)}")
print("=" * 50)
print()

# Bài 285: Tìm đường đi trong đồ thị có trọng số âm
print("Bài 285: Tìm đường đi trong đồ thị có trọng số âm")
def shortest_path_negative_weights(graph, start):
    vertices = list(graph.keys())
    distances = {v: float('infinity') for v in vertices}
    distances[start] = 0
    
    for _ in range(len(vertices) - 1):
        for u in vertices:
            for v, weight in graph[u].items():
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
    
    # Kiểm tra chu trình âm
    for u in vertices:
        for v, weight in graph[u].items():
            if distances[u] + weight < distances[v]:
                return None  # Có chu trình âm
    
    return distances

graph = {
    'A': {'B': -1, 'C': 4},
    'B': {'C': 3, 'D': 2, 'E': 2},
    'C': {},
    'D': {'B': 1, 'C': 5},
    'E': {'D': -3}
}

print("Đồ thị có trọng số âm:", graph)
print("Khoảng cách từ A:", shortest_path_negative_weights(graph, 'A'))
print("=" * 50)
print()

# Bài 286: Tìm đường đi trong đồ thị có hướng
print("Bài 286: Tìm đường đi trong đồ thị có hướng")
def directed_graph_path(graph, start, end):
    visited = set()
    path = []
    
    def dfs(node):
        if node == end:
            path.append(node)
            return True
        
        if node in visited:
            return False
        
        visited.add(node)
        path.append(node)
        
        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True
        
        path.pop()
        return False
    
    if dfs(start):
        return path
    return None

graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': ['E'],
    'E': []
}

print("Đồ thị có hướng:", graph)
print(f"Đường đi từ A đến E: {directed_graph_path(graph, 'A', 'E')}")
print("=" * 50)
print()

# Bài 287: Tìm đường đi trong đồ thị vô hướng
print("Bài 287: Tìm đường đi trong đồ thị vô hướng")
def undirected_graph_path(graph, start, end):
    visited = set()
    queue = [(start, [start])]
    
    while queue:
        node, path = queue.pop(0)
        
        if node == end:
            return path
        
        if node not in visited:
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    
    return None

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['A', 'D'],
    'D': ['B', 'C', 'E'],
    'E': ['D']
}

print("Đồ thị vô hướng:", graph)
print(f"Đường đi từ A đến E: {undirected_graph_path(graph, 'A', 'E')}")
print("=" * 50)
print()

# Bài 288: Tìm đường đi trong đồ thị có chu trình
print("Bài 288: Tìm đường đi trong đồ thị có chu trình")
def graph_path_with_cycle(graph, start, end):
    visited = set()
    path = []
    
    def dfs(node):
        if node == end:
            path.append(node)
            return True
        
        if node in visited:
            return False
        
        visited.add(node)
        path.append(node)
        
        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True
        
        path.pop()
        visited.remove(node)
        return False
    
    if dfs(start):
        return path
    return None

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C', 'E'],
    'E': ['D']
}

print("Đồ thị có chu trình:", graph)
print(f"Đường đi từ A đến E: {graph_path_with_cycle(graph, 'A', 'E')}")
print("=" * 50)
print()

# Bài 289: Tìm đường đi trong đồ thị có nhiều đường đi
print("Bài 289: Tìm tất cả đường đi trong đồ thị")
def all_paths_in_graph(graph, start, end):
    paths = []
    
    def dfs(node, path, visited):
        if node == end:
            paths.append(path + [node])
            return
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path + [node], visited | {neighbor})
    
    dfs(start, [], {start})
    return paths

graph = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['D'],
    'D': ['E'],
    'E': []
}

print("Đồ thị:", graph)
print(f"Tất cả đường đi từ A đến E: {all_paths_in_graph(graph, 'A', 'E')}")
print("=" * 50)
print()

# Bài 290: Tìm đường đi ngắn nhất trong đồ thị có nhiều đường đi
print("Bài 290: Tìm đường đi ngắn nhất trong đồ thị có nhiều đường đi")
def shortest_path_multiple(graph, start, end):
    from collections import deque
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        node, path = queue.popleft()
        
        if node == end:
            return path
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None

graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['D', 'F'],
    'D': ['E', 'F'],
    'E': ['G'],
    'F': ['G'],
    'G': []
}

print("Đồ thị:", graph)
print(f"Đường đi ngắn nhất từ A đến G: {shortest_path_multiple(graph, 'A', 'G')}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập nâng cao!")
