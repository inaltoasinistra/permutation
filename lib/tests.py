from unittest import TestCase, main
import random
import os
import sys
import json
from lib import ordering, mapping, mnemonic
from lib.mapping import *
from lib.ordering import *
from lib.mnemonic import *
from lib.encryption import *
from lib.utils import *


def get_test_data():
    """Read data/tests.json"""
    def f(path):
        """Read json"""
        with open(path, 'rt') as f:
            return json.load(f)
    try:
        path = os.path.join(os.path.dirname(sys.argv[0]), 'data', 'tests.json')
        return f(path)
    except FileNotFoundError:
        path = os.path.join('data', 'tests.json')
        return f(path)


class PermutationTestCase(TestCase):
    """
    Add a test to check valid permutation
    """

    def assertPermutation(self, test, valid):
        """test in (valid, reversed(valid)"""
        self.assertIn(test, (valid, list(reversed(valid))))


class Tests(PermutationTestCase):
    """General test"""

    def test_permutation_to_variable_positions(self):
        """Test perm_to_positions"""
        f = mapping.permutation_to_variable_positions
        self.assertEqual(f([0]), [])
        self.assertEqual(f([0, 1]), [0])
        self.assertEqual(f([3, 2, 1, 0]), [3, 2, 1])
        self.assertEqual(f([2, 0, 4, 1, 3]), [1, 2, 0, 1])

    def test_permutation_to_integer(self):
        """Test perm_to_int"""
        def reverse(perm):
            return list(reversed(perm))

        perm = [0, 1, 2, 3, 4, 5]
        self.assertEqual(permutation_to_integer(perm), 0)
        self.assertEqual(permutation_to_integer(reverse(perm)), 0)
        perm = [2, 0, 4, 1, 3]
        self.assertEqual(permutation_to_integer(perm), 37)
        self.assertEqual(permutation_to_integer(reverse(perm)), 37)

    def test_integer_to_variable_positions(self):
        """Test integer_to_variable_positions"""
        f = lambda *args: list(mapping.integer_to_variable_positions(*args))
        self.assertEqual(f(0, 5), [0, 0, 0, 0])
        self.assertEqual(f(119, 5),[4, 3, 2, 1])
        self.assertEqual(f(37, 5), [1, 2, 0, 1])

    def test_variable_to_absolute_positions(self):
        """Test variable_to_absolute_positions"""
        f = mapping.variable_to_absolute_positions
        self.assertEqual(f([0, 0, 0, 0, 0]), [0, 1, 2, 3, 4])
        self.assertEqual(f([1, 2, 0, 1, 0]), [2, 0, 4, 1, 3])

    def test_integer_to_permutation(self):
        """Test perm_to_int"""
        def perms(perm):
            """Return the valid orderings of the permutation"""
            return perm, list(reversed(perm))

        self.assertPermutation(integer_to_permutation(0, 5), [0, 1, 2, 3, 4])
        self.assertPermutation(integer_to_permutation(37, 5), [2, 0, 4, 1, 3])
        with self.assertRaises(ValueError):
            integer_to_permutation(119, 5)


class ProbabilisticTest(PermutationTestCase):
    """Generate random sequences and check mapping"""

    def get_shuffled(self, number):
        """Get number shuffled elements"""
        elements = list(range(number))
        random.shuffle(elements)
        return elements

    def test_sequances(self):
        """Random generation of permutations"""
        tries = 20
        number = 100
        for _ in range(tries):
            elements = self.get_shuffled(number)
            integer = permutation_to_integer(elements)
            permutation = integer_to_permutation(integer, number)
            self.assertPermutation(elements, permutation)

    def test_integers(self):
        """Random generation of integers"""
        tries = 20
        number = 100
        for _ in range(tries):
            integer = random.randint(0, mapping.fact(number) // 2 - 1)
            perm = integer_to_permutation(integer, number)
            check = permutation_to_integer(perm)
            self.assertEqual(integer, check)


class OrderingTest(PermutationTestCase):
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


class CardsPermutationTest(PermutationTestCase):
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


class CardsPermutationIntegerTest(PermutationTestCase):
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

        self.assertEqual(encode(list(reversed(cards))), 0)

        cards = [y[2] for y in ordering.load_ordering('French')['ordering']]
        self.assertEqual(encode(cards), 0)

        cards = [y[0] for y in ordering.load_ordering('test')['ordering']]
        self.assertEqual(encode(cards), 0)

    def test_from_integer(self):
        """Integer to cards"""
        cards = decode('French', 'Symbols', self.DATA['cards1_encoded'])
        self.assertPermutation(cards, self.DATA['cards1'].split())

        cards = decode('French', 'Italian', self.DATA['cards2_encoded'])
        split = [y.strip() for y in self.DATA['cards2'].split(',')]
        self.assertPermutation(cards, split)

        # Decode 0

        split = [y[0] for y in ordering.load_ordering('French')['ordering']]
        self.assertPermutation(decode('French', 'Symbols', 0), split)

        split = [y[2] for y in ordering.load_ordering('French')['ordering']]
        self.assertPermutation(decode('French', 'Italian', 0), split)

        split = [y[0] for y in ordering.load_ordering('test')['ordering']]
        self.assertPermutation(decode('test', 'test', 0), split)

    def test_back_and_forth(self):
        """Check both directions. Cards -> integer -> cards"""
        def test(cards_in, ordering_id, description):
            """Local operations"""
            integer = encode(cards_in)
            cards_out = decode(ordering_id, description, integer)
            self.assertPermutation(cards_in, cards_out)

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
        for integer in range(mapping.fact(number) // 2):
            perm = tuple(decode(ordering_id, description, integer))
            self.assertNotIn(perm, permutations)
            permutations.add(perm)
        self.assertEqual(len(permutations), mapping.fact(number) // 2)


class MnemonicTest(PermutationTestCase):
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


class EncryptionTest(PermutationTestCase):
    """Test encryption and decryption"""

    HEADER_LENGTH = 1

    def check(self, data, password):
        """Check the condition"""
        ctext = crypt(data, password)
        self.assertEqual(crypt(ctext, password), data)
        self.assertEqual(len(data), len(ctext))

        # header
        ctext = crypt(data, password, add_header=True)
        self.assertEqual(crypt(ctext, password, check_header=True), data)
        self.assertEqual(len(data), len(ctext) - self.HEADER_LENGTH)

    def test_back_and_forth(self):
        """Encrypt end decrypt"""
        password = 'password'
        data = b'\x22' * (64 - self.HEADER_LENGTH)
        self.check(data, password)
        password = '50:passw0rd'
        data = bytes([random.getrandbits(8) for _ in range(19)])
        self.check(data, password)
        data = bytes([random.getrandbits(8) for _ in range(18)])
        self.check(data, password)
        data = bytes([random.getrandbits(8) for _ in range(28)])
        self.check(data, password)
        data = bytes([random.getrandbits(8) for _ in range(27)])
        self.check(data, password)
        data = bytes(u'ß', 'utf-8')
        self.check(data, password)
        data = b'\x22' * 100
        with self.assertRaises(ValueError):
            self.check(data, password)
        with self.assertRaises(ValueError):
            crypt(b'\x0a123', password, check_header=True)


class IntegerBytesConversionTest(PermutationTestCase):
    """ Test utils functions """

    def check_int(self, integer):
        """back and forth"""
        data = integer_to_bytes(integer, 4)
        self.assertEqual(integer, bytes_to_integer(data))

    def check_bytes(self, data):
        """back and forth"""
        length = len(data)
        integer = bytes_to_integer(data)
        self.assertEqual(data, integer_to_bytes(integer, length))

    def test_back_and_forth(self):
        """Test conversions"""
        self.check_int(1000)
        self.check_int(100000)
        self.check_int(10000000)

        self.check_bytes(b'1234567890')
        self.check_bytes(b'H' * 100)

    def test_conversion(self):
        """Test fixed values"""
        self.assertEqual(1, bytes_to_integer(b'\x01'))
        self.assertEqual(0x122233, bytes_to_integer(b'\x12\x22\x33'))

        self.assertEqual(b'\x00', integer_to_bytes(0, 1))
        self.assertEqual(
            b'\x00\x11\x22\x33\x44', integer_to_bytes(0x11223344, 5))

if __name__ == "__main__":
    main()