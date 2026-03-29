# Python Exercises 51-60: Basic Level
# Bài tập Python 51-60: Cơ bản

# Bài 51: In các số từ 1 đến 10 sử dụng vòng lặp for
print("Bài 51: In các số từ 1 đến 10 sử dụng vòng lặp for")
for i in range(1, 11):
    print(i, end=" ")
print("\n" + "=" * 50)
print()

# Bài 52: In các số từ 10 đến 1 sử dụng vòng lặp for
print("Bài 52: In các số từ 10 đến 1 sử dụng vòng lặp for")
for i in range(10, 0, -1):
    print(i, end=" ")
print("\n" + "=" * 50)
print()

# Bài 53: Tính tổng các số từ 1 đến n
print("Bài 53: Tính tổng các số từ 1 đến n")
n = int(input("Nhập số n: "))
tong = 0
for i in range(1, n + 1):
    tong += i
print(f"Tổng các số từ 1 đến {n} là: {tong}")
print("=" * 50)
print()

# Bài 54: Tính tổng các số chẵn từ 1 đến n
print("Bài 54: Tính tổng các số chẵn từ 1 đến n")
n = int(input("Nhập số n: "))
tong_chan = 0
for i in range(2, n + 1, 2):
    tong_chan += i
print(f"Tổng các số chẵn từ 1 đến {n} là: {tong_chan}")
print("=" * 50)
print()

# Bài 55: Tính tổng các số lẻ từ 1 đến n
print("Bài 55: Tính tổng các số lẻ từ 1 đến n")
n = int(input("Nhập số n: "))
tong_le = 0
for i in range(1, n + 1, 2):
    tong_le += i
print(f"Tổng các số lẻ từ 1 đến {n} là: {tong_le}")
print("=" * 50)
print()

# Bài 56: In bảng cửu chương của một số
print("Bài 56: In bảng cửu chương của một số")
so = int(input("Nhập một số: "))
print(f"Bảng cửu chương của {so}:")
for i in range(1, 11):
    print(f"{so} x {i} = {so * i}")
print("=" * 50)
print()

# Bài 57: Đếm số chữ số của một số nguyên
print("Bài 57: Đếm số chữ số của một số nguyên")
so = int(input("Nhập một số nguyên: "))
so_chu_so = len(str(abs(so)))
print(f"Số {so} có {so_chu_so} chữ số")
print("=" * 50)
print()

# Bài 58: Tính tổng các chữ số của một số
print("Bài 58: Tính tổng các chữ số của một số")
so = int(input("Nhập một số nguyên: "))
tong_chu_so = sum(int(digit) for digit in str(abs(so)))
print(f"Tổng các chữ số của {so} là: {tong_chu_so}")
print("=" * 50)
print()

# Bài 59: Kiểm tra số nguyên tố
print("Bài 59: Kiểm tra số nguyên tố")
n = int(input("Nhập một số: "))
if n > 1:
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            print(f"{n} không phải là số nguyên tố")
            break
    else:
        print(f"{n} là số nguyên tố")
else:
    print(f"{n} không phải là số nguyên tố")
print("=" * 50)
print()

# Bài 60: In các số nguyên tố nhỏ hơn n
print("Bài 60: In các số nguyên tố nhỏ hơn n")
n = int(input("Nhập số n: "))
print(f"Các số nguyên tố nhỏ hơn {n}:")
for num in range(2, n):
    is_prime = True
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            is_prime = False
            break
    if is_prime:
        print(num, end=" ")
print("\n" + "=" * 50)
print()

print("Đã hoàn thành 10 bài tập cơ bản!")
