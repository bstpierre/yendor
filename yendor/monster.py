#!/usr/bin/python

import pygame

from . import coord


class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/dwarf-sm.png").convert()
        self.radius = self.image.get_rect().width
        self.coord = coord.Coord(150, 0)
        self.health = 1000

    @property
    def center(self):
        return coord.Coord.from_rect(self.rect, centered=True)

    @property
    def rect(self):
        r = self.image.get_rect()
        r.x = self.coord.x
        r.y = self.coord.y
        return r

    def update(self, dt):
        self.coord.y += 1

    def injure(self, damage):
        self.health -= damage
        print("ow", self.health)
        if self.health <= 0:
            self.kill()
