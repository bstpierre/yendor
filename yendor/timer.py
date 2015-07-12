#!/usr/bin/python

"""
Wraps pygame.time to track unpaused time in the game.
"""

import pygame


class Timer:
    def __init__(self):
        self.time = 0
        self.start = pygame.time.get_ticks()
        self.running = True

    def pause(self):
        assert self.running
        self.running = False
        self.time += pygame.time.get_ticks() - self.start

    def resume(self):
        assert not self.running
        self.running = True
        self.start = pygame.time.get_ticks()

    @property
    def ticks(self):
        if self.running:
            delta = pygame.time.get_ticks() - self.start
            return self.time + delta
        else:
            return self.time
