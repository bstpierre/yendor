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

    t = tower.Tower(bullet.Bullet)
    gs.add_tower(t)

    print("path: {}".format(g.path(g.spawn_origin, g.base)))

    ticks = 0

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
            elif event.type == pygame.MOUSEBUTTONUP:
                click = coord.Coord(event.pos[0], event.pos[1])
                bearing = t.center.bearing(click)
                print(bearing)
                v = velocity.Velocity(3, bearing)
                b = bullet.Bullet(v, t.center)
                b.rect.x = t.center.x
                b.rect.y = t.center.y
                gs.add_bullet(b)

        ticks += 1
        gs.update(ticks)

        # 30fps
        clock.tick(30)

        screen.fill(WHITE)
        gs.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
