"""Draws axis-aligned rectangles by click-and-drag."""

import pygame
import globals as g
from tools.tool import Tool


class RectangleTool(Tool):
    def __init__(self):
        self.is_dragging: bool = False
        self.start_pos: tuple[int, int] = (0, 0)
        self.end_pos: tuple[int, int] = (0, 0)

    def _get_rect(self) -> pygame.Rect:
        """Build a normalised Rect from two corner points."""
        x = min(self.start_pos[0], self.end_pos[0])
        y = min(self.start_pos[1], self.end_pos[1])
        w = abs(self.start_pos[0] - self.end_pos[0])
        h = abs(self.start_pos[1] - self.end_pos[1])
        return pygame.Rect(x, y, w, h)

    def draw(self, surface: pygame.Surface) -> None:
        if getattr(self, '_should_draw', False):
            rect = self._get_rect()
            if rect.width > 0 and rect.height > 0:
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
            rect = self._get_rect()
            if rect.width > 0 and rect.height > 0:
                color = g.colors[g.color_selected]
                pygame.draw.rect(screen, color, rect, 1)
