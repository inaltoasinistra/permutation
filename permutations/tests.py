from unittest import TestCase, main
import random
import os
import sys
import json
from permint import *
import ordering
from ordering import *
import permint
from mnemonic import *
import mnemonic


def get_test_data():
    """Read data/tests.json"""
    path = os.path.join(os.path.dirname(sys.argv[0]), 'data', 'tests.json')
    with open(path, 'rt') as f:
        return json.load(f)


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
            for column in ordering.column_iter(current):
                # Skip placeholder columns
                if set(column) != {''}:
                    self.assertEqual(len(set(column)), len(current))


class CardsPermutationTest(TestCase):
    """Check the conversion cards permutation <-> integer"""
    DATA = get_test_data()

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

        test(self.DATA['cards1'])
        test(self.DATA['cards2'])

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

        split = self.DATA['cards1'].split()
        permutation = ordering.names_to_permutation(split)
        names = ordering.permutation_to_names(permutation, 'French', 'Symbols')
        self.assertEqual(split, names)


class CardsPermutationIntegerTest(TestCase):
    """Cards to integer back and forth"""
    DATA = get_test_data()

    def test_to_integer(self):
        """cards to integer"""
        integer = encode(self.DATA['cards1'].split(' '))
        self.assertEqual(integer, self.DATA['cards1_encoded'])

        integer = encode([y.strip() for y in self.DATA['cards2'].split(',')])
        self.assertEqual(integer, self.DATA['cards2_encoded'])

        # The ordering of cards is encoded to 0
        cards = [y[0] for y in ordering.load_ordering('French')['ordering']]
        self.assertEqual(encode(cards), 0)

        self.assertEqual(encode(list(reversed(cards))), permint.fact(52) - 1)

        cards = [y[2] for y in ordering.load_ordering('French')['ordering']]
        self.assertEqual(encode(cards), 0)

        cards = [y[0] for y in ordering.load_ordering('test')['ordering']]
        self.assertEqual(encode(cards), 0)

    def test_from_integer(self):
        """Integer to cards"""
        cards = decode('French', 'Symbols', self.DATA['cards1_encoded'])
        self.assertEqual(cards, self.DATA['cards1'].split())

        cards = decode('French', 'Italian', self.DATA['cards2_encoded'])
        split = [y.strip() for y in self.DATA['cards2'].split(',')]
        self.assertEqual(cards, split)

        # Decode 0

        split = [y[0] for y in ordering.load_ordering('French')['ordering']]
        self.assertEqual(decode('French', 'Symbols', 0), split)

        split = [y[2] for y in ordering.load_ordering('French')['ordering']]
        self.assertEqual(decode('French', 'Italian', 0), split)

        split = [y[0] for y in ordering.load_ordering('test')['ordering']]
        self.assertEqual(decode('test', 'test', 0), split)

        # Decode fact(n) - 1

        number = len(ordering.load_ordering('French')['ordering'])
        integer = permint.fact(number) - 1

        split = [y[0] for y in ordering.load_ordering('French')['ordering']]
        self.assertEqual(decode('French', 'Symbols', integer), split[::-1])

        split = [y[2] for y in ordering.load_ordering('French')['ordering']]
        self.assertEqual(decode('French', 'Italian', integer), split[::-1])

        # FIXME
        # split = [y[0] for y in ordering.load_ordering('test')['ordering']]
        # self.assertEqual(decode('test', 'test', integer), split[::-1])

    def test_back_and_forth(self):
        """Check both directions. Cards -> integer -> cards"""
        def test(cards_in, ordering_id, description):
            """Local operations"""
            integer = encode(cards_in)
            cards_out = decode(ordering_id, description, integer)
            self.assertEqual(cards_in, cards_out)

        split = [y.strip() for y in self.DATA['cards1'].split(' ')]
        for _ in range(100):
            test(split, 'French', 'Symbols')
            random.shuffle(split)

        split = [y.strip() for y in self.DATA['cards2'].split(',')]
        for _ in range(100):
            test(split, 'French', 'Italian')
            random.shuffle(split)

    def test_mapping(self):
        """Test that all permutations are different"""
        ordering_id = 'test'
        description = 'test'
        permutations = set()
        number = len(ordering.load_ordering(ordering_id)['ordering'])
        for integer in range(permint.fact(number)):
            perm = tuple(decode(ordering_id, description, integer))
            self.assertNotIn(perm, permutations)
            permutations.add(perm)
        self.assertEqual(len(permutations), permint.fact(number))


class MnemonicTest(TestCase):
    """Test consistency of mnemonic conversion"""
    DATA = get_test_data()
    eng = [y for y in DATA['mnemonics_eng'] if y[0] != '#']
    ita = [y for y in DATA['mnemonics_ita'] if y[0] != '#']

    def test_to_integer(self):
        """Test mnemonic to integer using the test data"""
        for words in self.eng + self.ita:
            split = words[0].split()
            self.assertEqual(mnemonic_to_integer(split), words[1])

    def test_from_integer(self):
        """Test integer to mnemonic using the test data"""
        for words in self.eng:
            split = words[0].split()
            self.assertEqual(integer_to_mnemonic(words[1], 'english'), split)

        for words in self.ita:
            split = words[0].split()
            self.assertEqual(integer_to_mnemonic(words[1], 'italian'), split)

    def test_back_and_forth(self):
        """Back and forth on mnemonics of test data"""

        for words in self.eng:
            split = words[0].split()
            self.assertEqual(
                split, integer_to_mnemonic(mnemonic_to_integer(split)), split)

        for words in self.ita:
            split = words[0].split()
            print(split)
            print(mnemonic_to_integer(split))
            self.assertEqual(
                split, integer_to_mnemonic(
                    mnemonic_to_integer(split), 'italian'), split)

    def test_length(self):
        """Supported length"""
        for words in self.eng + self.ita:
            split = words[0].split()
            self.assertIn(len(split), mnemonic.WORDS_NUMBER, split)

    def test_words_length(self):
        """Check input"""

        with self.assertRaises(ValueError):
            mnemonic_to_integer(['boring', 'drum'])

if __name__ == "__main__":
    main()
