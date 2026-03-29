# Python Exercises 81-90: Basic Level
# Bài tập Python 81-90: Cơ bản

# Bài 81: Định nghĩa hàm đơn giản
print("Bài 81: Định nghĩa hàm đơn giản")
def chao():
    print("Xin chào!")

chao()
print("=" * 50)
print()

# Bài 82: Hàm có tham số
print("Bài 82: Hàm có tham số")
def chao_ten(ten):
    print(f"Xin chào, {ten}!")

chao_ten("Nam")
chao_ten("Lan")
print("=" * 50)
print()

# Bài 83: Hàm có giá trị trả về
print("Bài 83: Hàm có giá trị trả về")
def tinh_tong(a, b):
    return a + b

ket_qua = tinh_tong(5, 3)
print(f"5 + 3 = {ket_qua}")
print("=" * 50)
print()

# Bài 84: Hàm tính bình phương
print("Bài 84: Hàm tính bình phương")
def binh_phuong(x):
    return x ** 2

so = 4
print(f"Bình phương của {so} là: {binh_phuong(so)}")
print("=" * 50)
print()

# Bài 85: Hàm kiểm tra số chẵn
print("Bài 85: Hàm kiểm tra số chẵn")
def la_so_chan(n):
    return n % 2 == 0

print(f"4 là số chẵn: {la_so_chan(4)}")
print(f"7 là số chẵn: {la_so_chan(7)}")
print("=" * 50)
print()

# Bài 86: Hàm tìm max của 2 số
print("Bài 86: Hàm tìm max của 2 số")
def tim_max(a, b):
    if a > b:
        return a
    else:
        return b

print(f"Max của 10 và 20 là: {tim_max(10, 20)}")
print(f"Max của 30 và 15 là: {tim_max(30, 15)}")
print("=" * 50)
print()

# Bài 87: Hàm tính giai thừa
print("Bài 87: Hàm tính giai thừa")
def giai_thua(n):
    if n == 0 or n == 1:
        return 1
    ket_qua = 1
    for i in range(2, n + 1):
        ket_qua *= i
    return ket_qua

n = 5
print(f"{n}! = {giai_thua(n)}")
print("=" * 50)
print()

# Bài 88: Hàm kiểm tra số nguyên tố
print("Bài 88: Hàm kiểm tra số nguyên tố")
def la_nguyen_to(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

print(f"7 là số nguyên tố: {la_nguyen_to(7)}")
print(f"10 là số nguyên tố: {la_nguyen_to(10)}")
print("=" * 50)
print()

# Bài 89: Hàm có tham số mặc định
print("Bài 89: Hàm có tham số mặc định")
def tinh_luong(luong_co_ban, thuong=0):
    return luong_co_ban + thuong

print(f"Lương cơ bản 5000, thưởng 1000: {tinh_luong(5000, 1000)}")
print(f"Lương cơ bản 5000, không thưởng: {tinh_luong(5000)}")
print("=" * 50)
print()

# Bài 90: Hàm với số lượng tham số biến đổi
print("Bài 90: Hàm với số lượng tham số biến đổi")
def tinh_tong_bat_ki(*args):
    return sum(args)

print(f"Tổng 1, 2, 3: {tinh_tong_bat_ki(1, 2, 3)}")
print(f"Tổng 10, 20, 30, 40: {tinh_tong_bat_ki(10, 20, 30, 40)}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập cơ bản!")
