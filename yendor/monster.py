#!/usr/bin/python

import pygame

from . import (
    coord,
    dice,
    velocity,
    )

MONSTER_WIDTH = 32
MONSTER_HEIGHT = 32


class Monster(pygame.sprite.Sprite):
    def __init__(self, start, end, grid, code='?'):
        super().__init__()

        # Nethack monster HP == (monster level)d8
        # Tweaking it a bit here.
        self.health = dice.roll(self.level + 1, 8)

        # Nethack XP == (ML)*(ML+6)+1
        self.xp = self.level * (self.level + 6) + 1

        self._set_image(code)
        self.width = MONSTER_WIDTH
        self.height = MONSTER_HEIGHT
        self.radius = self.width / 2
        self.path = []

        self.velocity = velocity.Velocity(self.speed, coord.SOUTH)
        self.grid = grid
        self.coord = self.grid.grid_coord_to_client(start)
        self.start = start
        self.end = end
        self.update_path()

        if dice.chances(2, 5):
            self.money = dice.roll(self.level, 5)
        else:
            self.money = 0

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

    def _set_image(self, code):
        WHITE = (255, 255, 255)
        self.image = pygame.Surface((MONSTER_WIDTH, MONSTER_HEIGHT))
        font = pygame.font.Font(None, 32)
        text = font.render(code, True, WHITE)
        self.image.blit(text, (5, 5))

    def status_message(self, gs):
        """Returns string containing user-facing monster status."""
        gc = gs.grid.client_coord_to_grid(self.coord)
        msg = '{} @ {}'.format(self.__class__.__name__, gc)
        msg += ', health: {}, gold: {}'.format(self.health, self.money)
        return msg

    def _head_to_goal(self):
        assert len(self.path) > 0
        assert self.grid is not None
        goal_cc = self.grid.grid_coord_to_client(self.path[0])
        bearing = self.coord.bearing(goal_cc)
        self.velocity.set_direction(bearing)

    def update(self, dt):
        self.coord.x += self.velocity.xVelocity * (dt / 1000.0)
        self.coord.y += self.velocity.yVelocity * (dt / 1000.0)
        if len(self.path) == 0:
            print("SMASH BASE (via update)")
            self.kill()
            return
        else:
            goal_cc = self.grid.grid_coord_to_client(self.path[0])
            mc_round = coord.Coord(int(self.coord.x),
                                   int(self.coord.y))
            if mc_round.distance(goal_cc) < 2:  # XXX
                self.path.pop(0)
                if len(self.path) == 0:
                    print("SMASH BASE (update2)")
                    self.kill()
                    return
        self._head_to_goal()

    def update_path(self):
        my_gc = self.grid.client_coord_to_grid(self.center)
        self.path = self.grid.path(my_gc, self.end)
        if self.path:
            assert my_gc == self.path[0]
            self.path.pop(0)
            if len(self.path) == 0:
                print("SMASH BASE (via update_path)")
                self.kill()
                return
            else:
                self._head_to_goal()

    def injure(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()


class Jackal(Monster):
    speed = 30  # XXX
    level = 1

    def __init__(self, *args, **kwargs):
        self.damage = 4
        super().__init__(*args, code='d', **kwargs)


class Gnome(Monster):
    speed = 15  # XXX
    level = 3

    def __init__(self, *args, **kwargs):
        self.damage = 4
        super().__init__(*args, code='G', **kwargs)


class Orc(Monster):
    speed = 23  # XXX
    level = 3

    def __init__(self, *args, **kwargs):
        self.damage = 10
        super().__init__(*args, code='O', **kwargs)


class Dwarf(Monster):
    speed = 15  # XXX
    level = 4

    def __init__(self, *args, **kwargs):
        self.damage = 8
        super().__init__(*args, code='D', **kwargs)


class Lizard(Monster):
    speed = 15  # XXX
    level = 5

    def __init__(self, *args, **kwargs):
        self.damage = 6
        super().__init__(*args, code=':', **kwargs)


class Yeti(Monster):
    speed = 38  # XXX
    level = 7

    def __init__(self, *args, **kwargs):
        self.damage = 12
        super().__init__(*args, code='Y', **kwargs)


monsters = {n: g for (n, g) in globals().items() if (
    type(g) == type(Monster) and
    issubclass(g, Monster) and
    g is not Monster
    )}
