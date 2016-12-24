from unittest import TestCase, main
import random
from permint import *
import ordering
from ordering import *
import permint


class Tests(TestCase):
    """General test"""

    def test_permutation_to_variable_positions(self):
        """Test perm_to_positions"""
        f = permint.permutation_to_variable_positions
        self.assertEqual(f([0]), [])
        self.assertEqual(f([0, 1]), [0])
        self.assertEqual(f([3, 2, 1, 0]), [3, 2, 1])
        self.assertEqual(f([2, 0, 4, 1, 3]), [1, 2, 0, 1])

    def test_permutation_to_integer(self):
        """Test perm_to_int"""
        self.assertEqual(permutation_to_integer([0]), 0)
        self.assertEqual(permutation_to_integer([0, 1, 2, 3, 4, 5]), 0)
        self.assertEqual(permutation_to_integer([2, 0, 4, 1, 3]), 37)

    def test_integer_to_variable_positions(self):
        """Test integer_to_variable_positions"""
        f = lambda *args: list(permint.integer_to_variable_positions(*args))
        self.assertEqual(f(0, 5), [0, 0, 0, 0])
        self.assertEqual(f(119, 5),[4, 3, 2, 1])
        self.assertEqual(f(37, 5), [1, 2, 0, 1])

    def test_variable_to_absolute_positions(self):
        """Test variable_to_absolute_positions"""
        f = permint.variable_to_absolute_positions
        self.assertEqual(f([0, 0, 0, 0, 0]), [0, 1, 2, 3, 4])
        self.assertEqual(f([1, 2, 0, 1, 0]), [2, 0, 4, 1, 3])

    def test_integer_to_permutation(self):
        """Test perm_to_int"""
        self.assertEqual(integer_to_permutation(0, 5), [0, 1, 2, 3, 4])
        self.assertEqual(integer_to_permutation(119, 5), [4, 3, 2, 1, 0])
        self.assertEqual(integer_to_permutation(37, 5), [2, 0, 4, 1, 3])


class ProbabilisticTest(TestCase):
    """Generate random sequnces and check mapping"""

    def get_shuffled(self, number):
        """Get number shuffled elements"""
        elements = list(range(number))
        random.shuffle(elements)
        return elements

    def test_random(self):
        """Random generation of permutations"""
        tries = 20
        number = 100
        for _ in range(tries):
            elements = self.get_shuffled(number)
            integer = permutation_to_integer(elements)
            permutation = integer_to_permutation(integer, number)
            self.assertEqual(elements, permutation)


class OrderingTest(TestCase):
    """Check properties of ordering data"""

    def test_uniqueness(self):
        """The names of objects are unique"""
        data = ordering.load_ordering(None)
        for dataset in data.values():
            current = dataset['ordering']
            self.assertEqual(len(set([y[0] for y in current])), len(current))
            self.assertEqual(len(set([y[2] for y in current])), len(current))

if __name__ == "__main__":
    main()
