# Python Exercises 141-150: Intermediate Level
# Bài tập Python 141-150: Trung cấp

# Bài 141: Tìm số lớn nhất thứ hai trong danh sách
print("Bài 141: Tìm số lớn nhất thứ hai trong danh sách")
def so_lon_nhat_thu_hai(lst):
    if len(lst) < 2:
        return None
    lst_sap_xep = sorted(set(lst), reverse=True)
    return lst_sap_xep[1] if len(lst_sap_xep) >= 2 else None

danh_sach = [5, 2, 8, 1, 9, 3, 9]
print(f"Danh sách: {danh_sach}")
print(f"Số lớn nhất thứ hai: {so_lon_nhat_thu_hai(danh_sach)}")
print("=" * 50)
print()

# Bài 142: Tìm số nhỏ nhất thứ hai trong danh sách
print("Bài 142: Tìm số nhỏ nhất thứ hai trong danh sách")
def so_nho_nhat_thu_hai(lst):
    if len(lst) < 2:
        return None
    lst_sap_xep = sorted(set(lst))
    return lst_sap_xep[1] if len(lst_sap_xep) >= 2 else None

danh_sach = [5, 2, 8, 1, 3, 1]
print(f"Danh sách: {danh_sach}")
print(f"Số nhỏ nhất thứ hai: {so_nho_nhat_thu_hai(danh_sach)}")
print("=" * 50)
print()

# Bài 143: Tìm cặp số có tổng bằng k
print("Bài 143: Tìm cặp số có tổng bằng k")
def tim_cap_so(lst, k):
    seen = set()
    for num in lst:
        complement = k - num
        if complement in seen:
            return (complement, num)
        seen.add(num)
    return None

danh_sach = [2, 7, 11, 15]
k = 9
print(f"Danh sách: {danh_sach}")
print(f"Cặp số có tổng bằng {k}: {tim_cap_so(danh_sach, k)}")
print("=" * 50)
print()

# Bài 144: Tìm cặp số có hiệu bằng k
print("Bài 144: Tìm cặp số có hiệu bằng k")
def tim_cap_hieu(lst, k):
    seen = set()
    for num in lst:
        if num - k in seen:
            return (num - k, num)
        if num + k in seen:
            return (num + k, num)
        seen.add(num)
    return None

danh_sach = [1, 5, 3, 4, 2]
k = 2
print(f"Danh sách: {danh_sach}")
print(f"Cặp số có hiệu bằng {k}: {tim_cap_hieu(danh_sach, k)}")
print("=" * 50)
print()

# Bài 145: Tìm tất cả các cặp số có tổng bằng k
print("Bài 145: Tìm tất cả các cặp số có tổng bằng k")
def tim_tat_ca_cap(lst, k):
    ket_qua = []
    seen = {}
    for i, num in enumerate(lst):
        complement = k - num
        if complement in seen:
            ket_qua.append((complement, num))
        seen[num] = i
    return ket_qua

danh_sach = [1, 5, 7, -1, 5]
k = 6
print(f"Danh sách: {danh_sach}")
print(f"Tất cả các cặp có tổng bằng {k}: {tim_tat_ca_cap(danh_sach, k)}")
print("=" * 50)
print()

# Bài 146: Tìm phần tử xuất hiện nhiều nhất
print("Bài 146: Tìm phần tử xuất hiện nhiều nhất")
def phan_tu_xuat_hien_nhieu_nhat(lst):
    tan_suat = {}
    for item in lst:
        tan_suat[item] = tan_suat.get(item, 0) + 1
    return max(tan_suat, key=tan_suat.get)

danh_sach = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
print(f"Danh sách: {danh_sach}")
print(f"Phần tử xuất hiện nhiều nhất: {phan_tu_xuat_hien_nhieu_nhat(danh_sach)}")
print("=" * 50)
print()

# Bài 147: Tìm các phần tử xuất hiện hơn một lần
print("Bài 147: Tìm các phần tử xuất hiện hơn một lần")
def phan_tu_trung(lst):
    tan_suat = {}
    for item in lst:
        tan_suat[item] = tan_suat.get(item, 0) + 1
    return [item for item, count in tan_suat.items() if count > 1]

danh_sach = [1, 2, 2, 3, 3, 3, 4, 5]
print(f"Danh sách: {danh_sach}")
print(f"Các phần tử xuất hiện hơn một lần: {phan_tu_trung(danh_sach)}")
print("=" * 50)
print()

# Bài 148: Tìm các phần tử duy nhất
print("Bài 148: Tìm các phần tử duy nhất")
def phan_tu_duy_nhat(lst):
    tan_suat = {}
    for item in lst:
        tan_suat[item] = tan_suat.get(item, 0) + 1
    return [item for item, count in tan_suat.items() if count == 1]

danh_sach = [1, 2, 2, 3, 4, 4, 5]
print(f"Danh sách: {danh_sach}")
print(f"Các phần tử duy nhất: {phan_tu_duy_nhat(danh_sach)}")
print("=" * 50)
print()

# Bài 149: Xoay danh sách sang phải k vị trí
print("Bài 149: Xoay danh sách sang phải k vị trí")
def xoay_phai(lst, k):
    k = k % len(lst) if lst else 0
    return lst[-k:] + lst[:-k]

danh_sach = [1, 2, 3, 4, 5]
k = 2
print(f"Danh sách gốc: {danh_sach}")
print(f"Danh sách sau khi xoay phải {k} vị trí: {xoay_phai(danh_sach, k)}")
print("=" * 50)
print()

# Bài 150: Xoay danh sách sang trái k vị trí
print("Bài 150: Xoay danh sách sang trái k vị trí")
def xoay_trai(lst, k):
    k = k % len(lst) if lst else 0
    return lst[k:] + lst[:k]

danh_sach = [1, 2, 3, 4, 5]
k = 2
print(f"Danh sách gốc: {danh_sach}")
print(f"Danh sách sau khi xoay trái {k} vị trí: {xoay_trai(danh_sach, k)}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập trung cấp!")
