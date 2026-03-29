# Python Exercises 31-40: Basic Level
# Bài tập Python 31-40: Cơ bản

# Bài 31: Đảo ngược chuỗi
print("Bài 31: Đảo ngược chuỗi")
chuoi = input("Nhập một chuỗi: ")
chuoi_dao = chuoi[::-1]
print(f"Chuỗi đảo ngược: {chuoi_dao}")
print("=" * 50)
print()

# Bài 32: Đếm số ký tự trong chuỗi
print("Bài 32: Đếm số ký tự trong chuỗi")
chuoi = input("Nhập một chuỗi: ")
so_ky_tu = len(chuoi)
print(f"Số ký tự trong chuỗi: {so_ky_tu}")
print("=" * 50)
print()

# Bài 33: Chuyển đổi chuỗi sang chữ hoa
print("Bài 33: Chuyển đổi chuỗi sang chữ hoa")
chuoi = input("Nhập một chuỗi: ")
chuoi_hoa = chuoi.upper()
print(f"Chuỗi chữ hoa: {chuoi_hoa}")
print("=" * 50)
print()

# Bài 34: Chuyển đổi chuỗi sang chữ thường
print("Bài 34: Chuyển đổi chuỗi sang chữ thường")
chuoi = input("Nhập một chuỗi: ")
chuoi_thuong = chuoi.lower()
print(f"Chuỗi chữ thường: {chuoi_thuong}")
print("=" * 50)
print()

# Bài 35: Kiểm tra chuỗi có chứa khoảng trắng không
print("Bài 35: Kiểm tra chuỗi có chứa khoảng trắng không")
chuoi = input("Nhập một chuỗi: ")
if ' ' in chuoi:
    print("Chuỗi có chứa khoảng trắng")
else:
    print("Chuỗi không chứa khoảng trắng")
print("=" * 50)
print()

# Bài 36: Loại bỏ khoảng trắng ở đầu và cuối chuỗi
print("Bài 36: Loại bỏ khoảng trắng ở đầu và cuối chuỗi")
chuoi = input("Nhập một chuỗi (có thể có khoảng trắng đầu/cuối): ")
chuoi_da_xu_ly = chuoi.strip()
print(f"Chuỗi sau khi loại bỏ khoảng trắng: '{chuoi_da_xu_ly}'")
print("=" * 50)
print()

# Bài 37: Tìm vị trí của ký tự trong chuỗi
print("Bài 37: Tìm vị trí của ký tự trong chuỗi")
chuoi = input("Nhập một chuỗi: ")
ky_tu = input("Nhập ký tự cần tìm: ")
vi_tri = chuoi.find(ky_tu)
if vi_tri != -1:
    print(f"Ký tự '{ky_tu}' xuất hiện đầu tiên tại vị trí: {vi_tri}")
else:
    print(f"Ký tự '{ky_tu}' không có trong chuỗi")
print("=" * 50)
print()

# Bài 38: Thay thế ký tự trong chuỗi
print("Bài 38: Thay thế ký tự trong chuỗi")
chuoi = input("Nhập một chuỗi: ")
ky_tu_cu = input("Nhập ký tự cần thay thế: ")
ky_tu_moi = input("Nhập ký tự mới: ")
chuoi_moi = chuoi.replace(ky_tu_cu, ky_tu_moi)
print(f"Chuỗi sau khi thay thế: {chuoi_moi}")
print("=" * 50)
print()

# Bài 39: Kiểm tra chuỗi có phải là số không
print("Bài 39: Kiểm tra chuỗi có phải là số không")
chuoi = input("Nhập một chuỗi: ")
if chuoi.isdigit():
    print("Chuỗi là một số")
else:
    print("Chuỗi không phải là số")
print("=" * 50)
print()

# Bài 40: Tách chuỗi thành danh sách
print("Bài 40: Tách chuỗi thành danh sách")
chuoi = input("Nhập một chuỗi các từ: ")
danh_sach = chuoi.split()
print(f"Danh sách các từ: {danh_sach}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập cơ bản!")
