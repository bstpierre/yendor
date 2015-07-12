#!/usr/bin/python

import pygame

from . import (
    coord,
    dungeon,
    grid,
    monster,
    timer,
    tower,
    )


class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 5, 5)
        self.health = 100


class GameState:
    fps = 30

    def __init__(self, clock):
        self.time = timer.Timer()
        self.clock = clock
        self.bullets = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.clickables = pygame.sprite.Group()
        self.grid = grid.Grid(self)
        self.running = True
        self.paused = False
        self.placing_group = pygame.sprite.Group()
        self.placing_tower = None
        self.player = Player()

        # XXX - move logic from main into here.
        self.selected = None

        # Initial money (will get 25 more when loading the first level below).
        self.money = 5

        # Load dungeon when grid gets set.
        self.dungeon = None
        self.dungeon_level = 1
        self._load_dungeon()

    @property
    def rect(self):
        r = self.image.get_rect()
        r.x = self.coord.x
        r.y = self.coord.y
        return r

    def status_message(self):
        """Returns strings containing user-facing game status."""
        msgs = []
        msgs.append(self.dungeon.status_message())
        msgs.append("${}, Health: {}".format(self.money,
                                             self.player.health))
        return msgs

    def _load_dungeon(self):
        if self.dungeon_level < 0:  # FIXME: handle game-over
            return

        self.grid = grid.Grid(self)
        self.bullets.empty()
        self.monsters.empty()
        self.towers.empty()
        self.clickables.empty()
        self.placing_group.empty()

        filename = 'levels/{}.dungeon'.format(self.dungeon_level)
        try:
            self.dungeon = dungeon.Dungeon.load(self, filename)
        except IOError:
            print("GAME OVER")
            self.dungeon_level = -1  # FIXME: handle game-over
            return
        self.money += self.dungeon_level * 25
        self.dungeon_level += 1

    @property
    def seconds(self):
        return self.time.ticks / 1000.0

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
                        self.time.resume()
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    self.running = False
                elif event.key in [pygame.K_m]:
                    m = self.spawn_monster(monster.Orc)
                    m.update_path()
                elif event.key == pygame.K_p:
                    self.paused = True
                    self.time.pause()
                elif event.key == pygame.K_d:
                    import pdb
                    pdb.set_trace()
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
                    self.player.rect.x = event.pos[0]
                    self.player.rect.y = event.pos[1]
                    clicked = pygame.sprite.spritecollide(
                        self.player, self.clickables, False)
                    if clicked:
                        self.selected = clicked[0]
            elif event.type == pygame.MOUSEMOTION:
                if self.placing_tower is not None:
                    cc = coord.Coord(event.pos[0], event.pos[1])
                    aligned = self.grid.client_coord_aligned(cc)
                    self.placing_tower.rect.x = aligned.x
                    self.placing_tower.rect.y = aligned.y

    def update(self):
        if self.paused:
            # XXX - still want to be able to place towers while paused.
            return

        # Limit FPS
        dt = self.clock.tick(self.fps)

        if dt > 100:
            # Don't jump forward too much.
            return

        if not self.dungeon.active and len(self.monsters.sprites()) == 0:
            self._load_dungeon()
            return

        self.bullets.update(dt)
        self.monsters.update(dt)
        self.towers.update(self)

        # XXX
        class Base(pygame.sprite.Sprite):
            def __init__(self, c):
                super().__init__()
                self.rect = pygame.Rect(c.x, c.y, 32, 32)

        base = Base(self.grid.grid_coord_to_client(self.dungeon.base))

        # Check for monsters at base.
        smashers = pygame.sprite.spritecollide(
            base, self.monsters, False)
        for m in smashers:
            self.player.health -= m.damage
            m.kill()
            if self.player.health <= 0:
                print("YOU ARE DEAD! GAME OVER")
                self.paused = True
                return

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

        loaded = [t for t in self.towers.sprites() if t.loaded]

        # Fire the towers.
        in_range = pygame.sprite.groupcollide(
            loaded, self.monsters, False, False,
            collided=pygame.sprite.collide_circle)
        for t, ms in in_range.items():
            b = t.fire(ms, self.seconds)
            if b:
                self.add_bullet(b)

        self.dungeon.update(self)

    def add_bullet(self, b):
        self.bullets.add(b)

    def add_monster(self, m):
        self.monsters.add(m)
        self.clickables.add(m)

    def add_tower(self, t):
        if self.money < t.cost:
            print("Not enough money.")
            return

        if self.grid is not None:
            if self.grid.add_obstacle(t):
                self.money -= t.cost
                self.towers.add(t)
                self.clickables.add(t)

    def spawn_monster(self, cls):
        m = cls(self.dungeon.spawn_origin, self.dungeon.base, self.grid)
        self.add_monster(m)
        return m

    def draw(self, screen):
        BLACK = (0, 0, 0)

        font = pygame.font.Font(None, 18)

        # Draw wave status.
        text_x = grid.GRID_WIDTH + 20  # XXX
        text_y = 20
        for msg in self.status_message():
            text = font.render(msg, True, BLACK)
            screen.blit(text, [text_x, text_y])
            text_y += 20

        if self.selected is not None:
            text = font.render(self.selected.status_message(self),
                               True, BLACK)
            text_y = 100
            screen.blit(text, [text_x, text_y])

        self.grid.draw(screen)
        self.bullets.draw(screen)
        self.monsters.draw(screen)
        self.towers.draw(screen)
        self.placing_group.draw(screen)
