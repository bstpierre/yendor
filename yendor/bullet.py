#!/usr/bin/python

import pygame

from . import coord


class Bullet(pygame.sprite.Sprite):
    def __init__(self, velocity, coord):
        super().__init__()
        self.velocity = velocity
        self.image = pygame.Surface([5, 5])
        self.image.fill((200, 0, 0))
        self.coord = coord
        self.radius = self.rect.width
        self.damage = 1

    def update(self, dt):
        self.coord.x += self.velocity.xVelocity
        self.coord.y += self.velocity.yVelocity

    @property
    def rect(self):
        r = self.image.get_rect()
        r.x = self.coord.x
        r.y = self.coord.y
        return r
