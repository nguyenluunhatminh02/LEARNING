# Python Exercises 271-280: Advanced Level
# Bài tập Python 271-280: Nâng cao

# Bài 271: Tìm số tổ hợp C(n, k)
print("Bài 271: Tìm số tổ hợp C(n, k)")
def binomial_coefficient(n, k):
    if k > n - k:
        k = n - k
    
    res = 1
    for i in range(k):
        res = res * (n - i) // (i + 1)
    
    return res

n, k = 10, 3
print(f"C({n}, {k}) = {binomial_coefficient(n, k)}")
print(f"Tam giác Pascal:")
for i in range(6):
    row = [binomial_coefficient(i, j) for j in range(i + 1)]
    print(f"  {row}")
print("=" * 50)
print()

# Bài 272: Tìm số hoán vị P(n, k)
print("Bài 272: Tìm số hoán vị P(n, k)")
def permutation(n, k):
    if k > n:
        return 0
    
    res = 1
    for i in range(n, n - k, -1):
        res *= i
    
    return res

n, k = 5, 3
print(f"P({n}, {k}) = {permutation(n, k)}")
print(f"P(5, 5) = {permutation(5, 5)} (số hoán vị của 5 phần tử)")
print("=" * 50)
print()

# Bài 273: Tìm số phân hoạch số nguyên
print("Bài 273: Tìm số phân hoạch số nguyên")
def integer_partition(n):
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        dp[i][0] = 1
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i > j:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j] + dp[i][j - i]
    
    return dp[n][n]

for n in range(1, 11):
    print(f"p({n}) = {integer_partition(n)}")
print("=" * 50)
print()

# Bài 274: Tìm số cách đặt quân hậu
print("Bài 274: Tìm số cách đặt quân hậu")
def n_queens(n):
    def backtrack(row, cols, diag1, diag2):
        nonlocal count
        if row == n:
            count += 1
            return
        
        for col in range(n):
            d1 = row - col
            d2 = row + col
            
            if col in cols or d1 in diag1 or d2 in diag2:
                continue
            
            cols.add(col)
            diag1.add(d1)
            diag2.add(d2)
            
            backtrack(row + 1, cols, diag1, diag2)
            
            cols.remove(col)
            diag1.remove(d1)
            diag2.remove(d2)
    
    count = 0
    backtrack(0, set(), set(), set())
    return count

for n in range(1, 9):
    print(f"Số cách đặt {n} quân hậu: {n_queens(n)}")
print("=" * 50)
print()

# Bài 275: Tìm số cách tô màu đồ thị
print("Bài 275: Tìm số cách tô màu đồ thị")
def graph_coloring(graph, m):
    def color_node(node, colors):
        if node == len(graph):
            return 1
        
        count = 0
        for color in range(m):
            if is_valid(node, color, colors):
                colors[node] = color
                count += color_node(node + 1, colors)
                colors[node] = -1
        
        return count
    
    def is_valid(node, color, colors):
        for neighbor in graph[node]:
            if colors[neighbor] == color:
                return False
        return True
    
    colors = [-1] * len(graph)
    return color_node(0, colors)

graph = {
    0: [1, 2, 3],
    1: [0, 2],
    2: [0, 1, 3],
    3: [0, 2]
}

m = 3
print(f"Số cách tô màu đồ thị với {m} màu: {graph_coloring(graph, m)}")
print("=" * 50)
print()

# Bài 276: Tìm số cách đi trong lưới
print("Bài 276: Tìm số cách đi trong lưới với chướng ngại vật")
def unique_paths_with_obstacles_dp(obstacle_grid):
    m, n = len(obstacle_grid), len(obstacle_grid[0])
    
    if obstacle_grid[0][0] == 1:
        return 0
    
    dp = [[0] * n for _ in range(m)]
    dp[0][0] = 1
    
    for i in range(m):
        for j in range(n):
            if obstacle_grid[i][j] == 1:
                dp[i][j] = 0
            else:
                if i > 0:
                    dp[i][j] += dp[i - 1][j]
                if j > 0:
                    dp[i][j] += dp[i][j - 1]
    
    return dp[m - 1][n - 1]

obstacle_grid = [
    [0, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
]

print("Lưới với chướng ngại vật:", obstacle_grid)
print(f"Số cách đi: {unique_paths_with_obstacles_dp(obstacle_grid)}")
print("=" * 50)
print()

# Bài 277: Tìm số cách xếp ghế
print("Bài 277: Tìm số cách xếp ghế")
def seating_arrangements(n, k):
    if k > n:
        return 0
    
    # Số cách chọn k vị trí từ n vị trí
    choose = binomial_coefficient(n, k)
    
    # Số cách xếp k người vào k vị trí
    perm = permutation(k, k)
    
    return choose * perm

n, k = 5, 3
print(f"Số cách xếp {k} người vào {n} ghế: {seating_arrangements(n, k)}")
print("=" * 50)
print()

# Bài 278: Tìm số cách chia kẹo
print("Bài 278: Tìm số cách chia kẹo")
def distribute_candy(n, k):
    # Số nguyên dương
    return binomial_coefficient(n - 1, k - 1)

n, k = 10, 3
print(f"Số cách chia {n} kẹo cho {k} trẻ (mỗi trẻ ít nhất 1): {distribute_candy(n, k)}")
print("=" * 50)
print()

# Bài 279: Tìm số cách chọn nhóm
print("Bài 279: Tìm số cách chọn nhóm")
def choose_groups(n, k):
    return binomial_coefficient(n, k)

n, k = 10, 4
print(f"Số cách chọn nhóm {k} người từ {n} người: {choose_groups(n, k)}")
print("=" * 50)
print()

# Bài 280: Tìm số cách sắp xếp với điều kiện
print("Bài 280: Tìm số cách sắp xếp với điều kiện")
def derangements(n):
    if n == 0:
        return 1
    if n == 1:
        return 0
    
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 0
    
    for i in range(2, n + 1):
        dp[i] = (i - 1) * (dp[i - 1] + dp[i - 2])
    
    return dp[n]

for n in range(1, 11):
    print(f"!{n} (số hoán vị không cố định) = {derangements(n)}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập nâng cao!")
