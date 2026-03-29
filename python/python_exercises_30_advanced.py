# Python Exercises 291-300: Advanced Level
# Bài tập Python 291-300: Nâng cao

# Bài 291: Tìm đường đi trong đồ thị có trọng số
print("Bài 291: Tìm đường đi trong đồ thị có trọng số")
import heapq

def weighted_graph_path(graph, start, end):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        if current_node == end:
            break
        
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    # Tạo đường đi
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    
    return path[::-1] if path[-1] == start else None

graph = {
    'A': {'B': 5, 'C': 1},
    'B': {'A': 5, 'C': 2, 'D': 1},
    'C': {'A': 1, 'B': 2, 'D': 4, 'E': 8},
    'D': {'B': 1, 'C': 4, 'E': 3, 'F': 6},
    'E': {'C': 8, 'D': 3},
    'F': {'D': 6}
}

print("Đồ thị có trọng số:", graph)
print(f"Đường đi từ A đến F: {weighted_graph_path(graph, 'A', 'F')}")
print("=" * 50)
print()

# Bài 292: Tìm đường đi trong đồ thị có hướng và có trọng số
print("Bài 292: Tìm đường đi trong đồ thị có hướng và có trọng số")
def directed_weighted_path(graph, start, end):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_node]:
            continue
        
        if current_node == end:
            break
        
        for neighbor, weight in graph.get(current_node, {}).items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    # Tạo đường đi
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    
    return path[::-1] if path[-1] == start else None

graph = {
    'A': {'B': 3, 'C': 6},
    'B': {'C': 4, 'D': 4},
    'C': {'D': 8},
    'D': {'E': 5},
    'E': {}
}

print("Đồ thị có hướng và có trọng số:", graph)
print(f"Đường đi từ A đến E: {directed_weighted_path(graph, 'A', 'E')}")
print("=" * 50)
print()

# Bài 293: Tìm đường đi trong đồ thị có nhiều cạnh
print("Bài 293: Tìm đường đi trong đồ thị có nhiều cạnh")
def multi_edge_graph_path(graph, start, end):
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
    'A': ['B', 'B', 'C'],
    'B': ['D', 'D'],
    'C': ['D'],
    'D': ['E', 'E'],
    'E': []
}

print("Đồ thị có nhiều cạnh:", graph)
print(f"Đường đi từ A đến E: {multi_edge_graph_path(graph, 'A', 'E')}")
print("=" * 50)
print()

# Bài 294: Tìm đường đi trong đồ thị có vòng lặp
print("Bài 294: Tìm đường đi trong đồ thị có vòng lặp")
def graph_with_loops_path(graph, start, end):
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
    'B': ['B', 'D'],
    'C': ['D'],
    'D': ['E'],
    'E': []
}

print("Đồ thị có vòng lặp:", graph)
print(f"Đường đi từ A đến E: {graph_with_loops_path(graph, 'A', 'E')}")
print("=" * 50)
print()

# Bài 295: Tìm đường đi trong đồ thị có đỉnh cô lập
print("Bài 295: Tìm đường đi trong đồ thị có đỉnh cô lập")
def graph_with_isolated_path(graph, start, end):
    from collections import deque
    
    if start not in graph or end not in graph:
        return None
    
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
    'B': ['D'],
    'C': ['D'],
    'D': ['E'],
    'E': [],
    'F': [],  # Đỉnh cô lập
    'G': []   # Đỉnh cô lập
}

print("Đồ thị có đỉnh cô lập:", graph)
print(f"Đường đi từ A đến E: {graph_with_isolated_path(graph, 'A', 'E')}")
print(f"Đường đi từ A đến F: {graph_with_isolated_path(graph, 'A', 'F')}")
print("=" * 50)
print()

# Bài 296: Tìm đường đi trong đồ thị có nhiều thành phần liên thông
print("Bài 296: Tìm đường đi trong đồ thị có nhiều thành phần liên thông")
def multi_component_graph_path(graph, start, end):
    from collections import deque
    
    # Tìm thành phần liên thông của start
    component = set()
    queue = deque([start])
    component.add(start)
    
    while queue:
        node = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor not in component:
                component.add(neighbor)
                queue.append(neighbor)
    
    if end not in component:
        return None
    
    # Tìm đường đi
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
    'B': ['A', 'C'],
    'C': ['A', 'B'],
    'D': ['E', 'F'],
    'E': ['D', 'F'],
    'F': ['D', 'E'],
    'G': ['H'],
    'H': ['G']
}

print("Đồ thị có nhiều thành phần liên thông:", graph)
print(f"Đường đi từ A đến C: {multi_component_graph_path(graph, 'A', 'C')}")
print(f"Đường đi từ A đến D: {multi_component_graph_path(graph, 'A', 'D')}")
print("=" * 50)
print()

# Bài 297: Tìm đường đi trong đồ thị có hướng và vô hướng
print("Bài 297: Tìm đường đi trong đồ thị có hướng và vô hướng")
def mixed_graph_path(graph, start, end):
    from collections import deque
    
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        node, path = queue.popleft()
        
        if node == end:
            return path
        
        # Xử lý cả cạnh có hướng và vô hướng
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D'],
    'C': ['D'],
    'D': ['E'],
    'E': []
}

print("Đồ thị hỗn hợp:", graph)
print(f"Đường đi từ A đến E: {mixed_graph_path(graph, 'A', 'E')}")
print("=" * 50)
print()

# Bài 298: Tìm đường đi trong đồ thị có trọng số âm và dương
print("Bài 298: Tìm đường đi trong đồ thị có trọng số âm và dương")
def mixed_weight_graph_path(graph, start, end):
    vertices = list(graph.keys())
    distances = {v: float('infinity') for v in vertices}
    distances[start] = 0
    previous = {v: None for v in vertices}
    
    for _ in range(len(vertices) - 1):
        for u in vertices:
            for v, weight in graph.get(u, {}).items():
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    previous[v] = u
    
    # Kiểm tra chu trình âm
    for u in vertices:
        for v, weight in graph.get(u, {}).items():
            if distances[u] + weight < distances[v]:
                return None  # Có chu trình âm
    
    # Tạo đường đi
    if distances[end] == float('infinity'):
        return None
    
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    
    return path[::-1]

graph = {
    'A': {'B': 5, 'C': -2},
    'B': {'C': 3, 'D': 2},
    'C': {'D': 1},
    'D': {'E': 4},
    'E': {}
}

print("Đồ thị có trọng số âm và dương:", graph)
print(f"Đường đi từ A đến E: {mixed_weight_graph_path(graph, 'A', 'E')}")
print("=" * 50)
print()

# Bài 299: Tìm đường đi trong đồ thị có nhiều đỉnh
print("Bài 299: Tìm đường đi trong đồ thị có nhiều đỉnh")
def large_graph_path(graph, start, end):
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

# Tạo đồ thị lớn
graph = {str(i): [str(j) for j in range(i+1, min(i+5, 20))] for i in range(20)}
graph['19'] = []

print("Đồ thị lớn với 20 đỉnh")
print(f"Đường đi từ 0 đến 19: {large_graph_path(graph, '0', '19')}")
print("=" * 50)
print()

# Bài 300: Tìm đường đi trong đồ thị phức tạp
print("Bài 300: Tìm đường đi trong đồ thị phức tạp")
def complex_graph_path(graph, start, end):
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

# Tạo đồ thị phức tạp
graph = {
    'A': ['B', 'C', 'D'],
    'B': ['E', 'F'],
    'C': ['G', 'H'],
    'D': ['I', 'J'],
    'E': ['K'],
    'F': ['K'],
    'G': ['L'],
    'H': ['L'],
    'I': ['M'],
    'J': ['M'],
    'K': ['N'],
    'L': ['N'],
    'M': ['N'],
    'N': ['O'],
    'O': []
}

print("Đồ thị phức tạp:", graph)
print(f"Đường đi từ A đến O: {complex_graph_path(graph, 'A', 'O')}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập nâng cao!")
print("=" * 50)
print()
print("CHÚC MỪNG! ĐÃ HOÀN THÀNH TẤT CẢ 300 BÀI TẬP PYTHON!")
print("=" * 50)
print()
print("Tóm tắt:")
print("- 100 bài tập cơ bản (Files 1-10)")
print("- 100 bài tập trung cấp (Files 11-20)")
print("- 100 bài tập nâng cao (Files 21-30)")
print("- Tổng cộng: 300 bài tập")
print()
print("Các chủ đề bao gồm:")
print("• Cơ bản: Biến, toán tử, điều kiện, vòng lặp, hàm, chuỗi, list, tuple, dict, set, file")
print("• Trung cấp: Thuật toán tìm kiếm, sắp xếp, xử lý chuỗi, ma trận, số học nâng cao")
print("• Nâng cao: Cấu trúc dữ liệu, đồ thị, thuật toán tối ưu hóa, quy hoạch động, toán học nâng cao")
print()
print("Chúc bạn học tập hiệu quả!")
