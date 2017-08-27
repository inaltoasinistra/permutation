"""
First rule: Don't Roll Your Own Cryptography
"""
import os
import scrypt
import xxtea
from math import log2
from random import getrandbits
from permutation.ordering import get_ordering_length
from permutation.mapping import fact
from permutation.utils import log, integer_to_bytes, bytes_to_integer, b2x

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


def encoding_len(max_len):
    """Compute the len of the clear data
    Round to multiple of 4
    Remove header: clear text, xxtea
    """

    def simulate(length):
        """Simulate enc. Doc only"""
        length += 2  # Add header
        if length % 4 == 0:
            return max(length, 8)
        return max((length // 4 + 1) * 4, 8)

    return max_len // 4 * 4 - 2


def crypt_data(integer, mode, ordering, password):
    """Do encrypt operations"""

    # available length
    max_bits = int(log2(
        fact(get_ordering_length(ordering)) // 2
    ))
    length = max_bits // 8
    useless_bits = max_bits % 8
    assert 0 <= useless_bits <= 7
    # useless_bits: the most significant bits that will be encoded
    # in the permutation. They are less than a byte so the encryption function
    # do not use them.
    # We assign a random value to them to preserve plausible deniability

    max_len = length
    if mode == 'encode':
        length = encoding_len(length)
    elif mode == 'decode':
        if useless_bits:
            # If there is padding we need one more byte to decode it
            length += 1
    data = integer_to_bytes(integer, length)
    log('input in bytes', b2x(data), len(data))
    if mode == 'encode':
        data = crypt(data, password, True)
        useless_bytes = max_len - len(data)
        assert len(data) <= max_len, (
            'Encrypted data is too long (%d, max %d)' % (len(data), max_len))
        assert 0 < useless_bytes < 4, (
            'useless_bytes not valid (%d)' % (useless_bytes, ))
        if useless_bytes:
            # Add bytes padding
            padding = bytes([getrandbits(8) for _ in range(useless_bytes)])
            data = padding + data
        if useless_bits:
            padding = bytes([getrandbits(useless_bits)])
            log('useless_bits', useless_bits)
            log('len(data1)', len(data))
            log('padding', padding[0])
            data = padding + data
    elif mode == 'decode':
        # Remove padding bits
        if useless_bits:
            data = data[1:]
            log('padding bits removed', b2x(data), len(data))
        # Remove padding bytes
        if len(data) % 4:
            data = data[len(data) % 4:]
        data = decrypt(data, password, True)
    log('output in bytes', b2x(data), len(data))
    integer = bytes_to_integer(data)
    assert log2(integer) <= max_bits, (
        'Encrypted integer is too long (%.2f, max %d)' % (
            log2(integer), max_bits))

    if mode == 'encode':
        used = log2(integer)
        total = log2(fact(get_ordering_length(ordering)) // 2)
        log('Used bits %.2f - %.2f = %.2f' % (total, used, total - used))
        # If we leave suspicious null bits on the right (or in other places)
        # plausible deniability is lost

    return integer


__all__ = [
    'crypt_data'
]
