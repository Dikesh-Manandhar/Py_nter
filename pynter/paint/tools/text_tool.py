"""
text_tool.py — Text input tool for placing text on the canvas.

Click to set insertion point, type text, press ENTER to commit, ESC to cancel.

COMPUTER GRAPHICS CONCEPT:
    Text rendering converts font glyph outlines (vector data) into a bitmap
    (raster data) at a given size, then blits that bitmap onto the canvas.
"""

import pygame
import globals as g
from tools.tool import Tool


class TextTool(Tool):
    """Place text on the canvas by clicking and typing."""

    FONT_SIZE = 24  # Default font size in pixels

    def __init__(self):
        self.current_text: str = ""
        self.text_pos: tuple[int, int] | None = None
        self.is_typing: bool = False
        self._font: pygame.font.Font | None = None

    @property
    def font(self) -> pygame.font.Font:
        """Lazy-init font so pygame.font.init() has time to run."""
        if self._font is None:
            self._font = pygame.font.SysFont("Arial", self.FONT_SIZE)
        return self._font

    def draw(self, surface: pygame.Surface) -> None:
        if getattr(self, '_commit', False):
            if self.current_text and self.text_pos:
                color = g.colors[g.color_selected]
                text_surface = self.font.render(self.current_text, True, color)
                surface.blit(text_surface, self.text_pos)
            # Reset for next text placement
            self.current_text = ""
            self.text_pos = None
            self.is_typing = False
            self._commit = False

    def handle_events(self, event: pygame.event.Event) -> None:
        mx, my = g.mouse_pos

        # Click to set text position
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if mx > g.SIDE_PANEL_WIDTH and my > g.TOP_BAR_HEIGHT:
                if self.is_typing and self.current_text:
                    self._commit = True
                self.text_pos = (mx, my)
                self.current_text = ""
                self.is_typing = True

        # Keyboard input while typing
        if event.type == pygame.KEYDOWN and self.is_typing:
            if event.key == pygame.K_RETURN:
                if self.current_text:
                    self._commit = True
                else:
                    self.is_typing = False

            elif event.key == pygame.K_ESCAPE:
                self.current_text = ""
                self.text_pos = None
                self.is_typing = False

            elif event.key == pygame.K_BACKSPACE:
                self.current_text = self.current_text[:-1]

            else:
                if event.unicode and event.unicode.isprintable():
                    self.current_text += event.unicode

    def preview(self, screen: pygame.Surface) -> None:
        if self.is_typing and self.text_pos:
            color = g.colors[g.color_selected]

            if self.current_text:
                text_surface = self.font.render(self.current_text, True, color)
                screen.blit(text_surface, self.text_pos)
                # Blinking cursor after text
                cursor_x = self.text_pos[0] + text_surface.get_width() + 2
                cursor_y = self.text_pos[1]
                # Blink cursor
                if (pygame.time.get_ticks() // 500) % 2 == 0:
                    pygame.draw.line(screen, color,
                                     (cursor_x, cursor_y),
                                     (cursor_x, cursor_y + self.FONT_SIZE), 2)
            else:
                # No text yet — show cursor at click point
                if (pygame.time.get_ticks() // 500) % 2 == 0:
                    pygame.draw.line(screen, color,
                                     self.text_pos,
                                     (self.text_pos[0],
                                      self.text_pos[1] + self.FONT_SIZE), 2)
