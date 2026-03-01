"""Draws straight lines using Bresenham's Line Algorithm.

Click to set start point, drag and release to draw the line.

=============================================================================
COMPUTER GRAPHICS CONCEPT -- Bresenham's Line Algorithm
=============================================================================
Draws a straight line between two points using ONLY integer arithmetic
(additions and comparisons -- no floating-point multiply or divide).

Key idea:
    At each step, a "decision parameter" determines whether the next pixel
    goes straight or diagonally. When the error crosses a threshold, it
    steps in the secondary axis.

    For slopes |m| <= 1, we step along X and decide on Y.
    For slopes |m| >  1, we step along Y and decide on X.
=============================================================================
"""

import pygame
import globals as g
from tools.tool import Tool


class LineTool(Tool):
    def __init__(self):
        self.is_dragging: bool = False
        self.initial_pos: tuple[int, int] = (0, 0)
        self.final_pos: tuple[int, int] = (0, 0)

    def _draw_line_bresenham(self, surface: pygame.Surface,
                             p0: tuple[int, int], pf: tuple[int, int],
                             color: tuple[int, int, int]) -> None:
        """Rasterise a line from p0 to pf using Bresenham's algorithm."""
        x0, y0 = p0
        xf, yf = pf
        dx = xf - x0
        dy = yf - y0

        # Vertical line (infinite slope)
        if dx == 0:
            step = 1 if dy > 0 else -1
            y = y0
            while y != yf + step:
                surface.set_at((x0, y), color)
                y += step
            return

        slope = abs(dy / dx)

        # |slope| <= 1: step along X, decide on Y
        if slope <= 1:
            if dx < 0:
                x0, y0, xf, yf = xf, yf, x0, y0
                dx, dy = -dx, -dy

            decision = 2 * abs(dy) - dx
            y = y0
            y_step = 1 if dy > 0 else -1

            for x in range(x0, xf + 1):
                surface.set_at((x, y), color)
                if decision > 0:
                    y += y_step
                    decision += 2 * (abs(dy) - dx)
                else:
                    decision += 2 * abs(dy)

        # |slope| > 1: step along Y, decide on X
        else:
            if dy < 0:
                x0, y0, xf, yf = xf, yf, x0, y0
                dx, dy = -dx, -dy

            decision = 2 * abs(dx) - dy
            x = x0
            x_step = 1 if dx > 0 else -1

            for y in range(y0, yf + 1):
                surface.set_at((x, y), color)
                if decision > 0:
                    x += x_step
                    decision += 2 * (abs(dx) - dy)
                else:
                    decision += 2 * abs(dx)

    def draw(self, surface: pygame.Surface) -> None:
        if getattr(self, '_should_draw', False):
            color = g.colors[g.color_selected]
            if self.initial_pos[0] > self.final_pos[0]:
                self._draw_line_bresenham(surface, self.final_pos,
                                          self.initial_pos, color)
            else:
                self._draw_line_bresenham(surface, self.initial_pos,
                                          self.final_pos, color)
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
            color = g.colors[g.color_selected]
            pygame.draw.line(screen, color, self.initial_pos, self.final_pos, 1)
