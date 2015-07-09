#!/usr/bin/python

import math

import pytest

from yendor import coord
from yendor import velocity

EAST = 0
NORTHEAST = math.pi / 4.0
NORTH = math.pi / 2.0
NORTHWEST = (3.0 * math.pi) / 4.0
WEST = math.pi
SOUTHWEST = (5.0 * math.pi) / 4.0
SOUTH = (3.0 * math.pi) / 2.0
SOUTHEAST = (7.0 * math.pi) / 4.0


def test_bearing_same():
    c = coord.Coord(0, 0)
    assert c.bearing(c) == coord.EAST
    v = velocity.Velocity(100, c.bearing(c))
    assert v.xVelocity == 100
    assert v.yVelocity == 0


def test_bearing_east():
    c = coord.Coord(0, 0)
    east = coord.Coord(1, 0)
    assert c.bearing(east) == coord.EAST
    assert east.bearing(c) == coord.WEST
    v = velocity.Velocity(100, c.bearing(east))
    assert v.xVelocity == 100
    assert v.yVelocity == 0

    assert c.bearing(c.east()) == coord.EAST


def test_bearing_northeast():
    c = coord.Coord(0, 0)
    northeast = coord.Coord(1, -1)
    assert c.bearing(northeast) == coord.NORTHEAST
    assert northeast.bearing(c) == coord.SOUTHWEST
    v = velocity.Velocity(100, c.bearing(northeast))
    assert v.xVelocity > 0
    assert v.yVelocity < 0


def test_bearing_north():
    c = coord.Coord(2, 2)
    north = coord.Coord(2, 1)
    assert c.bearing(north) == coord.NORTH
    assert north.bearing(c) == coord.SOUTH
    v = velocity.Velocity(100, c.bearing(north))
    assert 1e-9 > abs(v.xVelocity)
    assert v.yVelocity == -100

    assert c.bearing(c.north()) == coord.NORTH


def test_bearing_northwest():
    c = coord.Coord(0, 0)
    northwest = coord.Coord(-1, -1)
    assert c.bearing(northwest) == coord.NORTHWEST
    assert northwest.bearing(c) == coord.SOUTHEAST
    v = velocity.Velocity(100, c.bearing(northwest))
    assert v.xVelocity < -70
    assert v.yVelocity < -70


def test_bearing_west():
    c = coord.Coord(0, 0)
    west = coord.Coord(-1, 0)
    assert c.bearing(west) == coord.WEST
    assert west.bearing(c) == coord.EAST
    v = velocity.Velocity(100, c.bearing(west))
    assert v.xVelocity == -100
    assert 1e-9 > abs(v.yVelocity)

    assert c.bearing(c.west()) == coord.WEST


def test_bearing_southwest():
    c = coord.Coord(0, 0)
    southwest = coord.Coord(-1, 1)
    assert c.bearing(southwest) == coord.SOUTHWEST
    assert southwest.bearing(c) == coord.NORTHEAST
    v = velocity.Velocity(100, c.bearing(southwest))
    assert v.xVelocity < -70
    assert v.yVelocity > 70


def test_bearing_south():
    c = coord.Coord(0, 0)
    south = coord.Coord(0, 1)
    assert c.bearing(south) == coord.SOUTH
    assert south.bearing(c) == coord.NORTH
    v = velocity.Velocity(100, c.bearing(south))
    assert 1e-9 > abs(v.xVelocity)
    assert v.yVelocity == 100

    assert c.bearing(c.south()) == coord.SOUTH


def test_bearing_southeast():
    c = coord.Coord(0, 0)
    southeast = coord.Coord(1, 1)
    assert c.bearing(southeast) == coord.SOUTHEAST
    assert southeast.bearing(c) == coord.NORTHWEST
    v = velocity.Velocity(100, c.bearing(southeast))
    assert v.xVelocity > 70
    assert v.yVelocity > 70


def test_bearing_northwest_far():
    tower = coord.Coord(208.0, 216.0)
    monster = coord.Coord(162.0, 166.0)
    bearing = tower.bearing(monster)
    v = velocity.Velocity(100, bearing)
    assert v.xVelocity < 0
    assert v.yVelocity < 0


def test_bearing_west_far():
    tower = coord.Coord(256, 0)
    monster = coord.Coord(288, 0)
    bearing = tower.bearing(monster)
    assert bearing == coord.EAST
    v = velocity.Velocity(100, bearing)
    assert v.xVelocity == 100
    assert v.yVelocity == 0


def test_ordering():
    c1 = coord.Coord(5, 50)
    c2 = coord.Coord(6, 27)
    c3 = coord.Coord(6, 28)
    c4 = coord.Coord(6, 28)

    assert c1 < c2
    assert c2 > c1
    assert c1 != c2
    assert c2 != c1
    assert not (c1 == c2)
    assert not (c2 == c1)

    assert c2 < c3
    assert c3 > c2
    assert c2 != c3
    assert c3 != c2
    assert not (c2 == c3)
    assert not (c3 == c2)

    assert c1 < c3
    assert c3 > c1
    assert c3 == c3
    assert c3 == c4
    assert not (c3 != c3)
    assert not (c3 != c4)

    with pytest.raises(TypeError):
        c1 < 5
    assert not (c1 == 5)
    assert (c1 != 5)
    assert not (c1 == 50)
    assert not (c1 == (5, 50))
