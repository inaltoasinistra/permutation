#!/usr/bin/env python3

"""
usage:
    main.py encode
    main.py decode
    main.py help

e.g. tragedia malinteso attorno lacuna invece michele produrre vispo
     brillante buio valgo umano
     A♥ 2♥ 3♥ 4♥ 5♥ 6♥ 7♥ 8♥ 9♥ 10♥ J♥ Q♥ K♥ A♦ 2♦ 3♦ 4♦ 4♠ 5♠ 8♠ 3♣
     4♣ 8♦ 7♦ 2♣ K♠ Q♠ 7♠ J♦ 9♠ 9♣ A♣ Q♦ 5♦ 10♠ 3♠ K♦ K♣ 10♦ 10♣ 2♠
     9♦ J♠ 8♣ A♠ Q♣ 6♠ J♣ 6♦ 6♣ 7♣ 5♣
"""
from getpass import getpass
import sys

from ordering import encode, decode
from mnemonic import mnemonic_to_integer, integer_to_mnemonic

def main():
    if not sys.argv[1:]:
        print(__doc__)
        sys.exit()
    if sys.argv[1] == 'encode':
        seed = getpass('BIP39 seed: ')
        integer = mnemonic_to_integer(seed.split())
        print(' '.join(decode('French', 'Symbols', integer)))
    elif sys.argv[1] == 'decode':
        perm = getpass('Cards permutation: ')
        integer = encode(perm.split())
        print(' '.join(integer_to_mnemonic(integer, 'english')))
    else:
        print(__doc__)
        sys.exit()

if __name__ == "__main__":
    main()
