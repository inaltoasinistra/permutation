"""
First rule: Don't Roll Your Own Cryptography
"""
from hashlib import sha512


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


def crypt(data, password):
    """Return encrypted or decrypted data"""
    key = get_key(password)[:len(data)]
    if len(data) != len(key):
        raise ValueError('Data length is greater than 64 bytes')
    res = []
    for d, k in zip(data, key):
        res.append(d ^ k)
    return bytes(res)


__all__ = [
    'crypt'
]
