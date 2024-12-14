import flet as ft
from enum import Enum
import asyncio
from fluentflet.utils.fluent_design_system import FluentDesignSystem


class CheckState(Enum):
    UNCHECKED = "unchecked"
    CHECKED = "checked"
    INDETERMINATE = "indeterminate"


class Checkbox(ft.Container):
    CHECK_ICON_SIZE = 10

    def __init__(
        self,
        state: CheckState = CheckState.UNCHECKED,
        label: str = "",
        size: int = 20,
        on_change=None,
        disabled: bool = False,
        three_state: bool = False,
        design_system: FluentDesignSystem = None,
        is_dark_mode: bool = True,
        **kwargs
    ):
        # Initialize parent first
        super().__init__(animate=ft.animation.Animation(100, "easeOut"), **kwargs)

        # Initialize design system
        self.design_system = design_system or FluentDesignSystem()
        self.theme = (
            self.design_system.dark_theme
            if is_dark_mode
            else self.design_system.light_theme
        )

        # Define style configurations
        styles = {
            "box_bgcolor": {
                ft.ControlState.DEFAULT: self.theme.fills.get_fill(
                    "control_fill_tertiary"
                ),
                ft.ControlState.HOVERED: self.theme.fills.get_fill(
                    "control_fill_secondary"
                ),
                ft.ControlState.PRESSED: self.theme.fills.get_fill(
                    "control_fill_tertiary"
                ),
                ft.ControlState.DISABLED: self.theme.fills.get_fill(
                    "control_fill_disabled"
                ),
            },
            "border": {
                ft.ControlState.DEFAULT: ft.BorderSide(
                    1, self.theme.fills.get_fill("control_fill_default", 0.0578)
                ),
                ft.ControlState.HOVERED: ft.BorderSide(
                    1, self.theme.fills.get_fill("control_fill_default", 0.078)
                ),
                ft.ControlState.PRESSED: ft.BorderSide(
                    1, self.theme.fills.get_fill("control_fill_default", 0.0578)
                ),
                ft.ControlState.DISABLED: ft.BorderSide(
                    1, self.theme.fills.get_fill("control_fill_default", 0.042)
                ),
            },
            "checked_bgcolor": {
                ft.ControlState.DEFAULT: self.theme.colors.get_color("accent_default"),
                ft.ControlState.HOVERED: self.theme.colors.get_color(
                    "accent_secondary"
                ),
                ft.ControlState.PRESSED: self.theme.colors.get_color("accent_tertiary"),
                ft.ControlState.DISABLED: self.theme.colors.get_color(
                    "accent_disabled"
                ),
            },
            "check_color": {
                ft.ControlState.DEFAULT: self.theme.colors.get_color(
                    "text_on_accent_primary"
                ),
                ft.ControlState.HOVERED: self.theme.colors.get_color(
                    "text_on_accent_primary"
                ),
                ft.ControlState.PRESSED: self.theme.colors.get_color(
                    "text_on_accent_secondary"
                ),
                ft.ControlState.DISABLED: self.theme.colors.get_color(
                    "text_on_accent_disabled"
                ),
            },
        }

        self.state = state
        self._is_disabled = disabled
        self.on_change = on_change
        self.size = size
        self.style_config = styles
        self.three_state = three_state
        self._hovered = False
        self._pressed = False

        # Get initial state
        initial_state = (
            ft.ControlState.DISABLED if disabled else ft.ControlState.DEFAULT
        )

        # Create a Container for the icon to handle animations
        self.check_icon = ft.Icon(
            name=self._get_icon_name(),
            size=self.CHECK_ICON_SIZE,
            color=styles["check_color"][initial_state],
            visible=state != CheckState.UNCHECKED,
        )

        # Wrap icon in a container to handle animations
        self.icon_container = ft.Container(
            content=self.check_icon,
            animate_scale=ft.animation.Animation(
                duration=self.design_system.control_properties.control_normal_duration,
                curve="decelerate",
            ),
            scale=1 if state != CheckState.UNCHECKED else 0,
        )

        # Create checkbox container
        self.checkbox = ft.Container(
            width=size,
            height=size,
            border_radius=self.design_system.control_properties.control_corner_radius,
            animate=ft.animation.Animation(
                duration=self.design_system.control_properties.control_fast_duration,
                curve="easeOut",
            ),
            content=self.icon_container,
            alignment=ft.alignment.center,
            bgcolor=(
                styles["checked_bgcolor"][initial_state]
                if state != CheckState.UNCHECKED
                else styles["box_bgcolor"][initial_state]
            ),
            border=ft.border.all(width=1, color=styles["border"][initial_state].color),
        )

        # Create label if provided
        content = [self.checkbox]
        if label:
            content.append(
                ft.Text(
                    label,
                    size=int(
                        self.design_system.font_sizes.body_font_size.replace("px", "")
                    ),
                    font_family=self.design_system.font_families.font_family_text,
                    color=(
                        self.theme.colors.get_color("text_disabled")
                        if disabled
                        else self.theme.colors.get_color("text_primary")
                    ),
                )
            )

        # Update container content
        self.content = ft.Row(content, spacing=8)
        self.on_click = self._on_click if not disabled else None
        self.on_hover = self._on_hover if not disabled else None

    def update_theme(self, is_dark_mode: bool):
        """Update checkbox theme colors"""
        self.theme = (
            self.design_system.dark_theme
            if is_dark_mode
            else self.design_system.light_theme
        )
        # Update style configurations with new theme
        self.style_config = {
            "box_bgcolor": {
                ft.ControlState.DEFAULT: self.theme.fills.get_fill(
                    "control_fill_tertiary"
                ),
                ft.ControlState.HOVERED: self.theme.fills.get_fill(
                    "control_fill_secondary"
                ),
                ft.ControlState.PRESSED: self.theme.fills.get_fill(
                    "control_fill_tertiary"
                ),
                ft.ControlState.DISABLED: self.theme.fills.get_fill(
                    "control_fill_disabled"
                ),
            },
            "border": {
                ft.ControlState.DEFAULT: ft.BorderSide(
                    1, self.theme.fills.get_fill("control_fill_default", 0.0578)
                ),
                ft.ControlState.HOVERED: ft.BorderSide(
                    1, self.theme.fills.get_fill("control_fill_default", 0.078)
                ),
                ft.ControlState.PRESSED: ft.BorderSide(
                    1, self.theme.fills.get_fill("control_fill_default", 0.0578)
                ),
                ft.ControlState.DISABLED: ft.BorderSide(
                    1, self.theme.fills.get_fill("control_fill_default", 0.042)
                ),
            },
            "checked_bgcolor": {
                ft.ControlState.DEFAULT: self.theme.colors.get_color("accent_default"),
                ft.ControlState.HOVERED: self.theme.colors.get_color(
                    "accent_secondary"
                ),
                ft.ControlState.PRESSED: self.theme.colors.get_color("accent_tertiary"),
                ft.ControlState.DISABLED: self.theme.colors.get_color(
                    "accent_disabled"
                ),
            },
            "check_color": {
                ft.ControlState.DEFAULT: self.theme.colors.get_color(
                    "text_on_accent_primary"
                ),
                ft.ControlState.HOVERED: self.theme.colors.get_color(
                    "text_on_accent_primary"
                ),
                ft.ControlState.PRESSED: self.theme.colors.get_color(
                    "text_on_accent_secondary"
                ),
                ft.ControlState.DISABLED: self.theme.colors.get_color(
                    "text_on_accent_disabled"
                ),
            },
        }
        self._update_checkbox_style()

    # Rest of the methods remain unchanged...
    def _get_icon_name(self):
        if self.state == CheckState.CHECKED:
            return ft.icons.CHECK_ROUNDED
        elif self.state == CheckState.INDETERMINATE:
            return ft.icons.HORIZONTAL_RULE_ROUNDED
        return ft.icons.CHECK_ROUNDED

    def _get_current_state(self):
        if self._is_disabled:
            return ft.ControlState.DISABLED
        if self._pressed:
            return ft.ControlState.PRESSED
        if self._hovered:
            return ft.ControlState.HOVERED
        return ft.ControlState.DEFAULT

    def _get_next_state(self):
        if not self.three_state:
            return (
                CheckState.CHECKED
                if self.state == CheckState.UNCHECKED
                else CheckState.UNCHECKED
            )

        if self.state == CheckState.UNCHECKED:
            return CheckState.CHECKED
        elif self.state == CheckState.CHECKED:
            return CheckState.INDETERMINATE
        else:
            return CheckState.UNCHECKED

    async def _animate_icon(self, visible: bool):
        # If hiding, scale down first
        if not visible:
            self.icon_container.scale = 0
            self.update()
            await asyncio.sleep(0.15)  # Wait for animation
            self.check_icon.visible = False
        # If showing, make visible then scale up
        else:
            self.check_icon.visible = True
            self.check_icon.name = self._get_icon_name()
            self.icon_container.scale = 0
            self.update()
            await asyncio.sleep(0.01)  # Small delay for visibility
            self.icon_container.scale = 1
        self.update()

    def _update_checkbox_style(self):
        if not hasattr(self, "page"):
            return

        control_state = self._get_current_state()

        self.checkbox.bgcolor = (
            self.style_config["checked_bgcolor"][control_state]
            if self.state != CheckState.UNCHECKED
            else self.style_config["box_bgcolor"][control_state]
        )

        self.checkbox.border = ft.border.all(
            width=1, color=self.style_config["border"][control_state].color
        )

        self.check_icon.color = self.style_config["check_color"][control_state]

        self.update()

    async def _animate_click(self):
        await asyncio.sleep(0.1)  # 100ms delay
        self._pressed = False
        old_state = self.state
        self.state = self._get_next_state()

        # Animate the icon
        if old_state == CheckState.UNCHECKED:
            await self._animate_icon(True)
        elif self.state == CheckState.UNCHECKED:
            await self._animate_icon(False)
        else:
            # Just update the icon for state changes between checked/indeterminate
            self.check_icon.name = self._get_icon_name()
            self.update()

        self.checkbox.scale = 1.0
        self._update_checkbox_style()
        if self.on_change:
            self.on_change(self.state)

    def _on_click(self, e):
        self._pressed = True
        self._update_checkbox_style()
        self.checkbox.scale = 0.95
        self.page.run_task(self._animate_click)

    def _on_hover(self, e):
        self._hovered = e.data == "true"
        self._update_checkbox_style()
