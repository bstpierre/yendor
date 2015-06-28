#!/usr/bin/python

import math

# N.B. pygame coordinate system has origin in the upper-left, so these
# directions are y-inverted from standard Cartesian.
EAST = 0
NORTHEAST = (-1.0 * math.pi) / 4.0
NORTH = (3.0 * math.pi) / 2.0
NORTHWEST = (5.0 * math.pi) / 4.0
WEST = math.pi
SOUTHWEST = (3.0 * math.pi) / 4.0
SOUTH = math.pi / 2.0
SOUTHEAST = math.pi / 4.0


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        """Distance from self to other."""
        xd = self.x - other.x
        yd = self.y - other.y
        return math.sqrt(xd * xd + yd * yd)

    def bearing(self, other):
        """Returns angle in radians from self to other."""
        if (self.x < other.x and self.y >= other.y):
            # Quadrant I
            opp = other.y - self.y
            adj = other.x - self.x
            quad = 0.0
            print("q1")
        elif (self.x > other.x and self.y >= other.y):
            # Quadrant II
            opp = self.y - other.y
            adj = self.x - other.x
            quad = math.pi
            print("q2")
        elif (self.x >= other.x and self.y < other.y):
            # Quadrant III
            opp = self.x - other.x
            adj = other.y - self.y
            quad = math.pi * -1.5
            print("q3")
        elif (self.x <= other.x and self.y < other.y):
            # Quadrant IV
            opp = self.x - other.x
            adj = other.y - self.y
            quad = (math.pi / 2.0)
            print("q4")
        else:
            # If no matches, it's the same coord.
            print("same")
            return 0

        if (adj == 0):
            # XXX - this shouldn't be reachable, should be caught by
            # the last 'else' above.
            assert(False), "not reached"
        else:
            theta = math.atan(float(opp) / float(adj)) + quad
            return theta

    @staticmethod
    def from_rect(r, centered=False):
        if centered:
            x = r.x + (r.width / 2.0)
            y = r.y + (r.height / 2.0)
            return Coord(x, y)
        else:
            return Coord(r.x, r.y)
