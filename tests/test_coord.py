#!/usr/bin/python

import math

import pytest

from yendor import coord

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

def test_bearing_east():
    c = coord.Coord(0, 0)
    east = coord.Coord(1, 0)
    assert c.bearing(east) == coord.EAST
    assert east.bearing(c) == coord.WEST

def test_bearing_northeast():
    c = coord.Coord(0, 0)
    northeast = coord.Coord(1, -1)
    assert c.bearing(northeast) == coord.NORTHEAST
    assert northeast.bearing(c) == coord.SOUTHWEST

def test_bearing_north():
    c = coord.Coord(2, 2)
    north = coord.Coord(2, 1)
    assert c.bearing(north) == coord.NORTH
    assert north.bearing(c) == coord.SOUTH

def test_bearing_northwest():
    c = coord.Coord(0, 0)
    northwest = coord.Coord(-1, 1)
    assert c.bearing(northwest) == coord.NORTHWEST
    assert northwest.bearing(c) == coord.SOUTHEAST

def test_bearing_west():
    c = coord.Coord(0, 0)
    west = coord.Coord(-1, 0)
    assert c.bearing(west) == coord.WEST
    assert west.bearing(c) == coord.EAST

def test_bearing_southwest():
    c = coord.Coord(0, 0)
    southwest = coord.Coord(-1, -1)
    assert c.bearing(southwest) == coord.SOUTHWEST
    assert southwest.bearing(c) == coord.NORTHEAST

def test_bearing_south():
    c = coord.Coord(0, 0)
    south = coord.Coord(0, -1)
    assert c.bearing(south) == coord.SOUTH
    assert south.bearing(c) == coord.NORTH

def test_bearing_southeast():
    c = coord.Coord(0, 0)
    southeast = coord.Coord(1, -1)
    assert c.bearing(southeast) == coord.SOUTHEAST
    assert southeast.bearing(c) == coord.NORTHWEST
