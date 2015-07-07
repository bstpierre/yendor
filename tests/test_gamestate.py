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

def test_gamestate_handle_events_pause_quit():
    clock = Mock()
    waves = MagicMock()
    waves.__len__.return_value = 2

    with patch.object(pygame.event, 'get') as event_get:
        def event_get_called():
            return cur_events

        event_get.side_effect = event_get_called

        gs = gamestate.GameState(clock, waves)
        assert not gs.paused
        assert gs.running

        # No events, no changes.
        cur_events = []
        gs.handle_events()
        assert not gs.paused
        assert gs.running
        assert event_get.call_count == 1

        # 'quit' -- q -> not-running
        event_key_q = Mock()
        event_key_q.type = pygame.KEYDOWN
        event_key_q.key = pygame.K_q
        cur_events = [event_key_q]
        gs.handle_events()
        assert not gs.paused
        assert not gs.running
        assert event_get.call_count == 2

        # 'pause' -- p -> paused, p -> unpaused
        gs = gamestate.GameState(clock, waves)
        event_key_p = Mock()
        event_key_p.type = pygame.KEYDOWN
        event_key_p.key = pygame.K_p
        cur_events = [event_key_p]
        gs.handle_events()
        assert gs.paused
        assert gs.running

        # (toggle-unpaused)
        gs.handle_events()
        assert not gs.paused
        assert gs.running

        # (toggle-paused, then quit while paused)
        gs.handle_events()
        assert gs.paused
        assert gs.running
        cur_events = [event_key_q]
        gs.handle_events()
        assert gs.paused
        assert not gs.running
