"""
color_select.py — Retro-styled colour palette bar + RGB colour picker.

Features:
    • 24 preset colour swatches (including white)
    • Click any swatch to select it as the drawing colour
    • SAVE button (bitmap floppy-disk icon)
    • PICK button opens an inline RGB colour picker panel
    • LEFT / RIGHT arrow keys cycle through colours
    • Colour picker has three sliders (R, G, B) and a preview swatch
"""

import pygame
import globals as g
from bitmap_utils import bitmap_to_surface, ICON_FILE_SAVE, ICON_COLOR_PICKER, ICON_BIN

# Retro colours (matching tool_select.py)
RETRO_BG       = (42, 42, 54)
RETRO_BG_LIGHT = (58, 58, 72)
RETRO_BORDER   = (80, 80, 100)
RETRO_TEXT     = (200, 200, 210)
RETRO_HIGHLIGHT = (0, 180, 220)


class ColorSelect:
    """Manages the colour palette toolbar and RGB colour picker panel."""

    def __init__(self):
        self.color_rects: list[pygame.Rect] = []
        self.save_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.clear_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.pick_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.color_mouse_hover: int = -1
        self.save_requested: bool = False
        self.clear_requested: bool = False

        # Colour picker state
        self.picker_open: bool = False
        self.picker_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        # Custom RGB values for the picker (start with mid-gray)
        self.pick_r: int = 128
        self.pick_g: int = 128
        self.pick_b: int = 128
        # Which slider is being dragged (-1 = none)
        self._dragging_slider: int = -1

        self._save_icon: pygame.Surface | None = None
        self._pick_icon: pygame.Surface | None = None
        self._bin_icon: pygame.Surface | None = None

    def init(self):
        """Initialise palette colours, compute swatch rects, and pre-render icons."""
        # 24 colours
        g.colors = [
            (255, 255, 255),  # WHITE  ← newly added
            (245, 245, 245),  # RAYWHITE
            (253, 249, 0),    # YELLOW
            (255, 203, 0),    # GOLD
            (255, 161, 0),    # ORANGE
            (255, 109, 194),  # PINK
            (230, 41, 55),    # RED
            (190, 33, 55),    # MAROON
            (0, 228, 48),     # GREEN
            (0, 158, 47),     # LIME
            (0, 117, 44),     # DARKGREEN
            (102, 191, 255),  # SKYBLUE
            (0, 121, 241),    # BLUE
            (0, 82, 172),     # DARKBLUE
            (200, 122, 255),  # PURPLE
            (135, 60, 190),   # VIOLET
            (112, 31, 126),   # DARKPURPLE
            (211, 176, 131),  # BEIGE
            (127, 106, 79),   # BROWN
            (76, 63, 47),     # DARKBROWN
            (200, 200, 200),  # LIGHTGRAY
            (130, 130, 130),  # GRAY
            (80, 80, 80),     # DARKGRAY
            (0, 0, 0),        # BLACK
        ]
        g.MAX_COLORS_COUNT = len(g.colors)
        g.color_selected = 0

        # Swatch rectangles
        swatch_size = 26
        gap = 2
        start_x = 180
        self.color_rects = []
        for i in range(g.MAX_COLORS_COUNT):
            rect = pygame.Rect(start_x + (swatch_size + gap) * i, 12,
                               swatch_size, swatch_size)
            self.color_rects.append(rect)

        # Action buttons (right side of top bar)
        btn_size = 36
        right_x = g.SCREEN_WIDTH - 50
        self.save_rect   = pygame.Rect(right_x - btn_size * 2 - 12, 7, btn_size, btn_size)
        self.clear_rect  = pygame.Rect(right_x - btn_size - 4, 7, btn_size, btn_size)
        self.pick_rect   = pygame.Rect(right_x - btn_size * 3 - 20, 7, btn_size, btn_size)

        # Colour picker panel (below top bar, initially hidden)
        self.picker_rect = pygame.Rect(g.SIDE_PANEL_WIDTH + 10, g.TOP_BAR_HEIGHT + 4,
                                       320, 120)

        # Pre-render icons
        self._save_icon = bitmap_to_surface(ICON_FILE_SAVE, RETRO_TEXT, scale=2)
        self._pick_icon = bitmap_to_surface(ICON_COLOR_PICKER, RETRO_TEXT, scale=2)
        self._bin_icon  = bitmap_to_surface(ICON_BIN, RETRO_TEXT, scale=2)

    # Slider helpers

    def _slider_rects(self) -> list[tuple[pygame.Rect, str, int]]:
        """Return (track_rect, label, value) for R, G, B sliders."""
        px, py = self.picker_rect.x, self.picker_rect.y
        track_w = 200
        sliders = [
            (pygame.Rect(px + 30, py + 14, track_w, 14), "R", self.pick_r),
            (pygame.Rect(px + 30, py + 42, track_w, 14), "G", self.pick_g),
            (pygame.Rect(px + 30, py + 70, track_w, 14), "B", self.pick_b),
        ]
        return sliders

    def _value_from_slider(self, track: pygame.Rect, mx: int) -> int:
        """Convert mouse x → 0-255 value within a slider track."""
        ratio = max(0.0, min(1.0, (mx - track.x) / track.width))
        return int(ratio * 255)

    # Events

    def handle_events(self, event: pygame.event.Event) -> None:
        mx, my = g.mouse_pos

        # Keyboard navigation
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                g.color_selected = min(g.color_selected + 1,
                                       g.MAX_COLORS_COUNT - 1)
            elif event.key == pygame.K_LEFT:
                g.color_selected = max(g.color_selected - 1, 0)

        # Hover detection
        if event.type == pygame.MOUSEMOTION:
            self.color_mouse_hover = -1
            for i, rect in enumerate(self.color_rects):
                if rect.collidepoint(mx, my):
                    self.color_mouse_hover = i
                    break

            # Handle slider dragging
            if self._dragging_slider >= 0:
                sliders = self._slider_rects()
                track = sliders[self._dragging_slider][0]
                val = self._value_from_slider(track, mx)
                if self._dragging_slider == 0:
                    self.pick_r = val
                elif self._dragging_slider == 1:
                    self.pick_g = val
                else:
                    self.pick_b = val

        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Save button
            if self.save_rect.collidepoint(mx, my):
                self.save_requested = True
                return

            # Clear button
            if self.clear_rect.collidepoint(mx, my):
                self.clear_requested = True
                return

            # Colour picker toggle button
            if self.pick_rect.collidepoint(mx, my):
                self.picker_open = not self.picker_open
                return

            # Colour picker panel interactions
            if self.picker_open and self.picker_rect.collidepoint(mx, my):
                # Check slider clicks
                sliders = self._slider_rects()
                for idx, (track, _, _) in enumerate(sliders):
                    if track.collidepoint(mx, my):
                        self._dragging_slider = idx
                        val = self._value_from_slider(track, mx)
                        if idx == 0:
                            self.pick_r = val
                        elif idx == 1:
                            self.pick_g = val
                        else:
                            self.pick_b = val
                        return

                # Check "Apply" button
                apply_rect = pygame.Rect(self.picker_rect.x + 250,
                                         self.picker_rect.y + 88,
                                         60, 24)
                if apply_rect.collidepoint(mx, my):
                    custom = (self.pick_r, self.pick_g, self.pick_b)
                    g.colors[g.color_selected] = custom
                    self.picker_open = False
                    return
                return

            # Click on a swatch
            for i, rect in enumerate(self.color_rects):
                if rect.collidepoint(mx, my):
                    g.color_selected = i
                    break

        # Mouse release → stop dragging slider
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._dragging_slider = -1

    # Rendering

    def draw(self, screen: pygame.Surface) -> None:
        """Render the colour bar, buttons, and (if open) the colour picker."""

        # 1. Top bar background
        pygame.draw.rect(screen, RETRO_BG,
                         (0, 0, g.SCREEN_WIDTH, g.TOP_BAR_HEIGHT))
        # Bottom border
        pygame.draw.line(screen, RETRO_BORDER,
                         (0, g.TOP_BAR_HEIGHT),
                         (g.SCREEN_WIDTH, g.TOP_BAR_HEIGHT), 2)

        # 2. Colour swatches
        for i, rect in enumerate(self.color_rects):
            if i < len(g.colors):
                pygame.draw.rect(screen, g.colors[i], rect)
                pygame.draw.rect(screen, RETRO_BORDER, rect, 1)

        # 3. Hover highlight
        if self.color_mouse_hover >= 0:
            hr = self.color_rects[self.color_mouse_hover]
            pygame.draw.rect(screen, (255, 255, 255), hr.inflate(4, 4), 2)

        # 4. Selected swatch highlight
        if 0 <= g.color_selected < len(self.color_rects):
            sr = self.color_rects[g.color_selected]
            pygame.draw.rect(screen, RETRO_HIGHLIGHT, sr.inflate(6, 6), 2)

        # 5. Current colour preview
        preview = pygame.Rect(g.SIDE_PANEL_WIDTH + 10, 8, 30, 34)
        pygame.draw.rect(screen, g.colors[g.color_selected], preview)
        pygame.draw.rect(screen, RETRO_TEXT, preview, 1)

        # 6. Action buttons
        self._draw_button(screen, self.pick_rect, self._pick_icon, "PICK")
        self._draw_button(screen, self.save_rect, self._save_icon, "SAVE")
        self._draw_button(screen, self.clear_rect, self._bin_icon, "CLR")

        # 7. Colour picker panel
        if self.picker_open:
            self._draw_picker(screen)

    def _draw_button(self, screen: pygame.Surface, rect: pygame.Rect,
                     icon: pygame.Surface | None, label: str) -> None:
        """Render an icon button with a small label."""
        pygame.draw.rect(screen, RETRO_BG_LIGHT, rect)
        pygame.draw.rect(screen, RETRO_BORDER, rect, 1)
        if icon:
            ix = rect.x + (rect.width - icon.get_width()) // 2
            iy = rect.y + 2
            screen.blit(icon, (ix, iy))
        font = pygame.font.SysFont("Courier", 9, bold=True)
        lbl = font.render(label, True, RETRO_TEXT)
        screen.blit(lbl, (rect.x + (rect.width - lbl.get_width()) // 2,
                          rect.bottom - 10))

    def _draw_picker(self, screen: pygame.Surface) -> None:
        """Render the inline RGB colour picker panel."""
        pr = self.picker_rect

        # Panel background
        pygame.draw.rect(screen, RETRO_BG, pr)
        pygame.draw.rect(screen, RETRO_HIGHLIGHT, pr, 2)

        font = pygame.font.SysFont("Courier", 13, bold=True)
        val_font = pygame.font.SysFont("Courier", 12)

        sliders = self._slider_rects()
        slider_colors = [(220, 60, 60), (60, 200, 60), (60, 100, 220)]

        for idx, (track, label, value) in enumerate(sliders):
            # Label
            lbl = font.render(label, True, slider_colors[idx])
            screen.blit(lbl, (track.x - 20, track.y))

            # Track background
            pygame.draw.rect(screen, (30, 30, 40), track)
            pygame.draw.rect(screen, RETRO_BORDER, track, 1)

            # Filled portion
            fill_w = int((value / 255) * track.width)
            fill_rect = pygame.Rect(track.x, track.y, fill_w, track.height)
            pygame.draw.rect(screen, slider_colors[idx], fill_rect)

            # Thumb
            thumb_x = track.x + fill_w - 3
            pygame.draw.rect(screen, (255, 255, 255),
                             (thumb_x, track.y - 2, 6, track.height + 4))

            # Value text
            val_surf = val_font.render(str(value), True, RETRO_TEXT)
            screen.blit(val_surf, (track.right + 8, track.y))

        # Preview swatch
        preview_color = (self.pick_r, self.pick_g, self.pick_b)
        prev_rect = pygame.Rect(pr.x + 250, pr.y + 14, 50, 60)
        pygame.draw.rect(screen, preview_color, prev_rect)
        pygame.draw.rect(screen, RETRO_TEXT, prev_rect, 1)

        # Hex label
        hex_str = f"#{self.pick_r:02X}{self.pick_g:02X}{self.pick_b:02X}"
        hex_surf = val_font.render(hex_str, True, RETRO_TEXT)
        screen.blit(hex_surf, (prev_rect.x, prev_rect.bottom + 4))

        # "Apply" button
        apply_rect = pygame.Rect(pr.x + 250, pr.y + 88, 60, 24)
        pygame.draw.rect(screen, RETRO_HIGHLIGHT, apply_rect)
        pygame.draw.rect(screen, (255, 255, 255), apply_rect, 1)
        apply_lbl = font.render("APPLY", True, (0, 0, 0))
        screen.blit(apply_lbl, (apply_rect.x + (apply_rect.width - apply_lbl.get_width()) // 2,
                                apply_rect.y + 5))
