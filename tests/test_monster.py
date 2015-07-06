#!/usr/bin/python

from unittest.mock import Mock

import pygame
import pygame.freetype
import pytest

from yendor import (
    monster,
    )


@pytest.fixture
def fontinit():
    pygame.init()
    pygame.freetype.init()


def test_monster_update(fontinit):
    m = monster.Dwarf()
    assert m.rect.x == 256
    assert m.rect.y == 0

    # 1s update, should move south 10px
    # XXX - move hardcoded 30px/s velocity out of monster.py
    m.update(1000)
    assert m.rect.x == 256
    assert m.rect.y == 30

    # NOTE: monster will be inactive after that update because the
    # path was empty.


def test_monster_injure(fontinit):
    g = pygame.sprite.Group()
    m = monster.Orc()
    g.add(m)
    assert m.alive()

    assert m.health == 25
    m.injure(24)
    assert m.health == 1
    assert m.alive()
    m.injure(1)
    assert m.health == 0
    assert not m.alive()

def test_monster_status_message(fontinit):
    m = monster.Orc()
    m.health = 1234
    gs = Mock()
    gs.grid = Mock()
    gs.grid.client_coord_to_grid.return_value = "XYZ"
    msg = m.status_message(gs)
    assert "Orc @ XYZ" in msg
    assert "health: 1234" in msg
