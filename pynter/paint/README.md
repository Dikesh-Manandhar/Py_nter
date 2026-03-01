# Pixel-Craft — Python Version

A pixel-art drawing application built with **Python** and **pygame**.

This is a group project for our **Computer Graphics and Visualization (ENCT 201)** course at Thapathali Campus, IOE.

---

## Features

| Tool | Description | Algorithm / Concept |
|------|-------------|---------------------|
| **Pencil** | Freehand drawing with fixed-size brush | Circle stamping |
| **Brush** | Freehand drawing with adjustable size (scroll wheel) | Circle stamping |
| **Eraser** | Removes drawings by painting white (scroll to resize) | Rectangle fill |
| **Line** | Click-drag to draw straight lines | **Bresenham's Line Algorithm** |
| **Circle** | Click to set centre, drag for radius | **Midpoint Circle Algorithm** |
| **Rectangle** | Click-drag to draw rectangles | Min/max bounding box |
| **Square** | Click-drag to draw perfect squares | Constrained rectangle |
| **Triangle** | Click-drag to draw isosceles triangles | Polygon with 3 vertices |
| **Ellipse** | Click-drag to draw ellipses | **Midpoint Ellipse Algorithm** |
| **Bezier Curve** | Click to place control points, Enter to commit | **Bernstein Polynomial / Bezier formula** |
| **Fill** | Click to flood-fill a contiguous region | **BFS Flood Fill** |
| **Hypnotiser** | Hold-drag to draw concentric circles continuously | Midpoint Circle (repeated) |
| **Select Box** | Click-drag to select/move rectangular regions | Pixel buffer copy |
| **Text** | Click to place text, type, Enter to commit | Font rasterisation |
| **Eye Dropper** | Click to sample a pixel's color | Framebuffer read-back |
| **Magnifier** | Hover to see a magnified loupe | Surface scaling |
| **Spray** | Hold to spray random dots in a circle | **Monte Carlo / rejection sampling** |
| **Symmetry** | Draw with N-fold rotational symmetry | **2D Rotation Transform** |
| **Save** | Cmd+S / Ctrl+S to save canvas as PNG | `pygame.image.save()` |
| **Undo/Redo** | Ctrl+Z / Ctrl+Y | Snapshot stack |
| **Image Filters** | Blur, Sharpen, Edge Detect, Emboss | **Image Convolution** |

---

## How to Run

### Prerequisites
- **Python 3.10+** (for `X | None` type hints)
- **pip** (Python package manager)

### Steps

```bash
# 1. Navigate to the python-version folder
cd python-version

# 2. (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate    # macOS/Linux
# venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python main.py
```

---

## Controls

| Input | Action |
|-------|--------|
| **Left click** | Draw with the selected tool |
| **Right click** | Show brush outline (Brush/Pencil) |
| **Scroll wheel** | Resize Brush / Eraser |
| **Left/Right arrows** | Cycle through colors |
| **Click color swatch** | Select a color |
| **Click tool button** | Select a tool |
| **Enter** | Commit Bezier curve to canvas |
| **Cmd+S / Ctrl+S** | Save canvas as `my_painting.png` |
| **ESC** | Exit the application |

---

## Project Structure

```
python-version/
├── main.py               # Entry point
├── main_window_gui.py    # Main window and event loop
├── canvas.py             # Drawing canvas surface with undo/redo
├── color_select.py       # Color palette toolbar + RGB picker
├── tool_select.py        # Tool selection panel (Strategy Pattern)
├── globals.py            # Shared state & math utils
├── bitmap_utils.py       # 1-bit bitmap icon rendering
├── image_filters.py      # Convolution-based image filters
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── tools/
    ├── __init__.py       # Package init — exports all 18 tools
    ├── tool.py           # Abstract base class
    ├── pencil_tool.py    # Freehand pencil
    ├── brush_tool.py     # Adjustable brush
    ├── eraser_tool.py    # Eraser
    ├── line_tool.py      # Bresenham's Line Algorithm
    ├── circle_tool.py    # Midpoint Circle Algorithm
    ├── rectangle_tool.py # Rectangle drawing
    ├── square_tool.py    # Constrained square
    ├── triangle_tool.py  # Isosceles triangle
    ├── ellipse_tool.py   # Midpoint Ellipse Algorithm
    ├── curve_tool.py     # Bezier curves (Bernstein polynomial)
    ├── fill_tool.py      # BFS flood fill
    ├── hypnotiser_tool.py# Concentric circle effect
    ├── select_box_tool.py# Rectangular selection & move
    ├── text_tool.py      # Text placement
    ├── eyedropper_tool.py# Color sampling
    ├── magnifier_tool.py # Zoom loupe
    ├── spray_tool.py     # Spray can (Monte Carlo sampling)
    └── symmetry_tool.py  # N-fold rotational symmetry (2D rotation)
```

---

## Computer Graphics Algorithms Used

### 1. Bresenham's Line Algorithm (`line_tool.py`)
Draws straight lines using only integer arithmetic. Handles all octants by splitting into |slope| ≤ 1 and |slope| > 1 cases.

### 2. Midpoint Circle Algorithm (`circle_tool.py`)
Rasterises circles using 8-fold symmetry and a decision parameter. Only computes one octant; mirrors the rest.

### 3. Midpoint Ellipse Algorithm (`ellipse_tool.py`)
Extends the midpoint concept to ellipses. Splits the quadrant into two regions based on the slope of the curve.

### 4. Bezier Curves (`curve_tool.py`)
Uses the Bernstein polynomial form to evaluate curves defined by any number of control points. The nCr (binomial coefficient) function is used to weight each control point.

### 5. BFS Flood Fill (`fill_tool.py`)
Replaces all connected pixels of the same color starting from a seed point using breadth-first search.

### 6. Monte Carlo Sampling (`spray_tool.py`)
Uses rejection sampling inside a circle to spray random dots, producing a stippled airbrush effect.

### 7. 2D Rotation Transform (`symmetry_tool.py`)
Replicates each stroke N times using the standard 2D rotation matrix, creating kaleidoscope / mandala patterns.

### 8. Image Convolution (`image_filters.py`)
Applies 3×3 kernels (Blur, Sharpen, Edge Detect, Emboss) to the canvas using the convolution formula.

---

## Licence

This project is licensed under an unmodified zlib/libpng licence.
