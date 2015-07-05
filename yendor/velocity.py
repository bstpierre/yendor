#!/usr/bin/python

import math


class Velocity:
    def __init__(self, speed, direction):
        self.speed = speed
        self.xVelocity = 0
        self.yVelocity = 0
        self.set_direction(direction)

    def __str__(self):
        return "Velocity({}, {}, ({}, {}))".format(
            self.speed, self.direction,
            self.xVelocity, self.yVelocity)

    def set_direction(self, d):
        self.direction = d
        self.xVelocity = math.cos(d) * self.speed
        self.yVelocity = math.sin(d) * self.speed
