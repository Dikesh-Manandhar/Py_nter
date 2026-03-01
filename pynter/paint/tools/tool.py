"""
tool.py — Abstract base class for all drawing tools.

Every tool must inherit from this class and implement:
    draw(surface)        — Render permanent marks on the canvas surface.
    handle_events(event) — React to pygame events (mouse clicks, keys, etc.).
    preview(screen)      — Draw a temporary overlay on the main screen.

DESIGN PATTERN: Strategy Pattern
    The Canvas holds a reference to the current Tool object. When the user
    switches tools (via ToolSelect), the Canvas swaps the reference.
    Canvas.draw() just calls tool.draw() without knowing which tool is active.
"""

from abc import ABC, abstractmethod
import pygame


class Tool(ABC):
    """Abstract base class that all drawing tools must implement."""

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Draw permanent pixels/shapes onto the canvas surface."""
        pass

    @abstractmethod
    def handle_events(self, event: pygame.event.Event) -> None:
        """Handle mouse presses, releases, motion, key presses, etc."""
        pass

    @abstractmethod
    def preview(self, screen: pygame.Surface) -> None:
        """Draw temporary overlays (cursor indicators, drag previews) on the display."""
        pass
