#!/usr/bin/python

import copy

from yendor import (
    coord,
    monster,
    tower,
    wave,
    )


class Dungeon:
    def __init__(self, waves):
        self.waves = waves
        self.spawn_origin = coord.Coord(0, 0)
        self.base = coord.Coord(0, 0)
        self.cur_wave = 0
        self.active = True

    def status_message(self):
        """Returns strings containing user-facing game status."""
        nwaves = len(self.waves)
        cur = self.cur_wave
        if cur < nwaves:
            w = self.waves[cur]
            cur = cur + 1
        else:
            w = self.waves[-1]
            cur = nwaves
        msg = "Wave {}/{}, Monster {}/{}".format(
            cur, nwaves, w.spawned, w.count)
        return msg

    def update(self, gs):
        """Perform per-tick updates."""
        # Spawn monsters.
        if self.cur_wave < len(self.waves):
            w = self.waves[self.cur_wave]
            w.update(gs)
            if not w.active:
                self.cur_wave += 1
                if self.cur_wave < len(self.waves):
                    self.waves[self.cur_wave].start(gs.seconds)
                else:
                    self.active = False

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
                elif ch == '>':
                    d.base = copy.copy(gc)
        return d
