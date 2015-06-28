#!/usr/bin/python

import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, velocity):
        super().__init__()
        self.velocity = velocity
        self.image = pygame.Surface([5, 5])
        self.image.fill((200, 0, 0))
        self.rect = self.image.get_rect()
        self.radius = self.rect.width
        self.damage = 20

    def update(self, dt):
        self.rect.x += self.velocity.xVelocity
        self.rect.y += self.velocity.yVelocity
