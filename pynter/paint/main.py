"""
main.py — Entry point for the Pixel-Craft Python application.

Creates the main window, initialises it, starts the event loop,
and shuts down when the user closes the window.

HOW TO RUN:
    cd python-version
    pip install -r requirements.txt
    python main.py

CONTROLS:
    - Click a tool button on the left panel to select it.
    - Click a color swatch on the top bar to pick a color.
    - Left/Right arrow keys to cycle through colors.
    - Left mouse button to draw on the canvas.
    - Mouse scroll wheel to resize Brush / Eraser.
    - For Curve Tool: click to place control points, press Enter to commit.
    - Cmd+S (macOS) / Ctrl+S (Win/Linux) to save the canvas as a PNG.
    - ESC or close the window to exit.
"""

from main_window_gui import MainWindowGUI


def main():
    app = MainWindowGUI()
    app.init()
    app.start_loop()
    app.shut_down()


if __name__ == "__main__":
    main()
