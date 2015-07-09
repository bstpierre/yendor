#!/usr/bin/python

import pygame

from . import (
    bullet,
    coord,
    velocity,
    )

TOWER_WIDTH = 32
TOWER_HEIGHT = 32

BLUE = (64, 64, 255)
BROWN = (135, 80, 25)


class Tower(pygame.sprite.Sprite):
    def __init__(self, bullet_factory, code='?', color=BLUE):
        super().__init__()
        self._set_image(code, color)
        self.rect = self.image.get_rect()
        self.radius = 100  # range
        self.rate = 0.5  # seconds to reload
        self.last_fired = 0
        self.loaded = True
        self.bullet_factory = bullet_factory

    @property
    def center(self):
        return coord.Coord.from_rect(self.rect, centered=True)

    @property
    def coord(self):
        return coord.Coord.from_rect(self.rect, centered=False)

    def _set_image(self, code, color):
        WHITE = (255, 255, 255)
        self.image = pygame.Surface((TOWER_WIDTH, TOWER_HEIGHT))
        self.image.fill(color)
        font = pygame.font.Font(None, 24)
        text = font.render(code, True, WHITE)
        self.image.blit(text, (5, 10))

    def status_message(self, gs):
        """Returns string containing user-facing tower status."""
        gc = gs.grid.client_coord_to_grid(self.coord)
        msg = '{} @ {}'.format(self.__class__.__name__, gc)
        shots_per_second = float(gs.fps) / float(self.rate)
        damage_per_second = self.bullet_factory.damage * shots_per_second
        msg += ', damage/sec: {}'.format(damage_per_second)
        return msg

    def update(self, gs):
        if self.last_fired + self.rate < gs.seconds:
            self.loaded = True

    def fire(self, monster, seconds):
        self.loaded = False
        self.last_fired = seconds
        mc = monster.center
        tc = self.center
        bearing = tc.bearing(mc)
        v = velocity.Velocity(speed=600, direction=bearing)
        b = self.bullet_factory(velocity=v, coord=tc)
        return b


class Slingshot(Tower):
    cost = 20

    def __init__(self):
        super().__init__(bullet_factory=bullet.Bullet,
                         code='S1', color=BLUE)


class Wall(Tower):
    cost = 2

    def __init__(self):
        super().__init__(bullet_factory=None,
                         code='', color=BROWN)
        self.radius = 0  # range

    def fire(self, monster, ticks):
        return None

    def status_message(self, gs):
        return ''
