#!/usr/bin/python

"""
Manage XP levels and player capabilities.
"""

from . import (
    tower,
    )


class Level:
    def __init__(self, n, towers):
        self.level = n
        self.towers = towers


# FIXME: figure out a way to lock tower upgrades
_levels = {
    1: Level(1, [tower.Slingshot]),
    2: Level(2, [tower.Slingshot, tower.DartTower]),
    3: Level(3, [tower.Slingshot, tower.DartTower]),
    }


def get_level(xp):
    """Return the Level corresponding to an amount of XP."""
    thresholds = (
        # level 1 requires 0 xp
        0,
        # level 2 requires 100 xp
        100,
        # level 3 requires 250 xp
        250,
        )

    level = 0
    for t in thresholds:
        if xp >= t:
            level += 1
        else:
            break

    level = max(1, level)
    return _levels[level]
