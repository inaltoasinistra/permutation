import json
import os
import sys


def load_ordering(key):
    """Load static ordering information"""
    path = os.path.join(os.path.dirname(sys.argv[0]), 'data', 'ordering.json')
    with open(path, 'rt') as f:
        obj = json.load(f)
    if key is not None:
        return obj[key]
    return obj


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
