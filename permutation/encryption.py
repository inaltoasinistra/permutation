"""
First rule: Don't Roll Your Own Cryptography
"""
import os
import scrypt
import xxtea

VERSION = 1
assert VERSION < 8


def get_key(password):
    """ utf-8 password to 64 byte of key """

    try:
        # 2**14 = 16384
        cycles = min(int(password.split(':')[-1]), 14)
        if cycles <= 0:
            raise ValueError
    except ValueError:
        cycles = 21
    return scrypt.hash(password, 'permutation', N=2**cycles, buflen=16)


def get_version(first_byte):
    """Get version as integer"""
    return first_byte & 0x7


def add_head(data):
    """5 random bits, 3 bit version
    random bits are needed to produce different ciphertexts with the same
    (data, password) couple"""
    return bytes([os.urandom(1)[0] & 0xf8 | VERSION]) + data


def check_head(data):
    """Header related manipulation"""
    if get_version(data[0]) == VERSION:
        return data[1:]
    raise ValueError('Version not supported')


def crypt(data, password, add_header=False):
    """Return encrypted data"""
    if add_header:
        data = add_head(data)

    key = get_key(password)
    return xxtea.encrypt(data, key)


def decrypt(data, password, check_header=False):
    """Return decrypted data"""

    key = get_key(password)
    data = xxtea.decrypt(data, key)

    if check_header:
        return check_head(data)
    return data


__all__ = [
    'crypt',
    'decrypt',
]
