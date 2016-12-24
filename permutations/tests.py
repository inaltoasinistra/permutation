from unittest import TestCase, main
from permutations import *


class Tests(TestCase):
    """General test"""

    def test_permutation_to_variable_positions(self):
        """Test perm_to_positions"""
        self.assertEqual(permutation_to_variable_positions([0]), [])
        self.assertEqual(permutation_to_variable_positions([0, 1]), [0])
        self.assertEqual(permutation_to_variable_positions([3, 2, 1, 0]), [3, 2, 1])
        self.assertEqual(permutation_to_variable_positions(
            [2, 0, 4, 1, 3]), [1, 2, 0, 1])

    def test_permutation_to_integer(self):
        """Test perm_to_int"""
        self.assertEqual(permutation_to_integer([0]), 0)
        self.assertEqual(permutation_to_integer([0, 1, 2, 3, 4, 5]), 0)
        self.assertEqual(permutation_to_integer([2, 0, 4, 1, 3]), 37)

    def test_integer_to_permutation(self):
        """Test perm_to_int"""
        # self.assertEqual(integer_to_permutation(0), [])
        # self.assertEqual(integer_to_permutation([0, 1, 2, 3, 4, 5]), 0)
        # self.assertEqual(integer_to_permutation([2, 0, 4, 1, 3]), 37)


if __name__ == "__main__":
    main()
