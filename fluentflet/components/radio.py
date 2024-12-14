import flet as ft
from fluentflet.utils.fluent_design_system import FluentDesignSystem


class Radio(ft.Container):
    def __init__(
        self,
        value=None,
        label="",
        selected=False,
        disabled=False,
        design_system: FluentDesignSystem = None,
        is_dark_mode: bool = True,
        **kwargs,
    ):
        self.design_system = design_system or FluentDesignSystem()
        self.theme = (
            self.design_system.dark_theme
            if is_dark_mode
            else self.design_system.light_theme
        )

        self.value = value
        self._selected = selected
        self._disabled = disabled
        self.is_hovered = False
        self.is_pressed = False
        self._radio_group = None

        self.styles = {
            "selected": {
                "inner": self.theme.colors.get_color("text_on_accent_primary"),
                "outer": self.theme.colors.get_color("accent_default"),
                "border_width": 2,
                "border_color": self.theme.colors.get_color("accent_default"),
            },
            "hovered": {
                "inner": "transparent",
                "outer": self.theme.fills.get_fill("control_fill_secondary"),
                "border_width": 1,
                "border_color": self.theme.fills.get_fill(
                    "control_fill_default", 0.078
                ),
            },
            "pressed": {
                "inner": self.theme.colors.get_color("text_on_accent_primary"),
                "outer": self.theme.fills.get_fill("control_fill_tertiary"),
                "border_width": 1,
                "border_color": self.theme.fills.get_fill(
                    "control_fill_default", 0.0578
                ),
            },
            "default": {
                "inner": ft.colors.with_opacity(0.1, "#000000"),
                "outer": ft.colors.with_opacity(0.1, "#000000"),
                "border_width": 1,
                "border_color": self.theme.fills.get_fill(
                    "control_fill_default", 0.0578
                ),
            },
            "disabled": {
                "inner": "transparent",
                "outer": self.theme.fills.get_fill("control_fill_disabled"),
                "border_width": 1,
                "border_color": self.theme.fills.get_fill("control_fill_disabled"),
            },
        }

        self.radio_label = ft.Text(
            label,
            size=int(self.design_system.font_sizes.body_font_size.replace("px", "")),
            font_family=self.design_system.font_families.font_family_text,
            color=self.theme.colors.get_color(
                "text_disabled" if disabled else "text_primary"
            ),
        )
        self._create_components()

        self.content_row = ft.Row(
            [self.radio_circle, self.radio_label],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.container_gesture = ft.GestureDetector(
            content=self.content_row,
            on_tap=self._handle_tap,
            on_tap_down=self._handle_tap_down,
            on_tap_up=self._handle_tap_up,
            mouse_cursor=ft.MouseCursor.CLICK,
        )

        super().__init__(
            content=self.container_gesture,
            animate=ft.animation.Animation(
                duration=self.design_system.control_properties.control_fast_duration,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
            **kwargs,
        )

    def update_theme(self, is_dark_mode: bool):
        """Update radio theme colors"""
        self.theme = (
            self.design_system.dark_theme
            if is_dark_mode
            else self.design_system.light_theme
        )

        # Update styles with new theme colors
        self.styles = {
            "selected": {
                "inner": self.theme.colors.get_color("text_on_accent_primary"),
                "outer": self.theme.colors.get_color("accent_default"),
                "border_width": 2,
                "border_color": self.theme.colors.get_color("accent_default"),
            },
            "hovered": {
                "inner": "transparent",
                "outer": self.theme.fills.get_fill("control_fill_secondary"),
                "border_width": 1,
                "border_color": self.theme.fills.get_fill(
                    "control_fill_default", 0.078
                ),
            },
            "pressed": {
                "inner": self.theme.colors.get_color("text_on_accent_primary"),
                "outer": self.theme.fills.get_fill("control_fill_tertiary"),
                "border_width": 1,
                "border_color": self.theme.fills.get_fill(
                    "control_fill_default", 0.0578
                ),
            },
            "default": {
                "inner": ft.colors.with_opacity(0.1, "#000000"),
                "outer": ft.colors.with_opacity(0.1, "#000000"),
                "border_width": 1,
                "border_color": self.theme.fills.get_fill(
                    "control_fill_default", 0.0578
                ),
            },
            "disabled": {
                "inner": "transparent",
                "outer": self.theme.fills.get_fill("control_fill_disabled"),
                "border_width": 1,
                "border_color": self.theme.fills.get_fill("control_fill_disabled"),
            },
        }

        # Update label color
        self.radio_label.color = self.theme.colors.get_color(
            "text_disabled" if self._disabled else "text_primary"
        )

        # Update styles
        self._update_styles()
        self.update()

    def _create_components(self):
        self.inner_circle = ft.Container(
            width=16,
            height=16,
            border_radius=8,
            margin=ft.margin.all(2),
            animate=ft.animation.Animation(
                duration=self.design_system.control_properties.control_fast_duration,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
        )

        self.outer_circle = ft.Container(
            width=20,
            height=20,
            border_radius=10,
            content=self.inner_circle,
            animate=ft.animation.Animation(
                duration=self.design_system.control_properties.control_fast_duration,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
        )

        self.radio_circle = self.outer_circle
        self.radio_circle.on_hover = self._handle_hover
        self._update_styles()

    # Rest of the methods remain unchanged...
    def _get_style(self):
        if self._disabled:
            return self.styles["disabled"]
        if self.is_pressed:
            return self.styles["pressed"]
        if self._selected:
            return self.styles["selected"]
        if self.is_hovered:
            return self.styles["hovered"]
        return self.styles["default"]

    def _update_styles(self):
        style = self._get_style()
        self.inner_circle.bgcolor = style["inner"]
        self.outer_circle.bgcolor = style["outer"]
        self.outer_circle.border = ft.border.all(
            style["border_width"], style["border_color"]
        )
        if self._disabled:
            self.radio_label.color = self.theme.colors.get_color("text_disabled")

    def _handle_tap(self, e):
        if not self._disabled:
            if self._radio_group:
                self._radio_group.select_radio(self)
            else:
                # For standalone radio behavior
                self._selected = not self._selected
                self._update_styles()
                self.update()

    def _handle_tap_down(self, e):
        if self._disabled:
            return
        self.is_pressed = True
        self._update_styles()
        self.outer_circle.scale = 0.95
        self.update()

    def _handle_tap_up(self, e):
        if self._disabled:
            return
        self.is_pressed = False
        self._update_styles()
        self.outer_circle.scale = 1.0
        self.update()

    def _handle_hover(self, e):
        if self._disabled:
            return
        self.is_hovered = e.data == "true"
        if not self.is_pressed:
            self._update_styles()
            self.outer_circle.scale = 1.05 if self.is_hovered else 1.0
        self.update()

    def select(self):
        if self._selected != True:
            self._selected = True
            self._update_styles()
            self.update()

    def unselect(self):
        if self._selected != False:
            self._selected = False
            self._update_styles()
            self.update()


class RadioGroup(ft.Container):
    def __init__(
        self,
        content=None,
        value=None,
        on_change=None,
        design_system: FluentDesignSystem = None,
        is_dark_mode: bool = True,
        **kwargs,
    ):
        self.design_system = design_system or FluentDesignSystem()
        self.theme = (
            self.design_system.dark_theme
            if is_dark_mode
            else self.design_system.light_theme
        )

        self.radios = []
        self._value = value
        self._on_change = on_change

        super().__init__(content=content, **kwargs)

        if isinstance(content, ft.Column):
            for control in content.controls:
                self._find_radios(control)
        else:
            self._find_radios(content)

        if self._value is not None:
            self._select_by_value(self._value)

    def update_theme(self, is_dark_mode: bool):
        """Update radio group theme colors"""
        self.theme = (
            self.design_system.dark_theme
            if is_dark_mode
            else self.design_system.light_theme
        )
        # Update theme for all radio buttons
        for radio in self.radios:
            radio.update_theme(is_dark_mode)
        self.update()

    # Rest of RadioGroup methods remain unchanged...
    def _find_radios(self, content):
        """Recursively find all Radio components and register them"""
        if isinstance(content, Radio):
            content._radio_group = self
            self.radios.append(content)
        elif isinstance(content, ft.Container):
            if hasattr(content, "content"):
                self._find_radios(content.content)
        elif isinstance(content, (ft.Column, ft.Row)):
            for control in content.controls:
                self._find_radios(control)
        elif isinstance(content, (list, tuple)):
            for item in content:
                self._find_radios(item)

    def select_radio(self, selected_radio):
        old_value = self._value
        self._value = selected_radio.value

        for radio in self.radios:
            if radio != selected_radio:
                radio.unselect()

        selected_radio.select()

        if old_value != self._value and self._on_change:
            self._on_change(self._value)

        self.update()

    def did_mount(self):
        # Re-select initial value if needed
        if self._value is not None:
            self._select_by_value(self._value)
        self.update()

    def _select_by_value(self, value):
        matching_radio = None
        for radio in self.radios:
            if radio.value == value:
                matching_radio = radio
                break

        if matching_radio:
            self.select_radio(matching_radio)
        else:
            print(f"No radio found with value: {value}")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._value != new_value:
            self._value = new_value
            self._select_by_value(new_value)
