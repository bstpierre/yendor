#!/usr/bin/python

import math

import pygame
import pygame.freetype
import pytest

from yendor import (
    bullet,
    coord,
    monster,
    velocity,
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

    assert m.health == 1000
    m.injure(999)
    assert m.health == 1
    assert m.alive()
    m.injure(1)
    assert m.health == 0
    assert not m.alive()
