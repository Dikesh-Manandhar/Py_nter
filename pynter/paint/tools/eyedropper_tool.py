"""
eyedropper_tool.py — Color picker (Eye Dropper) tool.

Click on any pixel to sample its color and set it as the current drawing color.
If the sampled color matches a palette color, that swatch is selected.
Otherwise, the sampled color replaces the current palette slot.

COMPUTER GRAPHICS CONCEPT:
    The eyedropper reads back the color value from the framebuffer at a
    given pixel coordinate using surface.get_at((x, y)).
"""

import pygame
import globals as g
from tools.tool import Tool


class EyeDropperTool(Tool):
    """Sample a pixel color from the canvas and set it as the active color."""

    def __init__(self):
        self.sampled_color: tuple[int, int, int] | None = None

    def draw(self, surface: pygame.Surface) -> None:
        if getattr(self, '_sample_pos', None) is not None:
            x, y = self._sample_pos
            self._sample_pos = None

            w, h = surface.get_size()
            if 0 <= x < w and 0 <= y < h:
                pixel_color = surface.get_at((x, y))[:3]
                self.sampled_color = pixel_color

                # Try to match in palette
                for i, c in enumerate(g.colors):
                    if c == pixel_color:
                        g.color_selected = i
                        return

                # Not in palette → replace current slot
                g.colors[g.color_selected] = pixel_color

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if mx > g.SIDE_PANEL_WIDTH and my > g.TOP_BAR_HEIGHT:
                self._sample_pos = (mx, my)

    def preview(self, screen: pygame.Surface) -> None:
        mx, my = g.mouse_pos
        if my <= g.TOP_BAR_HEIGHT:
            return

        # Crosshair cursor
        pygame.draw.line(screen, (0, 0, 0), (mx - 8, my), (mx + 8, my), 1)
        pygame.draw.line(screen, (0, 0, 0), (mx, my - 8), (mx, my + 8), 1)
        pygame.draw.circle(screen, (0, 0, 0), (mx, my), 3, 1)

        if self.sampled_color:
            swatch = pygame.Rect(mx + 12, my - 12, 16, 16)
            pygame.draw.rect(screen, self.sampled_color, swatch)
            pygame.draw.rect(screen, (0, 0, 0), swatch, 1)
