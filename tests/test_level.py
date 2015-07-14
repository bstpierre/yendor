#!/usr/bin/python

from yendor import level


def test_level_neg():
    assert level.get_level(-1).level == 1


def test_level_zero():
    assert level.get_level(0).level == 1


def test_level_one():
    assert level.get_level(1).level == 1
    assert level.get_level(99).level == 1


def test_level_two():
    assert level.get_level(100).level == 2
    assert level.get_level(249).level == 2


def test_level_three():
    assert level.get_level(250).level == 3
    assert level.get_level(2500).level == 3
