#!/usr/bin/python

import pygame

from . import monster


class GameState:
    def __init__(self, waves):
        self.ticks = 0
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.clickables = pygame.sprite.Group()
        self.grid = None
        self.waves = waves
        self.cur_wave = 0

    @property
    def rect(self):
        r = self.image.get_rect()
        r.x = self.coord.x
        r.y = self.coord.y
        return r

    def set_grid(self, g):
        self.grid = g

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

        # Spawn monsters.
        if self.cur_wave < len(self.waves):
            w = self.waves[self.cur_wave]
            w.update(self)
            if not w.active:
                self.cur_wave += 1
                if self.cur_wave < len(self.waves):
                    self.waves[self.cur_wave].last = self.ticks

    def add_bullet(self, b):
        self.bullets.add(b)

    def add_monster(self, m):
        self.monsters.add(m)
        self.clickables.add(m)

    def add_tower(self, t):
        if self.grid is not None:
            if self.grid.add_obstacle(t):
                self.towers.add(t)
                self.clickables.add(t)

    def spawn_monster(self, cls):
        m = cls()
        m.update_path(self.grid)
        self.add_monster(m)
        return m

    def draw(self, screen):
        self.grid.draw(screen)
        self.bullets.draw(screen)
        self.monsters.draw(screen)
        self.towers.draw(screen)
