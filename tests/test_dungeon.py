#!/usr/bin/python

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


def test_dungeon_load(fontinit):
    grid = Mock()

    expected_spawn = coord.Coord(1, 0)
    expected_base = coord.Coord(12, 14)

    def gc_to_cc(*args, **kwargs):
        return coord.Coord(0, 0)

    grid.grid_coord_to_client.side_effect = gc_to_cc

    d = dungeon.Dungeon.load(grid, 'levels/1.dungeon')
    assert d.spawn_origin == expected_spawn
    assert d.base == expected_base


def test_dungeon_message(fontinit):
    w1 = Mock()
    w1.spawned = 3
    w1.count = 4
    w2 = Mock()
    w2.spawned = 5
    w2.count = 6
    d = dungeon.Dungeon([w1, w2])

    msg = d.status_message()
    assert "1/2" in msg
    assert "3/4" in msg

    d.cur_wave += 1
    msg = d.status_message()
    assert "2/2" in msg
    assert "5/6" in msg

    d.cur_wave += 1
    msg = d.status_message()
    assert "2/2" in msg
    assert "5/6" in msg


def test_dungeon_update():
    gs = Mock()
    w1 = Mock()
    w1.active = True
    w2 = Mock()
    w2.active = True
    d = dungeon.Dungeon([w1, w2])

    # Can update a bunch of times, no advancing until the first wave
    # becomes inactive.
    for i in range(30):
        d.update(gs)
        assert d.cur_wave == 0
        assert w1.update.call_count == i + 1
        assert w2.update.call_count == 0

    w1.active = False
    d.update(gs)
    assert w1.update.call_count == i + 2
    assert d.cur_wave == 1

    w1.update.called = False
    for j in range(30):
        d.update(gs)
        assert d.cur_wave == 1
        assert w1.update.call_count == i + 2
        assert w2.update.call_count == j + 1
