# Python Exercises 211-220: Advanced Level
# Bài tập Python 211-220: Nâng cao

# Bài 211: Tính định thức ma trận (Laplace Expansion)
print("Bài 211: Tính định thức ma trận (Laplace Expansion)")
def dinh_thuc(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    det = 0
    for j in range(n):
        minor = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += ((-1) ** j) * matrix[0][j] * dinh_thuc(minor)
    
    return det

ma_tran = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận: {ma_tran}")
print(f"Định thức: {dinh_thuc(ma_tran)}")
print("=" * 50)
print()

# Bài 212: Tìm ma trận nghịch đảo
print("Bài 212: Tìm ma trận nghịch đảo")
def nghich_dao(matrix):
    n = len(matrix)
    det = dinh_thuc(matrix)
    
    if det == 0:
        return None  # Ma trận không có nghịch đảo
    
    # Tìm ma trận phụ hợp
    adj = []
    for i in range(n):
        adj_row = []
        for j in range(n):
            minor = [row[:j] + row[j+1:] for k, row in enumerate(matrix) if k != i]
            cofactor = ((-1) ** (i + j)) * dinh_thuc(minor)
            adj_row.append(cofactor)
        adj.append(adj_row)
    
    # Chuyển vị ma trận phụ hợp
    adj_transpose = [[adj[j][i] for j in range(n)] for i in range(n)]
    
    # Chia cho định thức
    inverse = [[adj_transpose[i][j] / det for j in range(n)] for i in range(n)]
    
    return inverse

ma_tran = [
    [4, 7],
    [2, 6]
]
print(f"Ma trận: {ma_tran}")
print(f"Ma trận nghịch đảo: {nghich_dao(ma_tran)}")
print("=" * 50)
print()

# Bài 213: Giải hệ phương trình tuyến tính (Gaussian Elimination)
print("Bài 213: Giải hệ phương trình tuyến tính (Gaussian Elimination)")
def gaussian_elimination(A, b):
    n = len(A)
    
    # Tạo ma trận mở rộng
    augmented = [row + [b[i]] for i, row in enumerate(A)]
    
    # Khử Gauss
    for i in range(n):
        # Tìm hàng có phần tử lớn nhất ở cột i
        max_row = max(range(i, n), key=lambda r: abs(augmented[r][i]))
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        
        # Khử
        for j in range(i + 1, n):
            factor = augmented[j][i] / augmented[i][i]
            for k in range(i, n + 1):
                augmented[j][k] -= factor * augmented[i][k]
    
    # Thay thế ngược
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = augmented[i][n]
        for j in range(i + 1, n):
            x[i] -= augmented[i][j] * x[j]
        x[i] /= augmented[i][i]
    
    return x

A = [
    [2, 1, -1],
    [-3, -1, 2],
    [-2, 1, 2]
]
b = [8, -11, -3]

print(f"Hệ phương trình:")
for i in range(len(A)):
    print(f"  {A[i][0]}x1 + {A[i][1]}x2 + {A[i][2]}x3 = {b[i]}")
print(f"Nghiệm: {gaussian_elimination(A, b)}")
print("=" * 50)
print()

# Bài 214: Tìm giá trị riêng và vector riêng (Power Iteration)
print("Bài 214: Tìm giá trị riêng và vector riêng (Power Iteration)")
def power_iteration(matrix, num_iterations=100):
    n = len(matrix)
    
    # Khởi tạo vector ngẫu nhiên
    b_k = [1.0] * n
    
    for _ in range(num_iterations):
        # Nhân ma trận với vector
        b_k1 = [sum(matrix[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        
        # Tìm giá trị lớn nhất
        b_k1_norm = max(abs(x) for x in b_k1)
        
        # Chuẩn hóa
        b_k = [x / b_k1_norm for x in b_k1]
    
    # Tính giá trị riêng
    eigenvalue = sum(sum(matrix[i][j] * b_k[j] for j in range(n)) * b_k[i] for i in range(n))
    
    return eigenvalue, b_k

matrix = [
    [2, -1, 0],
    [-1, 2, -1],
    [0, -1, 2]
]

print(f"Ma trận: {matrix}")
eigenvalue, eigenvector = power_iteration(matrix)
print(f"Giá trị riêng lớn nhất: {eigenvalue}")
print(f"Vector riêng tương ứng: {eigenvector}")
print("=" * 50)
print()

# Bài 215: Phân tích LU
print("Bài 215: Phân tích LU")
def lu_decomposition(matrix):
    n = len(matrix)
    L = [[0] * n for _ in range(n)]
    U = [[0] * n for _ in range(n)]
    
    for i in range(n):
        # Tính U
        for j in range(i, n):
            U[i][j] = matrix[i][j] - sum(L[i][k] * U[k][j] for k in range(i))
        
        # Tính L
        for j in range(i, n):
            if i == j:
                L[i][i] = 1
            else:
                L[j][i] = (matrix[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]
    
    return L, U

matrix = [
    [2, 1, 1],
    [4, 3, 3],
    [8, 7, 9]
]

print(f"Ma trận: {matrix}")
L, U = lu_decomposition(matrix)
print(f"Ma trận L: {L}")
print(f"Ma trận U: {U}")
print("=" * 50)
print()

# Bài 216: Phân tích QR
print("Bài 216: Phân tích QR")
import math

def qr_decomposition(matrix):
    n = len(matrix)
    m = len(matrix[0])
    
    Q = [[0.0] * m for _ in range(n)]
    R = [[0.0] * m for _ in range(m)]
    
    for k in range(m):
        # Tính vector q
        q = [matrix[i][k] for i in range(n)]
        
        for j in range(k):
            # Tính R[j][k]
            R[j][k] = sum(Q[i][j] * matrix[i][k] for i in range(n))
            
            # Trừ chiếu
            for i in range(n):
                q[i] -= R[j][k] * Q[i][j]
        
        # Tính R[k][k]
        R[k][k] = math.sqrt(sum(q[i] ** 2 for i in range(n)))
        
        # Chuẩn hóa q
        for i in range(n):
            Q[i][k] = q[i] / R[k][k] if R[k][k] != 0 else 0
    
    return Q, R

matrix = [
    [12, -51, 4],
    [6, 167, -68],
    [-4, 24, -41]
]

print(f"Ma trận: {matrix}")
Q, R = qr_decomposition(matrix)
print(f"Ma trận Q: {Q}")
print(f"Ma trận R: {R}")
print("=" * 50)
print()

# Bài 217: Tìm đường đi ngắn nhất (Bellman-Ford)
print("Bài 217: Tìm đường đi ngắn nhất (Bellman-Ford)")
def bellman_ford(graph, start):
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

print("Đồ thị:", graph)
print("Khoảng cách từ A:", bellman_ford(graph, 'A'))
print("=" * 50)
print()

# Bài 218: Tìm luồng cực đại trong mạng (Ford-Fulkerson)
print("Bài 218: Tìm luồng cực đại trong mạng (Ford-Fulkerson)")
def bfs_ford_fulkerson(graph, source, sink, parent):
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

def ford_fulkerson(graph, source, sink):
    parent = {}
    max_flow = 0
    
    while bfs_ford_fulkerson(graph, source, sink, parent):
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
print("Luồng cực đại từ S đến T:", ford_fulkerson(graph, 'S', 'T'))
print("=" * 50)
print()

# Bài 219: Tìm đường đi Euler
print("Bài 219: Tìm đường đi Euler")
def has_eulerian_path(graph):
    odd_degree = 0
    for node in graph:
        if len(graph[node]) % 2 != 0:
            odd_degree += 1
    
    return odd_degree == 0 or odd_degree == 2

def find_eulerian_path(graph):
    if not has_eulerian_path(graph):
        return None
    
    # Tìm điểm bắt đầu
    start = next(iter(graph))
    for node in graph:
        if len(graph[node]) % 2 != 0:
            start = node
            break
    
    path = []
    stack = [start]
    
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
print("Có đường đi Euler:", has_eulerian_path(graph))
print("Đường đi Euler:", find_eulerian_path(graph))
print("=" * 50)
print()

# Bài 220: Tìm đường đi Hamilton
print("Bài 220: Tìm đường đi Hamilton")
def hamiltonian_path(graph, path, visited):
    if len(path) == len(graph):
        return path
    
    current = path[-1]
    for neighbor in graph[current]:
        if neighbor not in visited:
            visited.add(neighbor)
            path.append(neighbor)
            ket_qua = hamiltonian_path(graph, path, visited)
            if ket_qua:
                return ket_qua
            path.pop()
            visited.remove(neighbor)
    
    return None

def find_hamiltonian_path(graph):
    for start in graph:
        visited = {start}
        path = [start]
        ket_qua = hamiltonian_path(graph, path, visited)
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
print("Đường đi Hamilton:", find_hamiltonian_path(graph))
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập nâng cao!")
