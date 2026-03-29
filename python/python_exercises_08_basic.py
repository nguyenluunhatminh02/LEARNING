# Python Exercises 71-80: Basic Level
# Bài tập Python 71-80: Cơ bản

# Bài 71: Tạo set chứa các số không trùng nhau
print("Bài 71: Tạo set chứa các số không trùng nhau")
set_so = {1, 2, 3, 4, 5, 5, 4, 3, 2, 1}
print(f"Set (không có phần tử trùng): {set_so}")
print("=" * 50)
print()

# Bài 72: Thêm phần tử vào set
print("Bài 72: Thêm phần tử vào set")
set_so = {1, 2, 3}
set_so.add(4)
set_so.add(5)
print(f"Set sau khi thêm phần tử: {set_so}")
print("=" * 50)
print()

# Bài 73: Xóa phần tử khỏi set
print("Bài 73: Xóa phần tử khỏi set")
set_so = {1, 2, 3, 4, 5}
set_so.discard(3)
set_so.remove(2)
print(f"Set sau khi xóa phần tử: {set_so}")
print("=" * 50)
print()

# Bài 74: Kiểm tra phần tử trong set
print("Bài 74: Kiểm tra phần tử trong set")
set_so = {1, 2, 3, 4, 5}
phan_tu = 3
if phan_tu in set_so:
    print(f"{phan_tu} có trong set")
else:
    print(f"{phan_tu} không có trong set")
print("=" * 50)
print()

# Bài 75: Tính giao của hai set
print("Bài 75: Tính giao của hai set")
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}
giao = set1 & set2
print(f"Giao của hai set: {giao}")
print("=" * 50)
print()

# Bài 76: Tính hợp của hai set
print("Bài 76: Tính hợp của hai set")
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}
hop = set1 | set2
print(f"Hợp của hai set: {hop}")
print("=" * 50)
print()

# Bài 77: Tính hiệu của hai set
print("Bài 77: Tính hiệu của hai set")
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}
hieu = set1 - set2
print(f"Hieu set1 - set2: {hieu}")
print("=" * 50)
print()

# Bài 78: Tính độ dài của set
print("Bài 78: Tính độ dài của set")
set_so = {1, 2, 3, 4, 5}
do_dai = len(set_so)
print(f"Độ dài của set: {do_dai}")
print("=" * 50)
print()

# Bài 79: Chuyển list sang set để loại bỏ trùng
print("Bài 79: Chuyển list sang set để loại bỏ trùng")
list_so = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
set_so = set(list_so)
print(f"List ban đầu: {list_so}")
print(f"Set sau khi chuyển: {set_so}")
print("=" * 50)
print()

# Bài 80: Kiểm tra hai set có bằng nhau không
print("Bài 80: Kiểm tra hai set có bằng nhau không")
set1 = {1, 2, 3, 4, 5}
set2 = {5, 4, 3, 2, 1}
set3 = {1, 2, 3, 4}
if set1 == set2:
    print("set1 và set2 bằng nhau")
else:
    print("set1 và set2 không bằng nhau")
if set1 == set3:
    print("set1 và set3 bằng nhau")
else:
    print("set1 và set3 không bằng nhau")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập cơ bản!")
