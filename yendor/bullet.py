#!/usr/bin/python

import pygame

from . import (
    dice,
    )


class Bullet(pygame.sprite.Sprite):
    # Subclass must provide self.damage_roll = (qty, sides)

    def __init__(self, velocity, coord):
        super().__init__()
        self.damage = dice.roll(*self.damage_roll)
        self.velocity = velocity
        self.image = pygame.Surface([5, 5])
        self.image.fill((200, 0, 0))
        self.coord = coord
        self.radius = self.rect.width

    def update(self, dt):
        """Update the Bullet for `dt` milliseconds."""
        self.coord.x += self.velocity.xVelocity * (dt / 1000.0)
        self.coord.y += self.velocity.yVelocity * (dt / 1000.0)

    @property
    def rect(self):
        r = self.image.get_rect()
        r.x = self.coord.x
        r.y = self.coord.y
        return r


class Stone(Bullet):
    # Damage is 1d6
    # XXX - should wrap this into dice.Roll or DiceSpec
    damage_roll = (1, 3)


class Flint(Bullet):
    damage_roll = (1, 6)


class Dart(Bullet):
    damage_roll = (2, 3)
