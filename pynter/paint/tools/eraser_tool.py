"""Eraser tool -- paints white rectangles to erase canvas content.

Scroll wheel adjusts eraser size.
"""

import pygame
import globals as g
from tools.tool import Tool

ERASER_COLOR = (255, 255, 255)


class EraserTool(Tool):
    MIN_SIZE = 20
    MAX_SIZE = 80

    def __init__(self):
        self.eraser_size: int = 20

    def draw(self, surface: pygame.Surface) -> None:
        buttons = pygame.mouse.get_pressed()
        if buttons[0]:
            mx, my = g.mouse_pos
            if my > g.TOP_BAR_HEIGHT and mx > g.SIDE_PANEL_WIDTH:
                half = self.eraser_size // 2
                rect = pygame.Rect(mx - half, my - half,
                                   self.eraser_size, self.eraser_size)
                pygame.draw.rect(surface, ERASER_COLOR, rect)

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEWHEEL:
            self.eraser_size += event.y * 5
            self.eraser_size = max(self.MIN_SIZE, min(self.MAX_SIZE, self.eraser_size))

    def preview(self, screen: pygame.Surface) -> None:
        mx, my = g.mouse_pos
        if my <= g.TOP_BAR_HEIGHT:
            return
        half = self.eraser_size // 2
        inner = pygame.Rect(mx - half, my - half,
                            self.eraser_size, self.eraser_size)
        outer = pygame.Rect(mx - half - 2, my - half - 2,
                            self.eraser_size + 4, self.eraser_size + 4)
        pygame.draw.rect(screen, (128, 128, 128), outer, 2)
        pygame.draw.rect(screen, ERASER_COLOR, inner)
