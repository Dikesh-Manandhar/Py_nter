"""
triangle_tool.py — Draws triangles by click-and-drag.

The user clicks to set the base-centre, then drags upward or downward to
set the apex.  The resulting triangle is isosceles:

        apex
        /  \\
       /    \\
      /______\\
    base-left  base-right

The base width equals the vertical drag distance, giving a well-proportioned
triangle.

Corresponds to: TriangleTool.h in the C++ version (was an empty stub).

COMPUTER GRAPHICS CONCEPT:
    A triangle is the simplest polygon.  It is defined by exactly 3 vertices
    and drawn as a closed polyline (outline) using pygame.draw.polygon.
    Triangles are the fundamental building block in 3D graphics — every 3D
    mesh is composed of triangles.
"""

import pygame
import globals as g
from tools.tool import Tool


class TriangleTool(Tool):
    """Draws isosceles triangles by click-and-drag."""

    def __init__(self):
        self.is_dragging: bool = False
        self.start_pos: tuple[int, int] = (0, 0)
        self.end_pos: tuple[int, int] = (0, 0)

    def _get_triangle_points(self) -> list[tuple[int, int]]:
        """Compute the 3 vertices of an isosceles triangle."""
        sx, sy = self.start_pos
        ex, ey = self.end_pos

        dy = abs(ey - sy)
        half_base = dy // 2

        apex = (ex, ey)
        base_left = (sx - half_base, sy)
        base_right = (sx + half_base, sy)

        return [apex, base_left, base_right]

    def draw(self, surface: pygame.Surface) -> None:
        if getattr(self, '_should_draw', False):
            pts = self._get_triangle_points()
            color = g.colors[g.color_selected]
            if abs(self.end_pos[1] - self.start_pos[1]) > 2:
                pygame.draw.polygon(surface, color, pts, 1)
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
            pts = self._get_triangle_points()
            if abs(self.end_pos[1] - self.start_pos[1]) > 2:
                color = g.colors[g.color_selected]
                pygame.draw.polygon(screen, color, pts, 1)
