# Python Exercises 11-20: Basic Level
# Bài tập Python 11-20: Cơ bản

# Bài 11: Nhập dữ liệu từ bàn phím
# print("Bài 11: Nhập dữ liệu từ bàn phím")
# ten = input("Nhập tên của bạn: ")
# print(f"Xin chào, {ten}!")
# print("=" * 50)
# print()

# Bài 12: Nhập số và tính bình phương
print("Bài 12: Nhập số và tính bình phương")
so = float(input("Nhập một số: "))
binh_phuong = so ** 2
print(f"Bình phương của {so} là: {binh_phuong}")
print("=" * 50)
print()

# # Bài 13: Kiểm tra số chẵn hoặc lẻ
# print("Bài 13: Kiểm tra số chẵn hoặc lẻ")
# number = int(input("Nhập một số nguyên: "))
# if number % 2 == 0:
#     print(f"{number} là số chẵn")
# else:
#     print(f"{number} là số lẻ")
# print("=" * 50)
# print()

# # Bài 14: Kiểm tra số dương, âm hoặc bằng 0
# print("Bài 14: Kiểm tra số dương, âm hoặc bằng 0")
# num = float(input("Nhập một số: "))
# if num > 0:
#     print(f"{num} là số dương")
# elif num < 0:
#     print(f"{num} là số âm")
# else:
#     print(f"{num} bằng 0")
# print("=" * 50)
# print()

# # Bài 15: Tìm số lớn nhất trong 2 số
# print("Bài 15: Tìm số lớn nhất trong 2 số")
# a = float(input("Nhập số thứ nhất: "))
# b = float(input("Nhập số thứ hai: "))
# if a > b:
#     print(f"Số lớn nhất là: {a}")
# else:
#     print(f"Số lớn nhất là: {b}")
# print("=" * 50)
# print()

# # Bài 16: Tìm số nhỏ nhất trong 3 số
# print("Bài 16: Tìm số nhỏ nhất trong 3 số")
# x = float(input("Nhập số thứ nhất: "))
# y = float(input("Nhập số thứ hai: "))
# z = float(input("Nhập số thứ ba: "))
# min_num = min(x, y, z)
# print(f"Số nhỏ nhất là: {min_num}")
# print("=" * 50)
# print()

# # Bài 17: Kiểm tra năm nhuận
# print("Bài 17: Kiểm tra năm nhuận")
# nam = int(input("Nhập năm: "))
# if (nam % 4 == 0 and nam % 100 != 0) or (nam % 400 == 0):
#     print(f"{nam} là năm nhuận")
# else:
#     print(f"{nam} không phải là năm nhuận")
# print("=" * 50)
# print()

# # Bài 18: Tính diện tích hình chữ nhật
# print("Bài 18: Tính diện tích hình chữ nhật")
# dai = float(input("Nhập chiều dài: "))
# rong = float(input("Nhập chiều rộng: "))
# dien_tich = dai * rong
# print(f"Diện tích hình chữ nhật là: {dien_tich}")
# print("=" * 50)
# print()

# # Bài 19: Tính chu vi hình chữ nhật
# print("Bài 19: Tính chu vi hình chữ nhật")
# dai = float(input("Nhập chiều dài: "))
# rong = float(input("Nhập chiều rộng: "))
# chu_vi = 2 * (dai + rong)
# print(f"Chu vi hình chữ nhật là: {chu_vi}")
# print("=" * 50)
# print()

# # Bài 20: Tính diện tích hình tròn
# print("Bài 20: Tính diện tích hình tròn")
# import math
# ban_kinh = float(input("Nhập bán kính hình tròn: "))
# dien_tich = math.pi * ban_kinh ** 2
# print(f"Diện tích hình tròn là: {dien_tich:.2f}")
# print("=" * 50)
# print()

# print("Đã hoàn thành 10 bài tập cơ bản!")
