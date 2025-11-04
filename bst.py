import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

BinTree: TypeAlias = Union["Node", None]

@dataclass(frozen=True)
class Node:
    value: Any
    left: BinTree
    right: BinTree


# --- The Binary Search Tree class ---
@dataclass(frozen=True)
class BinarySearchTree:
    comes_before: Callable[[Any, Any], bool]
    tree: BinTree

def is_empty(bst: BinarySearchTree) -> bool:
    return bst.tree is None

def insert(bst: BinarySearchTree, val: Any) -> BinarySearchTree:
    def insert_helper(tree: BinTree, val: Any, comes_before: Callable[[Any, Any], bool]) -> BinTree:
        if tree is None:
            return Node(val, None, None)
        if comes_before(val, tree.value):
            return Node(tree.value, insert_helper(tree.left, val, comes_before), tree.right)
        else:
            return Node(tree.value, tree.left, insert_helper(tree.right, val, comes_before))
    return BinarySearchTree(bst.comes_before, insert_helper(bst.tree, val, bst.comes_before))


def lookup(bst: BinarySearchTree, val: Any) -> bool:
    def lookup_helper(tree: BinTree, val: Any, comes_before: Callable[[Any, Any], bool]) -> bool:
        if tree is None:
            return False
        if (not comes_before(val, tree.value)) and (not comes_before(tree.value, val)):
            return True  # values equal
        elif comes_before(val, tree.value):
            return lookup_helper(tree.left, val, comes_before)
        else:
            return lookup_helper(tree.right, val, comes_before)
    return lookup_helper(bst.tree, val, bst.comes_before)


def delete(bst: BinarySearchTree, val: Any) -> BinarySearchTree:
    def find_min(tree: BinTree) -> Any:
        if tree.left is None:
            return tree.value
        return find_min(tree.left)
    
    def delete_helper(tree: BinTree, val: Any, comes_before: Callable[[Any, Any], bool]) -> BinTree:
        if tree is None:
            return None
        
        # Check equality first
        if (not comes_before(val, tree.value)) and (not comes_before(tree.value, val)):
            # Case 1: no children
            if tree.left is None and tree.right is None:
                return None
            # Case 2: one child
            elif tree.left is None:
                return tree.right
            elif tree.right is None:
                return tree.left
            # Case 3: two children
            else:
                successor_val = find_min(tree.right)
                return Node(successor_val, tree.left, delete_helper(tree.right, successor_val, comes_before))
        elif comes_before(val, tree.value):
            return Node(tree.value, delete_helper(tree.left, val, comes_before), tree.right)
        else:
            return Node(tree.value, tree.left, delete_helper(tree.right, val, comes_before))
    
    return BinarySearchTree(bst.comes_before, delete_helper(bst.tree, val, bst.comes_before))


# Basic numeric comparison
def num_comes_before(a: int, b: int) -> bool:
    return a < b

# Alphabetical comparison
def str_comes_before(a: str, b: str) -> bool:
    return a < b

# Custom for distance from origin
@dataclass(frozen=True)
class Point2:
    x: float
    y: float

def dist_comes_before(a: Point2, b: Point2) -> bool:
    return (a.x**2 + a.y**2) < (b.x**2 + b.y**2)

class TestBST(unittest.TestCase):
    def test_insert_and_lookup_numeric(self):
        bst = BinarySearchTree(num_comes_before, None)
        bst = insert(bst, 5)
        bst = insert(bst, 3)
        bst = insert(bst, 7)
        self.assertTrue(lookup(bst, 3))
        self.assertFalse(lookup(bst, 8))
    
    def test_delete(self):
        bst = BinarySearchTree(num_comes_before, None)
        for n in [5, 3, 7, 2, 4]:
            bst = insert(bst, n)
        bst = delete(bst, 3)
        self.assertFalse(lookup(bst, 3))
    
    def test_strings(self):
        bst = BinarySearchTree(str_comes_before, None)
        for w in ["dog", "cat", "apple"]:
            bst = insert(bst, w)
        self.assertTrue(lookup(bst, "cat"))
        bst = delete(bst, "cat")
        self.assertFalse(lookup(bst, "cat"))
    
    def test_points(self):
        p1, p2, p3 = Point2(1, 1), Point2(3, 4), Point2(0, 2)
        bst = BinarySearchTree(dist_comes_before, None)
        bst = insert(bst, p1)
        bst = insert(bst, p2)
        bst = insert(bst, p3)
        self.assertTrue(lookup(bst, p3))

if __name__ == '__main__':
    unittest.main()