# Python Exercises 161-170: Intermediate Level
# Bài tập Python 161-170: Trung cấp

# Bài 161: Tìm số nguyên tố trong khoảng
print("Bài 161: Tìm số nguyên tố trong khoảng")
def tim_so_nguyen_to_trong_khoang(start, end):
    ket_qua = []
    for num in range(start, end + 1):
        if num > 1:
            is_prime = True
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0:
                    is_prime = False
                    break
            if is_prime:
                ket_qua.append(num)
    return ket_qua

start, end = 10, 50
print(f"Các số nguyên tố từ {start} đến {end}: {tim_so_nguyen_to_trong_khoang(start, end)}")
print("=" * 50)
print()

# Bài 162: Tìm các số hoàn hảo trong khoảng
print("Bài 162: Tìm các số hoàn hảo trong khoảng")
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

def tim_so_hoan_hao_trong_khoang(start, end):
    return [num for num in range(start, end + 1) if la_so_hoan_hao(num)]

start, end = 1, 10000
print(f"Các số hoàn hảo từ {start} đến {end}: {tim_so_hoan_hao_trong_khoang(start, end)}")
print("=" * 50)
print()

# Bài 163: Tìm các số Armstrong trong khoảng
print("Bài 163: Tìm các số Armstrong trong khoảng")
def la_so_armstrong(n):
    chuoi = str(n)
    so_chu_so = len(chuoi)
    tong = sum(int(digit) ** so_chu_so for digit in chuoi)
    return tong == n

def tim_so_armstrong_trong_khoang(start, end):
    return [num for num in range(start, end + 1) if la_so_armstrong(num)]

start, end = 100, 1000
print(f"Các số Armstrong từ {start} đến {end}: {tim_so_armstrong_trong_khoang(start, end)}")
print("=" * 50)
print()

# Bài 164: Tìm các số Fibonacci trong khoảng
print("Bài 164: Tìm các số Fibonacci trong khoảng")
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def tim_fibonacci_trong_khoang(start, end):
    ket_qua = []
    i = 1
    while True:
        fib = fibonacci(i)
        if fib > end:
            break
        if fib >= start:
            ket_qua.append(fib)
        i += 1
    return ket_qua

start, end = 10, 100
print(f"Các số Fibonacci từ {start} đến {end}: {tim_fibonacci_trong_khoang(start, end)}")
print("=" * 50)
print()

# Bài 165: Tìm các số Palindrome trong khoảng
print("Bài 165: Tìm các số Palindrome trong khoảng")
def la_so_palindrome(n):
    return str(n) == str(n)[::-1]

def tim_palindrome_trong_khoang(start, end):
    return [num for num in range(start, end + 1) if la_so_palindrome(num)]

start, end = 100, 200
print(f"Các số Palindrome từ {start} đến {end}: {tim_palindrome_trong_khoang(start, end)}")
print("=" * 50)
print()

# Bài 166: Tìm UCLN của nhiều số
print("Bài 166: Tìm UCLN của nhiều số")
def ucln(a, b):
    while b:
        a, b = b, a % b
    return a

def ucln_nhieu_so(lst):
    if not lst:
        return 0
    ket_qua = lst[0]
    for num in lst[1:]:
        ket_qua = ucln(ket_qua, num)
    return ket_qua

danh_sach = [24, 36, 48, 60]
print(f"Danh sách: {danh_sach}")
print(f"UCLN của các số: {ucln_nhieu_so(danh_sach)}")
print("=" * 50)
print()

# Bài 167: Tìm BCNN của nhiều số
print("Bài 167: Tìm BCNN của nhiều số")
def bcnn(a, b):
    return abs(a * b) // ucln(a, b)

def bcnn_nhieu_so(lst):
    if not lst:
        return 0
    ket_qua = lst[0]
    for num in lst[1:]:
        ket_qua = bcnn(ket_qua, num)
    return ket_qua

danh_sach = [4, 6, 8]
print(f"Danh sách: {danh_sach}")
print(f"BCNN của các số: {bcnn_nhieu_so(danh_sach)}")
print("=" * 50)
print()

# Bài 168: Kiểm tra số có phải là lũy thừa của 2
print("Bài 168: Kiểm tra số có phải là lũy thừa của 2")
def la_luy_thua_cua_2(n):
    return n > 0 and (n & (n - 1)) == 0

for so in [1, 2, 4, 8, 16, 32, 3, 5, 6, 7]:
    print(f"{so} là lũy thừa của 2: {la_luy_thua_cua_2(so)}")
print("=" * 50)
print()

# Bài 169: Tìm lũy thừa gần nhất của 2
print("Bài 169: Tìm lũy thừa gần nhất của 2")
def luy_thua_gan_nhat_cua_2(n):
    if n <= 1:
        return 1
    lower = 1
    while lower * 2 < n:
        lower *= 2
    upper = lower * 2
    return lower if n - lower <= upper - n else upper

for so in [10, 15, 20, 25, 30]:
    print(f"Lũy thừa của 2 gần nhất với {so}: {luy_thua_gan_nhat_cua_2(so)}")
print("=" * 50)
print()

# Bài 170: Tìm các ước số của một số
print("Bài 170: Tìm các ước số của một số")
def tim_uoc_so(n):
    uoc_so = []
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            uoc_so.append(i)
            if i != n // i:
                uoc_so.append(n // i)
    return sorted(uoc_so)

so = 36
print(f"Các ước số của {so}: {tim_uoc_so(so)}")
so = 100
print(f"Các ước số của {so}: {tim_uoc_so(so)}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập trung cấp!")
