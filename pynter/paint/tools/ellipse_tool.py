"""Draws ellipses using the Midpoint Ellipse Algorithm.

Click-drag to define bounding box, release to draw.

=============================================================================
COMPUTER GRAPHICS CONCEPT -- Midpoint Ellipse Algorithm
=============================================================================
Ellipse equation: (x-xc)^2/rx^2 + (y-yc)^2/ry^2 = 1

The first quadrant is split into TWO REGIONS based on slope:
    Region 1: |slope| < 1  (near top)  -- step X, decide on Y
    Region 2: |slope| >= 1 (near side) -- step Y, decide on X

A decision parameter in each region determines diagonal vs straight step.
We exploit 4-fold symmetry (not 8, since rx != ry in general).
=============================================================================
"""

import pygame
import globals as g
from tools.tool import Tool


class EllipseTool(Tool):
    def __init__(self):
        self.is_dragging: bool = False
        self.initial_pos: tuple[int, int] = (0, 0)
        self.final_pos: tuple[int, int] = (0, 0)

    def _draw_ellipse_midpoint(self, surface: pygame.Surface,
                               xc: int, yc: int, rx: int, ry: int,
                               color: tuple[int, int, int]) -> None:
        """Rasterise an ellipse at (xc, yc) with semi-axes rx, ry."""
        if rx <= 0 or ry <= 0:
            return

        rx2 = rx * rx
        ry2 = ry * ry
        two_rx2 = 2 * rx2
        two_ry2 = 2 * ry2

        x = 0
        y = ry
        px = 0
        py = two_rx2 * y

        def _plot_4(px_: int, py_: int):
            """Plot all 4 symmetric points."""
            surface.set_at((xc + px_, yc + py_), color)
            surface.set_at((xc - px_, yc + py_), color)
            surface.set_at((xc + px_, yc - py_), color)
            surface.set_at((xc - px_, yc - py_), color)

        # Region 1: |slope| < 1 -- step along X, decide on Y
        p1 = ry2 - (rx2 * ry) + (0.25 * rx2)
        _plot_4(x, y)

        while px < py:
            x += 1
            px += two_ry2
            if p1 < 0:
                p1 += ry2 + px
            else:
                y -= 1
                py -= two_rx2
                p1 += ry2 + px - py
            _plot_4(x, y)

        # Region 2: |slope| >= 1 -- step along Y, decide on X
        p2 = (ry2 * (x + 0.5) * (x + 0.5) +
              rx2 * (y - 1) * (y - 1) -
              rx2 * ry2)

        while y > 0:
            y -= 1
            py -= two_rx2
            if p2 > 0:
                p2 += rx2 - py
            else:
                x += 1
                px += two_ry2
                p2 += rx2 - py + px
            _plot_4(x, y)

    def _get_ellipse_params(self) -> tuple[int, int, int, int]:
        """Compute centre and semi-axes from bounding box corners."""
        xc = (self.initial_pos[0] + self.final_pos[0]) // 2
        yc = (self.initial_pos[1] + self.final_pos[1]) // 2
        rx = abs(self.final_pos[0] - self.initial_pos[0]) // 2
        ry = abs(self.final_pos[1] - self.initial_pos[1]) // 2
        return xc, yc, rx, ry

    def draw(self, surface: pygame.Surface) -> None:
        if getattr(self, '_should_draw', False):
            xc, yc, rx, ry = self._get_ellipse_params()
            color = g.colors[g.color_selected]
            self._draw_ellipse_midpoint(surface, xc, yc, rx, ry, color)
            self._should_draw = False

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if my > g.TOP_BAR_HEIGHT and mx > g.SIDE_PANEL_WIDTH:
                self.is_dragging = True
                self.initial_pos = event.pos
                self.final_pos = event.pos

        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.final_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.final_pos = event.pos
                self.is_dragging = False
                self._should_draw = True

    def preview(self, screen: pygame.Surface) -> None:
        if self.is_dragging:
            xc, yc, rx, ry = self._get_ellipse_params()
            if rx > 0 and ry > 0:
                color = g.colors[g.color_selected]
                rect = pygame.Rect(xc - rx, yc - ry, rx * 2, ry * 2)
                pygame.draw.ellipse(screen, color, rect, 1)
