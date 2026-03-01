"""
hypnotiser_tool.py — Draws concentric circles continuously while dragging.

Like CircleTool but draws on every frame while the mouse is held,
creating overlapping circles as the user moves. Uses the Midpoint Circle Algorithm.

COMPUTER GRAPHICS CONCEPT:
    Creative application of the midpoint circle algorithm. Drawing a circle
    at every frame while the mouse is held creates an interesting visual
    effect of many concentric / overlapping circles.
"""

import pygame
import math
import globals as g
from tools.tool import Tool


class HypnotiserTool(Tool):
    """Draws circles continuously while the mouse is held down."""

    def __init__(self):
        self.is_dragging: bool = False
        self.initial_pos: tuple[int, int] = (0, 0)
        self.final_pos: tuple[int, int] = (0, 0)
        self.radius: float = 0.0

    def _draw_circle_midpoint(self, surface: pygame.Surface,
                              cx: int, cy: int, r: int,
                              color: tuple[int, int, int]) -> None:
        """Midpoint Circle Algorithm — see circle_tool.py for details."""
        if r <= 0:
            return

        x = 0
        y = r
        decision = 1 - r

        def _plot_8(px: int, py: int):
            surface.set_at((cx + px, cy + py), color)
            surface.set_at((cx - px, cy + py), color)
            surface.set_at((cx + px, cy - py), color)
            surface.set_at((cx - px, cy - py), color)
            surface.set_at((cx + py, cy + px), color)
            surface.set_at((cx - py, cy + px), color)
            surface.set_at((cx + py, cy - px), color)
            surface.set_at((cx - py, cy - px), color)

        _plot_8(x, y)

        while x < y:
            x += 1
            if decision < 0:
                decision += 2 * x + 1
            else:
                y -= 1
                decision += 2 * (x - y) + 1
            _plot_8(x, y)

    def _distance(self, a: tuple, b: tuple) -> float:
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def draw(self, surface: pygame.Surface) -> None:
        buttons = pygame.mouse.get_pressed()
        if buttons[0] and self.is_dragging:
            mx, my = g.mouse_pos
            if mx > g.SIDE_PANEL_WIDTH and my > g.TOP_BAR_HEIGHT:
                color = g.colors[g.color_selected]
                self._draw_circle_midpoint(surface,
                                           self.initial_pos[0],
                                           self.initial_pos[1],
                                           int(self.radius), color)

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if my > g.TOP_BAR_HEIGHT and mx > g.SIDE_PANEL_WIDTH:
                self.is_dragging = True
                self.initial_pos = event.pos
                self.radius = 0

        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.final_pos = event.pos
            self.radius = self._distance(self.initial_pos, self.final_pos)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False

    def preview(self, screen: pygame.Surface) -> None:
        if self.is_dragging and self.radius > 0:
            color = g.colors[g.color_selected]
            pygame.draw.circle(screen, color, self.initial_pos,
                               int(self.radius), 1)
