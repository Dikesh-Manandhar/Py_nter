"""
spray_tool.py — Spray Can / Airbrush tool.

While the mouse button is held, random pixels are painted inside a circular
radius around the cursor. Scroll wheel adjusts the spray radius.

=============================================================================
COMPUTER GRAPHICS CONCEPT — Stochastic Point Sampling
=============================================================================
The spray can randomly samples a subset of pixels each frame using rejection
sampling inside a circle:
    1. Generate random (dx, dy) in range [-radius, +radius].
    2. If dx² + dy² ≤ radius² → paint that pixel.
    3. Otherwise, reject and try again.

This is a form of Monte Carlo sampling — a technique used extensively in
computer graphics for anti-aliasing, soft shadows, ambient occlusion,
and global illumination (path tracing).
=============================================================================
"""

import pygame
import random
import globals as g
from tools.tool import Tool


class SprayTool(Tool):
    """Spray can / airbrush with adjustable radius and density."""

    MIN_RADIUS = 5
    MAX_RADIUS = 60
    DEFAULT_RADIUS = 20
    # Dots sprayed per frame
    DENSITY = 30

    def __init__(self):
        self.radius: int = self.DEFAULT_RADIUS
        self.is_spraying: bool = False

    def draw(self, surface: pygame.Surface) -> None:
        """Spray random dots inside a circle using rejection sampling."""
        if not self.is_spraying:
            return

        mx, my = g.mouse_pos
        if mx <= g.SIDE_PANEL_WIDTH or my <= g.TOP_BAR_HEIGHT:
            return

        color = g.colors[g.color_selected]
        r = self.radius

        for _ in range(self.DENSITY):
            dx = random.randint(-r, r)
            dy = random.randint(-r, r)

            # Rejection test: keep only if inside the circle
            if dx * dx + dy * dy <= r * r:
                px, py = mx + dx, my + dy
                # Bounds check
                w, h = surface.get_size()
                if 0 <= px < w and 0 <= py < h:
                    surface.set_at((px, py), color)

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if mx > g.SIDE_PANEL_WIDTH and my > g.TOP_BAR_HEIGHT:
                self.is_spraying = True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_spraying = False

        # Scroll wheel: adjust radius
        elif event.type == pygame.MOUSEWHEEL:
            self.radius += event.y * 3
            self.radius = max(self.MIN_RADIUS, min(self.MAX_RADIUS, self.radius))

    def preview(self, screen: pygame.Surface) -> None:
        mx, my = g.mouse_pos
        if my <= g.TOP_BAR_HEIGHT:
            return
        color = g.colors[g.color_selected]
        # Spray radius circle
        pygame.draw.circle(screen, color, (mx, my), self.radius, 1)
        # Crosshair
        pygame.draw.line(screen, color, (mx - 3, my), (mx + 3, my), 1)
        pygame.draw.line(screen, color, (mx, my - 3), (mx, my + 3), 1)
