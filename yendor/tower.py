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
        self.rate = 20 # ticks to reload
        self.last_fired = 0
        self.loaded = True
        self.bullet_factory = bullet_factory

    def update(self, ticks):
        if self.last_fired + self.rate < ticks:
            self.loaded = True

    @property
    def center(self):
        return coord.Coord.from_rect(self.rect, centered=True)

    def fire(self, monster, ticks):
        self.loaded = False
        self.last_fired = ticks
        mc = monster.center
        tc = self.center
        bearing = tc.bearing(mc)
        v = velocity.Velocity(bearing, 5)
        print("firing at monster bearing {} ({})".format(
            bearing, v))
        b = self.bullet_factory(v)
        b.rect.x = tc.x
        b.rect.y = tc.y
        return b
