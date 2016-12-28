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


class CardsPermutationTest(TestCase):
    """Check the conversion cards permutation <-> integer"""

    CARDS1 = ('Q♠ K♦ 7♦ Q♥ 3♣ 7♠ 10♣ K♥ 5♦ 4♣ 9♣ 3♠ 6♠ J♠ 5♣ A♣ 8♥ A♦ K♣ 6♥ '
              '4♦ A♥ 10♠ A♠ 6♣ J♣ 5♠ 7♣ K♠ 10♦ 5♥ J♦ 8♠ 7♥ J♥ 9♦ 3♦ 9♠ 4♠ Q♣ '
              '2♣ 2♥ 4♥ 9♥ 6♦ Q♦ 8♦ 2♦ 3♥ 10♥ 2♠ 8♣')
    CARDS2 = ('Otto di Cuori, Quattro di Fiori, Asso di Cuori, Dieci di Fiori,'
              'Cinque di Fiori, Sette di Cuori, Fante di Fiori, Otto di Fiori,'
              'Tre di Fiori, Otto di Quadri, Nove di Quadri, Tre di Picche,'
              'Dieci di Cuori, Nove di Cuori, Cinque di Quadri,'
              'Fante di Picche, Fante di Cuori, Re di Fiori, Re di Quadri,'
              'Due di Fiori, Otto di Picche, Asso di Quadri, Dieci di Quadri,'
              'Sei di Quadri, Due di Quadri, Cinque di Picche,'
              'Quattro di Picche, Tre di Quadri, Re di Picche, Due di Picche,'
              'Nove di Picche, Sei di Cuori, Sette di Fiori, Sei di Picche,'
              'Asso di Picche, Sette di Quadri, Nove di Fiori, Sei di Fiori,'
              'Tre di Cuori, Quattro di Quadri, Donna di Cuori,'
              'Dieci di Picche, Due di Cuori, Asso di Fiori, Sette di Picche,'
              'Donna di Quadri, Cinque di Cuori, Donna di Picche,'
              'Donna di Fiori, Quattro di Cuori, Re di Cuori, Fante di Quadri')

    def test_to_permutation(self):
        """Cards to permutation"""

        def test(cards):
            """local operations"""
            split = cards.split(',') if ',' in cards else  cards.split()
            split = [y.strip() for y in split]
            self.assertEqual(len(split), len(set(split)))
            self.assertEqual(len(split), 52)

            permutation = ordering.names_to_permutation(split)
            self.assertEqual(set(permutation), set(range(len(split))))

        test(self.CARDS1)
        test(self.CARDS2)

        cards = 'Not Supported Test'
        with self.assertRaises(NotImplementedError):
            ordering.names_to_permutation(cards.split())

    def test_from_permutation(self):
        """Permutation to cards"""

        permutation = list(range(52))
        names = ordering.permutation_to_names(permutation, 'French', 'Symbols')
        self.assertEqual(len(names), len(permutation))
        self.assertEqual(len(set(names)), len(names))

        random.shuffle(permutation)
        names = ordering.permutation_to_names(permutation, 'French', 'Symbols')
        self.assertEqual(len(names), len(permutation))
        self.assertEqual(len(set(names)), len(names))

    def test_consistency(self):
        """Transform in both directions and check the result"""

        split = self.CARDS1.split()
        permutation = ordering.names_to_permutation(split)
        names = ordering.permutation_to_names(permutation, 'French', 'Symbols')
        self.assertEqual(split, names)

if __name__ == "__main__":
    main()
