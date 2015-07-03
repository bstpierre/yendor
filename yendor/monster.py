#!/usr/bin/python

import pygame

from . import (
    coord,
    velocity,
    )


class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.radius = self.width
        self.health = 1000
        self.path = []
        self.grid = None
        self.coord = coord.Coord(256, 0) # XXX
        self.velocity = velocity.Velocity(1, coord.SOUTH) # XXX

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

    def status_message(self, gs):
        """Returns string containing user-facing monster status."""
        gc = gs.grid.client_coord_to_grid(self.coord)
        msg = '{} @ {}'.format(self.__class__.__name__, gc)
        msg += ', health: {}'.format(self.health)
        return msg

    def _head_to_goal(self):
        assert len(self.path) > 0
        assert self.grid is not None
        goal_cc = self.grid.grid_coord_to_client(self.path[0])
        bearing = self.coord.bearing(goal_cc)
        self.velocity = velocity.Velocity(speed=1, direction=bearing)

    def update(self, dt):
        self.coord.x += self.velocity.xVelocity
        self.coord.y += self.velocity.yVelocity
        if len(self.path) == 0:
            print("SMASH BASE (via update)")
            self.kill()
            return
        else:
            goal = self.path[0]
            goal_cc = self.grid.grid_coord_to_client(self.path[0])
            mc_round = coord.Coord(int(self.coord.x),
                                   int(self.coord.y))
            if mc_round.distance(goal_cc) < 2: # XXX
                self.path.pop(0)
                if len(self.path) == 0:
                    print("SMASH BASE (update2)")
                    self.kill()
                    return
        self._head_to_goal()

    def update_path(self, grid):
        self.grid = grid
        my_gc = grid.client_coord_to_grid(self.center)
        self.path = grid.path(my_gc, grid.base)
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


class Dwarf(Monster):
    def __init__(self):
        self.image = pygame.image.load("assets/dwarf-sm.png").convert()
        super().__init__()


class Orc(Monster):
    def __init__(self):
        self.image = pygame.image.load("assets/orc-sm.png").convert()
        super().__init__()
