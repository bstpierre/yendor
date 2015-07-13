#!/usr/bin/python

from unittest.mock import Mock

import pygame
import pygame.freetype
import pytest

from yendor import (
    coord,
    monster,
    )


# FIXME: de-dupe with test_dungeon.py
@pytest.fixture
def fontinit():
    pygame.init()
    pygame.freetype.init()


mult = 32


def gc_to_cc(gc):
    return coord.Coord(gc.x * 32, gc.y * 32)


def cc_to_gc(cc):
    return coord.Coord(int(cc.x / 32), int(cc.y / 32))


def test_monster_update(fontinit):
    start = coord.Coord(3, 0)
    start_cc = gc_to_cc(start)
    end = start.south().south()
    g = pygame.sprite.Group()

    grid = Mock()
    grid.grid_coord_to_client.side_effect = gc_to_cc
    grid.client_coord_to_grid.side_effect = cc_to_gc
    grid.path.return_value = [start, start.south()]

    m = monster.Dwarf(start, end, grid)
    g.add(m)
    assert m.alive()
    assert m.rect.x == start_cc.x
    assert m.rect.y == start_cc.y
    assert m.velocity.direction == coord.SOUTH
    assert m.velocity.xVelocity < 1e-10

    # 1s update, should move south 30px
    # XXX - move hardcoded 30px/s velocity out of monster.py
    m.update(1000)
    assert m.coord.x == start_cc.x
    assert m.coord.y == start_cc.y + 30

    # Move the last 2px (1/15s) which will move to the base and the
    # monster will no longer be active.
    m.update(1/15.0 * 1000)
    assert not m.alive()


def test_monster_injure(fontinit):
    start = coord.Coord(0, 0)
    end = start.south()
    g = pygame.sprite.Group()

    grid = Mock()
    grid.grid_coord_to_client.side_effect = gc_to_cc
    grid.client_coord_to_grid.side_effect = cc_to_gc
    grid.path.return_value = [start, start.south()]

    m = monster.Orc(start, end, grid)
    g.add(m)
    assert m.alive()

    assert m.health == 30
    m.injure(24)
    assert m.health == 6
    assert m.alive()
    m.injure(6)
    assert m.health == 0
    assert not m.alive()


def test_monster_status_message(fontinit):
    start = coord.Coord(0, 0)
    end = start.south()

    grid = Mock()
    grid.grid_coord_to_client.side_effect = gc_to_cc
    grid.client_coord_to_grid.side_effect = cc_to_gc
    grid.path.return_value = [start, start.south()]

    m = monster.Orc(start, end, grid)
    m.health = 1234
    gs = Mock()
    gs.grid = Mock()
    gs.grid.client_coord_to_grid.return_value = "XYZ"
    msg = m.status_message(gs)
    assert "Orc @ XYZ" in msg
    assert "health: 1234" in msg
