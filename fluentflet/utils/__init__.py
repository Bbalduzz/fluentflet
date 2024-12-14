import flet as ft
import sys
from pathlib import Path
import os
from .runtime_icon_changer import change_app_icon
from .fluent_icons import FluentIcon, FluentIconStyle, FluentIcons

if sys.platform == "win32":
    from .apply_window_effects import _apply_blur
    from .enable_drag_and_drop import (
        _enable_drag_and_drop,
        _default_on_files_dropped,
        _default_on_drag_enter,
        _default_on_drag_over,
        _default_on_drag_leave,
    )

    def _set_blur(self, value: bool):
        if hasattr(self, "_mica") and self._mica:
            self._mica = False
        self._blur = value
        if value:
            self.apply_blur()

    # Set up accepts_drops property
    def _get_accepts_drops(self):
        if not hasattr(self, "_accepts_drops"):
            self._accepts_drops = False
        return self._accepts_drops

    def _set_accepts_drops(self, value):
        if not hasattr(self, "_accepts_drops"):
            self._accepts_drops = False
        if value != self._accepts_drops:
            self._accepts_drops = value
            if value:
                self.enable_drag_and_drop()

    # Initialize default properties
    ft.Page._blur = False
    ft.Page._accepts_drops = False

    # Set default methods
    # drag & drop
    ft.Page.on_files_dropped = _default_on_files_dropped
    ft.Page.on_drag_enter = _default_on_drag_enter
    ft.Page.on_drag_over = _default_on_drag_over
    ft.Page.on_drag_leave = _default_on_drag_leave
    ft.Page._default_on_files_dropped = _default_on_files_dropped
    ft.Page._default_on_drag_enter = _default_on_drag_enter
    ft.Page._default_on_drag_over = _default_on_drag_over
    ft.Page._default_on_drag_leave = _default_on_drag_leave

    # Set up properties
    ft.Page.blur_effect = property(lambda self: self._blur, _set_blur)
    ft.Page.accepts_drops = property(_get_accepts_drops, _set_accepts_drops)

    # Set up methods
    ft.Page.enable_drag_and_drop = _enable_drag_and_drop
    ft.Page.apply_blur = _apply_blur


def _set_icon(self, value: str):
    self._icon = value
    change_app_icon(value, self.title)


ft.Page._icon = None
ft.Page.icon = property(lambda self: self._icon, _set_icon)


def relative_to_assets(file):
    normalized_file_path = os.path.normpath(file)
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "fluentflet",
        "static",
        normalized_file_path,
    )
