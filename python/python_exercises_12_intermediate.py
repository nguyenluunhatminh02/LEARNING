# Python Exercises 111-120: Intermediate Level
# Bài tập Python 111-120: Trung cấp

# Bài 111: Sắp xếp danh sách theo điều kiện
print("Bài 111: Sắp xếp danh sách theo điều kiện")
danh_sach = [5, 2, 8, 1, 9, 3, 7, 4, 6]
print(f"Danh sách gốc: {danh_sach}")
danh_sach_chan = sorted([x for x in danh_sach if x % 2 == 0])
danh_sach_le = sorted([x for x in danh_sach if x % 2 != 0])
print(f"Số chẵn đã sắp xếp: {danh_sach_chan}")
print(f"Số lẻ đã sắp xếp: {danh_sach_le}")
print("=" * 50)
print()

# Bài 112: Tìm phần tử thứ k lớn nhất
print("Bài 112: Tìm phần tử thứ k lớn nhất")
def phan_tu_thu_k_lon_nhat(danh_sach, k):
    if k > len(danh_sach):
        return None
    danh_sach_sap_xep = sorted(danh_sach, reverse=True)
    return danh_sach_sap_xep[k - 1]

danh_sach = [3, 1, 4, 1, 5, 9, 2, 6]
k = 3
print(f"Danh sách: {danh_sach}")
print(f"Phần tử thứ {k} lớn nhất: {phan_tu_thu_k_lon_nhat(danh_sach, k)}")
print("=" * 50)
print()

# Bài 113: Xóa phần tử trùng trong danh sách
print("Bài 113: Xóa phần tử trùng trong danh sách")
danh_sach = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
print(f"Danh sách gốc: {danh_sach}")
danh_sach_khong_trung = list(dict.fromkeys(danh_sach))
print(f"Danh sách sau khi xóa trùng: {danh_sach_khong_trung}")
print("=" * 50)
print()

# Bài 114: Gộp hai danh sách đã sắp xếp
print("Bài 114: Gộp hai danh sách đã sắp xếp")
def gop_danh_sach(list1, list2):
    i = j = 0
    ket_qua = []
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            ket_qua.append(list1[i])
            i += 1
        else:
            ket_qua.append(list2[j])
            j += 1
    ket_qua.extend(list1[i:])
    ket_qua.extend(list2[j:])
    return ket_qua

list1 = [1, 3, 5, 7]
list2 = [2, 4, 6, 8]
print(f"List1: {list1}")
print(f"List2: {list2}")
print(f"Danh sách sau khi gộp: {gop_danh_sach(list1, list2)}")
print("=" * 50)
print()

# Bài 115: Tìm giao của hai danh sách
print("Bài 115: Tìm giao của hai danh sách")
def giao_danh_sach(list1, list2):
    return list(set(list1) & set(list2))

list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]
print(f"List1: {list1}")
print(f"List2: {list2}")
print(f"Giao của hai danh sách: {giao_danh_sach(list1, list2)}")
print("=" * 50)
print()

# Bài 116: Tìm hiệu của hai danh sách
print("Bài 116: Tìm hiệu của hai danh sách")
def hieu_danh_sach(list1, list2):
    return list(set(list1) - set(list2))

list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]
print(f"List1: {list1}")
print(f"List2: {list2}")
print(f"List1 - List2: {hieu_danh_sach(list1, list2)}")
print("=" * 50)
print()

# Bài 117: Tìm hợp của hai danh sách
print("Bài 117: Tìm hợp của hai danh sách")
def hop_danh_sach(list1, list2):
    return list(set(list1) | set(list2))

list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]
print(f"List1: {list1}")
print(f"List2: {list2}")
print(f"Hợp của hai danh sách: {hop_danh_sach(list1, list2)}")
print("=" * 50)
print()

# Bài 118: Chuyển đổi danh sách chuỗi thành danh sách số
print("Bài 118: Chuyển đổi danh sách chuỗi thành danh sách số")
danh_sach_chuoi = ["1", "2", "3", "4", "5"]
danh_sach_so = [int(x) for x in danh_sach_chuoi]
print(f"Danh sách chuỗi: {danh_sach_chuoi}")
print(f"Danh sách số: {danh_sach_so}")
print("=" * 50)
print()

# Bài 119: Lọc danh sách theo điều kiện
print("Bài 119: Lọc danh sách theo điều kiện")
danh_sach = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
danh_sach_chan = [x for x in danh_sach if x % 2 == 0]
danh_sach_lon_hon_5 = [x for x in danh_sach if x > 5]
print(f"Danh sách gốc: {danh_sach}")
print(f"Số chẵn: {danh_sach_chan}")
print(f"Số lớn hơn 5: {danh_sach_lon_hon_5}")
print("=" * 50)
print()

# Bài 120: Tìm tần suất xuất hiện của các phần tử
print("Bài 120: Tìm tần suất xuất hiện của các phần tử")
danh_sach = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
tan_suat = {}
for phan_tu in danh_sach:
    tan_suat[phan_tu] = tan_suat.get(phan_tu, 0) + 1
print(f"Danh sách: {danh_sach}")
print("Tần suất xuất hiện:")
for key, value in tan_suat.items():
    print(f"  {key}: {value} lần")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập trung cấp!")
