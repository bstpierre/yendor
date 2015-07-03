#!/usr/bin/python

import pygame

from . import coord
from . import velocity


class Tower(pygame.sprite.Sprite):
    def __init__(self, bullet_factory):
        super().__init__()
        self.image = pygame.image.load("assets/tower-sm.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200
        self.radius = 100 # range
        self.rate = 15 # ticks to reload
        self.last_fired = 0
        self.loaded = True
        self.bullet_factory = bullet_factory

    @property
    def center(self):
        return coord.Coord.from_rect(self.rect, centered=True)

    @property
    def coord(self):
        return coord.Coord.from_rect(self.rect, centered=False)

    def status_message(self, gs):
        """Returns string containing user-facing tower status."""
        gc = gs.grid.client_coord_to_grid(self.coord)
        msg = '{} @ {}'.format(self.__class__.__name__, gc)
        shots_per_second = float(gs.fps) / float(self.rate)
        damage_per_second = self.bullet_factory.damage * shots_per_second
        msg += ', damage/sec: {}'.format(damage_per_second)
        return msg

    def update(self, ticks):
        if self.last_fired + self.rate < ticks:
            self.loaded = True

    def fire(self, monster, ticks):
        self.loaded = False
        self.last_fired = ticks
        mc = monster.center
        tc = self.center
        bearing = tc.bearing(mc)
        v = velocity.Velocity(speed=20, direction=bearing)
        b = self.bullet_factory(velocity=v, coord=tc)
        return b
