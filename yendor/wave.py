#!/usr/bin/python

import pygame


class Wave:
    """A Wave spawns a series of monsters at a given interval.

        :param monster_class: class of Monster to spawn
        :param count: number of monsters to spawn
        :param inter: interval in seconds between monsters
    """
    def __init__(self, monster_class, count, inter):
        self.monster_class = monster_class
        self.count = count
        self.inter = inter
        self.spawned = 0
        self.last = 0

    @property
    def active(self):
        return self.count > self.spawned

    def start(self, seconds):
        """Set the wave to started at the given time."""
        self.last = seconds

    def update(self, gs):
        next = (self.last + self.inter)
        if gs.seconds > next:
            gs.spawn_monster(self.monster_class)
            self.spawned += 1
            self.last = gs.seconds
