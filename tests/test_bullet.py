#!/usr/bin/python

import math

import pytest

from yendor import (
    bullet,
    coord,
    velocity,
    )


def assert_almost_equals(a, b):
    DELTA = 0.0001
    assert abs(a - b) < DELTA

def test_bullet_update_east():
    v = velocity.Velocity(1000, coord.EAST)
    c = coord.Coord(100, 100)
    b = bullet.Bullet(v, c)

    # Each tick is 1ms, so divide velocity by 1000.
    b.update(10)
    assert b.rect.x == 110
    assert b.rect.y == 100

def test_bullet_update_north():
    v = velocity.Velocity(1000, coord.NORTH)
    c = coord.Coord(100, 100)
    b = bullet.Bullet(v, c)

    # Each tick is 1ms, so divide velocity by 1000.
    b.update(10)
    assert b.rect.x == 100
    assert b.rect.y == 90
