from unittest import TestCase, main
from permint import *


class Tests(TestCase):
    """General test"""

    def test_permutation_to_variable_positions(self):
        """Test perm_to_positions"""
        self.assertEqual(permutation_to_variable_positions([0]), [])
        self.assertEqual(permutation_to_variable_positions([0, 1]), [0])
        self.assertEqual(permutation_to_variable_positions(
            [3, 2, 1, 0]), [3, 2, 1])
        self.assertEqual(permutation_to_variable_positions(
            [2, 0, 4, 1, 3]), [1, 2, 0, 1])

    def test_permutation_to_integer(self):
        """Test perm_to_int"""
        self.assertEqual(permutation_to_integer([0]), 0)
        self.assertEqual(permutation_to_integer([0, 1, 2, 3, 4, 5]), 0)
        self.assertEqual(permutation_to_integer([2, 0, 4, 1, 3]), 37)

    def test_integer_to_variable_positions(self):
        """Test integer_to_variable_positions"""
        f = lambda *args: list(integer_to_variable_positions(*args))
        self.assertEqual(f(0, 5), [0, 0, 0, 0])
        self.assertEqual(f(119, 5),[4, 3, 2, 1])
        self.assertEqual(f(37, 5), [1, 2, 0, 1])

    def test_variable_to_absolute_positions(self):
        """Test variable_to_absolute_positions"""
        f = variable_to_absolute_positions
        self.assertEqual(f([0, 0, 0, 0, 0]), [0, 1, 2, 3, 4])
        self.assertEqual(f([1, 2, 0, 1, 0]), [2, 0, 4, 1, 3])

    def test_integer_to_permutation(self):
        """Test perm_to_int"""
        self.assertEqual(integer_to_permutation(0, 5), [0, 1, 2, 3, 4])
        self.assertEqual(integer_to_permutation(119, 5), [4, 3, 2, 1, 0])
        self.assertEqual(integer_to_permutation(37, 5), [2, 0, 4, 1, 3])


if __name__ == "__main__":
    main()
