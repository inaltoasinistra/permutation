# -*- coding: utf-8 -*-
import json
import os
import sys
from lib.mapping import *


def load_ordering(key):
    """Load static ordering information"""

    def f(path):
        """Read json"""
        with open(path, 'rt') as f:
            return json.load(f)
    try:
        path = os.path.join(os.path.dirname(
            sys.argv[0]), 'data', 'ordering.json')
        obj = f(path)
    except FileNotFoundError:
        path = os.path.join('data', 'ordering.json')
        obj = f(path)

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
                assert len(out) == len(names_set), \
                    'labels cannot be an iterator'
                return out
    raise NotImplementedError('Input names are not supported')


def permutation_to_names(permutation, key, description):
    """Convert a list of 0÷n-1 integers to the selected names permutation"""
    ordering = load_ordering(key)
    table = ordering['ordering']
    index = ordering['description'].index(description)
    out = []
    for position in permutation:
        out.append(table[position][index])
    return out


def encode(names):
    """Encode a list of objects to ordering positions"""
    permutation = names_to_permutation(names)
    return permutation_to_integer(permutation)


def decode(ordering_id, description, integer):
    """Encode a list of ordering positions to objects"""
    ordering_len = len(load_ordering(ordering_id)['ordering'])
    permutation = integer_to_permutation(integer, ordering_len)
    return permutation_to_names(permutation, ordering_id, description)


def get_ordering_length(ordering_id):
    """Return the number of elements"""
    return len(load_ordering(ordering_id)['ordering'])

__all__ = [
    "encode",
    "decode",
    "get_ordering_length",
]

if __name__ == "__main__":
    load_ordering('French')
