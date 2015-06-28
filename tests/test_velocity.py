#!/usr/bin/python

import math

import pytest

from yendor import coord
from yendor import velocity


def assert_almost_equals(a, b):
    DELTA = 0.0001
    assert abs(a - b) < DELTA

def test_velocity_east():
    v = velocity.Velocity(100, coord.EAST)
    assert v.speed == 100
    assert_almost_equals(v.xVelocity, 100)
    assert_almost_equals(v.yVelocity, 0)

def test_velocity_northeast():
    v = velocity.Velocity(100, coord.NORTHEAST)
    assert v.speed == 100
    assert_almost_equals(v.xVelocity, 70.7106)
    assert_almost_equals(v.yVelocity, -70.7106)
