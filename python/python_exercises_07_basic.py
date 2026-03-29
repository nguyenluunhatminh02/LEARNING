# Python Exercises 61-70: Basic Level
# Bài tập Python 61-70: Cơ bản

# Bài 61: In hình vuông bằng dấu *
print("Bài 61: In hình vuông bằng dấu *")
n = int(input("Nhập kích thước hình vuông: "))
for i in range(n):
    print("*" * n)
print("=" * 50)
print()

# Bài 62: In hình chữ nhật bằng dấu *
print("Bài 62: In hình chữ nhật bằng dấu *")
dai = int(input("Nhập chiều dài: "))
rong = int(input("Nhập chiều rộng: "))
for i in range(rong):
    print("*" * dai)
print("=" * 50)
print()

# Bài 63: In tam giác vuông phải bằng dấu *
print("Bài 63: In tam giác vuông phải bằng dấu *")
n = int(input("Nhập chiều cao tam giác: "))
for i in range(1, n + 1):
    print("*" * i)
print("=" * 50)
print()

# Bài 64: In tam giác vuông trái bằng dấu *
print("Bài 64: In tam giác vuông trái bằng dấu *")
n = int(input("Nhập chiều cao tam giác: "))
for i in range(1, n + 1):
    print(" " * (n - i) + "*" * i)
print("=" * 50)
print()

# Bài 65: Tạo tuple chứa các số từ 1 đến 5
print("Bài 65: Tạo tuple chứa các số từ 1 đến 5")
tuple_so = tuple(range(1, 6))
print(f"Tuple số: {tuple_so}")
print("=" * 50)
print()

# Bài 66: Truy cập phần tử trong tuple
print("Bài 66: Truy cập phần tử trong tuple")
tuple_so = (10, 20, 30, 40, 50)
print(f"Tuple: {tuple_so}")
print(f"Phần tử đầu tiên: {tuple_so[0]}")
print(f"Phần tử cuối cùng: {tuple_so[-1]}")
print(f"Phần tử thứ 3: {tuple_so[2]}")
print("=" * 50)
print()

# Bài 67: Tạo dictionary đơn giản
print("Bài 67: Tạo dictionary đơn giản")
sinh_vien = {
    "ten": "Nguyen Van A",
    "tuoi": 20,
    "lop": "CNTT-K15"
}
print(f"Thông tin sinh viên: {sinh_vien}")
print(f"Tên: {sinh_vien['ten']}")
print(f"Tuổi: {sinh_vien['tuoi']}")
print("=" * 50)
print()

# Bài 68: Thêm phần tử vào dictionary
print("Bài 68: Thêm phần tử vào dictionary")
sinh_vien = {
    "ten": "Nguyen Van A",
    "tuoi": 20
}
sinh_vien["lop"] = "CNTT-K15"
sinh_vien["diem"] = 8.5
print(f"Dictionary sau khi thêm: {sinh_vien}")
print("=" * 50)
print()

# Bài 69: Xóa phần tử khỏi dictionary
print("Bài 69: Xóa phần tử khỏi dictionary")
sinh_vien = {
    "ten": "Nguyen Van A",
    "tuoi": 20,
    "lop": "CNTT-K15",
    "diem": 8.5
}
khoa = sinh_vien.pop("lop", None)
print(f"Dictionary sau khi xóa 'lop': {sinh_vien}")
print("=" * 50)
print()

# Bài 70: Kiểm tra khóa trong dictionary
print("Bài 70: Kiểm tra khóa trong dictionary")
sinh_vien = {
    "ten": "Nguyen Van A",
    "tuoi": 20,
    "lop": "CNTT-K15"
}
khoa = "tuoi"
if khoa in sinh_vien:
    print(f"Khóa '{khoa}' có trong dictionary với giá trị: {sinh_vien[khoa]}")
else:
    print(f"Khóa '{khoa}' không có trong dictionary")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập cơ bản!")
