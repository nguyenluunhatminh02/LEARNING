# Bài 10: Trie & Advanced String Algorithms

## 🎯 Mục tiêu
- Trie (Prefix Tree)
- KMP pattern matching
- Rabin-Karp rolling hash

## 📖 Câu chuyện đời thường
> Bạn gõ "Nguy" trên điện thoại và nó gợi ý: "Nguyễn", "Nguyên", "Nguyễn Văn" — đó là **Trie** (đọc là "try"), cây lưu từ theo từng chữ cái. Gõ mỗi chữ là rẽ xuống 1 nhánh cây, từ gợi ý là các lá phía dưới. **KMP** giống tìm từ trong sách mà không cần quay lại đầu: khi so sánh thấy không khớp, bạn biết chính xác cần nhảy đến đâu thay vì bắt đầu lại từ đầu. **Rabin-Karp** giống như nhận dạng vân tay: thay vì so từng chữ, bạn tạo "dấu vân tay" (hash) cho đoạn văn và so vân tay — nhanh hơn nhiều.

---

## 1. Trie

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self._traverse(word)
        return node is not None and node.is_end
    
    def starts_with(self, prefix):
        return self._traverse(prefix) is not None
    
    def _traverse(self, s):
        node = self.root
        for char in s:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

# Use case: autocomplete, spell check, IP routing
# Word Search II (find all words in grid using Trie)
```

---

## 2. KMP (Knuth-Morris-Pratt) — O(N+M)

```python
def kmp_search(text, pattern):
    # Build failure function
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length:
            length = lps[length - 1]
        else:
            i += 1
    
    # Search
    i = j = 0
    results = []
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1; j += 1
        if j == len(pattern):
            results.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and text[i] != pattern[j]:
            j = lps[j - 1] if j else 0
            if j == 0 and text[i] != pattern[0]:
                i += 1
    return results
```

---

## 3. Rabin-Karp (Rolling Hash) — O(N) average

```python
def rabin_karp(text, pattern):
    base, mod = 256, 10**9 + 7
    m, n = len(pattern), len(text)
    
    pat_hash = 0
    txt_hash = 0
    h = pow(base, m - 1, mod)
    
    for i in range(m):
        pat_hash = (pat_hash * base + ord(pattern[i])) % mod
        txt_hash = (txt_hash * base + ord(text[i])) % mod
    
    for i in range(n - m + 1):
        if pat_hash == txt_hash and text[i:i+m] == pattern:
            return i  # found
        if i < n - m:
            txt_hash = (txt_hash * base - ord(text[i]) * h * base + ord(text[i+m])) % mod
    return -1
```

---

## 📝 Bài tập
1. Implement Autocomplete System (Trie)
2. Word Search II (Trie + Backtracking)
3. Repeated Substring Pattern (KMP)
4. Design Add and Search Words Data Structure

## 🎯 LeetCode Practice List

**Trie:**
- #208 Implement Trie (Medium) ⭐ must-do
- #211 Design Add and Search Words (Medium)
- #212 Word Search II (Hard) ⭐
- #642 Design Search Autocomplete System (Hard)
- #745 Prefix and Suffix Search (Hard)

**String Matching:**
- #28 Find Index of First Occurrence (Easy) → implement KMP
- #459 Repeated Substring Pattern (Easy)
- #686 Repeated String Match (Medium)

**String Manipulation:**
- #271 Encode and Decode Strings (Medium)
- #394 Decode String (Medium)
- #14 Longest Common Prefix (Easy)

> Mục tiêu: Giải ≥ 8/11 bài.

## 📚 Tài liệu
- *Introduction to Algorithms* — CLRS (Ch.32: String Matching)
