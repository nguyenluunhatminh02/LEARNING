# Python Exercises 121-130: Intermediate Level
# Bài tập Python 121-130: Trung cấp

# Bài 121: Tìm chuỗi con dài nhất không có ký tự lặp lại
print("Bài 121: Tìm chuỗi con dài nhất không có ký tự lặp lại")
def chuoi_con_dai_nhat(s):
    char_index = {}
    max_length = 0
    start = 0
    longest = ""
    
    for i, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        char_index[char] = i
        if i - start + 1 > max_length:
            max_length = i - start + 1
            longest = s[start:i+1]
    
    return longest

chuoi = "abcabcbb"
print(f"Chuỗi: {chuoi}")
print(f"Chuỗi con dài nhất không lặp: {chuoi_con_dai_nhat(chuoi)}")
chuoi = "bbbbb"
print(f"Chuỗi: {chuoi}")
print(f"Chuỗi con dài nhất không lặp: {chuoi_con_dai_nhat(chuoi)}")
print("=" * 50)
print()

# Bài 122: Kiểm tra chuỗi Palindrome
print("Bài 122: Kiểm tra chuỗi Palindrome")
def la_chuoi_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

for chuoi in ["radar", "level", "python", "A man a plan a canal Panama"]:
    print(f"'{chuoi}' là Palindrome: {la_chuoi_palindrome(chuoi)}")
print("=" * 50)
print()

# Bài 123: Đếm số từ trong chuỗi
print("Bài 123: Đếm số từ trong chuỗi")
chuoi = "Xin chào, đây là một chuỗi ví dụ"
so_tu = len(chuoi.split())
print(f"Chuỗi: '{chuoi}'")
print(f"Số từ: {so_tu}")
print("=" * 50)
print()

# Bài 124: Tìm từ dài nhất trong chuỗi
print("Bài 124: Tìm từ dài nhất trong chuỗi")
def tim_dai_nhat(s):
    tu = s.split()
    return max(tu, key=len) if tu else ""

chuoi = "Xin chào, đây là một chuỗi ví dụ"
print(f"Chuỗi: '{chuoi}'")
print(f"Từ dài nhất: '{tim_dai_nhat(chuoi)}'")
print("=" * 50)
print()

# Bài 125: Chuyển đổi chuỗi sang dạng title case
print("Bài 125: Chuyển đổi chuỗi sang dạng title case")
chuoi = "xin chào python programming"
chuoi_title = chuoi.title()
print(f"Chuỗi gốc: '{chuoi}'")
print(f"Title case: '{chuoi_title}'")
print("=" * 50)
print()

# Bài 126: Đếm số lần xuất hiện của từng ký tự
print("Bài 126: Đếm số lần xuất hiện của từng ký tự")
def dem_ky_tu(s):
    dem = {}
    for ky_tu in s:
        dem[ky_tu] = dem.get(ky_tu, 0) + 1
    return dem

chuoi = "hello world"
print(f"Chuỗi: '{chuoi}'")
print("Số lần xuất hiện của từng ký tự:")
for key, value in dem_ky_tu(chuoi).items():
    print(f"  '{key}': {value}")
print("=" * 50)
print()

# Bài 127: Xóa khoảng trắng thừa trong chuỗi
print("Bài 127: Xóa khoảng trắng thừa trong chuỗi")
def xoa_khoang_trang_thua(s):
    return ' '.join(s.split())

chuoi = "Xin   chào,   đây   là   chuỗi   ví   dụ"
print(f"Chuỗi gốc: '{chuoi}'")
print(f"Chuỗi sau khi xử lý: '{xoa_khoang_trang_thua(chuoi)}'")
print("=" * 50)
print()

# Bài 128: Tìm vị trí của tất cả các từ trong chuỗi
print("Bài 128: Tìm vị trí của tất cả các từ trong chuỗi")
def tim_vi_tri_tu(s, tu):
    vi_tri = []
    tu_list = s.split()
    for i, word in enumerate(tu_list):
        if word.lower() == tu.lower():
            vi_tri.append(i + 1)
    return vi_tri

chuoi = "xin chào xin chào xin chào"
tu = "xin"
print(f"Chuỗi: '{chuoi}'")
print(f"Từ '{tu}' xuất hiện tại vị trí: {tim_vi_tri_tu(chuoi, tu)}")
print("=" * 50)
print()

# Bài 129: Tách chuỗi theo điều kiện
print("Bài 129: Tách chuỗi theo điều kiện")
chuoi = "apple,banana,cherry,orange"
danh_sach = chuoi.split(',')
print(f"Chuỗi: '{chuoi}'")
print(f"Danh sách sau khi tách: {danh_sach}")
print("=" * 50)
print()

# Bài 130: Ghép danh sách thành chuỗi
print("Bài 130: Ghép danh sách thành chuỗi")
danh_sach = ["Xin", "chào", "Python", "Programming"]
chuoi = " ".join(danh_sach)
print(f"Danh sách: {danh_sach}")
print(f"Chuỗi sau khi ghép: '{chuoi}'")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập trung cấp!")
