# Python Exercises 231-240: Advanced Level
# Bài tập Python 231-240: Nâng cao

# Bài 231: Tìm dãy con chung dài nhất (LCS)
print("Bài 231: Tìm dãy con chung dài nhất (LCS)")
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    # Truy vết
    lcs = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            lcs.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    
    return lcs[::-1]

text1 = "ABCBDAB"
text2 = "BDCABA"
print(f"Chuỗi 1: {text1}")
print(f"Chuỗi 2: {text2}")
print(f"Dãy con chung dài nhất: {longest_common_subsequence(text1, text2)}")
print("=" * 50)
print()

# Bài 232: Tìm khoảng cách chỉnh sửa nhỏ nhất (Edit Distance)
print("Bài 232: Tìm khoảng cách chỉnh sửa nhỏ nhất (Edit Distance)")
def edit_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # Xóa
                                   dp[i][j - 1],      # Thêm
                                   dp[i - 1][j - 1])  # Thay thế
    
    return dp[m][n]

word1 = "kitten"
word2 = "sitting"
print(f"Word 1: {word1}")
print(f"Word 2: {word2}")
print(f"Khoảng cách chỉnh sửa: {edit_distance(word1, word2)}")
print("=" * 50)
print()

# Bài 233: Tìm chuỗi con Palindrome dài nhất
print("Bài 233: Tìm chuỗi con Palindrome dài nhất")
def longest_palindrome_substring(s):
    if not s:
        return ""
    
    n = len(s)
    start, max_length = 0, 1
    
    for i in range(n):
        # Palindrome độ dài lẻ
        left, right = i, i
        while left >= 0 and right < n and s[left] == s[right]:
            if right - left + 1 > max_length:
                start = left
                max_length = right - left + 1
            left -= 1
            right += 1
        
        # Palindrome độ dài chẵn
        left, right = i, i + 1
        while left >= 0 and right < n and s[left] == s[right]:
            if right - left + 1 > max_length:
                start = left
                max_length = right - left + 1
            left -= 1
            right += 1
    
    return s[start:start + max_length]

chuoi = "babad"
print(f"Chuỗi: {chuoi}")
print(f"Chuỗi con Palindrome dài nhất: {longest_palindrome_substring(chuoi)}")
print("=" * 50)
print()

# Bài 234: Tìm số cách đi từ góc trên trái sang góc dưới phải
print("Bài 234: Tìm số cách đi từ góc trên trái sang góc dưới phải")
def unique_paths(m, n):
    dp = [[1] * n for _ in range(m)]
    
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    
    return dp[m - 1][n - 1]

m, n = 3, 7
print(f"Lưới {m}x{n}")
print(f"Số cách đi: {unique_paths(m, n)}")
print("=" * 50)
print()

# Bài 235: Tìm số cách đi với chướng ngại vật
print("Bài 235: Tìm số cách đi với chướng ngại vật")
def unique_paths_with_obstacles(obstacle_grid):
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
print(f"Số cách đi: {unique_paths_with_obstacles(obstacle_grid)}")
print("=" * 50)
print()

# Bài 236: Tìm tổng đường đi lớn nhất
print("Bài 236: Tìm tổng đường đi lớn nhất")
def max_path_sum(triangle):
    n = len(triangle)
    dp = triangle[-1][:]
    
    for i in range(n - 2, -1, -1):
        for j in range(len(triangle[i])):
            dp[j] = triangle[i][j] + max(dp[j], dp[j + 1])
    
    return dp[0]

triangle = [
    [2],
    [3, 4],
    [6, 5, 7],
    [4, 1, 8, 3]
]
print("Tam giác số:", triangle)
print(f"Tổng đường đi lớn nhất: {max_path_sum(triangle)}")
print("=" * 50)
print()

# Bài 237: Tìm số cách chia tiền xu
print("Bài 237: Tìm số cách chia tiền xu")
def coin_change(coins, amount):
    dp = [float('infinity')] * (amount + 1)
    dp[0] = 0
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('infinity') else -1

coins = [1, 2, 5]
amount = 11
print(f"Tiền xu: {coins}")
print(f"Số tiền cần đổi: {amount}")
print(f"Số xu tối thiểu: {coin_change(coins, amount)}")
print("=" * 50)
print()

# Bài 238: Tìm số cách chia tiền xu (tất cả các cách)
print("Bài 238: Tìm số cách chia tiền xu (tất cả các cách)")
def coin_change_ways(coins, amount):
    dp = [0] * (amount + 1)
    dp[0] = 1
    
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]
    
    return dp[amount]

coins = [1, 2, 5]
amount = 5
print(f"Tiền xu: {coins}")
print(f"Số tiền cần đổi: {amount}")
print(f"Số cách đổi: {coin_change_ways(coins, amount)}")
print("=" * 50)
print()

# Bài 239: Bài toán cắt thanh (Rod Cutting)
print("Bài 239: Bài toán cắt thanh (Rod Cutting)")
def rod_cutting(prices, n):
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        max_val = float('-infinity')
        for j in range(1, i + 1):
            max_val = max(max_val, prices[j - 1] + dp[i - j])
        dp[i] = max_val
    
    return dp[n]

prices = [1, 5, 8, 9, 10, 17, 17, 20]
n = 8
print(f"Bảng giá: {prices}")
print(f"Độ dài thanh: {n}")
print(f"Giá trị tối đa: {rod_cutting(prices, n)}")
print("=" * 50)
print()

# Bài 240: Bài toán xâu con palindrome
print("Bài 240: Bài toán xâu con palindrome")
def min_insertions_to_make_palindrome(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    
    for gap in range(1, n):
        for i in range(n - gap):
            j = i + gap
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i + 1][j], dp[i][j - 1])
    
    return dp[0][n - 1]

chuoi = "ab"
print(f"Chuỗi: {chuoi}")
print(f"Số lần chèn tối thiểu: {min_insertions_to_make_palindrome(chuoi)}")
chuoi = "aa"
print(f"Chuỗi: {chuoi}")
print(f"Số lần chèn tối thiểu: {min_insertions_to_make_palindrome(chuoi)}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập nâng cao!")
