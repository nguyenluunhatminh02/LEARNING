# Bài 04: Trees & Binary Search Trees

## 🎯 Mục tiêu
- Binary Tree traversals (DFS, BFS)
- BST operations
- Common tree patterns

---

## 1. Tree Traversals

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# DFS — Inorder (Left, Root, Right) → BST sorted order
def inorder(root):
    if not root: return []
    return inorder(root.left) + [root.val] + inorder(root.right)

# DFS — Preorder (Root, Left, Right) → serialize tree
def preorder(root):
    if not root: return []
    return [root.val] + preorder(root.left) + preorder(root.right)

# DFS — Postorder (Left, Right, Root) → delete tree
def postorder(root):
    if not root: return []
    return postorder(root.left) + postorder(root.right) + [root.val]

# BFS — Level Order
from collections import deque
def level_order(root):
    if not root: return []
    result, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left: queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result
```

---

## 2. Common Tree Problems

```python
# Max Depth
def max_depth(root):
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# Invert Binary Tree
def invert_tree(root):
    if not root: return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root

# Lowest Common Ancestor (BST)
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root

# Validate BST
def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root: return True
    if root.val <= lo or root.val >= hi: return False
    return (is_valid_bst(root.left, lo, root.val) and 
            is_valid_bst(root.right, root.val, hi))

# Diameter of Binary Tree
def diameter(root):
    max_d = [0]
    def depth(node):
        if not node: return 0
        l, r = depth(node.left), depth(node.right)
        max_d[0] = max(max_d[0], l + r)
        return 1 + max(l, r)
    depth(root)
    return max_d[0]

# Serialize/Deserialize Binary Tree
def serialize(root):
    if not root: return "null"
    return f"{root.val},{serialize(root.left)},{serialize(root.right)}"
```

---

## 📝 Bài tập
1. Same Tree, Subtree of Another Tree
2. Binary Tree Right Side View (BFS)
3. Kth Smallest Element in BST
4. Construct Binary Tree from Preorder and Inorder

## 🎯 LeetCode Practice List

**Tree Traversal & DFS:**
- #104 Maximum Depth of Binary Tree (Easy)
- #226 Invert Binary Tree (Easy)
- #100 Same Tree (Easy)
- #572 Subtree of Another Tree (Easy)
- #543 Diameter of Binary Tree (Easy)
- #110 Balanced Binary Tree (Easy)

**BFS / Level Order:**
- #102 Binary Tree Level Order Traversal (Medium)
- #199 Binary Tree Right Side View (Medium)
- #297 Serialize and Deserialize Binary Tree (Hard)

**BST:**
- #98 Validate BST (Medium) ⭐
- #230 Kth Smallest Element in BST (Medium)
- #235 LCA of BST (Medium)
- #105 Construct from Preorder + Inorder (Medium)
- #124 Binary Tree Maximum Path Sum (Hard)

> Mục tiêu: Giải ≥ 11/14 bài.

## 📚 Tài liệu
- [NeetCode — Trees](https://neetcode.io/roadmap)
