
def integer_to_bytes(integer, length):
    return integer.to_bytes(length, 'big')


def bytes_to_integer(data):
    return int.from_bytes(data, 'big')
