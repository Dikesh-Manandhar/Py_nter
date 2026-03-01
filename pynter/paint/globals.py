"""
globals.py — Shared global state and utility functions for Pixel-Craft.

Stores variables accessed across multiple modules: mouse position,
color palette, selected color index. Also contains math helpers
used by the Bezier Curve Tool.
"""

import pygame
import math

# ===========================================================================
#  CONSTANTS
# ===========================================================================

# Number of colors in the palette (updated by ColorSelect.init())
MAX_COLORS_COUNT = 24

TOOL_BOX_ICONS_COUNT = 18

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
TOP_BAR_HEIGHT = 50
SIDE_PANEL_WIDTH = 140
FPS = 120

# ===========================================================================
#  GLOBAL STATE
# ===========================================================================

mouse_pos: tuple[int, int] = (0, 0)
colors: list[tuple[int, int, int]] = []
color_selected: int = 0

# ===========================================================================
#  UTILITY / MATH FUNCTIONS
# ===========================================================================


def factorial(n: int) -> int:
    """Compute n! iteratively. Used by nCr() for Bezier curves."""
    if n == 0:
        return 1
    product = 1
    for i in range(1, n + 1):
        product *= i
    return product


def nCr(n: int, r: int) -> int:
    """Binomial coefficient C(n, r) = n! / (r! * (n-r)!). Used in Bezier formula."""
    return factorial(n) // (factorial(r) * factorial(n - r))
