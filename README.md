# MCam

A minimal, borderless webcam displayer written in Python. It stays on top of other windows, making it perfect for presentations, screen sharing, or recording tutorials.

## Features
*   **Always on Top**: Floats over PowerPoint, Keynote, or Browser.
*   **Frameless**: No ugly window title bars.
*   **Smart Resize**: Drag the corner to resize without distorting your face (Aspect Fill).
*   **Draggable**: Click and drag anywhere to move it.

## Installation

1.  Ensure you have **Python** installed.
2.  Install the required dependencies:

```bash
pip install opencv-python pillow
```
*(Note: Tkinter is included with standard Python installations)*

## Usage

1.  Save the script as `mcam.py`.
2.  Run the script:

```bash
python mcam.py
```

### Controls
*   **Move**: Click and drag anywhere on the video.
*   **Resize**: Hover over the **bottom-right corner** (cursor will change) and drag to resize.
*   **Quit**: Right-click anywhere on the video or press `Esc`.

## Troubleshooting (macOS)
If the video does not appear, ensure your terminal (or IDE) has **Camera permissions** in `System Settings > Privacy & Security > Camera`.
