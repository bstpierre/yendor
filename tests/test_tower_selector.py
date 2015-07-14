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


def test_tower_selector(fontinit):
    ts = tower_selector.TowerSelector([])

    screen = Mock()
    with patch.object(pygame.font, 'Font') as Font:
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
        assert texts[0] == "TOWERS"
        assert len(texts) == 2
        assert texts[1] == "aaa"

        # XXX - this is a bit too hardwired to internal behavior
        assert rect.x == ts.rect.x
        assert rect.y == ts.rect.y + 20
        assert rect.width == ts.rect.width

        event = Mock()
        event.pos = (rect.x + 1, rect.y + 1)
        ts.handle_click(event)
        assert ts.selected_tower == t
