import flet as ft
from typing import Union
from fluentflet.components.button import Button, ButtonVariant
from fluentflet.utils.fluent_design_system import FluentDesignSystem


class Expander(ft.Container):
    def __init__(
        self,
        header: Union[str, ft.Control],
        content: ft.Control,
        expand: bool = False,
        width: int = 600,
        is_dark_mode: bool = True,
        **kwargs,
    ):
        # Initialize design system
        self.design_system = FluentDesignSystem()
        self.theme = (
            self.design_system.dark_theme
            if is_dark_mode
            else self.design_system.light_theme
        )

        self._expanded = expand
        self._width = width
        self._header = (
            header
            if isinstance(header, ft.Control)
            else ft.Text(
                header,
                size=int(
                    self.design_system.font_sizes.body_font_size.replace("px", "")
                ),
                font_family=self.design_system.font_families.font_family_text,
                color=self.theme.colors.get_color("text_primary"),
            )
        )
        self._content = content

        # Use Button component with design system
        self._expand_icon = Button(
            content=ft.Icon(
                name=ft.icons.EXPAND_LESS if expand else ft.icons.EXPAND_MORE,
                size=14,
                color="#ffffff",
            ),
            variant=ButtonVariant.HYPERLINK,
            on_click=self._toggle,
            design_system=self.design_system,
            is_dark_mode=is_dark_mode,
        )

        # Calculate the content height
        self._content_height = content.height if hasattr(content, "height") else None

        self._content_container = ft.Container(
            content=self._content,
            bgcolor=self.theme.fills.get_fill("control_fill_tertiary"),
            border_radius=ft.border_radius.only(
                bottom_left=self.design_system.control_properties.control_corner_radius,
                bottom_right=self.design_system.control_properties.control_corner_radius,
            ),
            padding=15,
            width=self._width,
            height=None if self._expanded else 0,
            animate=ft.animation.Animation(
                duration=self.design_system.control_properties.control_normal_duration,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
        )

        header_row = ft.Container(
            content=ft.Row(
                controls=[
                    self._header,
                    self._expand_icon,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            on_click=self._toggle,
            border_radius=ft.border_radius.only(
                top_left=self.design_system.control_properties.control_corner_radius,
                top_right=self.design_system.control_properties.control_corner_radius,
                bottom_left=(
                    self.design_system.control_properties.control_corner_radius
                    if not self._expanded
                    else 0
                ),
                bottom_right=(
                    self.design_system.control_properties.control_corner_radius
                    if not self._expanded
                    else 0
                ),
            ),
            padding=10,
            bgcolor=self.theme.fills.get_fill("control_fill_default"),
            # border=ft.border.all(1, self.theme.fills.get_fill("control_fill_default", 0.0578)),
            width=self._width,
            animate=ft.animation.Animation(
                duration=self.design_system.control_properties.control_normal_duration,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
        )

        self._header_row = header_row

        super().__init__(
            content=ft.Column(
                controls=[
                    header_row,
                    self._content_container,
                ],
                spacing=0,
                expand=True,
            ),
            expand=True,
            **kwargs,
        )

    def update_theme(self, is_dark_mode: bool):
        """Update expander theme colors"""
        self.theme = (
            self.design_system.dark_theme
            if is_dark_mode
            else self.design_system.light_theme
        )

        # Update header colors
        if isinstance(self._header, ft.Text):
            self._header.color = self.theme.colors.get_color("text_primary")

        # Update expand icon theme
        self._expand_icon.update_theme(is_dark_mode)

        # Update container colors
        self._content_container.bgcolor = self.theme.fills.get_fill(
            "control_fill_tertiary"
        )
        self._header_row.bgcolor = self.theme.fills.get_fill("control_fill_default")
        self._header_row.border = ft.border.all(
            1, self.theme.fills.get_fill("control_fill_default", 0.0578)
        )

        self.update()

    def _toggle(self, *_):
        self._expanded = not self._expanded

        if self._expanded:
            # Make content visible to measure it
            self._content_container.height = None
            self._content_container.update()

            # Measure the content after rendering
            self._content.update()
            content_height = 0
            if isinstance(self._content, ft.Column):
                for control in self._content.controls:
                    content_height += control.height or 40  # Default height if None
            else:
                content_height = self._content.height or 40

            self._content_height = content_height
            self._content_container.height = self._content_height + 20
        else:
            self._content_container.height = 0

        self._expand_icon.content.name = (
            ft.icons.EXPAND_LESS if self._expanded else ft.icons.EXPAND_MORE
        )

        self._header_row.border_radius = ft.border_radius.only(
            top_left=self.design_system.control_properties.control_corner_radius,
            top_right=self.design_system.control_properties.control_corner_radius,
            bottom_left=(
                self.design_system.control_properties.control_corner_radius
                if not self._expanded
                else 0
            ),
            bottom_right=(
                self.design_system.control_properties.control_corner_radius
                if not self._expanded
                else 0
            ),
        )

        self.update()

    @property
    def expanded(self) -> bool:
        return self._expanded

    @expanded.setter
    def expanded(self, value: bool):
        if self._expanded != value:
            self._expanded = value

            # Update content container height
            self._content_container.height = self._content_height if value else 0

            # Update the expand icon
            self._expand_icon.content.name = (
                ft.icons.EXPAND_LESS if value else ft.icons.EXPAND_MORE
            )

            # Update header border radius
            self._header_row.border_radius = ft.border_radius.only(
                top_left=self.design_system.control_properties.control_corner_radius,
                top_right=self.design_system.control_properties.control_corner_radius,
                bottom_left=(
                    self.design_system.control_properties.control_corner_radius
                    if not value
                    else 0
                ),
                bottom_right=(
                    self.design_system.control_properties.control_corner_radius
                    if not value
                    else 0
                ),
            )

            self.update()
