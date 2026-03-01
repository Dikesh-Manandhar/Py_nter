"""
square_tool.py — Draws perfect squares (equal width and height).

Click and drag to draw. Side length = max(|dx|, |dy|) so width == height.

COMPUTER GRAPHICS CONCEPT:
    A square is a rectangle with the constraint width == height.
    We enforce this by taking max(|dx|, |dy|) for both dimensions.
"""

import pygame
import globals as g
from tools.tool import Tool


class SquareTool(Tool):
    """Draws perfect square outlines (width == height)."""

    def __init__(self):
        self.is_dragging: bool = False
        self.start_pos: tuple[int, int] = (0, 0)
        self.end_pos: tuple[int, int] = (0, 0)

    def _get_square_rect(self) -> pygame.Rect:
        """Compute a square Rect from start_pos and end_pos."""
        dx = self.end_pos[0] - self.start_pos[0]
        dy = self.end_pos[1] - self.start_pos[1]
        side = max(abs(dx), abs(dy))

        x = self.start_pos[0] + (side if dx >= 0 else -side)
        y = self.start_pos[1] + (side if dy >= 0 else -side)

        rx = min(self.start_pos[0], x)
        ry = min(self.start_pos[1], y)
        return pygame.Rect(rx, ry, side, side)

    def draw(self, surface: pygame.Surface) -> None:
        if getattr(self, '_should_draw', False):
            rect = self._get_square_rect()
            if rect.width > 0:
                color = g.colors[g.color_selected]
                pygame.draw.rect(surface, color, rect, 1)
            self._should_draw = False

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if my > g.TOP_BAR_HEIGHT and mx > g.SIDE_PANEL_WIDTH:
                self.is_dragging = True
                self.start_pos = event.pos
                self.end_pos = event.pos

        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.end_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.end_pos = event.pos
                self.is_dragging = False
                self._should_draw = True

    def preview(self, screen: pygame.Surface) -> None:
        if self.is_dragging:
            rect = self._get_square_rect()
            if rect.width > 0:
                color = g.colors[g.color_selected]
                pygame.draw.rect(screen, color, rect, 1)
