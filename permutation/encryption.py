"""
First rule: Don't Roll Your Own Cryptography
"""
from hashlib import sha512

VERSION = 1


def get_key(password):
    """ utf-8 password to 64 byte of key """
    try:
        cycles = int(password.split(':')[0])
        if cycles <= 0:
            raise ValueError
    except ValueError:
        cycles = 1000000
    key = bytes(password, 'utf-8')
    for _ in range(cycles):
        key = sha512(key).digest()
    return key


def get_version(first_byte):
    """Get version as integer"""
    return first_byte & 0xf


def add_head(data):
    return bytes([VERSION]) + data


def check_head(data):
    """Header related manipulation"""
    if get_version(data[0]) == VERSION:
        return data[1:]
    raise ValueError('Version not supported')


def crypt(data, password, add_header=False, check_header=False):
    """Return encrypted or decrypted data"""
    assert not add_header or not check_header, 'You cannot set both'
    if add_header:
        data = add_head(data)

    key = get_key(password)[:len(data)]
    if len(data) != len(key):
        raise ValueError('Data length is greater than 64 bytes')
    res = []
    for d, k in zip(data, key):
        res.append(d ^ k)
    data = bytes(res)
    if check_header:
        return check_head(data)
    return data


__all__ = [
    'crypt'
]
