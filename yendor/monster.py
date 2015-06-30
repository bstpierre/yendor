#!/usr/bin/python

import pygame

from . import (
    coord,
    velocity,
    )


class Monster(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/dwarf-sm.png").convert()
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.radius = self.width
        self.health = 1000
        self.path = []
        self.grid = None
        self.coord = coord.Coord(200, 0) # XXX
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

    def _head_to_goal(self):
        assert len(self.path) > 0
        assert self.grid is not None
        goal = self.path[0]
        my_gc = self.grid.client_coord_to_grid(self.center)
        bearing = my_gc.bearing(goal)
        self.velocity = velocity.Velocity(speed=1, direction=bearing)

    def update(self, dt):
        self.coord.x += self.velocity.xVelocity
        self.coord.y += self.velocity.yVelocity
        my_gc = self.grid.client_coord_to_grid(self.center)
        if len(self.path) == 0:
            print("SMASH BASE (via update)")
            self.kill()
        else:
            goal = self.path[0]
            if my_gc == goal:
                self.path.pop(0)
                if len(self.path) == 0:
                    print("SMASH BASE (update2)")
                    self.kill()
                else:
                    self._head_to_goal()

    def update_path(self, grid):
        self.grid = grid
        my_gc = grid.client_coord_to_grid(self.center)
        self.path = grid.path(my_gc, grid.base)
        print("my_gc {}, path {}".format(my_gc, self.path))
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
        print("ow", self.health)
        if self.health <= 0:
            self.kill()
