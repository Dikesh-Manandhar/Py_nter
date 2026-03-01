"""
curve_tool.py — Bezier Curve Tool using the Bernstein polynomial method.

The user clicks on the canvas to place control points.  A smooth Bezier
curve is computed through those points in real time and displayed as a
preview.  When the user presses ENTER, the curve is committed to the canvas.
Control points can be repositioned by clicking and dragging them.

=============================================================================
COMPUTER GRAPHICS CONCEPT — Bezier Curves
=============================================================================
A Bezier curve of degree n is defined by n+1 control points P_0 ... P_n:

    B(t) = Σ_{i=0}^{n}  C(n,i) * (1-t)^(n-i) * t^i * P_i     for t ∈ [0,1]

Where C(n,i) is the binomial coefficient ("n choose i").

Important properties:
    • The curve always starts at P_0 and ends at P_n.
    • The curve is "pulled toward" intermediate control points but does
      not necessarily pass through them.
    • Higher-degree curves (more control points) produce smoother shapes.

This tool evaluates the Bezier formula at thousands of t values (t = 0.0
to 1.0 in steps of 0.001) to produce a dense series of pixel locations
that approximate the smooth curve.
=============================================================================
"""

import pygame
import math
import globals as g
from tools.tool import Tool


class CurveTool(Tool):
    """Interactive Bezier curve tool with draggable control points."""

    # Radius of the control-point handles (for display and hit testing)
    CONTROL_POINT_RADIUS = 8
    # Step size for curve sampling (smaller = smoother but slower)
    T_STEP = 0.001

    def __init__(self):
        # List of (x, y) control points placed by the user
        self.control_points: list[tuple[int, int]] = []
        # Pre-computed curve pixel positions (recomputed when points change)
        self.curve_points: list[tuple[float, float]] = []
        # True when user presses Enter → commit to canvas
        self.enter_pressed: bool = False
        # Drag state for repositioning existing control points
        self.is_changing_point: bool = False
        self.changing_index: int = -1

    # -----------------------------------------------------------------
    #  Bezier math
    # -----------------------------------------------------------------

    def _bezier_point(self, t: float) -> tuple[float, float]:
        """Evaluate the Bezier curve at parameter t using Bernstein polynomials."""
        n = len(self.control_points)
        x, y = 0.0, 0.0
        for i in range(n):
            # Binomial coefficient C(n-1, i)
            bin_coeff = g.nCr(n - 1, i)
            # Bernstein basis polynomial
            term = bin_coeff * ((1 - t) ** (n - 1 - i)) * (t ** i)
            x += term * self.control_points[i][0]
            y += term * self.control_points[i][1]
        return (x, y)

    def _compute_curve(self) -> list[tuple[float, float]]:
        """Sample the Bezier curve at many t values to get pixel positions."""
        if len(self.control_points) < 2:
            return []
        points = []
        t = 0.0
        while t <= 1.0:
            points.append(self._bezier_point(t))
            t += self.T_STEP
        return points

    # -----------------------------------------------------------------
    #  Tool interface
    # -----------------------------------------------------------------

    def draw(self, surface: pygame.Surface) -> None:
        if self.enter_pressed:
            color = g.colors[g.color_selected]
            for pt in self.curve_points:
                x, y = int(pt[0]), int(pt[1])
                if 0 <= x < surface.get_width() and 0 <= y < surface.get_height():
                    surface.set_at((x, y), color)
            self.control_points.clear()
            self.curve_points.clear()
            self.enter_pressed = False

    def handle_events(self, event: pygame.event.Event) -> None:
        mx, my = g.mouse_pos

        if mx < g.SIDE_PANEL_WIDTH or my < g.TOP_BAR_HEIGHT:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, pt in enumerate(self.control_points):
                dist = math.sqrt((mx - pt[0]) ** 2 + (my - pt[1]) ** 2)
                if dist <= self.CONTROL_POINT_RADIUS:
                    self.is_changing_point = True
                    self.changing_index = i
                    return

            self.control_points.append((mx, my))
            self.curve_points = self._compute_curve()

        elif event.type == pygame.MOUSEMOTION:
            if self.is_changing_point and self.changing_index >= 0:
                self.control_points[self.changing_index] = (mx, my)
                self.curve_points = self._compute_curve()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_changing_point = False
            self.changing_index = -1

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if len(self.control_points) >= 2:
                self.enter_pressed = True

    def preview(self, screen: pygame.Surface) -> None:
        if self.enter_pressed:
            return

        color = g.colors[g.color_selected]

        for pt in self.control_points:
            pygame.draw.circle(screen, (255, 0, 0), pt,
                               self.CONTROL_POINT_RADIUS)

        for pt in self.curve_points:
            x, y = int(pt[0]), int(pt[1])
            if 0 <= x < screen.get_width() and 0 <= y < screen.get_height():
                screen.set_at((x, y), color)
