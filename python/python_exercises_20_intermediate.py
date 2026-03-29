# Python Exercises 191-200: Intermediate Level
# Bài tập Python 191-200: Trung cấp

# Bài 191: Tính tổng đường chéo chính
print("Bài 191: Tính tổng đường chéo chính")
def tong_duong_cheo_chinh(matrix):
    if not matrix or not matrix[0]:
        return 0
    n = len(matrix)
    return sum(matrix[i][i] for i in range(n))

ma_tran = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận: {ma_tran}")
print(f"Tổng đường chéo chính: {tong_duong_cheo_chinh(ma_tran)}")
print("=" * 50)
print()

# Bài 192: Tính tổng đường chéo phụ
print("Bài 192: Tính tổng đường chéo phụ")
def tong_duong_cheo_phu(matrix):
    if not matrix or not matrix[0]:
        return 0
    n = len(matrix)
    return sum(matrix[i][n - 1 - i] for i in range(n))

ma_tran = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận: {ma_tran}")
print(f"Tổng đường chéo phụ: {tong_duong_cheo_phu(ma_tran)}")
print("=" * 50)
print()

# Bài 193: Kiểm tra ma trận có phải là ma trận tam giác trên không
print("Bài 193: Kiểm tra ma trận có phải là ma trận tam giác trên không")
def la_ma_tran_tam_giac_tren(matrix):
    if not matrix or not matrix[0]:
        return False
    n = len(matrix)
    for i in range(n):
        for j in range(i):
            if matrix[i][j] != 0:
                return False
    return True

ma_tran1 = [
    [1, 2, 3],
    [0, 5, 6],
    [0, 0, 9]
]
ma_tran2 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận 1: {ma_tran1}")
print(f"Là ma trận tam giác trên: {la_ma_tran_tam_giac_tren(ma_tran1)}")
print(f"Ma trận 2: {ma_tran2}")
print(f"Là ma trận tam giác trên: {la_ma_tran_tam_giac_tren(ma_tran2)}")
print("=" * 50)
print()

# Bài 194: Kiểm tra ma trận có phải là ma trận tam giác dưới không
print("Bài 194: Kiểm tra ma trận có phải là ma trận tam giác dưới không")
def la_ma_tran_tam_giac_duoi(matrix):
    if not matrix or not matrix[0]:
        return False
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] != 0:
                return False
    return True

ma_tran1 = [
    [1, 0, 0],
    [4, 5, 0],
    [7, 8, 9]
]
ma_tran2 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận 1: {ma_tran1}")
print(f"Là ma trận tam giác dưới: {la_ma_tran_tam_giac_duoi(ma_tran1)}")
print(f"Ma trận 2: {ma_tran2}")
print(f"Là ma trận tam giác dưới: {la_ma_tran_tam_giac_duoi(ma_tran2)}")
print("=" * 50)
print()

# Bài 195: Tìm hàng có tổng lớn nhất trong ma trận
print("Bài 195: Tìm hàng có tổng lớn nhất trong ma trận")
def hang_tong_lon_nhat(matrix):
    if not matrix or not matrix[0]:
        return None
    tong_hang = [sum(row) for row in matrix]
    max_tong = max(tong_hang)
    return [i for i, tong in enumerate(tong_hang) if tong == max_tong]

ma_tran = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận: {ma_tran}")
print(f"Hàng có tổng lớn nhất: {hang_tong_lon_nhat(ma_tran)}")
print("=" * 50)
print()

# Bài 196: Tìm cột có tổng lớn nhất trong ma trận
print("Bài 196: Tìm cột có tổng lớn nhất trong ma trận")
def cot_tong_lon_nhat(matrix):
    if not matrix or not matrix[0]:
        return None
    so_cot = len(matrix[0])
    tong_cot = [sum(matrix[i][j] for i in range(len(matrix))) for j in range(so_cot)]
    max_tong = max(tong_cot)
    return [j for j, tong in enumerate(tong_cot) if tong == max_tong]

ma_tran = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(f"Ma trận: {ma_tran}")
print(f"Cột có tổng lớn nhất: {cot_tong_lon_nhat(ma_tran)}")
print("=" * 50)
print()

# Bài 197: Nhân hai ma trận
print("Bài 197: Nhân hai ma trận")
def nhan_ma_tran(matrix1, matrix2):
    if not matrix1 or not matrix2 or not matrix1[0] or not matrix2[0]:
        return []
    n = len(matrix1)
    m = len(matrix2[0])
    p = len(matrix2)
    
    ket_qua = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for k in range(p):
                ket_qua[i][j] += matrix1[i][k] * matrix2[k][j]
    return ket_qua

ma_tran1 = [
    [1, 2],
    [3, 4]
]
ma_tran2 = [
    [5, 6],
    [7, 8]
]
print(f"Ma trận 1: {ma_tran1}")
print(f"Ma trận 2: {ma_tran2}")
print(f"Tích hai ma trận: {nhan_ma_tran(ma_tran1, ma_tran2)}")
print("=" * 50)
print()

# Bài 198: Cộng hai ma trận
print("Bài 198: Cộng hai ma trận")
def cong_ma_tran(matrix1, matrix2):
    if not matrix1 or not matrix2 or len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        return []
    return [[matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]

ma_tran1 = [
    [1, 2],
    [3, 4]
]
ma_tran2 = [
    [5, 6],
    [7, 8]
]
print(f"Ma trận 1: {ma_tran1}")
print(f"Ma trận 2: {ma_tran2}")
print(f"Tổng hai ma trận: {cong_ma_tran(ma_tran1, ma_tran2)}")
print("=" * 50)
print()

# Bài 199: Trừ hai ma trận
print("Bài 199: Trừ hai ma trận")
def tru_ma_tran(matrix1, matrix2):
    if not matrix1 or not matrix2 or len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        return []
    return [[matrix1[i][j] - matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]

ma_tran1 = [
    [5, 6],
    [7, 8]
]
ma_tran2 = [
    [1, 2],
    [3, 4]
]
print(f"Ma trận 1: {ma_tran1}")
print(f"Ma trận 2: {ma_tran2}")
print(f"Hiệu hai ma trận: {tru_ma_tran(ma_tran1, ma_tran2)}")
print("=" * 50)
print()

# Bài 200: Tính định thức ma trận 2x2
print("Bài 200: Tính định thức ma trận 2x2")
def dinh_thuc_2x2(matrix):
    if not matrix or len(matrix) != 2 or len(matrix[0]) != 2:
        return None
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

ma_tran = [
    [1, 2],
    [3, 4]
]
print(f"Ma trận: {ma_tran}")
print(f"Định thức: {dinh_thuc_2x2(ma_tran)}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập trung cấp!")
print("Hoàn thành tất cả 200 bài tập (100 cơ bản + 100 trung cấp)!")
