"""
select_box_tool.py — Rectangular selection tool.

Click and drag to select a rectangular region. Once selected, move it by
clicking inside and dragging. Press ENTER to commit, ESC to cancel.

COMPUTER GRAPHICS CONCEPT:
    Selection tools work by copying a rectangular region of pixels into
    a temporary buffer. The original area is filled with background color.
    The buffer is drawn at the cursor position as a floating overlay
    until the user commits or cancels.
"""

import pygame
import globals as g
from tools.tool import Tool


class SelectBoxTool(Tool):
    """Select, move, and re-place rectangular regions of the canvas."""

    def __init__(self):
        self.is_selecting: bool = False
        self.start_pos: tuple[int, int] = (0, 0)
        self.end_pos: tuple[int, int] = (0, 0)

        self.has_selection: bool = False
        self.is_moving: bool = False
        self.selected_surface: pygame.Surface | None = None
        self.selection_rect: pygame.Rect | None = None
        self.move_offset: tuple[int, int] = (0, 0)

    def _get_rect(self) -> pygame.Rect:
        """Build a normalised Rect from start_pos / end_pos."""
        x = min(self.start_pos[0], self.end_pos[0])
        y = min(self.start_pos[1], self.end_pos[1])
        w = abs(self.start_pos[0] - self.end_pos[0])
        h = abs(self.start_pos[1] - self.end_pos[1])
        return pygame.Rect(x, y, max(w, 1), max(h, 1))

    def draw(self, surface: pygame.Surface) -> None:
        if getattr(self, '_commit', False):
            if self.selected_surface and self.selection_rect:
                surface.blit(self.selected_surface, self.selection_rect.topleft)
            self._reset()
            self._commit = False

        # When selection is first made, cut the region from the canvas
        if getattr(self, '_cut', False):
            rect = self._get_rect()
            if rect.width > 1 and rect.height > 1:
                self.selected_surface = surface.subsurface(rect).copy()
                pygame.draw.rect(surface, (255, 255, 255), rect)
                self.selection_rect = rect.copy()
                self.has_selection = True
            self._cut = False

    def handle_events(self, event: pygame.event.Event) -> None:
        mx, my = g.mouse_pos

        # ENTER: commit the floating selection
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.has_selection:
                self._commit = True
            return

        # ESCAPE: cancel selection
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._reset()
            return

        # Mouse handling
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if mx <= g.SIDE_PANEL_WIDTH or my <= g.TOP_BAR_HEIGHT:
                return

            if self.has_selection and self.selection_rect and \
               self.selection_rect.collidepoint(mx, my):
                # Click inside existing selection → start moving
                self.is_moving = True
                self.move_offset = (mx - self.selection_rect.x,
                                    my - self.selection_rect.y)
            else:
                # Start a new selection
                self._reset()
                self.is_selecting = True
                self.start_pos = (mx, my)
                self.end_pos = (mx, my)

        elif event.type == pygame.MOUSEMOTION:
            if self.is_selecting:
                self.end_pos = (mx, my)
            elif self.is_moving and self.selection_rect:
                self.selection_rect.x = mx - self.move_offset[0]
                self.selection_rect.y = my - self.move_offset[1]

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_selecting:
                self.end_pos = (mx, my)
                self.is_selecting = False
                self._cut = True
            elif self.is_moving:
                self.is_moving = False

    def preview(self, screen: pygame.Surface) -> None:
        if self.is_selecting:
            rect = self._get_rect()
            pygame.draw.rect(screen, (0, 0, 200), rect, 1)

        if self.has_selection and self.selected_surface and self.selection_rect:
            screen.blit(self.selected_surface, self.selection_rect.topleft)
            pygame.draw.rect(screen, (0, 100, 255), self.selection_rect, 2)

    def _reset(self):
        """Clear all selection state."""
        self.is_selecting = False
        self.has_selection = False
        self.is_moving = False
        self.selected_surface = None
        self.selection_rect = None
