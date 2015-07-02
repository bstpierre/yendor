#!/usr/bin/python

import sys

import pygame
import pygame.freetype

from . import (
    bullet,
    coord,
    gamestate,
    grid,
    monster,
    tower,
    velocity,
    wave,
    )

def main(args=None):
    """The main routine."""
    # if args is None:
    #     args = sys.argv[1:]
    # XXX - arg parsing

    pygame.init()
    pygame.freetype.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    size = (800, 480)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Yendor Defender")

    clock = pygame.time.Clock()

    waves = [wave.Wave(monster.Dwarf, 5, 60),
             wave.Wave(monster.Orc, 2, 240)]
    gs = gamestate.GameState(waves)
    g = grid.Grid(gs)

    ticks = 0
    placing_group = pygame.sprite.Group()
    placing_tower = None

    font = pygame.font.Font(None, 18)

    selected = None

    running = True
    paused = False

    while running:
        if paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif (event.type == pygame.KEYDOWN and
                      event.key == pygame.K_p):
                    paused = False
            # 30fps
            clock.tick(30)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    running = False
                elif event.key in [pygame.K_m]:
                    m = gs.spawn_monster(monster.Orc)
                    m.update_path(gs.grid)
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key in [pygame.K_t]:
                    if placing_tower is None:
                        selected = None
                        placing_tower = tower.Tower(bullet.Bullet)
                        pos = pygame.mouse.get_pos()
                        cc = coord.Coord(pos[0], pos[1])
                        aligned = gs.grid.client_coord_aligned(cc)
                        placing_tower.rect.x = aligned.x
                        placing_tower.rect.y = aligned.y
                        placing_group.add(placing_tower)
                    else:
                        placing_tower.kill()
                        placing_tower = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if placing_tower is not None:
                    gs.add_tower(placing_tower)
                    placing_group.empty()
                    placing_tower = None
                else:
                    # FIXME
                    class Player(pygame.sprite.Sprite):
                        def __init__(self):
                            self.rect = pygame.Rect(event.pos[0],
                                                    event.pos[1],
                                                    5, 5)
                    p = Player()
                    clicked = pygame.sprite.spritecollide(
                        p, gs.clickables, False)
                    if clicked:
                        selected = clicked[0]
            elif event.type == pygame.MOUSEMOTION:
                if placing_tower is not None:
                    cc = coord.Coord(event.pos[0], event.pos[1])
                    aligned = gs.grid.client_coord_aligned(cc)
                    placing_tower.rect.x = aligned.x
                    placing_tower.rect.y = aligned.y

        ticks += 1
        gs.update(ticks)

        # 30fps
        clock.tick(30)

        screen.fill(WHITE)

        # Draw wave status.
        nwaves = len(gs.waves)
        w = gs.waves[gs.cur_wave] if gs.cur_wave < nwaves else gs.waves[-1]
        wave_msg = "Wave {}/{}, Monster {}/{}".format(
            gs.cur_wave + 1 if gs.cur_wave < nwaves else nwaves, nwaves,
            w.spawned, w.count)
        text = font.render(wave_msg, True, BLACK)
        text_x = grid.GRID_WIDTH + 20 # XXX
        text_y = 20
        screen.blit(text, [text_x, text_y])

        if selected is not None:
            r = selected.rect
            cc = coord.Coord.from_rect(r)
            gc = gs.grid.client_coord_to_grid(cc)
            agc = gs.grid.client_coord_aligned(cc)
            text = font.render("Monster @ {} / {} / {}".format(r, gc, agc),
                               True, BLACK)
            text_y = 100
            screen.blit(text, [text_x, text_y])

        gs.draw(screen)
        placing_group.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
