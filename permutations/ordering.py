import json
import os
import sys


def load_ordering(key, directory=None):
    """Load static ordering information"""
    if directory is None:
        path = os.path.join(
            os.path.dirname(sys.argv[0]), 'data', 'ordering.json')
    else:
        path = os.path.join(
            os.path.dirname(directory), 'data', 'ordering.json')
    with open(path, 'rt') as f:
        obj = json.load(f)
    if key is not None:
        return obj[key]
    return obj


def column_iter(matrix):
    """Iter over the columns"""
    if matrix:
        for i in range(len(matrix[0])):
            yield [y[i] for y in matrix]


def names_to_permutation(labels):
    """Convert a list of names to a permutation (listo of o÷n-1 integers)"""
    names_set = set(labels)
    for ordering in load_ordering(None).values():
        data = ordering['ordering']
        for ord_labels in column_iter(data):
            if set(ord_labels) == names_set:
                out = []
                for label in labels:
                    out.append(ord_labels.index(label))
                return out
    raise NotImplementedError('Input names are not supported')


def permutation_to_names(permutation, key, description):
    """Convert a list of 0÷n-1 integers to the selected names permutation"""


def encode(ordering_id, objects):
    """Encode a list of objects to ordering positions"""


def decode(ordering_id, positions):
    """Encode a list of ordering positions to objects"""


__all__ = [
    "encode",
    "decode",
]

if __name__ == "__main__":
    load_ordering('French')
