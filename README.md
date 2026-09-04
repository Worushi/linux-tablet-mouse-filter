# Linux Tablet Mouse Filter (PenPriority)

*(Прокрутите вниз для русской версии / Scroll down for the Russian version)*

---

## 🇬🇧 English

### The Problem
When using a drawing tablet (like XP-Pen, Wacom, Huion) on Linux, the physical mouse often interferes with the drawing process. Accidental mouse clicks can ruin a stroke, and the mouse scroll wheel rarely works correctly for zooming in apps like Krita or Blender.

### The Solution
This Python script acts as a lightweight semi-driver/filter using `evdev` and `uinput`. It monitors the tablet pen's hover state and dynamically controls the physical mouse:
1. **Mouse Blocking:** Completely disables physical mouse movement and clicks when the pen is hovering over the tablet.
2. **Scroll-to-Zoom:** When the pen is active, the mouse scroll wheel is intercepted and translated into `+` / `-` key presses, providing smooth zoom in Krita and other apps.
3. **Seamless Passthrough:** When the pen is removed from the tablet area, the physical mouse works completely normally.

### ✨ Features
- Works on both **Wayland** and **X11** (tested on Fedora KDE).
- Prevents accidental mouse clicks while drawing.
- Fixes the broken scroll-wheel zoom in Krita/Linux.
- Supports High-Resolution scroll wheels (ignores Hi-Res events to prevent zoom spam).
- Zero latency, runs as a background daemon.

### 🛠️ Requirements
- Python 3.6+
- `evdev` library (`pip install evdev`)
- Read/Write permissions for `/dev/input/` (run with `sudo` or add your user to the `input` group).

### 🚀 Installation & Usage
1. Clone the repo:
