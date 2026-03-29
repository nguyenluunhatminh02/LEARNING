# Python Exercises 221-230: Advanced Level
# Bài tập Python 221-230: Nâng cao

# Bài 221: Tìm số lớn nhất trong danh sách bằng chia để trị
print("Bài 221: Tìm số lớn nhất trong danh sách bằng chia để trị")
def tim_max_chia_de_tri(arr):
    if len(arr) == 1:
        return arr[0]
    
    mid = len(arr) // 2
    left_max = tim_max_chia_de_tri(arr[:mid])
    right_max = tim_max_chia_de_tri(arr[mid:])
    
    return left_max if left_max > right_max else right_max

danh_sach = [3, 7, 2, 9, 1, 5, 8]
print(f"Danh sách: {danh_sach}")
print(f"Số lớn nhất: {tim_max_chia_de_tri(danh_sach)}")
print("=" * 50)
print()

# Bài 222: Tìm số nhỏ nhất trong danh sách bằng chia để trị
print("Bài 222: Tìm số nhỏ nhất trong danh sách bằng chia để trị")
def tim_min_chia_de_tri(arr):
    if len(arr) == 1:
        return arr[0]
    
    mid = len(arr) // 2
    left_min = tim_min_chia_de_tri(arr[:mid])
    right_min = tim_min_chia_de_tri(arr[mid:])
    
    return left_min if left_min < right_min else right_min

danh_sach = [3, 7, 2, 9, 1, 5, 8]
print(f"Danh sách: {danh_sach}")
print(f"Số nhỏ nhất: {tim_min_chia_de_tri(danh_sach)}")
print("=" * 50)
print()

# Bài 223: Tính tổng danh sách bằng chia để trị
print("Bài 223: Tính tổng danh sách bằng chia để trị")
def tinh_tong_chia_de_tri(arr):
    if len(arr) == 1:
        return arr[0]
    
    mid = len(arr) // 2
    left_sum = tinh_tong_chia_de_tri(arr[:mid])
    right_sum = tinh_tong_chia_de_tri(arr[mid:])
    
    return left_sum + right_sum

danh_sach = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"Danh sách: {danh_sach}")
print(f"Tổng: {tinh_tong_chia_de_tri(danh_sach)}")
print("=" * 50)
print()

# Bài 224: Tìm phần tử lớn nhất thứ k bằng Quick Select
print("Bài 224: Tìm phần tử lớn nhất thứ k bằng Quick Select")
import random

def quick_select(arr, k):
    if len(arr) == 1:
        return arr[0]
    
    pivot = random.choice(arr)
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    L, M = len(left), len(middle)
    
    if k < L:
        return quick_select(left, k)
    elif k < L + M:
        return middle[0]
    else:
        return quick_select(right, k - L - M)

danh_sach = [3, 2, 1, 5, 6, 4]
k = 2
print(f"Danh sách: {danh_sach}")
print(f"Phần tử lớn nhất thứ {k}: {quick_select(danh_sach, k)}")
print("=" * 50)
print()

# Bài 225: Tìm cặp điểm gần nhất
print("Bài 225: Tìm cặp điểm gần nhất")
import math

def khoang_cach(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def cap_diem_gan_nhat_brute(points):
    min_dist = float('infinity')
    closest_pair = None
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = khoang_cach(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                closest_pair = (points[i], points[j])
    
    return closest_pair, min_dist

points = [(1, 2), (3, 4), (5, 6), (7, 8), (2, 3)]
print(f"Danh sách điểm: {points}")
closest_pair, min_dist = cap_diem_gan_nhat_brute(points)
print(f"Cặp điểm gần nhất: {closest_pair}")
print(f"Khoảng cách: {min_dist}")
print("=" * 50)
print()

# Bài 226: Tìm đường bao lồi (Convex Hull - Graham Scan)
print("Bài 226: Tìm đường bao lồi (Convex Hull - Graham Scan)")
def cross_product(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

def convex_hull(points):
    points = sorted(points)
    
    lower = []
    for p in points:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    
    return lower[:-1] + upper[:-1]

points = [(0, 0), (1, 1), (2, 2), (1, 2), (3, 1), (0, 3)]
print(f"Danh sách điểm: {points}")
print(f"Đường bao lồi: {convex_hull(points)}")
print("=" * 50)
print()

# Bài 227: Tìm tập con có tổng bằng k (Subset Sum)
print("Bài 227: Tìm tập con có tổng bằng k (Subset Sum)")
def subset_sum(numbers, target):
    n = len(numbers)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        dp[i][0] = True
    
    for i in range(1, n + 1):
        for j in range(1, target + 1):
            if numbers[i - 1] <= j:
                dp[i][j] = dp[i - 1][j] or dp[i - 1][j - numbers[i - 1]]
            else:
                dp[i][j] = dp[i - 1][j]
    
    return dp[n][target]

numbers = [3, 34, 4, 12, 5, 2]
target = 9
print(f"Danh sách số: {numbers}")
print(f"Có tập con có tổng bằng {target}: {subset_sum(numbers, target)}")
print("=" * 50)
print()

# Bài 228: Bài toán cái túi (Knapsack Problem)
print("Bài 228: Bài toán cái túi (Knapsack Problem)")
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], 
                              dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]

weights = [1, 3, 4, 5]
values = [1, 4, 5, 7]
capacity = 7
print(f"Trọng lượng: {weights}")
print(f"Giá trị: {values}")
print(f"Sức chứa: {capacity}")
print(f"Giá trị tối đa: {knapsack(weights, values, capacity)}")
print("=" * 50)
print()

# Bài 229: Bài toán người bán hàng (TSP - Dynamic Programming)
print("Bài 229: Bài toán người bán hàng (TSP - Dynamic Programming)")
def tsp(graph):
    n = len(graph)
    memo = {}
    
    def dp(mask, pos):
        if mask == (1 << n) - 1:
            return graph[pos][0] if graph[pos][0] != float('infinity') else float('infinity')
        
        if (mask, pos) in memo:
            return memo[(mask, pos)]
        
        ans = float('infinity')
        for city in range(n):
            if not (mask & (1 << city)):
                ans = min(ans, graph[pos][city] + dp(mask | (1 << city), city))
        
        memo[(mask, pos)] = ans
        return ans
    
    return dp(1, 0)

graph = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

print("Ma trận khoảng cách:", graph)
print("Độ dài đường đi ngắn nhất:", tsp(graph))
print("=" * 50)
print()

# Bài 230: Tìm dãy con tăng dài nhất (LIS)
print("Bài 230: Tìm dãy con tăng dài nhất (LIS)")
def longest_increasing_subsequence(arr):
    if not arr:
        return []
    
    n = len(arr)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    # Tìm dãy con
    max_length = max(dp)
    result = []
    current_length = max_length
    
    for i in range(n - 1, -1, -1):
        if dp[i] == current_length:
            result.append(arr[i])
            current_length -= 1
    
    return result[::-1]

danh_sach = [10, 22, 9, 33, 21, 50, 41, 60]
print(f"Danh sách: {danh_sach}")
print(f"Dãy con tăng dài nhất: {longest_increasing_subsequence(danh_sach)}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập nâng cao!")
