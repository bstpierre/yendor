#!/usr/bin/python

import random


def roll(qty, sides):
    return sum(random.randrange(1, sides + 1) for _ in range(qty))


def chances(qty, out_of):
    """'1 chance in 5' is chances(1, 5)"""
    # Chance succeeds if roll is lower than max.
    return roll(1, out_of) <= qty
