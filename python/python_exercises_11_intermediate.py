# Python Exercises 101-110: Intermediate Level
# Bài tập Python 101-110: Trung cấp

# Bài 101: Tìm số Fibonacci thứ n
print("Bài 101: Tìm số Fibonacci thứ n")
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

n = 10
print(f"Số Fibonacci thứ {n} là: {fibonacci(n)}")
print(f"10 số Fibonacci đầu tiên: {[fibonacci(i) for i in range(1, 11)]}")
print("=" * 50)
print()

# Bài 102: Kiểm tra số Fibonacci
print("Bài 102: Kiểm tra số Fibonacci")
def la_so_fibonacci(num):
    if num < 0:
        return False
    a, b = 0, 1
    while b < num:
        a, b = b, a + b
    return b == num

so = 21
print(f"{so} là số Fibonacci: {la_so_fibonacci(so)}")
so = 20
print(f"{so} là số Fibonacci: {la_so_fibonacci(so)}")
print("=" * 50)
print()

# Bài 103: Tính UCLN của hai số
print("Bài 103: Tính UCLN của hai số")
def ucln(a, b):
    while b:
        a, b = b, a % b
    return a

a, b = 48, 18
print(f"UCLN của {a} và {b} là: {ucln(a, b)}")
print("=" * 50)
print()

# Bài 104: Tính BCNN của hai số
print("Bài 104: Tính BCNN của hai số")
def bcnn(a, b):
    return abs(a * b) // ucln(a, b)

a, b = 12, 15
print(f"BCNN của {a} và {b} là: {bcnn(a, b)}")
print("=" * 50)
print()

# Bài 105: Kiểm tra số hoàn hảo
print("Bài 105: Kiểm tra số hoàn hảo")
def la_so_hoan_hao(n):
    if n <= 1:
        return False
    tong = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            tong += i
            if i != n // i:
                tong += n // i
    return tong == n

for so in [6, 28, 496]:
    print(f"{so} là số hoàn hảo: {la_so_hoan_hao(so)}")
print("=" * 50)
print()

# Bài 106: Tìm các số hoàn hảo nhỏ hơn n
print("Bài 106: Tìm các số hoàn hảo nhỏ hơn n")
n = 1000
print(f"Các số hoàn hảo nhỏ hơn {n}:")
for i in range(2, n):
    if la_so_hoan_hao(i):
        print(i, end=" ")
print("\n" + "=" * 50)
print()

# Bài 107: Kiểm tra số Armstrong
print("Bài 107: Kiểm tra số Armstrong")
def la_so_armstrong(n):
    chuoi = str(n)
    so_chu_so = len(chuoi)
    tong = sum(int(digit) ** so_chu_so for digit in chuoi)
    return tong == n

for so in [153, 370, 371, 407, 123]:
    print(f"{so} là số Armstrong: {la_so_armstrong(so)}")
print("=" * 50)
print()

# Bài 108: Tìm các số Armstrong trong khoảng
print("Bài 108: Tìm các số Armstrong trong khoảng")
bat_dau, ket_thuc = 100, 1000
print(f"Các số Armstrong từ {bat_dau} đến {ket_thuc}:")
for i in range(bat_dau, ket_thuc):
    if la_so_armstrong(i):
        print(i, end=" ")
print("\n" + "=" * 50)
print()

# Bài 109: Đảo ngược số
print("Bài 109: Đảo ngược số")
def dao_nguoc_so(n):
    return int(str(abs(n))[::-1]) * (1 if n >= 0 else -1)

so = 12345
print(f"Đảo ngược của {so} là: {dao_nguoc_so(so)}")
so = -6789
print(f"Đảo ngược của {so} là: {dao_nguoc_so(so)}")
print("=" * 50)
print()

# Bài 110: Kiểm tra số Palindrome
print("Bài 110: Kiểm tra số Palindrome")
def la_so_palindrome(n):
    return str(n) == str(n)[::-1]

for so in [121, 12321, 123, 45654]:
    print(f"{so} là số Palindrome: {la_so_palindrome(so)}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập trung cấp!")
