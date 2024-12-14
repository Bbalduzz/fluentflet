import ctypes
import threading
import time
import sys
from enum import Enum, auto


class BlurMode(Enum):
    ACRYLIC = auto()


def _find_flet_window(title):
    windows = []

    def enum_windows_callback(hwnd, _):
        if ctypes.windll.user32.IsWindowVisible(hwnd):
            length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
            if title in buff.value:
                windows.append(hwnd)
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    ctypes.windll.user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)

    return windows[0] if windows else None


def _hex_to_rgba_int(hex_color: str) -> int:
    """Convert hex color string to RGBA integer value."""
    alpha = hex_color[7:]
    blue = hex_color[5:7]
    green = hex_color[3:5]
    red = hex_color[1:3]
    return int(alpha + blue + green + red, 16)


def _apply_blur(self):
    if sys.platform != "win32":
        return

    self.bgcolor = "transparent"
    self.window.bgcolor = "transparent"

    def wait_and_apply():
        while True:
            hwnd = _find_flet_window(self.title)
            if not hwnd:
                time.sleep(0.1)
                continue

            class ACCENTPOLICY(ctypes.Structure):
                _fields_ = [
                    ("AccentState", ctypes.c_uint),
                    ("AccentFlags", ctypes.c_uint),
                    ("GradientColor", ctypes.c_uint),
                    ("AnimationId", ctypes.c_uint),
                ]

            class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
                _fields_ = [
                    ("Attribute", ctypes.c_int),
                    ("Data", ctypes.POINTER(ctypes.c_int)),
                    ("SizeOfData", ctypes.c_size_t),
                ]

            # Create and configure accent policy
            accent = ACCENTPOLICY()
            accent.AccentState = 4  # ACCENT_ENABLE_ACRYLICBLURBEHIND
            accent.AccentFlags = 2  # ACCENT_ENABLE_TRANSPARENTGRADIENT
            # Convert hex color to RGBA integer
            hex_color = "#12121240"  # Default translucent dark color
            accent.GradientColor = _hex_to_rgba_int(hex_color)

            # Create and configure composition attribute data
            data = WINDOWCOMPOSITIONATTRIBDATA()
            data.Attribute = 19  # WCA_ACCENT_POLICY
            data.SizeOfData = ctypes.sizeof(accent)
            data.Data = ctypes.cast(
                ctypes.pointer(accent), ctypes.POINTER(ctypes.c_int)
            )

            # Apply the acrylic blur effect
            ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.byref(data))

            # Apply dark mode
            data.Attribute = 26  # WCA_USEDARKMODECOLORS
            ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.byref(data))

            # Add rounded corners
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd,
                33,  # DWMWA_WINDOW_CORNER_PREFERENCE
                ctypes.byref(ctypes.c_int(2)),  # DWMWCP_SMALL
                ctypes.sizeof(ctypes.c_int),
            )
            break

        print("[DEBUG] enabled blur effect")

    threading.Thread(target=wait_and_apply, daemon=True).start()
