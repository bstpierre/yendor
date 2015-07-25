#!/usr/bin/python

from unittest.mock import Mock, patch

import pygame
import pygame.freetype
import pytest

from yendor import (
    tower_selector,
    )


# FIXME: de-dupe with test_dungeon.py, test_monster.py
@pytest.fixture
def fontinit():
    pygame.init()
    pygame.freetype.init()


@patch.object(pygame, 'Surface')
@patch.object(pygame.font, 'Font')
def test_tower_selector(Font, Surface, fontinit):
    ts = tower_selector.TowerSelector([])

    screen = Mock()
    font = Font.return_value

    surface = Mock()
    rect = Mock()
    rect.x = 0
    rect.y = 0
    rect.width = 0
    rect.height = 10
    surface.get_rect.return_value = rect

    texts = []

    def render(text, *args):
        texts.append(text)
        return surface

    font.render.side_effect = render
    ts.draw(screen)
    assert font.render.called
    assert texts[0] == "TOWERS"
    assert len(texts) == 1
    texts = []

    t = Mock()
    t.name = "aaa"
    ts.set_available([t])

    ts.draw(screen)
    assert len(texts) == 2
    assert "aaa" in texts

    event = Mock()
    event.pos = (rect.x + 1, rect.y + 1)
    ts.handle_button_click(None, t)
    assert ts.selected_tower == t
