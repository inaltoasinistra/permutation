#!/usr/bin/env python3
# coding=utf-8


def permutation_to_variable_positions(perm):
    """Position of an element counting only the available positions"""
    cpy = perm[:]
    positions = []
    for i in range(len(perm)-1):
        pos = cpy.index(i)
        positions.append(pos)
        del cpy[pos]
    return positions


def permutation_to_integer(perm):
    """Permutations (0÷n-1) to integer"""
    positions = permutation_to_variable_positions(perm)
    h = 1
    w = 1
    integer = 0
    for p in positions[::-1]:
        integer += p * w
        h += 1
        w *= h
    return integer


def integer_to_permutation(integer):
    pass
