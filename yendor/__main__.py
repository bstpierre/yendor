#!/usr/bin/python

import pygame
import pygame.freetype

from . import (
    gamestate,
    grid,
    )


def main(args=None):
    """The main routine."""
    # if args is None:
    #     args = sys.argv[1:]
    # XXX - arg parsing

    pygame.init()
    pygame.freetype.init()

    WHITE = (255, 255, 255)

    size = (800, 480)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Yendor Defender")

    clock = pygame.time.Clock()

    gs = gamestate.GameState(clock=clock)

    while gs.active():
        gs.handle_events()
        gs.update()

        screen.fill(WHITE)

        gs.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
