import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

from bst import *

class BSTTests(unittest.TestCase):
    def test_example_fun(self):
        self.assertEqual(True, example_fun(34))
        self.assertEqual(False,example_fun(1423))

if (__name__ == '__main__'):
    unittest.main()
