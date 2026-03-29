# Python Exercises 151-160: Intermediate Level
# Bài tập Python 151-160: Trung cấp

# Bài 151: Kiểm tra danh sách có phải là dãy số tăng dần không
print("Bài 151: Kiểm tra danh sách có phải là dãy số tăng dần không")
def la_day_tang(lst):
    return all(lst[i] <= lst[i+1] for i in range(len(lst)-1))

danh_sach1 = [1, 2, 3, 4, 5]
danh_sach2 = [1, 3, 2, 4, 5]
print(f"Danh sách 1: {danh_sach1}")
print(f"Là dãy tăng dần: {la_day_tang(danh_sach1)}")
print(f"Danh sách 2: {danh_sach2}")
print(f"Là dãy tăng dần: {la_day_tang(danh_sach2)}")
print("=" * 50)
print()

# Bài 152: Kiểm tra danh sách có phải là dãy số giảm dần không
print("Bài 152: Kiểm tra danh sách có phải là dãy số giảm dần không")
def la_day_giam(lst):
    return all(lst[i] >= lst[i+1] for i in range(len(lst)-1))

danh_sach1 = [5, 4, 3, 2, 1]
danh_sach2 = [5, 3, 4, 2, 1]
print(f"Danh sách 1: {danh_sach1}")
print(f"Là dãy giảm dần: {la_day_giam(danh_sach1)}")
print(f"Danh sách 2: {danh_sach2}")
print(f"Là dãy giảm dần: {la_day_giam(danh_sach2)}")
print("=" * 50)
print()

# Bài 153: Tìm dãy con tăng dài nhất
print("Bài 153: Tìm dãy con tăng dài nhất")
def day_con_tang_dai_nhat(lst):
    if not lst:
        return []
    
    max_len = 1
    max_start = 0
    current_len = 1
    current_start = 0
    
    for i in range(1, len(lst)):
        if lst[i] > lst[i-1]:
            current_len += 1
        else:
            if current_len > max_len:
                max_len = current_len
                max_start = current_start
            current_len = 1
            current_start = i
    
    if current_len > max_len:
        max_len = current_len
        max_start = current_start
    
    return lst[max_start:max_start + max_len]

danh_sach = [1, 2, 3, 1, 2, 3, 4, 1, 2]
print(f"Danh sách: {danh_sach}")
print(f"Dãy con tăng dài nhất: {day_con_tang_dai_nhat(danh_sach)}")
print("=" * 50)
print()

# Bài 154: Tìm dãy con giảm dài nhất
print("Bài 154: Tìm dãy con giảm dài nhất")
def day_con_giam_dai_nhat(lst):
    if not lst:
        return []
    
    max_len = 1
    max_start = 0
    current_len = 1
    current_start = 0
    
    for i in range(1, len(lst)):
        if lst[i] < lst[i-1]:
            current_len += 1
        else:
            if current_len > max_len:
                max_len = current_len
                max_start = current_start
            current_len = 1
            current_start = i
    
    if current_len > max_len:
        max_len = current_len
        max_start = current_start
    
    return lst[max_start:max_start + max_len]

danh_sach = [5, 4, 3, 2, 5, 4, 3, 2, 1]
print(f"Danh sách: {danh_sach}")
print(f"Dãy con giảm dài nhất: {day_con_giam_dai_nhat(danh_sach)}")
print("=" * 50)
print()

# Bài 155: Tìm tổng dãy con liên tục lớn nhất
print("Bài 155: Tìm tổng dãy con liên tục lớn nhất")
def tong_day_con_lon_nhat(lst):
    if not lst:
        return 0
    
    max_tong = lst[0]
    tong_hien_tai = lst[0]
    
    for i in range(1, len(lst)):
        tong_hien_tai = max(lst[i], tong_hien_tai + lst[i])
        max_tong = max(max_tong, tong_hien_tai)
    
    return max_tong

danh_sach = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(f"Danh sách: {danh_sach}")
print(f"Tổng dãy con liên tục lớn nhất: {tong_day_con_lon_nhat(danh_sach)}")
print("=" * 50)
print()

# Bài 156: Tìm dãy con có tổng bằng k
print("Bài 156: Tìm dãy con có tổng bằng k")
def day_con_tong_bang_k(lst, k):
    for i in range(len(lst)):
        tong = 0
        for j in range(i, len(lst)):
            tong += lst[j]
            if tong == k:
                return lst[i:j+1]
            if tong > k:
                break
    return None

danh_sach = [1, 4, 20, 3, 10, 5]
k = 33
print(f"Danh sách: {danh_sach}")
print(f"Dãy con có tổng bằng {k}: {day_con_tong_bang_k(danh_sach, k)}")
print("=" * 50)
print()

# Bài 157: Tìm dãy con có độ dài lớn nhất
print("Bài 157: Tìm dãy con có độ dài lớn nhất")
def day_con_dai_nhat(lst):
    if not lst:
        return []
    
    max_len = 1
    max_start = 0
    current_len = 1
    current_start = 0
    
    for i in range(1, len(lst)):
        if lst[i] == lst[i-1] + 1:
            current_len += 1
        else:
            if current_len > max_len:
                max_len = current_len
                max_start = current_start
            current_len = 1
            current_start = i
    
    if current_len > max_len:
        max_len = current_len
        max_start = current_start
    
    return lst[max_start:max_start + max_len]

danh_sach = [1, 2, 3, 5, 6, 7, 8, 10]
print(f"Danh sách: {danh_sach}")
print(f"Dãy con dài nhất: {day_con_dai_nhat(danh_sach)}")
print("=" * 50)
print()

# Bài 158: Tìm dãy con có tổng lớn nhất
print("Bài 158: Tìm dãy con có tổng lớn nhất")
def day_con_tong_lon_nhat(lst):
    if not lst:
        return []
    
    max_tong = lst[0]
    max_start = 0
    max_end = 0
    tong_hien_tai = lst[0]
    start_hien_tai = 0
    
    for i in range(1, len(lst)):
        if tong_hien_tai + lst[i] > lst[i]:
            tong_hien_tai += lst[i]
        else:
            tong_hien_tai = lst[i]
            start_hien_tai = i
        
        if tong_hien_tai > max_tong:
            max_tong = tong_hien_tai
            max_start = start_hien_tai
            max_end = i
    
    return lst[max_start:max_end + 1]

danh_sach = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(f"Danh sách: {danh_sach}")
print(f"Dãy con có tổng lớn nhất: {day_con_tong_lon_nhat(danh_sach)}")
print("=" * 50)
print()

# Bài 159: Tìm dãy con có tổng nhỏ nhất
print("Bài 159: Tìm dãy con có tổng nhỏ nhất")
def day_con_tong_nho_nhat(lst):
    if not lst:
        return []
    
    min_tong = lst[0]
    min_start = 0
    min_end = 0
    tong_hien_tai = lst[0]
    start_hien_tai = 0
    
    for i in range(1, len(lst)):
        if tong_hien_tai + lst[i] < lst[i]:
            tong_hien_tai += lst[i]
        else:
            tong_hien_tai = lst[i]
            start_hien_tai = i
        
        if tong_hien_tai < min_tong:
            min_tong = tong_hien_tai
            min_start = start_hien_tai
            min_end = i
    
    return lst[min_start:min_end + 1]

danh_sach = [3, -4, 2, -3, -1, 7, -5]
print(f"Danh sách: {danh_sach}")
print(f"Dãy con có tổng nhỏ nhất: {day_con_tong_nho_nhat(danh_sach)}")
print("=" * 50)
print()

# Bài 160: Tìm dãy con có độ dài bằng k
print("Bài 160: Tìm dãy con có độ dài bằng k")
def day_con_do_dai_k(lst, k):
    if k > len(lst):
        return []
    ket_qua = []
    for i in range(len(lst) - k + 1):
        ket_qua.append(lst[i:i+k])
    return ket_qua

danh_sach = [1, 2, 3, 4, 5, 6]
k = 3
print(f"Danh sách: {danh_sach}")
print(f"Các dãy con có độ dài {k}: {day_con_do_dai_k(danh_sach, k)}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập trung cấp!")
