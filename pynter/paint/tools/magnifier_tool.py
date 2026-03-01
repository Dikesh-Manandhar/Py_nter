"""
magnifier_tool.py — Zoom / Magnifier tool.

Shows a magnified loupe window near the cursor for inspecting pixel details.
Drawing still happens at 1:1 scale.

COMPUTER GRAPHICS CONCEPT — Scaling / Magnification:
    Zooming in 2D is achieved by scaling the canvas surface before blitting.
    This tool provides a read-only magnifier: it shows a zoomed-in loupe
    window near the cursor so you can inspect pixel details.
"""

import pygame
import globals as g
from tools.tool import Tool


class MagnifierTool(Tool):
    """Shows a magnified loupe of the canvas area around the cursor."""

    LOUPE_SIZE = 120   # Size of the magnifier window (pixels)
    ZOOM_FACTOR = 4    # Magnification level
    BORDER_COLOR = (0, 0, 0)

    def __init__(self):
        self._canvas_snapshot: pygame.Surface | None = None

    def draw(self, surface: pygame.Surface) -> None:
        """Capture canvas snapshot for loupe preview."""
        self._canvas_snapshot = surface

    def handle_events(self, event: pygame.event.Event) -> None:
        pass

    def preview(self, screen: pygame.Surface) -> None:
        if self._canvas_snapshot is None:
            return

        mx, my = g.mouse_pos
        if my <= g.TOP_BAR_HEIGHT:
            return

        canvas = self._canvas_snapshot
        cw, ch = canvas.get_size()

        src_size = self.LOUPE_SIZE // self.ZOOM_FACTOR

        src_x = max(0, min(mx - src_size // 2, cw - src_size))
        src_y = max(0, min(my - src_size // 2, ch - src_size))
        src_rect = pygame.Rect(src_x, src_y, src_size, src_size)

        try:
            sub = canvas.subsurface(src_rect).copy()
        except ValueError:
            return
        magnified = pygame.transform.scale(sub,
                                           (self.LOUPE_SIZE, self.LOUPE_SIZE))

        # Position loupe offset from cursor
        loupe_x = mx + 20
        loupe_y = my - self.LOUPE_SIZE // 2

        # Keep loupe on screen
        if loupe_x + self.LOUPE_SIZE > g.SCREEN_WIDTH:
            loupe_x = mx - self.LOUPE_SIZE - 20
        if loupe_y < 0:
            loupe_y = 0
        if loupe_y + self.LOUPE_SIZE > g.SCREEN_HEIGHT:
            loupe_y = g.SCREEN_HEIGHT - self.LOUPE_SIZE

        # Draw magnified image with border
        screen.blit(magnified, (loupe_x, loupe_y))
        pygame.draw.rect(screen, self.BORDER_COLOR,
                         (loupe_x, loupe_y, self.LOUPE_SIZE, self.LOUPE_SIZE), 2)

        # Crosshair in centre of loupe
        cx = loupe_x + self.LOUPE_SIZE // 2
        cy = loupe_y + self.LOUPE_SIZE // 2
        pygame.draw.line(screen, (255, 0, 0),
                         (cx - 6, cy), (cx + 6, cy), 1)
        pygame.draw.line(screen, (255, 0, 0),
                         (cx, cy - 6), (cx, cy + 6), 1)

        # Label
        font = pygame.font.SysFont(None, 16)
        label = font.render(f"{self.ZOOM_FACTOR}x", True, (0, 0, 0))
        screen.blit(label, (loupe_x + 4, loupe_y + 4))
