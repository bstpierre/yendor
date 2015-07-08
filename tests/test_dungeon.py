#!/usr/bin/python

import math
from unittest.mock import Mock

import pygame
import pygame.freetype
import pytest

from yendor import (
    coord,
    dungeon,
    )


@pytest.fixture
def fontinit():
    pygame.init()
    pygame.freetype.init()


def test_dungeon(fontinit):
    gs = Mock()
    gs.grid = Mock()

    expected_spawn = coord.Coord(1, 0)
    expected_base = coord.Coord(12, 14)
    coords = [expected_spawn, expected_base]

    def gc_to_cc(*args, **kwargs):
        return coord.Coord(0, 0)

    gs.grid.grid_coord_to_client.side_effect = gc_to_cc

    d = dungeon.Dungeon.load(gs, 'levels/1.dungeon')
    assert d.spawn_origin == expected_spawn
    assert d.base == expected_base
