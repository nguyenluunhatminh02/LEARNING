# Python Exercises 91-100: Basic Level
# Bài tập Python 91-100: Cơ bản

# Bài 91: Đọc file văn bản
print("Bài 91: Đọc file văn bản")
try:
    with open("test_file.txt", "w", encoding="utf-8") as f:
        f.write("Đây là file test\nDòng thứ hai")
    with open("test_file.txt", "r", encoding="utf-8") as f:
        noi_dung = f.read()
        print(f"Nội dung file:\n{noi_dung}")
except Exception as e:
    print(f"Có lỗi xảy ra: {e}")
print("=" * 50)
print()

# Bài 92: Ghi file văn bản
print("Bài 92: Ghi file văn bản")
try:
    with open("ghi_file.txt", "w", encoding="utf-8") as f:
        f.write("Xin chào Python!\n")
        f.write("Đây là dòng thứ hai\n")
        f.write("Đây là dòng thứ ba")
    print("Đã ghi file thành công!")
    with open("ghi_file.txt", "r", encoding="utf-8") as f:
        print(f"Nội dung file:\n{f.read()}")
except Exception as e:
    print(f"Có lỗi xảy ra: {e}")
print("=" * 50)
print()

# Bài 93: Đọc file từng dòng
print("Bài 93: Đọc file từng dòng")
try:
    with open("ghi_file.txt", "r", encoding="utf-8") as f:
        print("Đọc từng dòng:")
        for i, dong in enumerate(f, 1):
            print(f"Dòng {i}: {dong.strip()}")
except Exception as e:
    print(f"Có lỗi xảy ra: {e}")
print("=" * 50)
print()

# Bài 94: Thêm nội dung vào file
print("Bài 94: Thêm nội dung vào file")
try:
    with open("ghi_file.txt", "a", encoding="utf-8") as f:
        f.write("\nDòng được thêm mới")
    print("Đã thêm nội dung vào file!")
    with open("ghi_file.txt", "r", encoding="utf-8") as f:
        print(f"Nội dung file sau khi thêm:\n{f.read()}")
except Exception as e:
    print(f"Có lỗi xảy ra: {e}")
print("=" * 50)
print()

# Bài 95: Kiểm tra file tồn tại
print("Bài 95: Kiểm tra file tồn tại")
import os
file_name = "ghi_file.txt"
if os.path.exists(file_name):
    print(f"File '{file_name}' tồn tại")
else:
    print(f"File '{file_name}' không tồn tại")
print("=" * 50)
print()

# Bài 96: Lấy kích thước file
print("Bài 96: Lấy kích thước file")
import os
file_name = "ghi_file.txt"
if os.path.exists(file_name):
    kich_thuoc = os.path.getsize(file_name)
    print(f"Kích thước file '{file_name}': {kich_thuoc} bytes")
else:
    print(f"File '{file_name}' không tồn tại")
print("=" * 50)
print()

# Bài 97: Xóa file
print("Bài 97: Xóa file")
import os
file_name = "test_file.txt"
if os.path.exists(file_name):
    os.remove(file_name)
    print(f"Đã xóa file '{file_name}'")
else:
    print(f"File '{file_name}' không tồn tại")
print("=" * 50)
print()

# Bài 98: Đổi tên file
print("Bài 98: Đổi tên file")
import os
file_cu = "ghi_file.txt"
file_moi = "file_da_doi_ten.txt"
if os.path.exists(file_cu):
    os.rename(file_cu, file_moi)
    print(f"Đã đổi tên '{file_cu}' thành '{file_moi}'")
else:
    print(f"File '{file_cu}' không tồn tại")
print("=" * 50)
print()

# Bài 99: Tạo thư mục
print("Bài 99: Tạo thư mục")
import os
thu_muc = "test_folder"
if not os.path.exists(thu_muc):
    os.makedirs(thu_muc)
    print(f"Đã tạo thư mục '{thu_muc}'")
else:
    print(f"Thư mục '{thu_muc}' đã tồn tại")
print("=" * 50)
print()

# Bài 100: Liệt kê file trong thư mục
print("Bài 100: Liệt kê file trong thư mục")
import os
thu_muc = "."
danh_sach = os.listdir(thu_muc)
print(f"Các file trong thư mục '{thu_muc}':")
for item in danh_sach[:10]:  # Chỉ hiển thị 10 file đầu tiên
    print(f"  - {item}")
print("...")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập cơ bản!")
print("Hoàn thành tất cả 100 bài tập cơ bản!")
