"""
tool_select.py — Retro-styled tool selection panel (left side).

Displays a vertical grid of 16×16 bitmap icons rendered in a retro,
pixel-art style. Uses the Strategy Pattern — clicking a tool button
instantiates the matching Tool subclass.
"""

import pygame
from enum import IntEnum
import globals as g
from bitmap_utils import bitmap_to_surface, TOOL_ICON_BITMAPS

# Import all tool classes
from tools.pencil_tool import PencilTool
from tools.brush_tool import BrushTool
from tools.eraser_tool import EraserTool
from tools.line_tool import LineTool
from tools.circle_tool import CircleTool
from tools.rectangle_tool import RectangleTool
from tools.ellipse_tool import EllipseTool
from tools.curve_tool import CurveTool
from tools.hypnotiser_tool import HypnotiserTool
from tools.select_box_tool import SelectBoxTool
from tools.text_tool import TextTool
from tools.fill_tool import FillTool
from tools.eyedropper_tool import EyeDropperTool
from tools.magnifier_tool import MagnifierTool
from tools.square_tool import SquareTool
from tools.triangle_tool import TriangleTool
from tools.spray_tool import SprayTool
from tools.symmetry_tool import SymmetryTool
from tools.tool import Tool


# ── Retro colour palette ────────────────────────────────────────────────────
# These colours give the UI a classic 90s-era paint program look.
RETRO_BG        = (42, 42, 54)      # Dark panel background
RETRO_BG_LIGHT  = (58, 58, 72)      # Slightly lighter for button bg
RETRO_BORDER    = (80, 80, 100)     # Panel / button borders
RETRO_TEXT      = (200, 200, 210)   # Light text on dark background
RETRO_HIGHLIGHT = (0, 180, 220)     # Cyan highlight for selected tool
RETRO_ICON_FG   = (210, 210, 220)   # Icon foreground colour (light)
RETRO_HOVER     = (72, 72, 90)      # Button hover colour


class Tools(IntEnum):
    """Enum listing all available tools (index = button position)."""
    SELECT_BOX  = 0
    TEXT_INPUT   = 1
    ERASER      = 2
    FILL        = 3
    EYE_DROPPER = 4
    MAGNIFIER   = 5
    PENCIL      = 6
    BRUSH       = 7
    LINE        = 8
    CURVE       = 9
    SQUARE      = 10
    RECTANGLE   = 11
    CIRCLE      = 12
    ELLIPSE     = 13
    TRIANGLE    = 14
    HYPNOTISER  = 15
    SPRAY       = 16
    MANDALA     = 17


# Short 3-char labels shown beneath each icon
TOOL_LABELS = [
    "SEL", "TXT", "ERS", "FIL",
    "EYE", "MAG", "PEN", "BRU",
    "LIN", "CRV", "SQR", "REC",
    "CIR", "ELL", "TRI", "HYP",
    "SPR", "SYM",
]


class ToolSelect:
    """Manages the left-side tool panel with retro bitmap icons."""

    def __init__(self):
        self.tool_boxes: list[pygame.Rect] = []
        self.current_tool: Tool | None = None
        self.selected: Tools | None = None
        self.font: pygame.font.Font | None = None
        self.icon_cache: list[pygame.Surface] = []
        self.hover_index: int = -1

    def init(self) -> None:
        """Compute button positions, build icon cache, and init font."""
        self.font = pygame.font.SysFont("Courier", 11, bold=True)

        btn_w, btn_h = 50, 44
        gap_x, gap_y = 12, 52
        start_y = 70

        for i in range(g.TOOL_BOX_ICONS_COUNT):
            col = i % 2
            row = i // 2
            rect = pygame.Rect(
                12 + (btn_w + gap_x) * col,
                start_y + gap_y * row,
                btn_w,
                btn_h,
            )
            self.tool_boxes.append(rect)

        # Pre-render all bitmap icons at 2× scale
        for bmp in TOOL_ICON_BITMAPS:
            surf = bitmap_to_surface(bmp, RETRO_ICON_FG, scale=2)
            self.icon_cache.append(surf)

    # Tool factory (Strategy Pattern)

    def select_tool(self, tool: Tools) -> None:
        """Instantiate the appropriate Tool subclass."""
        self.selected = tool

        tool_map = {
            Tools.SELECT_BOX:  SelectBoxTool,
            Tools.TEXT_INPUT:   TextTool,
            Tools.PENCIL:      PencilTool,
            Tools.BRUSH:       BrushTool,
            Tools.ERASER:      EraserTool,
            Tools.FILL:        FillTool,
            Tools.EYE_DROPPER: EyeDropperTool,
            Tools.MAGNIFIER:   MagnifierTool,
            Tools.LINE:        LineTool,
            Tools.CIRCLE:      CircleTool,
            Tools.RECTANGLE:   RectangleTool,
            Tools.SQUARE:      SquareTool,
            Tools.ELLIPSE:     EllipseTool,
            Tools.CURVE:       CurveTool,
            Tools.TRIANGLE:    TriangleTool,
            Tools.HYPNOTISER:  HypnotiserTool,
            Tools.SPRAY:       SprayTool,
            Tools.MANDALA:     SymmetryTool,
        }

        tool_class = tool_map.get(tool)
        if tool_class is not None:
            self.current_tool = tool_class()
        else:
            self.current_tool = None
            print(f"Tool {tool.name} is not implemented yet.")

    def get_selected_tool(self) -> Tool | None:
        """Return the currently active Tool instance, or None."""
        return self.current_tool

    # Events

    def handle_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            for i, rect in enumerate(self.tool_boxes):
                if rect.collidepoint(mx, my):
                    self.select_tool(Tools(i))
                    break

        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            self.hover_index = -1
            for i, rect in enumerate(self.tool_boxes):
                if rect.collidepoint(mx, my):
                    self.hover_index = i
                    break

    # Rendering

    def draw(self, screen: pygame.Surface) -> None:
        # 1. Background
        pygame.draw.rect(screen, RETRO_BG,
                         (0, 0, g.SIDE_PANEL_WIDTH, g.SCREEN_HEIGHT))

        # 2. Right-edge border
        pygame.draw.line(screen, RETRO_BORDER,
                         (g.SIDE_PANEL_WIDTH, 0),
                         (g.SIDE_PANEL_WIDTH, g.SCREEN_HEIGHT), 2)

        # 3. Title
        title_font = pygame.font.SysFont("Courier", 18, bold=True)
        title_surf = title_font.render("TOOLS", True, RETRO_TEXT)
        title_x = (g.SIDE_PANEL_WIDTH - title_surf.get_width()) // 2
        screen.blit(title_surf, (title_x, 42))
        # Underline
        pygame.draw.line(screen, RETRO_BORDER,
                         (10, 60), (g.SIDE_PANEL_WIDTH - 10, 60), 1)

        # 4. Tool buttons
        for i, rect in enumerate(self.tool_boxes):
            # Determine button colour
            is_selected = self.selected is not None and i == self.selected.value
            if is_selected:
                bg = RETRO_HIGHLIGHT
            elif i == self.hover_index:
                bg = RETRO_HOVER
            else:
                bg = RETRO_BG_LIGHT

            # Button bg + border
            pygame.draw.rect(screen, bg, rect)
            border_col = RETRO_HIGHLIGHT if is_selected else RETRO_BORDER
            pygame.draw.rect(screen, border_col, rect, 1)

            # Icon (centred in upper portion)
            if i < len(self.icon_cache):
                icon = self.icon_cache[i]
                icon_x = rect.x + (rect.width - icon.get_width()) // 2
                icon_y = rect.y + 2
                screen.blit(icon, (icon_x, icon_y))

            # Label below icon
            if i < len(TOOL_LABELS) and self.font:
                lbl_color = (255, 255, 255) if is_selected else RETRO_TEXT
                lbl = self.font.render(TOOL_LABELS[i], True, lbl_color)
                lbl_x = rect.x + (rect.width - lbl.get_width()) // 2
                lbl_y = rect.y + rect.height - 12
                screen.blit(lbl, (lbl_x, lbl_y))
