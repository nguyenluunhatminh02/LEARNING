# Python Exercises 261-270: Advanced Level
# Bài tập Python 261-270: Nâng cao

# Bài 261: Tìm số Catalan thứ n
print("Bài 261: Tìm số Catalan thứ n")
def catalan_number(n):
    if n <= 1:
        return 1
    
    catalan = [0] * (n + 1)
    catalan[0] = 1
    catalan[1] = 1
    
    for i in range(2, n + 1):
        catalan[i] = 0
        for j in range(i):
            catalan[i] += catalan[j] * catalan[i - j - 1]
    
    return catalan[n]

n = 5
print(f"Số Catalan thứ {n}: {catalan_number(n)}")
print(f"10 số Catalan đầu tiên: {[catalan_number(i) for i in range(10)]}")
print("=" * 50)
print()

# Bài 262: Tìm số Stirling thứ hai
print("Bài 262: Tìm số Stirling thứ hai")
def stirling_number_second(n, k):
    if n == k == 0:
        return 1
    if n == 0 or k == 0:
        return 0
    if n == k:
        return 1
    if k > n:
        return 0
    
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            dp[i][j] = j * dp[i - 1][j] + dp[i - 1][j - 1]
    
    return dp[n][k]

n, k = 5, 3
print(f"Số Stirling thứ hai S({n}, {k}): {stirling_number_second(n, k)}")
print("=" * 50)
print()

# Bài 263: Tìm số Bell
print("Bài 263: Tìm số Bell")
def bell_number(n):
    bell = [[0] * (n + 1) for _ in range(n + 1)]
    bell[0][0] = 1
    
    for i in range(1, n + 1):
        bell[i][0] = bell[i - 1][i - 1]
        for j in range(1, i + 1):
            bell[i][j] = bell[i - 1][j - 1] + bell[i][j - 1]
    
    return bell[n][0]

n = 5
print(f"Số Bell thứ {n}: {bell_number(n)}")
print(f"10 số Bell đầu tiên: {[bell_number(i) for i in range(10)]}")
print("=" * 50)
print()

# Bài 264: Tìm số Bernoulli
print("Bài 264: Tìm số Bernoulli")
def bernoulli_number(n):
    if n == 0:
        return 1
    if n % 2 != 0:
        return 0
    
    B = [0] * (n + 1)
    B[0] = 1
    
    for m in range(1, n + 1):
        B[m] = 0
        for j in range(m):
            B[m] -= B[j] * (m + 1) // (m + 1 - j)
    
    return B[n]

for n in range(11):
    print(f"B({n}) = {bernoulli_number(n)}")
print("=" * 50)
print()

# Bài 265: Tìm số Euler
print("Bài 265: Tìm số Euler")
def euler_number(n):
    if n == 0:
        return 1
    
    E = [[0] * (n + 1) for _ in range(n + 1)]
    E[0][0] = 1
    
    for i in range(1, n + 1):
        for j in range(i + 1):
            E[i][j] = (i - j) * E[i - 1][j - 1] + (j + 1) * E[i - 1][j]
    
    return E[n][0]

for n in range(10):
    print(f"E({n}) = {euler_number(n)}")
print("=" * 50)
print()

# Bài 266: Tìm số Fibonacci bằng công thức Binet
print("Bài 266: Tìm số Fibonacci bằng công thức Binet")
import math

def fibonacci_binet(n):
    sqrt_5 = math.sqrt(5)
    phi = (1 + sqrt_5) / 2
    psi = (1 - sqrt_5) / 2
    return int((phi ** n - psi ** n) / sqrt_5)

n = 10
print(f"Số Fibonacci thứ {n}: {fibonacci_binet(n)}")
print(f"10 số Fibonacci đầu tiên: {[fibonacci_binet(i) for i in range(1, 11)]}")
print("=" * 50)
print()

# Bài 267: Tìm số Lucas
print("Bài 267: Tìm số Lucas")
def lucas_number(n):
    if n == 0:
        return 2
    if n == 1:
        return 1
    
    a, b = 2, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b

n = 10
print(f"Số Lucas thứ {n}: {lucas_number(n)}")
print(f"10 số Lucas đầu tiên: {[lucas_number(i) for i in range(10)]}")
print("=" * 50)
print()

# Bài 268: Tìm số Pell
print("Bài 268: Tìm số Pell")
def pell_number(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, 2 * b + a
    
    return b

n = 10
print(f"Số Pell thứ {n}: {pell_number(n)}")
print(f"10 số Pell đầu tiên: {[pell_number(i) for i in range(10)]}")
print("=" * 50)
print()

# Bài 269: Tìm số Jacobsthal
print("Bài 269: Tìm số Jacobsthal")
def jacobsthal_number(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + 2 * b
    
    return b

n = 10
print(f"Số Jacobsthal thứ {n}: {jacobsthal_number(n)}")
print(f"10 số Jacobsthal đầu tiên: {[jacobsthal_number(i) for i in range(10)]}")
print("=" * 50)
print()

# Bài 270: Tìm số Padovan
print("Bài 270: Tìm số Padovan")
def padovan_number(n):
    if n == 0 or n == 1 or n == 2:
        return 1
    
    P = [1, 1, 1]
    for i in range(3, n + 1):
        P.append(P[i - 2] + P[i - 3])
    
    return P[n]

n = 10
print(f"Số Padovan thứ {n}: {padovan_number(n)}")
print(f"10 số Padovan đầu tiên: {[padovan_number(i) for i in range(10)]}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập nâng cao!")
