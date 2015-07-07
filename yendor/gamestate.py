#!/usr/bin/python

import pygame

from . import (
    coord,
    monster,
    tower,
    )


class GameState:
    fps = 30

    def __init__(self, clock, waves):
        self.ticks = 0
        self.clock = clock
        self.waves = waves
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.clickables = pygame.sprite.Group()
        self.grid = None
        self.cur_wave = 0
        self.running = True
        self.paused = False
        self.placing_group = pygame.sprite.Group()
        self.placing_tower = None

        # XXX - move logic from main into here.
        self.selected = None

        # Initial money.
        self.money = 50

    @property
    def rect(self):
        r = self.image.get_rect()
        r.x = self.coord.x
        r.y = self.coord.y
        return r

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
        msgs = ["Wave {}/{}, Monster {}/{}".format(
            cur, nwaves, w.spawned, w.count),
                "${}".format(self.money),
                ]
        return msgs

    def set_grid(self, g):
        self.grid = g

    @property
    def seconds(self):
        return self.ticks / 1000.0

    def active(self):
        return self.running

    def handle_events(self):
        # FIXME: rework pause handling so that towers can be
        # placed/upgraded while paused -- but monsters don't move and
        # time doesn't advance while paused.
        if self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                        self.running = False
                    elif event.key == pygame.K_p:
                        self.paused = False
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    self.running = False
                elif event.key in [pygame.K_m]:
                    m = self.spawn_monster(monster.Orc)
                    m.update_path(self.grid)
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key in [pygame.K_t]:
                    if self.placing_tower is None:
                        self.selected = None
                        self.placing_tower = tower.Slingshot()
                        pos = pygame.mouse.get_pos()
                        cc = coord.Coord(pos[0], pos[1])
                        aligned = self.grid.client_coord_aligned(cc)
                        self.placing_tower.rect.x = aligned.x
                        self.placing_tower.rect.y = aligned.y
                        self.placing_group.add(self.placing_tower)
                    else:
                        self.placing_tower.kill()
                        self.placing_tower = None
                elif event.key in [pygame.K_w]:
                    if self.placing_tower is None:
                        self.selected = None
                        self.placing_tower = tower.Wall()
                        pos = pygame.mouse.get_pos()
                        cc = coord.Coord(pos[0], pos[1])
                        aligned = self.grid.client_coord_aligned(cc)
                        self.placing_tower.rect.x = aligned.x
                        self.placing_tower.rect.y = aligned.y
                        self.placing_group.add(self.placing_tower)
                    else:
                        self.placing_tower.kill()
                        self.placing_tower = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.placing_tower is not None:
                    self.add_tower(self.placing_tower)
                    self.placing_group.empty()
                    self.placing_tower = None
                else:
                    # FIXME
                    class Player(pygame.sprite.Sprite):
                        def __init__(self):
                            self.rect = pygame.Rect(event.pos[0],
                                                    event.pos[1],
                                                    5, 5)
                    p = Player()
                    clicked = pygame.sprite.spritecollide(
                        p, self.clickables, False)
                    if clicked:
                        self.selected = clicked[0]
            elif event.type == pygame.MOUSEMOTION:
                if self.placing_tower is not None:
                    cc = coord.Coord(event.pos[0], event.pos[1])
                    aligned = self.grid.client_coord_aligned(cc)
                    self.placing_tower.rect.x = aligned.x
                    self.placing_tower.rect.y = aligned.y

    def update(self):
        # Limit FPS
        dt = self.clock.tick(self.fps)
        self.ticks = pygame.time.get_ticks()

        self.bullets.update(dt)
        self.monsters.update(dt)
        self.towers.update(self)

        # Injure monsters with bullets.
        hits = pygame.sprite.groupcollide(self.bullets,
                                          self.monsters,
                                          True, False)
        for b, ms in hits.items():
            for m in ms:
                # Note: bullet only one hits one monster, so break.
                m.injure(b.damage)
                if not m.alive():
                    self.money += m.money
                break

        # Fire the towers.
        # XXX - should filter out the walls (i.e towers that can't fire).
        in_range = pygame.sprite.groupcollide(
            self.towers, self.monsters, False, False,
            collided=pygame.sprite.collide_circle)
        for t, ms in in_range.items():
            # FIXME: only check 'ready' tower group for collisions
            if not t.loaded:
                continue
            for m in ms:
                b = t.fire(m, self.seconds)
                if b:
                    self.add_bullet(b)
                # XXX tower only fires at one monster
                break

        # Spawn monsters.
        if self.cur_wave < len(self.waves):
            w = self.waves[self.cur_wave]
            w.update(self)
            if not w.active:
                self.cur_wave += 1
                if self.cur_wave < len(self.waves):
                    self.waves[self.cur_wave].start(self.seconds)

    def add_bullet(self, b):
        self.bullets.add(b)

    def add_monster(self, m):
        self.monsters.add(m)
        self.clickables.add(m)

    def add_tower(self, t):
        if self.money < t.cost:
            print("Not enough money.")
            return

        self.money -= t.cost
        if self.grid is not None:
            if self.grid.add_obstacle(t):
                self.towers.add(t)
                self.clickables.add(t)

    def spawn_monster(self, cls):
        m = cls()
        m.update_path(self.grid)
        self.add_monster(m)
        return m

    def draw(self, screen):
        self.grid.draw(screen)
        self.bullets.draw(screen)
        self.monsters.draw(screen)
        self.towers.draw(screen)
        self.placing_group.draw(screen)
