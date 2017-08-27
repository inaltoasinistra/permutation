import sys

VERBOSITY = False


def integer_to_bytes(integer, length):
    return integer.to_bytes(length, 'big')


def bytes_to_integer(data):
    return int.from_bytes(data, 'big')


def b2x(bb):
    return '0x' + ''.join(['%02x' % y for y in bb])


def log(*args):
    """ print to stderr """
    if VERBOSITY:
        print(*args, file=sys.stderr)
