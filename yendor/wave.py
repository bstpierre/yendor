#!/usr/bin/python

import pygame


class Wave:
    def __init__(self, monster_class, count, inter):
        self.monster_class = monster_class
        self.count = count
        self.inter = inter
        self.spawned = 0
        self.last = 0

    @property
    def active(self):
        return self.count > self.spawned

    def update(self, gs):
        next = (self.last + self.inter)
        if gs.ticks > next:
            gs.spawn_monster(self.monster_class)
            self.spawned += 1
            self.last = gs.ticks
