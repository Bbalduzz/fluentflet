import flet as ft
from fluentflet.utils.fluent_design_system import FluentDesignSystem
from fluentflet.components.tooltip import ToolTip
from enum import Enum


class SliderOrientation(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class Slider(ft.Container):
    def __init__(
        self,
        value=0,
        min=0,
        max=100,
        on_change=None,
        size=200,
        disabled=False,
        orientation=SliderOrientation.HORIZONTAL,
        is_dark_mode: bool = True,
        **kwargs
    ):
        self.current_value = value
        self.min = min
        self.max = max
        self._on_change = on_change
        self.size = size
        self.orientation = orientation
        self.dragging = False
        self.thumb_size = 22
        self.is_hovered = False
        self.is_pressed = False
        self.drag_start = 0
        self.initial_thumb_pos = 0
        self._disabled = disabled
        self.design_system = FluentDesignSystem()
        self.theme = (
            self.design_system.dark_theme
            if is_dark_mode
            else self.design_system.light_theme
        )

        self.styles = {
            "thumb": {
                "outer": {
                    ft.ControlState.DEFAULT: (
                        "#454545"
                        if is_dark_mode
                        else self.theme.fills.get_fill("control_fill_tertiary", 1)
                    ),
                    ft.ControlState.DISABLED: self.theme.fills.get_fill(
                        "control_fill_disabled"
                    ),
                },
                "inner": {
                    ft.ControlState.DEFAULT: self.theme.colors.get_color(
                        "accent_default"
                    ),
                    ft.ControlState.DISABLED: self.theme.colors.get_color(
                        "accent_disabled"
                    ),
                },
            },
            "track": {
                "base": {
                    ft.ControlState.DEFAULT: self.theme.fills.get_fill(
                        "control_strong_fill_default"
                    ),
                    ft.ControlState.DISABLED: self.theme.fills.get_fill(
                        "control_fill_disabled"
                    ),
                },
                "active": {
                    ft.ControlState.DEFAULT: self.theme.colors.get_color(
                        "accent_default"
                    ),
                    ft.ControlState.DISABLED: self.theme.colors.get_color(
                        "accent_disabled"
                    ),
                },
            },
        }

        self._create_components()

        # Adjusted container size and padding
        super().__init__(
            content=self._create_slider(),
            width=(
                size + self.thumb_size
                if orientation == SliderOrientation.HORIZONTAL
                else 55
            ),
            height=(
                55
                if orientation == SliderOrientation.HORIZONTAL
                else size + self.thumb_size
            ),
            padding=ft.padding.only(
                left=0, right=0, top=self.thumb_size / 2, bottom=self.thumb_size / 2
            ),
            **kwargs
        )

    def _get_color(self, component_path, state=ft.ControlState.DEFAULT):
        state = ft.ControlState.DISABLED if self._disabled else state
        path_parts = component_path.split(".")
        current = self.styles
        for part in path_parts:
            current = current[part]
        return current[state]

    def _create_components(self):
        self._tooltip = ToolTip(
            message=str(round(self.current_value, 1)),
        )

        self.inner_thumb = ft.Container(
            width=18,
            height=18,
            border_radius=9,
            bgcolor=self._get_color("thumb.inner"),
            margin=ft.margin.all(5),
            animate=ft.animation.Animation(150, ft.AnimationCurve.EASE_OUT),
        )

        self.thumb_container = ft.Container(
            width=self.thumb_size,
            height=self.thumb_size,
            border_radius=self.thumb_size / 2,
            bgcolor=self._get_color("thumb.outer"),
            content=self.inner_thumb,
            animate=ft.animation.Animation(150, ft.AnimationCurve.EASE_OUT),
            tooltip=self._tooltip,
        )

        self.thumb_ring = ft.GestureDetector(
            content=self.thumb_container,
            on_pan_start=self.handle_pan_start,
            on_pan_update=self.handle_pan_update,
            on_pan_end=self.handle_pan_end,
            mouse_cursor=(
                ft.MouseCursor.FORBIDDEN if self._disabled else ft.MouseCursor.BASIC
            ),
        )

        self.thumb_container.on_hover = self.handle_hover

        # Track dimensions and margins
        if self.orientation == SliderOrientation.HORIZONTAL:
            track_width = self.size
            track_height = 4
            track_margin = ft.margin.only(top=10, left=self.thumb_size / 2)
        else:
            track_width = 4
            track_height = self.size
            track_margin = ft.margin.only(top=self.thumb_size / 2, left=10)

        self.base_track = ft.Container(
            bgcolor=self._get_color("track.base"),
            border_radius=2,
            width=track_width,
            height=track_height,
            margin=track_margin,
        )

        # Initialize active track with correct dimensions
        initial_percentage = (self.current_value - self.min) / (self.max - self.min)
        initial_active_width = (
            track_width * initial_percentage
            if self.orientation == SliderOrientation.HORIZONTAL
            else track_width
        )
        initial_active_height = (
            track_height
            if self.orientation == SliderOrientation.HORIZONTAL
            else track_height * initial_percentage
        )

        self.active_track = ft.Container(
            bgcolor=self._get_color("track.active"),
            border_radius=2,
            width=initial_active_width,
            height=initial_active_height,
            margin=track_margin,
        )

        self.update_thumb_position()

    def _create_slider(self):
        return ft.Stack(
            [
                self.base_track,
                self.active_track,
                self.thumb_ring,
            ]
        )

    def handle_pan_start(self, e: ft.DragStartEvent):
        if self._disabled:
            return
        self.dragging = True
        self.is_pressed = True
        self.drag_start = (
            e.local_x if self.orientation == SliderOrientation.HORIZONTAL else e.local_y
        )
        self.initial_thumb_pos = (
            self.thumb_ring.left
            if self.orientation == SliderOrientation.HORIZONTAL
            else self.thumb_ring.top or 0
        )
        self.inner_thumb.margin = ft.margin.all(7)
        self.update()

    def handle_pan_update(self, e: ft.DragUpdateEvent):
        if not self.dragging or self._disabled:
            return

        delta = (
            (e.local_x - self.drag_start)
            if self.orientation == SliderOrientation.HORIZONTAL
            else (e.local_y - self.drag_start)
        )
        new_position = self.initial_thumb_pos + delta

        # Adjust position calculation
        max_pos = self.size
        new_position = max(0, min(max_pos, new_position))

        percentage = new_position / max_pos
        new_value = self.min + percentage * (self.max - self.min)

        # For vertical slider, invert the value calculation
        if self.orientation == SliderOrientation.VERTICAL:
            new_value = self.max - percentage * (self.max - self.min)

        self.current_value = new_value
        self._tooltip.message = str(round(self.current_value, 1))

        if self.orientation == SliderOrientation.HORIZONTAL:
            self.thumb_ring.left = new_position
            self.active_track.width = new_position
        else:
            self.thumb_ring.top = new_position
            self.active_track.height = self.size * (
                1 - percentage
            )  # Inverted for vertical
            self.active_track.margin = ft.margin.only(
                top=self.thumb_size / 2 + new_position, left=self.thumb_size / 2
            )

        if self._on_change:
            self._on_change(self)
        self.update()

    def handle_pan_end(self, e):
        if self._disabled:
            return
        self.dragging = False
        self.is_pressed = False
        self.inner_thumb.margin = ft.margin.all(5)
        self.update()

    def handle_hover(self, e):
        if self._disabled:
            return
        self.is_hovered = e.data == "true"
        if not self.is_pressed:
            self.inner_thumb.margin = ft.margin.all(3 if self.is_hovered else 5)
        self.update()

    def update_thumb_position(self):
        percentage = (self.current_value - self.min) / (self.max - self.min)

        if self.orientation == SliderOrientation.HORIZONTAL:
            position = percentage * self.size
            self.thumb_ring.left = position
            self.active_track.width = position
        else:
            position = (1 - percentage) * self.size  # Inverted for vertical
            self.thumb_ring.top = position
            self.active_track.height = self.size * percentage
            self.active_track.margin = ft.margin.only(
                top=self.thumb_size / 2 + position, left=self.thumb_size / 2
            )

        self._tooltip.message = str(round(self.current_value, 1))

    @property
    def value(self):
        return self.current_value

    @value.setter
    def value(self, new_value):
        if self._disabled:
            return
        self.current_value = max(self.min, min(self.max, new_value))
        self.update_thumb_position()
        if hasattr(self, "_page"):
            self.update()

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, value: bool):
        if self._disabled == value:
            return

        self._disabled = value
        self.inner_thumb.bgcolor = self._get_color("thumb.inner")
        self.thumb_container.bgcolor = self._get_color("thumb.outer")
        self.base_track.bgcolor = self._get_color("track.base")
        self.active_track.bgcolor = self._get_color("track.active")
        self.thumb_ring.mouse_cursor = (
            ft.MouseCursor.FORBIDDEN if value else ft.MouseCursor.BASIC
        )

        if hasattr(self, "_page"):
            self.update()
