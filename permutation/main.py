#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""
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
import sys
import argparse
from math import log2, floor
from getpass import getpass
from ordering import encode, decode, get_ordering_length
from mnemonic import mnemonic_to_integer, integer_to_mnemonic
from encryption import crypt
from utils import integer_to_bytes, bytes_to_integer


def fact(y):
    """Factorial"""
    if y:
        return y * fact(y - 1)
    return 1


def get_passwd():
    """Wrap getpass"""
    password = None
    while True:
        password = getpass('Insert the password: ')
        confirm = getpass('Confirm the password: ')
        if password != confirm:
            print('Retry')
        else:
            break
    return password

    
def crypt_data(integer, args):
    """Do encrypt operations"""
    mode = args.mode
    password = get_passwd()

    length = int(floor(log2(fact(get_ordering_length(args.ordering))) / 8))
    if mode == 'encode':
        length -= 1
    data = integer_to_bytes(integer, length)
    data = crypt(data, password, mode == 'encode', mode == 'decode')
    integer = bytes_to_integer(data)

    return integer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', type=str,
                        help='encode or decode')
    parser.add_argument('--ordering', dest='ordering', type=str,
                        default='French',
                        help='objects of the permutation')
    parser.add_argument('--labels', dest='labels', type=str,
                        default='Symbols',
                        help='~ of objects')
    parser.add_argument('--language', dest='language', type=str,
                        default='english',
                        help='~ of the seed wordlist')

    args = parser.parse_args()

    if args.mode == 'encode':
        seed = input('BIP39 seed: ')
        integer = mnemonic_to_integer(seed.split())
        integer = crypt_data(integer, args)
        print(' '.join(decode(args.ordering, args.labels, integer)))
    elif args.mode == 'decode':
        perm = input('Cards permutation: ')
        integer = encode(perm.split())
        integer = crypt_data(integer, args)
        print(' '.join(integer_to_mnemonic(integer, args.language)))
    else:
        print(__doc__)
        sys.exit()

if __name__ == "__main__":
    main()
