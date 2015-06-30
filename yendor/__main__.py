#!/usr/bin/python

import sys

import pygame

from . import (
    bullet,
    coord,
    gamestate,
    grid,
    monster,
    tower,
    velocity,
    )

def main(args=None):
    """The main routine."""
    # if args is None:
    #     args = sys.argv[1:]
    # XXX - arg parsing

    WHITE = (255, 255, 255)

    size = (600, 480)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Yendor Defender")

    clock = pygame.time.Clock()

    gs = gamestate.GameState()
    g = grid.Grid(gs)

    ticks = 0
    placing_group = pygame.sprite.Group()
    placing_tower = None

    pygame.init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                    running = False
                elif event.key in [pygame.K_m]:
                    m = gs.spawn_monster()
                    m.update_path(gs.grid)
                elif event.key in [pygame.K_t]:
                    if placing_tower is None:
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
        gs.draw(screen)
        placing_group.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
