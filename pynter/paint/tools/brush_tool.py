"""Freehand brush with adjustable size (scroll wheel to resize)."""

import pygame
import globals as g
from tools.tool import Tool


class BrushTool(Tool):
    MIN_SIZE = 2
    MAX_SIZE = 50

    def __init__(self):
        self.brush_size: float = 20.0

    def draw(self, surface: pygame.Surface) -> None:
        buttons = pygame.mouse.get_pressed()
        if buttons[0]:
            mx, my = g.mouse_pos
            if my > g.TOP_BAR_HEIGHT and mx > g.SIDE_PANEL_WIDTH:
                color = g.colors[g.color_selected]
                pygame.draw.circle(surface, color, (mx, my), int(self.brush_size))

    def handle_events(self, event: pygame.event.Event) -> None:
        """Scroll wheel adjusts brush size."""
        if event.type == pygame.MOUSEWHEEL:
            self.brush_size += event.y * 5
            self.brush_size = max(self.MIN_SIZE, min(self.MAX_SIZE, self.brush_size))

    def preview(self, screen: pygame.Surface) -> None:
        mx, my = g.mouse_pos
        if my <= g.TOP_BAR_HEIGHT:
            return
        color = g.colors[g.color_selected]
        right_held = pygame.mouse.get_pressed()[2]
        if right_held:
            pygame.draw.circle(screen, (128, 128, 128), (mx, my),
                               int(self.brush_size), 1)
        else:
            pygame.draw.circle(screen, color, (mx, my), int(self.brush_size))
