# Python Exercises 131-140: Intermediate Level
# Bài tập Python 131-140: Trung cấp

# Bài 131: Sắp xếp dictionary theo giá trị
print("Bài 131: Sắp xếp dictionary theo giá trị")
dict_data = {'a': 5, 'b': 2, 'c': 8, 'd': 1}
print(f"Dictionary gốc: {dict_data}")
dict_sap_xep_tang = dict(sorted(dict_data.items(), key=lambda x: x[1]))
dict_sap_xep_giam = dict(sorted(dict_data.items(), key=lambda x: x[1], reverse=True))
print(f"Sắp xếp tăng dần: {dict_sap_xep_tang}")
print(f"Sắp xếp giảm dần: {dict_sap_xep_giam}")
print("=" * 50)
print()

# Bài 132: Gộp hai dictionary
print("Bài 132: Gộp hai dictionary")
dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}
dict_gop = {**dict1, **dict2}
print(f"Dictionary 1: {dict1}")
print(f"Dictionary 2: {dict2}")
print(f"Dictionary sau khi gộp: {dict_gop}")
print("=" * 50)
print()

# Bài 133: Tìm khóa có giá trị lớn nhất
print("Bài 133: Tìm khóa có giá trị lớn nhất")
dict_data = {'a': 5, 'b': 2, 'c': 8, 'd': 1}
khoa_max = max(dict_data, key=dict_data.get)
print(f"Dictionary: {dict_data}")
print(f"Khóa có giá trị lớn nhất: '{khoa_max}' với giá trị {dict_data[khoa_max]}")
print("=" * 50)
print()

# Bài 134: Đảo ngược dictionary (key thành value, value thành key)
print("Bài 134: Đảo ngược dictionary")
def dao_nguoc_dict(d):
    return {v: k for k, v in d.items()}

dict_data = {'a': 1, 'b': 2, 'c': 3}
print(f"Dictionary gốc: {dict_data}")
print(f"Dictionary sau khi đảo ngược: {dao_nguoc_dict(dict_data)}")
print("=" * 50)
print()

# Bài 135: Lọc dictionary theo điều kiện
print("Bài 135: Lọc dictionary theo điều kiện")
dict_data = {'a': 5, 'b': 2, 'c': 8, 'd': 1, 'e': 10}
dict_loc = {k: v for k, v in dict_data.items() if v > 3}
print(f"Dictionary gốc: {dict_data}")
print(f"Dictionary sau khi lọc (value > 3): {dict_loc}")
print("=" * 50)
print()

# Bài 136: Tính tổng các giá trị trong dictionary
print("Bài 136: Tính tổng các giá trị trong dictionary")
dict_data = {'a': 5, 'b': 2, 'c': 8, 'd': 1}
tong = sum(dict_data.values())
print(f"Dictionary: {dict_data}")
print(f"Tổng các giá trị: {tong}")
print("=" * 50)
print()

# Bài 137: Tìm giá trị trung bình của các giá trị trong dictionary
print("Bài 137: Tìm giá trị trung bình của các giá trị trong dictionary")
dict_data = {'a': 5, 'b': 2, 'c': 8, 'd': 1}
trung_binh = sum(dict_data.values()) / len(dict_data)
print(f"Dictionary: {dict_data}")
print(f"Giá trị trung bình: {trung_binh}")
print("=" * 50)
print()

# Bài 138: Tìm các khóa chung giữa hai dictionary
print("Bài 138: Tìm các khóa chung giữa hai dictionary")
dict1 = {'a': 1, 'b': 2, 'c': 3}
dict2 = {'b': 20, 'c': 30, 'd': 40}
khoa_chung = set(dict1.keys()) & set(dict2.keys())
print(f"Dictionary 1: {dict1}")
print(f"Dictionary 2: {dict2}")
print(f"Các khóa chung: {khoa_chung}")
print("=" * 50)
print()

# Bài 139: Tạo dictionary từ hai danh sách
print("Bài 139: Tạo dictionary từ hai danh sách")
khoa = ['a', 'b', 'c', 'd']
gia_tri = [1, 2, 3, 4]
dict_moi = dict(zip(khoa, gia_tri))
print(f"Danh sách khóa: {khoa}")
print(f"Danh sách giá trị: {gia_tri}")
print(f"Dictionary mới: {dict_moi}")
print("=" * 50)
print()

# Bài 140: Xóa các khóa có giá trị None
print("Bài 140: Xóa các khóa có giá trị None")
def xoa_none(d):
    return {k: v for k, v in d.items() if v is not None}

dict_data = {'a': 1, 'b': None, 'c': 3, 'd': None, 'e': 5}
print(f"Dictionary gốc: {dict_data}")
print(f"Dictionary sau khi xóa None: {xoa_none(dict_data)}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập trung cấp!")
