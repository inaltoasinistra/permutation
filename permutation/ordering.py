# -*- coding: utf-8 -*-
import os
from permutation.mapping import *


def get_abs_path(relative):
    """Return a valid path"""
    for path in (
            os.path.join(os.path.dirname(__file__), relative), relative):
        if os.path.exists(path):
            return path
    raise ValueError('Path "%s" not found' % relative)


def load_ordering(key):
    """Load static ordering information"""

    path = get_abs_path(os.path.join('data', 'ordering', '%s.txt' % key))
    with open(path, 'rt') as f:
        return [line.strip() for line in f.readlines()]


def load_orderings(yield_keys=False):
    """Load all orderings"""
    path = get_abs_path(os.path.join('data', 'ordering'))
    for name in os.listdir(path):
        if name.endswith('.txt'):
            ordering = load_ordering(name[:-4])
            if yield_keys:
                yield name[:-4], ordering
            else:
                yield ordering


def names_to_permutation(labels):
    """Convert a list of names to a permutation (listo of o÷n-1 integers)"""
    names_set = set(labels)
    for ordering in load_orderings():
        if set(ordering) == names_set:
            out = []
            for label in labels:
                out.append(ordering.index(label))
            assert len(out) == len(names_set), 'Names decoding error'
            return out
    raise NotImplementedError('Input names are not supported')


def permutation_to_names(permutation, key):
    """Convert a list of 0÷n-1 integers to the selected names permutation"""
    ordering = load_ordering(key)
    out = []
    for position in permutation:
        out.append(ordering[position])
    return out


def encode(names):
    """Encode a list of objects to ordering positions"""
    permutation = names_to_permutation(names)
    return permutation_to_integer(permutation)


def decode(ordering_key, integer):
    """Encode a list of ordering positions to objects"""
    ordering_len = len(load_ordering(ordering_key))
    permutation = integer_to_permutation(integer, ordering_len)
    return permutation_to_names(permutation, ordering_key)


def get_ordering_length(ordering_key):
    """Return the number of elements"""
    return len(load_ordering(ordering_key))

__all__ = [
    "encode",
    "decode",
    "get_ordering_length",
]

if __name__ == "__main__":
    load_ordering('French')
