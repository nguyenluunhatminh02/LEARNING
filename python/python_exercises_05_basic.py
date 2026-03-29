# Python Exercises 41-50: Basic Level
# Bài tập Python 41-50: Cơ bản

# Bài 41: Tạo danh sách số từ 1 đến 10
print("Bài 41: Tạo danh sách số từ 1 đến 10")
danh_sach = list(range(1, 11))
print(f"Danh sách số từ 1 đến 10: {danh_sach}")
print("=" * 50)
print()

# Bài 42: Tính tổng các phần tử trong danh sách
print("Bài 42: Tính tổng các phần tử trong danh sách")
danh_sach = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
tong = sum(danh_sach)
print(f"Tổng các phần tử: {tong}")
print("=" * 50)
print()

# Bài 43: Tìm giá trị lớn nhất trong danh sách
print("Bài 43: Tìm giá trị lớn nhất trong danh sách")
danh_sach = [12, 45, 23, 67, 34, 89, 12]
max_val = max(danh_sach)
print(f"Giá trị lớn nhất: {max_val}")
print("=" * 50)
print()

# Bài 44: Tìm giá trị nhỏ nhất trong danh sách
print("Bài 44: Tìm giá trị nhỏ nhất trong danh sách")
danh_sach = [12, 45, 23, 67, 34, 89, 12]
min_val = min(danh_sach)
print(f"Giá trị nhỏ nhất: {min_val}")
print("=" * 50)
print()

# Bài 45: Sắp xếp danh sách theo thứ tự tăng dần
print("Bài 45: Sắp xếp danh sách theo thứ tự tăng dần")
danh_sach = [5, 2, 8, 1, 9, 3]
danh_sach.sort()
print(f"Danh sách sau khi sắp xếp: {danh_sach}")
print("=" * 50)
print()

# Bài 46: Sắp xếp danh sách theo thứ tự giảm dần
print("Bài 46: Sắp xếp danh sách theo thứ tự giảm dần")
danh_sach = [5, 2, 8, 1, 9, 3]
danh_sach.sort(reverse=True)
print(f"Danh sách sau khi sắp xếp giảm dần: {danh_sach}")
print("=" * 50)
print()

# Bài 47: Đảo ngược danh sách
print("Bài 47: Đảo ngược danh sách")
danh_sach = [1, 2, 3, 4, 5]
danh_sach.reverse()
print(f"Danh sách sau khi đảo ngược: {danh_sach}")
print("=" * 50)
print()

# Bài 48: Thêm phần tử vào danh sách
print("Bài 48: Thêm phần tử vào danh sách")
danh_sach = [1, 2, 3]
phan_tu = 4
danh_sach.append(phan_tu)
print(f"Danh sách sau khi thêm {phan_tu}: {danh_sach}")
print("=" * 50)
print()

# Bài 49: Xóa phần tử khỏi danh sách
print("Bài 49: Xóa phần tử khỏi danh sách")
danh_sach = [1, 2, 3, 4, 5]
phan_tu = 3
if phan_tu in danh_sach:
    danh_sach.remove(phan_tu)
    print(f"Danh sách sau khi xóa {phan_tu}: {danh_sach}")
else:
    print(f"{phan_tu} không có trong danh sách")
print("=" * 50)
print()

# Bài 50: Đếm số lần xuất hiện của phần tử
print("Bài 50: Đếm số lần xuất hiện của phần tử")
danh_sach = [1, 2, 3, 2, 4, 2, 5]
phan_tu = 2
so_lan = danh_sach.count(phan_tu)
print(f"{phan_tu} xuất hiện {so_lan} lần trong danh sách")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập cơ bản!")
