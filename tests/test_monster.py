#!/usr/bin/python

from unittest.mock import Mock, patch

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

    m = monster.Lizard(start, end, grid)
    g.add(m)
    assert m.alive()
    assert m.rect.x == start_cc.x
    assert m.rect.y == start_cc.y
    assert m.velocity.direction == coord.SOUTH
    assert m.velocity.xVelocity < 1e-10

    # Update should move monster south by 30px.
    expected_y = 30
    ms_per_px = 1000.0 / m.speed
    m.update(ms_per_px * expected_y)
    assert m.coord.x == start_cc.x
    assert abs(m.coord.y - (start_cc.y + expected_y)) < 0.0001

    # Move the last 2px which will move to the base and the monster
    # will no longer be active.
    m.update(ms_per_px * 2)
    assert not m.alive()


def test_monster_injure(fontinit):
    start = coord.Coord(0, 0)
    end = start.south()
    g = pygame.sprite.Group()

    grid = Mock()
    grid.grid_coord_to_client.side_effect = gc_to_cc
    grid.client_coord_to_grid.side_effect = cc_to_gc
    grid.path.return_value = [start, start.south()]

    with patch.object(monster.dice, 'roll') as roll:
        roll.return_value = 18
        m = monster.Orc(start, end, grid)
        g.add(m)
        assert m.alive()

        assert m.health == 18
        m.injure(12)
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


def test_monster_has_money_prob(fontinit):
    start = coord.Coord(0, 0)
    end = start.south()

    grid = Mock()
    grid.grid_coord_to_client.side_effect = gc_to_cc
    grid.client_coord_to_grid.side_effect = cc_to_gc

    def path(*args, **kwargs):
        return [start, start.south()]

    grid.path.side_effect = path

    ms = [monster.Orc(start, end, grid) for _ in range(1000)]
    monied = [m for m in ms if m.money > 0]

    # Expect 2/5 to have money, or about 400. (In about a half-dozen
    # trials this range worked; it's likely that there will be a false
    # failure at some point, but most trials should fall in this
    # range. I wrote this test because I was suspicious after playing
    # that not enough monsters were given gold based on the 2/5 rule.)
    nmonied = len(monied)
    assert nmonied > 360 and nmonied < 440
