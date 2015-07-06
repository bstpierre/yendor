#!/usr/bin/python

from unittest.mock import MagicMock, Mock, patch

import pygame
import pygame.freetype
import pytest

from yendor import (
    gamestate,
    )


@pytest.fixture
def fontinit():
    pygame.init()
    pygame.freetype.init()


def test_gamestate_update_monster_kill_money():
    clock = Mock()
    waves = MagicMock()
    waves.__len__.return_value = 2
    b = Mock()
    m = Mock()
    m.alive.return_value = False
    m.money = 10

    with patch.object(pygame.sprite, 'groupcollide') as groupcollide:
        def groupcollide_called(g1, g2, *args, **kwargs):
            # groupcollide is called for bullets and towers; we only
            # want to return results for bullets here.
            if g1 is gs.bullets:
                return {b: [m, m, m]}
            else:
                return {}
        groupcollide.side_effect = groupcollide_called
        gs = gamestate.GameState(clock, waves)
        assert gs.money == 50
        gs.update()
        assert gs.money == 60

        # Bullet had multiple "hittable" monsters, but only one
        # monster took the damage.
        assert m.injure.called == 1
