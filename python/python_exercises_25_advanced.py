# Python Exercises 241-250: Advanced Level
# Bài tập Python 241-250: Nâng cao

# Bài 241: Tìm chuỗi con có tổng lớn nhất
print("Bài 241: Tìm chuỗi con có tổng lớn nhất")
def max_subarray_sum(arr):
    if not arr:
        return 0
    
    max_sum = arr[0]
    current_sum = arr[0]
    
    for i in range(1, len(arr)):
        current_sum = max(arr[i], current_sum + arr[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum

danh_sach = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(f"Danh sách: {danh_sach}")
print(f"Tổng chuỗi con lớn nhất: {max_subarray_sum(danh_sach)}")
print("=" * 50)
print()

# Bài 242: Tìm chuỗi con có tích lớn nhất
print("Bài 242: Tìm chuỗi con có tích lớn nhất")
def max_product_subarray(arr):
    if not arr:
        return 0
    
    max_product = arr[0]
    min_product = arr[0]
    result = arr[0]
    
    for i in range(1, len(arr)):
        if arr[i] < 0:
            max_product, min_product = min_product, max_product
        
        max_product = max(arr[i], max_product * arr[i])
        min_product = min(arr[i], min_product * arr[i])
        result = max(result, max_product)
    
    return result

danh_sach = [2, 3, -2, 4]
print(f"Danh sách: {danh_sach}")
print(f"Tích chuỗi con lớn nhất: {max_product_subarray(danh_sach)}")
print("=" * 50)
print()

# Bài 243: Tìm chuỗi con có độ dài nhỏ nhất với tổng >= k
print("Bài 243: Tìm chuỗi con có độ dài nhỏ nhất với tổng >= k")
def min_subarray_length(arr, k):
    n = len(arr)
    min_length = float('infinity')
    current_sum = 0
    left = 0
    
    for right in range(n):
        current_sum += arr[right]
        
        while current_sum >= k:
            min_length = min(min_length, right - left + 1)
            current_sum -= arr[left]
            left += 1
    
    return min_length if min_length != float('infinity') else 0

danh_sach = [2, 3, 1, 2, 4, 3]
k = 7
print(f"Danh sách: {danh_sach}")
print(f"Tổng cần đạt: {k}")
print(f"Độ dài chuỗi con nhỏ nhất: {min_subarray_length(danh_sach, k)}")
print("=" * 50)
print()

# Bài 244: Tìm chuỗi con không có ký tự lặp lại dài nhất
print("Bài 244: Tìm chuỗi con không có ký tự lặp lại dài nhất")
def length_of_longest_substring(s):
    char_index = {}
    max_length = 0
    start = 0
    
    for i, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        char_index[char] = i
        max_length = max(max_length, i - start + 1)
    
    return max_length

chuoi = "abcabcbb"
print(f"Chuỗi: {chuoi}")
print(f"Độ dài chuỗi con không lặp dài nhất: {length_of_longest_substring(chuoi)}")
print("=" * 50)
print()

# Bài 245: Tìm chuỗi con Palindrome dài nhất
print("Bài 245: Tìm chuỗi con Palindrome dài nhất")
def longest_palindrome_subsequence(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    
    for i in range(n):
        dp[i][i] = 1
    
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                if length == 2:
                    dp[i][j] = 2
                else:
                    dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    
    return dp[0][n - 1]

chuoi = "bbbab"
print(f"Chuỗi: {chuoi}")
print(f"Độ dài chuỗi con Palindrome dài nhất: {longest_palindrome_subsequence(chuoi)}")
print("=" * 50)
print()

# Bài 246: Tìm chuỗi con tăng dài nhất
print("Bài 246: Tìm chuỗi con tăng dài nhất")
def longest_increasing_subsequence_length(arr):
    if not arr:
        return 0
    
    n = len(arr)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

danh_sach = [10, 9, 2, 5, 3, 7, 101, 18]
print(f"Danh sách: {danh_sach}")
print(f"Độ dài chuỗi con tăng dài nhất: {longest_increasing_subsequence_length(danh_sach)}")
print("=" * 50)
print()

# Bài 247: Tìm chuỗi con giảm dài nhất
print("Bài 247: Tìm chuỗi con giảm dài nhất")
def longest_decreasing_subsequence_length(arr):
    if not arr:
        return 0
    
    n = len(arr)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[j] > arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

danh_sach = [10, 9, 2, 5, 3, 7, 101, 18]
print(f"Danh sách: {danh_sach}")
print(f"Độ dài chuỗi con giảm dài nhất: {longest_decreasing_subsequence_length(danh_sach)}")
print("=" * 50)
print()

# Bài 248: Tìm chuỗi con có tổng bằng k
print("Bài 248: Tìm chuỗi con có tổng bằng k")
def subarray_sum(arr, k):
    prefix_sum = {0: -1}
    current_sum = 0
    
    for i, num in enumerate(arr):
        current_sum += num
        
        if current_sum - k in prefix_sum:
            return [prefix_sum[current_sum - k] + 1, i]
        
        prefix_sum[current_sum] = i
    
    return None

danh_sach = [1, 2, 3, 4, 5]
k = 9
print(f"Danh sách: {danh_sach}")
print(f"Tổng cần tìm: {k}")
print(f"Vị trí chuỗi con: {subarray_sum(danh_sach, k)}")
print("=" * 50)
print()

# Bài 249: Tìm chuỗi con có tích bằng k
print("Bài 249: Tìm chuỗi con có tích bằng k")
def subarray_product(arr, k):
    if k == 0:
        return None
    
    product = 1
    left = 0
    
    for right in range(len(arr)):
        product *= arr[right]
        
        while product > k and left <= right:
            product /= arr[left]
            left += 1
        
        if product == k:
            return [left, right]
    
    return None

danh_sach = [1, 2, 3, 4, 5]
k = 24
print(f"Danh sách: {danh_sach}")
print(f"Tích cần tìm: {k}")
print(f"Vị trí chuỗi con: {subarray_product(danh_sach, k)}")
print("=" * 50)
print()

# Bài 250: Tìm chuỗi con có độ dài lớn nhất với điều kiện
print("Bài 250: Tìm chuỗi con có độ dài lớn nhất với điều kiện")
def max_subarray_with_condition(arr, condition):
    max_length = 0
    current_length = 0
    
    for num in arr:
        if condition(num):
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 0
    
    return max_length

danh_sach = [1, 2, 3, 4, 5, 1, 2, 3]
print(f"Danh sách: {danh_sach}")
print(f"Độ dài chuỗi con tăng liên tiếp dài nhất: {max_subarray_with_condition(danh_sach, lambda x: x > 0)}")
print("=" * 50)
print()

print("Đã hoàn thành 10 bài tập nâng cao!")
