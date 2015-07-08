#!/usr/bin/python

import copy

from yendor import (
    coord,
    grid,
    monster,
    tower,
    wave,
    )


class Dungeon:
    def __init__(self, waves):
        self.waves = waves
        self.spawn_origin = coord.Coord(0, 0)
        self.base = coord.Coord(0, 0)

    @staticmethod
    def load(gs, filename):
        spec = open(filename, 'r').readlines()
        wave_spec = spec[0].strip()
        waves = [wave.Wave(*args) for args in
                 eval(wave_spec, monster.monsters, {})]

        d = Dungeon(waves)

        gc = coord.Coord(0, 0)
        for y, line in enumerate(spec[1:]):
            gc.y = y
            for x, ch in enumerate(line.strip()):
                gc.x = x
                if ch == '.':
                    continue
                elif ch == '#':
                    cc = gs.grid.grid_coord_to_client(gc)
                    wall = tower.Wall()
                    wall.rect.x = cc.x
                    wall.rect.y = cc.y
                    wall.cost = 0
                    gs.add_tower(wall)
                elif ch == '<':
                    d.spawn_origin = copy.copy(gc)
                    print("spawn_origin {}".format(d.spawn_origin))
                elif ch == '>':
                    d.base = copy.copy(gc)
                    print("base {}".format(d.base))
        return d
