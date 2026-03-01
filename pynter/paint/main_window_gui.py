"""
main_window_gui.py — Main application window and event loop.

This class ties everything together:
    - Creates the pygame window
    - Initialises the three main UI components (Canvas, ColorSelect, ToolSelect)
    - Runs the main game loop:  handle events → draw → repeat

Corresponds to: MainWindowGUI.h / MainWindowGUI.cpp in the C++ version.

=============================================================================
APPLICATION ARCHITECTURE OVERVIEW
=============================================================================

    ┌─────────────────────────────────────────────────────────────────────┐
    │                         MainWindowGUI                              │
    │                                                                     │
    │   ┌─────────────┐  ┌─────────────────────────────────────────────┐ │
    │   │  ToolSelect │  │                Canvas                       │ │
    │   │  (left bar) │  │  (off-screen surface + active tool)         │ │
    │   │             │  │                                             │ │
    │   │  [PEN]      │  │    The user draws here using the            │ │
    │   │  [BRU]      │  │    currently selected tool and color.       │ │
    │   │  [ERS]      │  │                                             │ │
    │   │  [LIN]      │  │                                             │ │
    │   │  [CIR]      │  │                                             │ │
    │   │  ...        │  │                                             │ │
    │   └─────────────┘  └─────────────────────────────────────────────┘ │
    │   ┌──────────────────── ColorSelect (top bar) ──────────────────┐ │
    │   │  [SAVE]  [■][■][■][■][■][■][■] ...                          │ │
    │   └─────────────────────────────────────────────────────────────┘ │
    └─────────────────────────────────────────────────────────────────────┘

    The MAIN LOOP runs at the target FPS and repeats:
        1. Poll events  → forward to ToolSelect, ColorSelect, Canvas
        2. Draw          → Canvas first, then ToolSelect & ColorSelect on top
        3. Flip display  → show the frame

=============================================================================
"""

import pygame
import sys
import globals as g
from canvas import Canvas
from color_select import ColorSelect
from tool_select import ToolSelect


class MainWindowGUI:
    """Top-level application class. Call init() → start_loop() → shut_down()."""

    def __init__(self):
        self.screen: pygame.Surface | None = None
        self.clock: pygame.time.Clock | None = None
        self._toast_text: str = ""
        self._toast_timer: float = 0.0
        self.colors_panel: ColorSelect | None = None
        self.tool_select: ToolSelect | None = None
        self.canvas: Canvas | None = None

    def init(self) -> None:
        """Initialise pygame, create the window, and set up UI components."""
        # Initialise pygame
        pygame.init()
        pygame.font.init()

        # Create window
        self.screen = pygame.display.set_mode(
            (g.SCREEN_WIDTH, g.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Pixel-Craft  ✦  Retro Edition")

        # Clock for frame rate
        self.clock = pygame.time.Clock()

        # Create UI components
        self.colors_panel = ColorSelect()
        self.tool_select = ToolSelect()
        self.canvas = Canvas(self.tool_select)

        # Initialise components
        self.colors_panel.init()
        self.tool_select.init()
        self.canvas.init()

    def start_loop(self) -> None:
        """Run the main event loop until the user exits."""
        running = True
        while running:
            # Update mouse position
            g.mouse_pos = pygame.mouse.get_pos()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

                # ESC to exit
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    break

                # Ctrl+S / Cmd+S to save
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_s
                        and (pygame.key.get_mods() & (pygame.KMOD_META | pygame.KMOD_CTRL))):
                    saved = self.canvas.save_image()
                    if saved:
                        self._show_toast(f"Image saved as: {saved}")

                # Ctrl+Z / Cmd+Z to undo
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_z
                        and (pygame.key.get_mods() & (pygame.KMOD_META | pygame.KMOD_CTRL))
                        and not (pygame.key.get_mods() & pygame.KMOD_SHIFT)):
                    self.canvas.undo()

                # Ctrl+Y or Ctrl+Shift+Z to redo
                if event.type == pygame.KEYDOWN:
                    mods = pygame.key.get_mods()
                    if ((event.key == pygame.K_y and (mods & (pygame.KMOD_META | pygame.KMOD_CTRL)))
                            or (event.key == pygame.K_z and (mods & (pygame.KMOD_META | pygame.KMOD_CTRL))
                                and (mods & pygame.KMOD_SHIFT))):
                        self.canvas.redo()

                # Forward to UI components
                self.handle_events(event)

            # Handle save/clear button clicks
            if self.colors_panel.save_requested:
                saved = self.canvas.save_image()
                if saved:
                    self._show_toast(f"Image saved as: {saved}")
                self.colors_panel.save_requested = False

            # Handle clear button
            if self.colors_panel.clear_requested:
                self.canvas.save_snapshot()
                self.canvas.canvas_surface.fill((255, 255, 255))
                self.colors_panel.clear_requested = False

            # Drawing
            self.draw()

            # Update display
            pygame.display.flip()

            # Cap frame rate
            self.clock.tick(g.FPS)

    def handle_events(self, event: pygame.event.Event) -> None:
        """Forward an event to Canvas, ColorSelect, and ToolSelect."""
        self.canvas.handle_events(event)
        self.colors_panel.handle_events(event)
        self.tool_select.handle_events(event)

    def draw(self) -> None:
        """Render all UI components (canvas first, then panels on top)."""
        self.screen.fill((255, 255, 255))
        self.canvas.draw(self.screen)
        self.colors_panel.draw(self.screen)
        self.tool_select.draw(self.screen)

        # Draw toast notification (if active)
        if self._toast_timer > 0:
            self._toast_timer -= 1.0 / g.FPS
            alpha = min(255, int(255 * min(self._toast_timer, 1.0)))
            font = pygame.font.SysFont("monospace", 18, bold=True)
            text_surf = font.render(self._toast_text, True, (255, 255, 255))
            pad_x, pad_y = 16, 10
            box_w = text_surf.get_width() + pad_x * 2
            box_h = text_surf.get_height() + pad_y * 2
            box_x = (g.SCREEN_WIDTH - box_w) // 2
            box_y = g.SCREEN_HEIGHT - 70
            toast_bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            toast_bg.fill((30, 30, 30, alpha))
            self.screen.blit(toast_bg, (box_x, box_y))
            text_surf.set_alpha(alpha)
            self.screen.blit(text_surf, (box_x + pad_x, box_y + pad_y))

    def _show_toast(self, message: str, duration: float = 3.0) -> None:
        """Display a toast notification for the given duration (seconds)."""
        self._toast_text = message
        self._toast_timer = duration

    def shut_down(self) -> None:
        """Clean up pygame resources."""
        pygame.quit()
        sys.exit()
