#!/usr/bin/python

from . import coord


GRID_WIDTH = 320
GRID_HEIGHT = 320

BASE_WIDTH = 32
BASE_HEIGHT = 32


class Grid:
    def __init__(self, gs):
        self.gs = gs
        self.gs.set_grid(self)

        self.cell_size = 20 # each grid cell occupies X*Y pixels
        self.cols = GRID_WIDTH / self.cell_size
        self.rows = GRID_HEIGHT / self.cell_size
        self.obstacles = set()

        # XXX - move these to Dungeon class
        base_cc = coord.Coord(GRID_WIDTH - BASE_WIDTH,
                              GRID_HEIGHT - BASE_HEIGHT)
        self.base = self.client_coord_to_grid(base_cc)
        self.spawn_origin = coord.Coord(0, 0)

    def draw(self, screen):
        RED = (255, 0, 0)

        # Draw the Yendorian base.
        self.image = pygame.Surface([32, 32])
        self.image.fill(RED)

    def passable(self, c):
        """Return true if there are no obstacles at the given
        grid-coord."""
        return c not in self.obstacles

    def add_obstacle(self, obs):
        """Return True if obstacle can be added, False otherwise.

        If obstacle can be added, update all monsters' paths.

        `obs` must implement a `center` attribute that returns a
        client-based Coord.
        """
        tower_gc = self.client_coord_to_grid(obs.center)
        if not self.passable(tower_gc):
            print("Can't place tower on existing tower")
            return False

        # Track locations of monsters.
        locs = set()
        locs.add(self.spawn_origin)
        for m in self.gs.monsters:
            gc = self.client_coord_to_grid(m.center)
            if gc == tower_gc:
                print("Can't place tower on monster")
                return False
            locs.add(gc)

        # Will remove this below if it can't be placed here without
        # blocking paths.
        self.obstacles.add(obs)

        for loc in locs:
            path = self.path(loc, self.base)
            if len(path) == 0:
                self.towers.pop()
                print("Can't place tower to block path")
                return False

        for m in self.gs.monsters:
            m.update_path(self)

        print("added obstacle at {}".format(tower_gc))
        return True

    def grid_coord_to_client(self, cc):
        """Given a grid-based Coord, return a client-based Coord
        that covers the grid location."""
        left = cc.x * self.cell_size
        top = cc.y * self.cell_size
        x = left + self.cell_size / 2
        y = top + self.cell_size / 2

        return coord.Coord(x, y)

    def client_coord_to_grid(self, c):
        """Given a client-based Coord, return a grid-based Coord."""
        x = int(c.x / self.cell_size)
        y = int(c.y / self.cell_size)
        return coord.Coord(x, y)

    def in_bounds(self, gc):
        return (gc.x >= 0 and
                gc.x < self.cols and
                gc.y >= 0 and
                gc.y < self.rows)

    def neighbors(self, gc):
        neighs = [gc.east(),
                  gc.south(),
                  gc.west(),
                  gc.north()]

        return [n for n in neighs if (self.in_bounds(n) and
                                      self.passable(n))]

    def path(self, start, finish):
        """
        Returns a list of coordinates that can be followed for a path
        from start (a grid-based Coord) to finish (a grid-based
        Coord).

        http:#www.redblobgames.com/pathfinding/a-star/introduction.html
        """
        frontier = [start]
        came_from = {
            start: None
            }

        while len(frontier) > 0:
            current = frontier.pop(0)
            if current == finish:
                break

            # print("neighbors({}): {}".format(current,
            #                                  self.neighbors(current)))
            for neigh in self.neighbors(current):
                if neigh not in came_from:
                    frontier.append(neigh)
                    came_from[neigh] = current

        # Return the shortest path.
        path = []

        current = came_from[finish]
        while current is not None:
            path.insert(0, current)
            current = came_from[current]

        if len(path) > 0:
            path.append(finish)

        return path
