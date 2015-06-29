#!/usr/bin/python

import functools
import math

# N.B. pygame coordinate system has origin in the upper-left, so these
# directions are y-inverted from standard Cartesian.
EAST = 0
NORTHEAST = math.pi * 1.75
NORTH = math.pi * 1.5
NORTHWEST = math.pi * 1.25
WEST = math.pi
SOUTHWEST = math.pi * 0.75
SOUTH = math.pi * 0.5
SOUTHEAST = math.pi * 0.25


@functools.total_ordering
class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, rhs):
        if isinstance(rhs, Coord):
            return (self.x == rhs.x and
                    self.y == rhs.y)
        return NotImplemented

    def __lt__(self, rhs):
        if isinstance(rhs, Coord):
            if self.x == rhs.x:
                return self.y < rhs.y
            else:
                return self.x < rhs.x
        return NotImplemented

    def __cmp__(self, rhs):
        if self.x != rhs.x:
            return self.x - rhs.x
        else:
            return self.y - rhs.y

    def __hash__(self):
        # XXX - assuming x and y fit into 16b
        return (self.x << 16) | self.y

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def distance(self, other):
        """Distance from self to other."""
        xd = self.x - other.x
        yd = self.y - other.y
        return math.sqrt(xd * xd + yd * yd)

    def bearing(self, other):
        """Returns angle in radians from self to other."""
        if (self.x < other.x):
            # Quadrant I or IV
            if (self.y > other.y):
                # Quadrant I
                opp = other.y - self.y
                adj = other.x - self.x
                quad = 0.0
                print("q1")
            elif self.y < other.y:
                # Quadrant IV
                opp = self.x - other.x
                adj = other.y - self.y
                quad = math.pi * 0.5
                print("q4")
            else:
                # Due east
                print("east")
                return EAST
        elif (self.x > other.x):
            # Quadrant II or III
            if (self.y > other.y):
                # Quadrant II
                opp = self.y - other.y
                adj = self.x - other.x
                quad = math.pi
                print("q2")
            elif (self.y < other.y):
                # Quadrant III
                opp = self.x - other.x
                adj = other.y - self.y
                quad = math.pi * 0.5
                print("q3")
            else:
                # Due west
                print("west")
                return WEST
        else:
            # Xs are equal
            if (self.y < other.y):
                # Due south
                print("south")
                return SOUTH
            elif (self.y > other.y):
                # Due north
                print("north")
                return NORTH
            else:
                print("same")
                return EAST  # XXX arbitrary

        def norm(angle):
            """Normalize angle to 0-2pi."""
            twopi = 2.0 * math.pi
            if angle < 0:
                return norm(angle + twopi)
            elif angle > twopi:
                return norm(angle - twopi)
            else:
                return angle

        if (adj == 0):
            # XXX - this shouldn't be reachable, should be caught by
            # the last 'else' above.
            assert(False), "not reached"
        else:
            theta = math.atan(float(opp) / float(adj)) + quad
            return norm(theta)

    @staticmethod
    def from_rect(r, centered=False):
        if centered:
            x = r.x + (r.width / 2.0)
            y = r.y + (r.height / 2.0)
            return Coord(x, y)
        else:
            return Coord(r.x, r.y)

    def east(self):
        return Coord(self.x + 1, self.y)

    def south(self):
        return Coord(self.x, self.y + 1)

    def west(self):
        return Coord(self.x - 1, self.y)

    def north(self):
        return Coord(self.x, self.y - 1)
