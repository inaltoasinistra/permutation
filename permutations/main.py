#!/usr/bin/env python3

"""
usage:
    main.py encode
    main.py decode
    main.py help
"""
from getpass import getpass
import sys
from ordering import encode, decode

def main():
    if not sys.argv[1:]:
        print(__doc__)
        sys.exit()
    if sys.argv[1] == 'encode':
        seed = getpass('BIP39 seed: ')
    elif sys.argv[1] == 'decode':
        perm = getpass('Cards permutation: ')
    else:
        print(__doc__)
        sys.exit()

if __name__ == "__main__":
    main()
