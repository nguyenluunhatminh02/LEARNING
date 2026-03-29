# Python Exercises 21-30: Basic Level
# Bài tập Python 21-30: Cơ bản

# Bài 21: Tính chu vi hình tròn
print("Bài 21: Tính chu vi hình tròn")
import math
ban_kinh = float(input("Nhập bán kính hình tròn: "))
chu_vi = 2 * math.pi * ban_kinh
print(f"Chu vi hình tròn là: {chu_vi:.2f}")
print("=" * 50)
print()

# Bài 22: Tính diện tích tam giác
print("Bài 22: Tính diện tích tam giác")
day = float(input("Nhập độ dài đáy: "))
cao = float(input("Nhập chiều cao: "))
dien_tich = 0.5 * day * cao
print(f"Diện tích tam giác là: {dien_tich}")
print("=" * 50)
print()

# Bài 23: Tính thể tích hình lập phương
print("Bài 23: Tính thể tích hình lập phương")
canh = float(input("Nhập độ dài cạnh: "))
the_tich = canh ** 3
print(f"Thể tích hình lập phương là: {the_tich}")
print("=" * 50)
print()

# Bài 24: Tính thể tích hình hộp chữ nhật
print("Bài 24: Tính thể tích hình hộp chữ nhật")
dai = float(input("Nhập chiều dài: "))
rong = float(input("Nhập chiều rộng: "))
cao = float(input("Nhập chiều cao: "))
the_tich = dai * rong * cao
print(f"Thể tích hình hộp chữ nhật là: {the_tich}")
print("=" * 50)
print()

# Bài 25: Chuyển đổi km sang m
print("Bài 25: Chuyển đổi km sang m")
km = float(input("Nhập số km: "))
m = km * 1000
print(f"{km} km = {m} m")
print("=" * 50)
print()

# Bài 26: Chuyển đổi m sang cm
print("Bài 26: Chuyển đổi m sang cm")
m = float(input("Nhập số m: "))
cm = m * 100
print(f"{m} m = {cm} cm")
print("=" * 50)
print()

# Bài 27: Chuyển đổi kg sang g
print("Bài 27: Chuyển đổi kg sang g")
kg = float(input("Nhập số kg: "))
g = kg * 1000
print(f"{kg} kg = {g} g")
print("=" * 50)
print()

# Bài 28: Tính giá trị tuyệt đối
print("Bài 28: Tính giá trị tuyệt đối")
so = float(input("Nhập một số: "))
gia_tri_tuyet_doi = abs(so)
print(f"Giá trị tuyệt đối của {so} là: {gia_tri_tuyet_doi}")
print("=" * 50)
print()

# Bài 29: Làm tròn số
print("Bài 29: Làm tròn số")
so = float(input("Nhập một số thập phân: "))
so_lam_tron = round(so, 2)
print(f"Số sau khi làm tròn 2 chữ số: {so_lam_tron}")
print("=" * 50)
print()

# Bài 30: Tính giai thừa của một số
print("Bài 30: Tính giai thừa của một số")
n = int(input("Nhập một số nguyên dương: "))
giai_thua = 1
for i in range(1, n + 1):
    giai_thua *= i
print(f"{n}! = {giai_thua}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập cơ bản!")
