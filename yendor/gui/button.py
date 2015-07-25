#!/usr/bin/python

"""
Button class implements a pushbutton widget.

When the user clicks the button an event is posted to the pygame event
loop.
"""

import weakref

import pygame


class Button(pygame.sprite.Sprite):
    # States
    HIGHLIGHTED = 1
    INACTIVE = 2
    PRESSED = 3

    buttons = weakref.WeakSet()

    def __init__(self, x, y, width, height, text,
                 callback, callback_arg):
        super().__init__()
        self.callback = callback
        self.callback_arg = callback_arg
        self.rect = pygame.Rect(x, y, width, height)

        text_color = (255, 255, 255)  # WHITE
        self.normal_bg = (32, 32, 32)  # BLACK
        self.highlight_bg = (32, 32, 180)  # BLUE

        font = pygame.font.Font(None, 16)
        self.text = font.render(text, True, text_color)

        self.image = pygame.Surface((width, height))

        # Set state... is mouse currently over the button?
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos[0], pos[1]):
            self.state = self.HIGHLIGHTED
        else:
            self.state = self.INACTIVE

        self._set_image()

        # Keep track of all buttons created. They will be
        # automatically removed from the set when they no longer have
        # a strong reference.
        Button.buttons.add(self)

    def _set_image(self):
        if self.state == self.INACTIVE:
            self.image.fill(self.normal_bg)
        else:
            # state is HIGHLIGHTED or PRESSED
            self.image.fill(self.highlight_bg)
        offset = (5, 5)
        self.image.blit(self.text, offset)

    def _handle_event(self, event):
        """
        This is the per-instance event handler, which should only
        be called by the class event handler. Users should call
        Button.handle_event().
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos[0], event.pos[1]):
                self.state = self.PRESSED
                self.callback(self, self.callback_arg)
                return True
        elif event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos[0], pos[1]):
                self.state = self.HIGHLIGHTED
                self._set_image()
                return True
            else:
                self.state = self.INACTIVE
                self._set_image()

        return False

    @classmethod
    def handle_event(cls, event):
        for btn in cls.buttons:
            if btn._handle_event(event):
                return True

        return False
