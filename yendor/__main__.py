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
    BLACK = (0, 0, 0)

    size = (800, 480)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Yendor Defender")

    clock = pygame.time.Clock()

    gs = gamestate.GameState(clock=clock)
    grid.Grid(gs)

    font = pygame.font.Font(None, 18)

    while gs.active():
        gs.handle_events()
        gs.update()

        screen.fill(WHITE)

        # Draw wave status.
        text_x = grid.GRID_WIDTH + 20  # XXX
        text_y = 20
        for msg in gs.status_message():
            text = font.render(msg, True, BLACK)
            screen.blit(text, [text_x, text_y])
            text_y += 20

        if gs.selected is not None:
            text = font.render(gs.selected.status_message(gs), True, BLACK)
            text_y = 100
            screen.blit(text, [text_x, text_y])

        gs.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
