# Python Exercises 181-190: Intermediate Level
# Bài tập Python 181-190: Trung cấp

# Bài 181: Tìm phần tử lớn nhất trong ma trận
print("Bài 181: Tìm phần tử lớn nhất trong ma trận")
def max_ma_tran(matrix):
    if not matrix or not matrix[0]:
        return None
    return max(max(row) for row in matrix)

ma_tran = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận: {ma_tran}")
print(f"Phần tử lớn nhất: {max_ma_tran(ma_tran)}")
print("=" * 50)
print()

# Bài 182: Tìm phần tử nhỏ nhất trong ma trận
print("Bài 182: Tìm phần tử nhỏ nhất trong ma trận")
def min_ma_tran(matrix):
    if not matrix or not matrix[0]:
        return None
    return min(min(row) for row in matrix)

ma_tran = [
    [9, 8, 7],
    [6, 5, 4],
    [3, 2, 1]
]
print(f"Ma trận: {ma_tran}")
print(f"Phần tử nhỏ nhất: {min_ma_tran(ma_tran)}")
print("=" * 50)
print()

# Bài 183: Tính tổng các phần tử trong ma trận
print("Bài 183: Tính tổng các phần tử trong ma trận")
def tong_ma_tran(matrix):
    return sum(sum(row) for row in matrix)

ma_tran = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận: {ma_tran}")
print(f"Tổng các phần tử: {tong_ma_tran(ma_tran)}")
print("=" * 50)
print()

# Bài 184: Tính trung bình cộng các phần tử trong ma trận
print("Bài 184: Tính trung bình cộng các phần tử trong ma trận")
def trung_binh_ma_tran(matrix):
    if not matrix or not matrix[0]:
        return 0
    tong = sum(sum(row) for row in matrix)
    so_luong = sum(len(row) for row in matrix)
    return tong / so_luong

ma_tran = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận: {ma_tran}")
print(f"Trung bình cộng: {trung_binh_ma_tran(ma_tran)}")
print("=" * 50)
print()

# Bài 185: Tìm tổng của từng hàng trong ma trận
print("Bài 185: Tìm tổng của từng hàng trong ma trận")
def tong_tung_hang(matrix):
    return [sum(row) for row in matrix]

ma_tran = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận: {ma_tran}")
print(f"Tổng từng hàng: {tong_tung_hang(ma_tran)}")
print("=" * 50)
print()

# Bài 186: Tìm tổng của từng cột trong ma trận
print("Bài 186: Tìm tổng của từng cột trong ma trận")
def tong_tung_cot(matrix):
    if not matrix or not matrix[0]:
        return []
    so_cot = len(matrix[0])
    ket_qua = []
    for j in range(so_cot):
        tong_cot = sum(matrix[i][j] for i in range(len(matrix)))
        ket_qua.append(tong_cot)
    return ket_qua

ma_tran = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận: {ma_tran}")
print(f"Tổng từng cột: {tong_tung_cot(ma_tran)}")
print("=" * 50)
print()

# Bài 187: Chuyển vị ma trận
print("Bài 187: Chuyển vị ma trận")
def chuyen_vi(matrix):
    if not matrix or not matrix[0]:
        return []
    return [[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]

ma_tran = [
    [1, 2, 3],
    [4, 5, 6]
]
print(f"Ma trận gốc: {ma_tran}")
print(f"Ma trận chuyển vị: {chuyen_vi(ma_tran)}")
print("=" * 50)
print()

# Bài 188: Kiểm tra ma trận có đối xứng không
print("Bài 188: Kiểm tra ma trận có đối xứng không")
def la_ma_tran_doi_xung(matrix):
    if not matrix or not matrix[0]:
        return False
    n = len(matrix)
    m = len(matrix[0])
    if n != m:
        return False
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

ma_tran1 = [
    [1, 2, 3],
    [2, 5, 6],
    [3, 6, 9]
]
ma_tran2 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận 1: {ma_tran1}")
print(f"Là ma trận đối xứng: {la_ma_tran_doi_xung(ma_tran1)}")
print(f"Ma trận 2: {ma_tran2}")
print(f"Là ma trận đối xứng: {la_ma_tran_doi_xung(ma_tran2)}")
print("=" * 50)
print()

# Bài 189: Tìm đường chéo chính của ma trận vuông
print("Bài 189: Tìm đường chéo chính của ma trận vuông")
def duong_cheo_chinh(matrix):
    if not matrix or not matrix[0]:
        return []
    n = len(matrix)
    return [matrix[i][i] for i in range(n)]

ma_tran = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận: {ma_tran}")
print(f"Đường chéo chính: {duong_cheo_chinh(ma_tran)}")
print("=" * 50)
print()

# Bài 190: Tìm đường chéo phụ của ma trận vuông
print("Bài 190: Tìm đường chéo phụ của ma trận vuông")
def duong_cheo_phu(matrix):
    if not matrix or not matrix[0]:
        return []
    n = len(matrix)
    return [matrix[i][n - 1 - i] for i in range(n)]

ma_tran = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận: {ma_tran}")
print(f"Đường chéo phụ: {duong_cheo_phu(ma_tran)}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập trung cấp!")
