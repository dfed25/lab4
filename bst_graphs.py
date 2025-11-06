import sys
import unittest
from typing import *
from dataclasses import dataclass
import math
import matplotlib.pyplot as plt
import numpy as np
import random
import time

sys.setrecursionlimit(10**6)

from bst import *

# Constants
TREES_PER_RUN: int = 1000  # lowered for speed (increase later to 10000)

# Generate a random Binary Search Tree with n random floats
def random_tree(n: int) -> BinarySearchTree:
    bst = BinarySearchTree(num_comes_before, None)
    for _ in range(n):
        val = random.random()
        bst = insert(bst, val)
    return bst

# Compute height of a BinTree
def height(tree) -> int:
    if tree is None:
        return 0
    return 1 + max(height(tree.left), height(tree.right))

# Compute height of a BST
def bst_height(bst: BinarySearchTree) -> int:
    return height(bst.tree)

# Compute average height across TREES_PER_RUN random BSTs for each N
def average_heights(n_values):
    avg_heights = []
    for n in n_values:
        total_height = 0
        for _ in range(TREES_PER_RUN):
            t = random_tree(n)
            total_height += bst_height(t)
        avg_height = total_height / TREES_PER_RUN
        avg_heights.append(avg_height)
        print(f"N={n}, average height={avg_height}")
    return avg_heights

# Compute average insertion time across TREES_PER_RUN random BSTs for each N
def average_insert_time(n_values):
    avg_times = []
    for n in n_values:
        total_time = 0
        for _ in range(TREES_PER_RUN):
            t = random_tree(n)
            val = random.random()
            start = time.perf_counter()
            t = insert(t, val)
            end = time.perf_counter()
            total_time += (end - start)
        avg_times.append(total_time / TREES_PER_RUN)
        print(f"N={n}, avg insert time={avg_times[-1]}")
    return avg_times

# Plot function (no plt.show() yet)
def plot_graph(x, y, title, xlabel, ylabel, filename):
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.savefig(filename)

# Main routine
def main():
    n_values = [int(x) for x in range(0, 500, 10)]

    print("Measuring average heights...")
    heights = average_heights(n_values)
    plot_graph(
        n_values,
        heights,
        "Average BST Height",
        "N (tree size)",
        "Average Height",
        "bst_height.png",
    )

    print("Measuring insert times...")
    insert_times = average_insert_time(n_values)
    plot_graph(
        n_values,
        insert_times,
        "BST Insert Time",
        "N (tree size)",
        "Average Insert Time (s)",
        "bst_insert_time.png",
    )

    #Show all graphs at once at the very end
    plt.show()

if __name__ == '__main__':
    main()