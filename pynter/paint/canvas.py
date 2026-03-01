"""
canvas.py — The main drawing canvas where all painting happens.

The Canvas uses an off-screen pygame.Surface (called `canvas_surface`) to
store all the drawn pixels.  Each frame, the active tool draws onto this
surface, and then the surface is blitted (copied) to the main display.
Tool previews (cursor indicators, drag guidelines) are drawn AFTER the
blit so they appear on-screen but are NOT saved to the canvas.

Includes an **Undo / Redo** stack that snapshots the canvas when the user
starts a new stroke.  Ctrl+Z undoes, Ctrl+Y / Ctrl+Shift+Z redoes.

Corresponds to: Canvas.h / Canvas.cpp in the C++ version.

=============================================================================
COMPUTER GRAPHICS CONCEPT — Undo / Redo with Snapshot Stack
=============================================================================
The simplest undo scheme records a complete copy of the canvas surface
before each editing operation.  Undo restores the previous copy; redo
re-applies the one that was undone.

    undo_stack:  [ snap_0, snap_1, snap_2 ]  ← most recent on top
    redo_stack:  [ snap_3 ]                  ← cleared on new stroke

Trade-off:
    + Very simple to implement (just surface.copy())
    + Works with any tool without special per-tool logic
    – Uses O(N × W × H) memory for N undo steps

For production apps, "command pattern" or delta-based undo is preferred,
but the snapshot approach is clear and correct for a course project.
=============================================================================
"""

import pygame
import globals as g
from tool_select import ToolSelect


# Maximum number of undo snapshots to keep in memory
MAX_UNDO_STEPS = 30


class Canvas:
    """
    Manages the off-screen drawing surface, undo/redo, and delegates to
    the active tool.
    """

    def __init__(self, tool_select: ToolSelect):
        self.tool_select = tool_select
        self.canvas_surface: pygame.Surface | None = None
        # Undo / redo snapshot stacks
        self._undo_stack: list[pygame.Surface] = []
        self._redo_stack: list[pygame.Surface] = []
        # Track whether the mouse was down last frame (to detect stroke start)
        self._was_drawing: bool = False

    def init(self) -> None:
        """Create the off-screen canvas surface, filled with white."""
        self.canvas_surface = pygame.Surface(
            (g.SCREEN_WIDTH, g.SCREEN_HEIGHT)
        )
        self.canvas_surface.fill((255, 255, 255))

    # ── Undo / Redo ──────────────────────────────────────────────────────

    def save_snapshot(self) -> None:
        """
        Push a copy of the current canvas onto the undo stack.
        Called automatically at the start of each new stroke.
        """
        if self.canvas_surface is None:
            return
        snapshot = self.canvas_surface.copy()
        self._undo_stack.append(snapshot)
        # Trim to maximum size
        if len(self._undo_stack) > MAX_UNDO_STEPS:
            self._undo_stack.pop(0)
        # Any new edit invalidates the redo history
        self._redo_stack.clear()

    def undo(self) -> None:
        """Restore the canvas to its state before the last stroke."""
        if not self._undo_stack or self.canvas_surface is None:
            return
        # Save current state to redo stack
        self._redo_stack.append(self.canvas_surface.copy())
        # Pop and restore the previous state
        self.canvas_surface = self._undo_stack.pop()

    def redo(self) -> None:
        """Re-apply the last undone edit."""
        if not self._redo_stack or self.canvas_surface is None:
            return
        # Save current state to undo stack
        self._undo_stack.append(self.canvas_surface.copy())
        # Pop and restore from redo stack
        self.canvas_surface = self._redo_stack.pop()

    # ── Event handling ───────────────────────────────────────────────────

    def handle_events(self, event: pygame.event.Event) -> None:
        """
        Forward events to the active tool.
        Auto-snapshot on stroke start (mouse down inside canvas).
        """
        tool = self.tool_select.get_selected_tool()
        if tool is not None:
            tool.handle_events(event)

        # Detect stroke start → save snapshot for undo
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if mx > g.SIDE_PANEL_WIDTH and my > g.TOP_BAR_HEIGHT:
                self.save_snapshot()

    # ── Drawing ──────────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface) -> None:
        """
        1. Let the active tool draw permanent pixels onto canvas_surface.
        2. Blit the canvas_surface onto the main display.
        3. Let the active tool draw temporary previews on the display.
        """
        tool = self.tool_select.get_selected_tool()

        if tool is not None:
            tool.draw(self.canvas_surface)

        screen.blit(self.canvas_surface, (0, 0))

        if tool is not None:
            mx, my = g.mouse_pos
            if my > g.TOP_BAR_HEIGHT and mx > g.SIDE_PANEL_WIDTH:
                tool.preview(screen)

    def save_image(self, filename: str = "my_painting.png") -> str | None:
        """Save the current canvas to a PNG file."""
        if self.canvas_surface is not None:
            pygame.image.save(self.canvas_surface, filename)
            print(f"Image saved as: {filename}")
            return filename
        return None
