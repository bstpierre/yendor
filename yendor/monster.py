#!/usr/bin/python

import pygame

from . import coord


class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/dwarf-sm.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.radius = self.rect.width
        self.health = 1000

    @property
    def center(self):
        return coord.Coord.from_rect(self.rect, centered=True)

    def update(self, dt):
        self.rect.y += 1

    def injure(self, damage):
        self.health -= damage
        print("ow", self.health)
        if self.health <= 0:
            self.kill()
