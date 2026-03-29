# Python Exercises 171-180: Intermediate Level
# Bài tập Python 171-180: Trung cấp

# Bài 171: Đổi số thập phân sang nhị phân
print("Bài 171: Đổi số thập phân sang nhị phân")
def thap_phan_sang_nhi_phan(n):
    if n == 0:
        return "0"
    ket_qua = ""
    while n > 0:
        ket_qua = str(n % 2) + ket_qua
        n = n // 2
    return ket_qua

so = 10
print(f"{so} trong hệ nhị phân: {thap_phan_sang_nhi_phan(so)}")
so = 25
print(f"{so} trong hệ nhị phân: {thap_phan_sang_nhi_phan(so)}")
print("=" * 50)
print()

# Bài 172: Đổi số nhị phân sang thập phân
print("Bài 172: Đổi số nhị phân sang thập phân")
def nhi_phan_sang_thap_phan(s):
    ket_qua = 0
    for i, digit in enumerate(reversed(s)):
        if digit == '1':
            ket_qua += 2 ** i
    return ket_qua

so_nhi_phan = "1010"
print(f"{so_nhi_phan} trong hệ thập phân: {nhi_phan_sang_thap_phan(so_nhi_phan)}")
so_nhi_phan = "11001"
print(f"{so_nhi_phan} trong hệ thập phân: {nhi_phan_sang_thap_phan(so_nhi_phan)}")
print("=" * 50)
print()

# Bài 173: Đổi số thập phân sang hệ 16
print("Bài 173: Đổi số thập phân sang hệ 16")
def thap_phan_sang_hex(n):
    hex_chars = "0123456789ABCDEF"
    if n == 0:
        return "0"
    ket_qua = ""
    while n > 0:
        ket_qua = hex_chars[n % 16] + ket_qua
        n = n // 16
    return ket_qua

so = 255
print(f"{so} trong hệ 16: {thap_phan_sang_hex(so)}")
so = 4096
print(f"{so} trong hệ 16: {thap_phan_sang_hex(so)}")
print("=" * 50)
print()

# Bài 174: Đổi số hệ 16 sang thập phân
print("Bài 174: Đổi số hệ 16 sang thập phân")
def hex_sang_thap_phan(s):
    hex_chars = "0123456789ABCDEF"
    ket_qua = 0
    for i, digit in enumerate(reversed(s.upper())):
        ket_qua += hex_chars.index(digit) * (16 ** i)
    return ket_qua

so_hex = "FF"
print(f"{so_hex} trong hệ thập phân: {hex_sang_thap_phan(so_hex)}")
so_hex = "100"
print(f"{so_hex} trong hệ thập phân: {hex_sang_thap_phan(so_hex)}")
print("=" * 50)
print()

# Bài 175: Đổi số thập phân sang hệ 8
print("Bài 175: Đổi số thập phân sang hệ 8")
def thap_phan_sang_bat_phan(n):
    if n == 0:
        return "0"
    ket_qua = ""
    while n > 0:
        ket_qua = str(n % 8) + ket_qua
        n = n // 8
    return ket_qua

so = 64
print(f"{so} trong hệ 8: {thap_phan_sang_bat_phan(so)}")
so = 100
print(f"{so} trong hệ 8: {thap_phan_sang_bat_phan(so)}")
print("=" * 50)
print()

# Bài 176: Đổi số hệ 8 sang thập phân
print("Bài 176: Đổi số hệ 8 sang thập phân")
def bat_phan_sang_thap_phan(s):
    ket_qua = 0
    for i, digit in enumerate(reversed(s)):
        ket_qua += int(digit) * (8 ** i)
    return ket_qua

so_bat_phan = "100"
print(f"{so_bat_phan} trong hệ thập phân: {bat_phan_sang_thap_phan(so_bat_phan)}")
so_bat_phan = "144"
print(f"{so_bat_phan} trong hệ thập phân: {bat_phan_sang_thap_phan(so_bat_phan)}")
print("=" * 50)
print()

# Bài 177: Kiểm tra số có phải là số chính phương không
print("Bài 177: Kiểm tra số có phải là số chính phương không")
def la_so_chinh_phuong(n):
    if n < 0:
        return False
    can_bac_hai = int(n ** 0.5)
    return can_bac_hai * can_bac_hai == n

for so in [1, 4, 9, 16, 25, 2, 3, 5, 7, 8]:
    print(f"{so} là số chính phương: {la_so_chinh_phuong(so)}")
print("=" * 50)
print()

# Bài 178: Tìm các số chính phương trong khoảng
print("Bài 178: Tìm các số chính phương trong khoảng")
def tim_so_chinh_phuong_trong_khoang(start, end):
    ket_qua = []
    for num in range(start, end + 1):
        if la_so_chinh_phuong(num):
            ket_qua.append(num)
    return ket_qua

start, end = 1, 100
print(f"Các số chính phương từ {start} đến {end}: {tim_so_chinh_phuong_trong_khoang(start, end)}")
print("=" * 50)
print()

# Bài 179: Kiểm tra số có phải là số tam giác không
print("Bài 179: Kiểm tra số có phải là số tam giác không")
def la_so_tam_giac(n):
    if n <= 0:
        return False
    total = 0
    i = 1
    while total < n:
        total += i
        i += 1
    return total == n

for so in [1, 3, 6, 10, 15, 21, 2, 4, 5, 7]:
    print(f"{so} là số tam giác: {la_so_tam_giac(so)}")
print("=" * 50)
print()

# Bài 180: Tìm các số tam giác trong khoảng
print("Bài 180: Tìm các số tam giác trong khoảng")
def tim_so_tam_giac_trong_khoang(start, end):
    ket_qua = []
    for num in range(start, end + 1):
        if la_so_tam_giac(num):
            ket_qua.append(num)
    return ket_qua

start, end = 1, 100
print(f"Các số tam giác từ {start} đến {end}: {tim_so_tam_giac_trong_khoang(start, end)}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập trung cấp!")
