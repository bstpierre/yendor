#!/usr/bin/python

import pygame

from . import (
    bullet,
    coord,
    velocity,
    )

TOWER_WIDTH = 32
TOWER_HEIGHT = 32

BLUE = (64, 64, 255)
BROWN = (135, 80, 25)


class Tower(pygame.sprite.Sprite):
    def __init__(self, bullet_factory, code='?', color=BLUE):
        super().__init__()
        self.code = code
        self.color = color
        self._set_image(code, color)
        self.rect = self.image.get_rect()
        self.radius = 100  # range
        self.rate = 0.5  # seconds to reload
        self.last_fired = 0
        self.loaded = True
        self.bullet_factory = bullet_factory
        self.level = 1

    @property
    def center(self):
        return coord.Coord.from_rect(self.rect, centered=True)

    @property
    def coord(self):
        return coord.Coord.from_rect(self.rect, centered=False)

    def _set_image(self, code, color):
        WHITE = (255, 255, 255)
        self.image = pygame.Surface((TOWER_WIDTH, TOWER_HEIGHT))
        self.image.fill(color)
        font = pygame.font.Font(None, 24)
        text = font.render(code, True, WHITE)
        self.image.blit(text, (5, 10))

    def status_message(self, gs):
        """Returns string containing user-facing tower status."""
        gc = gs.grid.client_coord_to_grid(self.coord)
        msg = '{} @ {}'.format(self.__class__.__name__, gc)
        shots_per_second = float(gs.fps) / float(self.rate)
        damage_per_second = self.bullet_factory.damage * shots_per_second
        msg += ', damage/sec: {}'.format(damage_per_second)
        return msg

    def update(self, gs):
        if self.last_fired + self.rate < gs.seconds:
            self.loaded = True

    def fire(self, monsters, seconds):
        assert len(monsters) > 0
        target = monsters[0]
        # XXX - move this "algorithm" into a Targeting class
        for m in monsters:
            if len(m.path) < len(target.path):
                target = m

        self.loaded = False
        self.last_fired = seconds
        mc = target.center
        tc = self.center
        bearing = tc.bearing(mc)
        v = velocity.Velocity(speed=600, direction=bearing)
        b = self.bullet_factory(velocity=v, coord=tc)
        return b

    def upgrade_cost(self):
        if self.level <= len(self.upgrade_costs):
            return self.upgrade_costs[self.level - 1]
        return None


class Slingshot(Tower):
    cost = 20
    upgrade_costs = [10]

    def __init__(self):
        super().__init__(bullet_factory=bullet.Stone,
                         code='S1', color=BLUE)

    def upgrade(self):
        self.level += 1
        # FIXME: do this right
        self.bullet_factory = bullet.Flint
        self.code = 'S{}'.format(self.level)
        self._set_image(self.code, self.color)


class DartTower(Tower):
    cost = 35
    upgrade_costs = []

    def __init__(self):
        super().__init__(bullet_factory=bullet.Dart,
                         code='D1', color=BLUE)


class Wall(Tower):
    cost = 2

    def __init__(self):
        super().__init__(bullet_factory=None,
                         code='', color=BROWN)
        self.radius = 0  # range
        self.loaded = False

    def update(self, gs):
        pass

    def fire(self, monster, ticks):
        return None

    def status_message(self, gs):
        return ''
