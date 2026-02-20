# utils.py - Utility functions
import os
import ctypes


def setup_dpi_awareness():
    """Enable high-DPI awareness on Windows to fix blurry text"""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    except (AttributeError, OSError):
        try:
            ctypes.windll.user32.SetProcessDPIAware()  # Fallback for older Windows
        except (AttributeError, OSError):
            pass


def suppress_tk_warnings():
    """Suppress Tk deprecation warning on macOS"""
    os.environ['TK_SILENCE_DEPRECATION'] = '1'


def lighten_color(hex_color):
    """Lighten a hex color for hover effect"""
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    r = min(255, int(r * 1.15))
    g = min(255, int(g * 1.15))
    b = min(255, int(b * 1.15))
    return f'#{r:02x}{g:02x}{b:02x}'
