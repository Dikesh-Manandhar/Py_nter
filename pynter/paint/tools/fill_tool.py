"""
fill_tool.py — Flood Fill (Paint Bucket) tool.

Click on any pixel in the canvas to fill the entire contiguous region of
the same color with the currently selected color.  This is the classic
"paint bucket" operation found in MS Paint and similar editors.

=============================================================================
COMPUTER GRAPHICS CONCEPT — Flood Fill Algorithm (BFS)
=============================================================================
Flood fill replaces all connected pixels of a "target color" with a "fill
color", starting from a seed point.

Algorithm (Breadth-First Search / BFS):
    1. Read the color of the clicked pixel → this is the "target color".
    2. If target color == fill color, do nothing (already filled).
    3. Create a queue and enqueue the seed pixel.
    4. While the queue is not empty:
        a. Dequeue a pixel (x, y).
        b. If it's outside bounds or not the target color, skip it.
        c. Set its color to the fill color.
        d. Enqueue its 4 neighbours (up, down, left, right).

    We use BFS rather than recursive DFS to avoid Python's recursion limit
    on large fill areas.

    A `visited` set prevents re-processing the same pixel.
=============================================================================
"""

import pygame
from collections import deque
import globals as g
from tools.tool import Tool


class FillTool(Tool):
    """Flood-fill a contiguous same-color region with the selected color."""

    def __init__(self):
        self._fill_pos: tuple[int, int] | None = None

    def draw(self, surface: pygame.Surface) -> None:
        if self._fill_pos is None:
            return

        x, y = self._fill_pos
        self._fill_pos = None

        w, h = surface.get_size()
        if x < 0 or x >= w or y < 0 or y >= h:
            return

        target_color = surface.get_at((x, y))[:3]
        fill_color = g.colors[g.color_selected]

        if target_color == fill_color:
            return

        # BFS Flood Fill
        surface.lock()

        queue = deque()
        queue.append((x, y))
        visited = set()
        visited.add((x, y))

        while queue:
            cx, cy = queue.popleft()

            current = surface.get_at((cx, cy))[:3]
            if current != target_color:
                continue

            surface.set_at((cx, cy), fill_color)

            for nx, ny in [(cx + 1, cy), (cx - 1, cy),
                           (cx, cy + 1), (cx, cy - 1)]:
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))

        surface.unlock()

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if mx > g.SIDE_PANEL_WIDTH and my > g.TOP_BAR_HEIGHT:
                self._fill_pos = (mx, my)

    def preview(self, screen: pygame.Surface) -> None:
        mx, my = g.mouse_pos
        if my <= g.TOP_BAR_HEIGHT:
            return
        size = 8
        color = g.colors[g.color_selected]
        pygame.draw.line(screen, color, (mx - size, my), (mx + size, my), 1)
        pygame.draw.line(screen, color, (mx, my - size), (mx, my + size), 1)
