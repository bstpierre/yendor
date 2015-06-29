#!/usr/bin/python

import pygame

from . import coord


class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/dwarf-sm.png").convert()
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.radius = self.width
        self.coord = coord.Coord(200, 0)
        self.health = 1000
        self.path = []

    @property
    def center(self):
        return coord.Coord(self.coord.x + self.width / 2,
                           self.coord.y + self.height / 2)

    @property
    def rect(self):
        r = self.image.get_rect()
        r.x = self.coord.x
        r.y = self.coord.y
        return r

    def update(self, dt):
        self.coord.y += 1

    def update_path(self, grid):
        my_gc = grid.client_coord_to_grid(self.center)
        self.path = grid.path(my_gc, grid.base)

    def injure(self, damage):
        self.health -= damage
        print("ow", self.health)
        if self.health <= 0:
            self.kill()
