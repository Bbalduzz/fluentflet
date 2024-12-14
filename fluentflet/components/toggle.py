import flet as ft
from typing import Union
from fluentflet.utils.fluent_design_system import FluentDesignSystem


class Toggle(ft.Container):
    def __init__(
        self,
        value=False,
        label: Union[str, dict] = None,
        label_position=ft.LabelPosition.RIGHT,
        on_change=None,
        label_style=None,
        disabled=False,
        width=40,
        height=20,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._width = width
        self._height = height
        self.value = value
        self.on_content = label.get("on_content") if isinstance(label, dict) else label
        self.off_content = (
            label.get("off_content") if isinstance(label, dict) else label
        )
        self._label = self.on_content if value else self.off_content
        self.label_position = label_position
        self.on_change = on_change
        self.disabled = disabled
        self.label_style = label_style
        self.theme = FluentDesignSystem().dark_theme

        self._handle_size = height - 4
        self._handle_expanded_width = width - 20  # Width when stretched

        # Create track
        self._track = ft.Container(
            width=width,
            height=height,
            border_radius=height / 2,
            bgcolor=self.theme.fills.get_fill("control_fill_transparent"),
            border=ft.border.all(1, self.theme.colors.get_color("text_tertiary")),
            animate=ft.animation.Animation(300, "easeInOut"),
        )

        # Create handle
        handle_size = height - 6
        self._handle = ft.Container(
            width=handle_size,
            height=handle_size,
            left=3 if not value else width - handle_size - 2,
            top=3,
            bgcolor=self.theme.colors.get_color("text_primary"),
            border_radius=handle_size / 2,
            animate_position=ft.animation.Animation(
                300, ft.AnimationCurve.EASE_OUT_EXPO
            ),  # Animate position changes
        )

        # Create gesture detector
        self._gesture = ft.GestureDetector(
            content=ft.Container(
                width=width,
                height=height,
            ),
            on_tap=self._handle_click,
            on_tap_down=self._handle_tap_down,
            on_tap_up=self._handle_tap_up,
            mouse_cursor=ft.MouseCursor.BASIC if disabled else ft.MouseCursor.CLICK,
        )

        # Create the toggle stack
        toggle_stack = ft.Stack(
            controls=[self._track, self._handle, self._gesture],
            width=width,
            height=height,
        )

        # If there's a label, create a row with the label
        if label:
            self._label_text = ft.Text(
                self._label,
                style=label_style,
                color=(
                    self.theme.colors.get_color("text_disabled")
                    if disabled
                    else self.theme.colors.get_color("text_primary")
                ),
                size=15,
            )

            self.content = ft.Row(
                controls=(
                    [self._label_text, toggle_stack]
                    if label_position == ft.LabelPosition.LEFT
                    else [toggle_stack, self._label_text]
                ),
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        else:
            self.content = toggle_stack

        self._update_colors()

    def _handle_click(self, e):
        if not self.disabled:
            self.value = not self.value
            self._handle.left = (
                3 if not self.value else self._width - self._handle_size - 2
            )
            self._update_colors()
            # Update label text if using on/off content
            if hasattr(self, "_label_text"):
                self._label_text.value = (
                    self.on_content if self.value else self.off_content
                )
            if self.on_change:
                # Just pass the event through with our data
                e.data = self.value
                self.on_change(self.value)
            self.update()

    def _handle_tap_down(self, e):
        if not self.disabled:
            # Stretch handle width
            self._handle.width = self._handle_expanded_width
            self._handle.left = 3
            self._handle.update()

    def _handle_tap_up(self, e):
        if not self.disabled:
            self._handle.width = self._handle_size
            self._handle.left = (
                3 if not self.value else self._width - self._handle_size - 2
            )
            self._handle.update()

    def _update_colors(self):
        if self.disabled:
            self._track.border_color = self.theme.colors.get_color("text_disabled")
            self._track.bgcolor = self.theme.fills.get_fill("control_fill_transparent")
            self._handle.bgcolor = self.theme.colors.get_color("text_disabled")
            if hasattr(self, "_label_text"):
                self._label_text.color = self.theme.colors.get_color("text_disabled")
        else:
            if self.value:
                self._track.border_color = self.theme.colors.get_color("accent_default")
                self._track.bgcolor = self.theme.colors.get_color("accent_default")
                self._handle.bgcolor = self.theme.colors.get_color(
                    "text_on_accent_primary"
                )
            else:
                self._track.border_color = self.theme.colors.get_color("text_tertiary")
                self._track.bgcolor = self.theme.fills.get_fill(
                    "control_fill_transparent"
                )
                self._handle.bgcolor = self.theme.colors.get_color("text_primary")
            if hasattr(self, "_label_text"):
                self._label_text.color = self.theme.colors.get_color("text_primary")

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        if hasattr(self, "_label_text"):
            self._label_text.value = value
            self.update()
