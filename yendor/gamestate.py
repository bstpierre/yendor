#!/usr/bin/python

import pygame

from . import monster


class GameState:
    def __init__(self):
        self.ticks = 0
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()

    @property
    def rect(self):
        r = self.image.get_rect()
        r.x = self.coord.x
        r.y = self.coord.y
        return r

    def update(self, ticks):
        self.ticks = ticks
        self.bullets.update(ticks)
        self.monsters.update(ticks)
        self.towers.update(ticks)

        # Injure monsters with bullets.
        hits = pygame.sprite.groupcollide(self.bullets,
                                          self.monsters,
                                          True, False)
        for b, ms in hits.items():
            for m in ms:
                m.injure(b.damage)
                # XXX - bullet only one hits one monster
                break

        # Fire the towers.
        in_range = pygame.sprite.groupcollide(
            self.towers, self.monsters, False, False,
            collided=pygame.sprite.collide_circle)
        for t, ms in in_range.items():
            # FIXME: only check 'ready' tower group for collisions
            if not t.loaded:
                continue
            for m in ms:
                b = t.fire(m, ticks)
                self.add_bullet(b)
                # XXX tower only fires at one monster
                break

    def add_bullet(self, b):
        self.bullets.add(b)

    def add_monster(self, m):
        self.monsters.add(m)

    def add_tower(self, t):
        self.towers.add(t)

    def spawn_monster(self):
        self.add_monster(monster.Monster())

    def draw(self, screen):
        self.bullets.draw(screen)
        self.monsters.draw(screen)
        self.towers.draw(screen)
