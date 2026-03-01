"""Draws circles using the Midpoint Circle Algorithm.

Click to set centre, drag for radius, release to draw.

=============================================================================
COMPUTER GRAPHICS CONCEPT -- Midpoint Circle Algorithm
=============================================================================
Rasterises a circle using ONLY integer arithmetic.

1. 8-fold symmetry: if (x, y) is on the circle, so are
   (-x,y), (x,-y), (-x,-y), (y,x), (-y,x), (y,-x), (-y,-x).
   We only compute one octant and mirror the rest.

2. Start at (0, r) and step x forward. A decision parameter
   decides whether y stays or decreases by 1:
       p_initial = 1 - r
       If p < 0  -->  p = p + 2*x + 1          (stay on same row)
       If p >= 0 -->  y--; p = p + 2*(x-y) + 1 (move down a row)
=============================================================================
"""

import pygame
import math
import globals as g
from tools.tool import Tool


class CircleTool(Tool):
    def __init__(self):
        self.is_dragging: bool = False
        self.initial_pos: tuple[int, int] = (0, 0)
        self.final_pos: tuple[int, int] = (0, 0)
        self.radius: float = 0.0

    def _draw_circle_midpoint(self, surface: pygame.Surface,
                              cx: int, cy: int, r: int,
                              color: tuple[int, int, int]) -> None:
        """Rasterise a circle at (cx, cy) with radius r using midpoint algorithm."""
        if r <= 0:
            return

        x = 0
        y = r
        decision = 1 - r

        def _plot_8_points(px: int, py: int):
            """Plot all 8 symmetric points."""
            surface.set_at((cx + px, cy + py), color)
            surface.set_at((cx - px, cy + py), color)
            surface.set_at((cx + px, cy - py), color)
            surface.set_at((cx - px, cy - py), color)
            surface.set_at((cx + py, cy + px), color)
            surface.set_at((cx - py, cy + px), color)
            surface.set_at((cx + py, cy - px), color)
            surface.set_at((cx - py, cy - px), color)

        _plot_8_points(x, y)

        while x < y:
            x += 1
            if decision < 0:
                decision += 2 * x + 1
            else:
                y -= 1
                decision += 2 * (x - y) + 1
            _plot_8_points(x, y)

    def _distance(self, a: tuple[int, int], b: tuple[int, int]) -> float:
        return math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

    def draw(self, surface: pygame.Surface) -> None:
        if getattr(self, '_should_draw', False):
            mx, my = g.mouse_pos
            if mx > g.SIDE_PANEL_WIDTH and my > g.TOP_BAR_HEIGHT:
                color = g.colors[g.color_selected]
                self._draw_circle_midpoint(surface,
                                           self.initial_pos[0],
                                           self.initial_pos[1],
                                           int(self.radius), color)
            self._should_draw = False

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
            if self.is_dragging:
                self.final_pos = event.pos
                self.radius = self._distance(self.initial_pos, self.final_pos)
                self.is_dragging = False
                self._should_draw = True

    def preview(self, screen: pygame.Surface) -> None:
        if self.is_dragging and self.radius > 0:
            color = g.colors[g.color_selected]
            pygame.draw.circle(screen, color, self.initial_pos,
                               int(self.radius), 1)
