#!/usr/bin/python

import pygame

from . import (
    grid,
    tower,
    )


class TowerSelector:
    """UI for the user to select which tower type to build.
    """
    def __init__(self):
        self.rect = pygame.Rect(grid.GRID_WIDTH + 20, 200, 200, 200)
        self.towers = []
        self.selected_tower = None

    def draw(self, screen):
        BLACK = (0, 0, 0)
        font = pygame.font.Font(None, 18)

        text_x = self.rect.x
        text_y = self.rect.y

        text = font.render("TOWERS", True, BLACK)
        screen.blit(text, [text_x, text_y])
        text_y += 20

        text_x += 10
        towers = [("Slingshot", tower.Slingshot),
                  ("Dart", tower.DartTower),
                  ]
        self.towers = []
        for name, t in towers:
            text = font.render(name, True, BLACK)
            r = text.get_rect()
            r.x += self.rect.x
            r.y += text_y
            r.width = self.rect.width
            self.towers.append((r, t))
            screen.blit(text, [text_x, text_y])
            text_y += 20

        assert text_y < (self.rect.x + self.rect.height)

    def handle_click(self, event):
        for r, t in self.towers:
            if r.collidepoint(event.pos[0], event.pos[1]):
                self.selected_tower = t
                break
