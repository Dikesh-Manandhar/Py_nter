"""
symmetry_tool.py — N-fold Symmetry / Mandala drawing tool.

Every stroke the user makes is replicated N times around a central point,
rotated by 360°/N each time.  This produces stunning kaleidoscope / mandala
patterns with minimal effort.

=============================================================================
COMPUTER GRAPHICS CONCEPT — 2D Rotation Transform
=============================================================================
To rotate a point (x, y) around an origin (cx, cy) by angle θ:

    x' = cx + (x - cx) · cos(θ) − (y - cy) · sin(θ)
    y' = cy + (x - cx) · sin(θ) + (y - cy) · cos(θ)

This is the fundamental 2D rotation matrix:

    ┌ cos θ  −sin θ ┐
    └ sin θ   cos θ ┘

For N-fold symmetry we repeat the stroke at angles:
    θ_k = k · (2π / N),    k = 0, 1, …, N-1

The tool also optionally mirrors each rotated copy (reflection symmetry),
which doubles the visual complexity.

Scroll wheel adjusts N (the fold count) in range [2, 16].
=============================================================================
"""

import pygame
import math
import globals as g
from tools.tool import Tool


class SymmetryTool(Tool):
    """N-fold rotational symmetry drawing (mandala / kaleidoscope)."""

    MIN_FOLDS = 2
    MAX_FOLDS = 16
    DEFAULT_FOLDS = 6
    BRUSH_SIZE = 2  # Radius of each dot

    def __init__(self):
        self.folds: int = self.DEFAULT_FOLDS
        self.is_drawing: bool = False
        self.prev_pos: tuple[int, int] | None = None
        # Centre of symmetry — middle of the canvas
        self.cx: int = g.SIDE_PANEL_WIDTH + (g.SCREEN_WIDTH - g.SIDE_PANEL_WIDTH) // 2
        self.cy: int = g.TOP_BAR_HEIGHT + (g.SCREEN_HEIGHT - g.TOP_BAR_HEIGHT) // 2
        self.mirror: bool = True

    def _rotate_point(self, x: int, y: int, angle: float) -> tuple[int, int]:
        """Rotate point (x, y) around (cx, cy) by `angle` radians."""
        dx = x - self.cx
        dy = y - self.cy
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        rx = self.cx + int(dx * cos_a - dy * sin_a)
        ry = self.cy + int(dx * sin_a + dy * cos_a)
        return (rx, ry)

    def _reflect_point(self, x: int, y: int, angle: float) -> tuple[int, int]:
        """Reflect point (x, y) across a line through (cx, cy) at `angle`."""
        dx = x - self.cx
        dy = y - self.cy
        cos2a = math.cos(2 * angle)
        sin2a = math.sin(2 * angle)
        rx = self.cx + int(dx * cos2a + dy * sin2a)
        ry = self.cy + int(dx * sin2a - dy * cos2a)
        return (rx, ry)

    def _draw_symmetric_line(self, surface: pygame.Surface,
                              p1: tuple[int, int], p2: tuple[int, int],
                              color: tuple[int, int, int]) -> None:
        """Draw a line from p1 to p2, replicated N times with rotational symmetry."""
        angle_step = 2 * math.pi / self.folds

        for k in range(self.folds):
            angle = k * angle_step

            # Rotate both endpoints
            rp1 = self._rotate_point(p1[0], p1[1], angle)
            rp2 = self._rotate_point(p2[0], p2[1], angle)
            pygame.draw.line(surface, color, rp1, rp2, self.BRUSH_SIZE * 2)

            if self.mirror:
                mp1 = self._reflect_point(p1[0], p1[1], angle / 2)
                mp2 = self._reflect_point(p2[0], p2[1], angle / 2)
                pygame.draw.line(surface, color, mp1, mp2, self.BRUSH_SIZE * 2)

    def draw(self, surface: pygame.Surface) -> None:
        if not self.is_drawing:
            return

        mx, my = g.mouse_pos
        if mx <= g.SIDE_PANEL_WIDTH or my <= g.TOP_BAR_HEIGHT:
            return

        color = g.colors[g.color_selected]

        if self.prev_pos is not None:
            self._draw_symmetric_line(surface, self.prev_pos, (mx, my), color)

        self.prev_pos = (mx, my)

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if mx > g.SIDE_PANEL_WIDTH and my > g.TOP_BAR_HEIGHT:
                self.is_drawing = True
                self.prev_pos = (mx, my)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_drawing = False
            self.prev_pos = None

        # Scroll: adjust fold count
        elif event.type == pygame.MOUSEWHEEL:
            self.folds += event.y
            self.folds = max(self.MIN_FOLDS, min(self.MAX_FOLDS, self.folds))

        # M key: toggle mirror
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self.mirror = not self.mirror

    def preview(self, screen: pygame.Surface) -> None:
        """Draw symmetry axis guide lines and info text."""
        mx, my = g.mouse_pos
        if my <= g.TOP_BAR_HEIGHT:
            return

        color = g.colors[g.color_selected]
        angle_step = 2 * math.pi / self.folds
        guide_len = max(g.SCREEN_WIDTH, g.SCREEN_HEIGHT)

        # Draw symmetry axis lines (thin, semi-transparent)
        for k in range(self.folds):
            angle = k * angle_step
            ex = self.cx + int(guide_len * math.cos(angle))
            ey = self.cy + int(guide_len * math.sin(angle))
            # Use a translucent surface for the guide lines
            pygame.draw.line(screen, (80, 80, 100), (self.cx, self.cy), (ex, ey), 1)

        # Centre dot
        pygame.draw.circle(screen, RETRO_HIGHLIGHT, (self.cx, self.cy), 4)
        pygame.draw.circle(screen, (255, 255, 255), (self.cx, self.cy), 2)

        # Info text
        font = pygame.font.SysFont("Courier", 14, bold=True)
        mirror_str = " +Mirror" if self.mirror else ""
        info = f"{self.folds}-fold{mirror_str}  [scroll ±N, M=mirror]"
        surf = font.render(info, True, (200, 200, 210))
        screen.blit(surf, (g.SIDE_PANEL_WIDTH + 10, g.SCREEN_HEIGHT - 24))


# Colour constant used in preview (matching tool_select.py)
RETRO_HIGHLIGHT = (0, 180, 220)
