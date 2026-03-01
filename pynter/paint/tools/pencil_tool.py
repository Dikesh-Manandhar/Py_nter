"""Freehand drawing tool with a fixed-size brush (radius = 5 px).

Stamps filled circles at the mouse position while the left button is held.
"""

import pygame
import globals as g
from tools.tool import Tool


class PencilTool(Tool):
    PENCIL_RADIUS = 5

    def draw(self, surface: pygame.Surface) -> None:
        buttons = pygame.mouse.get_pressed()
        if buttons[0]:
            mx, my = g.mouse_pos
            if my > g.TOP_BAR_HEIGHT and mx > g.SIDE_PANEL_WIDTH:
                color = g.colors[g.color_selected]
                pygame.draw.circle(surface, color, (mx, my), self.PENCIL_RADIUS)

    def handle_events(self, event: pygame.event.Event) -> None:
        pass

    def preview(self, screen: pygame.Surface) -> None:
        """Show a filled circle cursor indicator."""
        mx, my = g.mouse_pos
        if my > g.TOP_BAR_HEIGHT:
            color = g.colors[g.color_selected]
            pygame.draw.circle(screen, color, (mx, my), self.PENCIL_RADIUS)
