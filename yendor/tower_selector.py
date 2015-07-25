#!/usr/bin/python

import pygame

from . import (
    grid,
    )
from . gui import (
    button,
    )


class TowerSelector:
    """UI for the user to select which tower type to build.
    """
    def __init__(self, towers):
        self.rect = pygame.Rect(grid.GRID_WIDTH + 20, 200, 200, 200)
        self.available = towers
        self.towers = []
        self.selected_tower = None
        self.buttons = pygame.sprite.Group()
        self.set_available(towers)

    def set_available(self, towers):
        self.available = towers

        if self.selected_tower not in towers:
            self.selected_tower = None

        # Start at y-offset to give room for title.
        btn_x = self.rect.x
        btn_y = self.rect.y + 20

        self.buttons.empty()
        for tclass in towers:
            # FIXME: generate Menu instead of Buttons
            btn = button.Button(btn_x, btn_y, self.rect.width, 20,
                                tclass.name, self.handle_button_click,
                                tclass)
            self.buttons.add(btn)
            btn_y += 20

        assert btn_y < (self.rect.x + self.rect.height)

    def draw(self, screen):
        BLACK = (0, 0, 0)
        font = pygame.font.Font(None, 18)
        text = font.render("TOWERS", True, BLACK)
        screen.blit(text, [self.rect.x, self.rect.y])

        self.buttons.draw(screen)

    def handle_button_click(self, btn, tclass):
        self.selected_tower = tclass
