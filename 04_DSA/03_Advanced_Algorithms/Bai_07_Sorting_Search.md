# Bài 07: Sorting & Binary Search

## 🎯 Mục tiêu
- Sorting algorithms chính
- Binary Search variants
- Search in rotated/matrix arrays

---

## 1. Sorting

```python
# QuickSort — O(N log N) avg, O(N²) worst
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + mid + quicksort(right)

# MergeSort — O(N log N) guaranteed, stable
def mergesort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = mergesort(arr[:mid])
    right = mergesort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]
```

---

## 2. Binary Search Variants

```python
# Standard binary search
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target: return mid
        elif nums[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1

# First/Last occurrence (bisect)
def first_occurrence(nums, target):
    lo, hi = 0, len(nums) - 1
    result = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            result = mid
            hi = mid - 1  # keep searching left
        elif nums[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return result

# Search in Rotated Sorted Array
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target: return mid
        if nums[lo] <= nums[mid]:  # left half sorted
            if nums[lo] <= target < nums[mid]: hi = mid - 1
            else: lo = mid + 1
        else:  # right half sorted
            if nums[mid] < target <= nums[hi]: lo = mid + 1
            else: hi = mid - 1
    return -1

# Binary search on answer (min/max optimization)
def min_days_bouquets(bloomDay, m, k):
    def can_make(days):
        bouquets = flowers = 0
        for bloom in bloomDay:
            if bloom <= days:
                flowers += 1
                if flowers == k:
                    bouquets += 1
                    flowers = 0
            else:
                flowers = 0
        return bouquets >= m
    
    lo, hi = min(bloomDay), max(bloomDay)
    result = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if can_make(mid):
            result = mid
            hi = mid - 1
        else:
            lo = mid + 1
    return result
```

---

## 📝 Bài tập
1. Find Minimum in Rotated Sorted Array
2. Koko Eating Bananas (Binary Search on answer)
3. Search a 2D Matrix
4. Median of Two Sorted Arrays (hard)

## 🎯 LeetCode Practice List

**Binary Search — Classic:**
- #704 Binary Search (Easy)
- #35 Search Insert Position (Easy)
- #74 Search a 2D Matrix (Medium)
- #33 Search in Rotated Sorted Array (Medium) ⭐
- #153 Find Minimum in Rotated Sorted Array (Medium)
- #981 Time Based Key-Value Store (Medium)

**Binary Search — On Answer:**
- #875 Koko Eating Bananas (Medium) ⭐
- #1011 Capacity To Ship Packages (Medium)
- #410 Split Array Largest Sum (Hard)
- #4 Median of Two Sorted Arrays (Hard)

**Sorting:**
- #912 Sort an Array (Medium) → implement QuickSort/MergeSort
- #148 Sort List (Medium) → merge sort on linked list
- #179 Largest Number (Medium)
- #56 Merge Intervals (Medium) ⭐

> Mục tiêu: Giải ≥ 11/14 bài.

## 📚 Tài liệu
- [Binary Search Patterns](https://leetcode.com/discuss/general-discussion/786126/)
