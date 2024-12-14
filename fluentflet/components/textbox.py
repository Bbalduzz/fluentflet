import flet as ft
from fluentflet.utils import FluentIcon, FluentIcons, FluentIconStyle
from fluentflet.utils.fluent_design_system import FluentDesignSystem
from fluentflet.components.button import Button, ButtonVariant


class TextBox(ft.Container):
    def __init__(
        self,
        design_system: FluentDesignSystem = FluentDesignSystem(),
        placeholder: str = "TextBox",
        width: int = 200,
        text_size: int = 14,
        height: int = 32,
        password: bool = False,
        actions_visible: bool = True,
        prefix: str = None,
        suffix: str = None,
        **kwargs
    ):
        # Keep the kwargs handling for TextField
        textfield_props = set(dir(ft.TextField)) - set(dir(ft.Container))
        textfield_props = {prop for prop in textfield_props if not prop.startswith("_")}
        textfield_kwargs = {
            k: kwargs.pop(k) for k in dict(kwargs) if k in textfield_props
        }

        super().__init__(**kwargs)
        self.design_system = design_system
        self.theme = self.design_system.dark_theme  # or light_theme based on your needs
        self.width = width
        self.height = height + 2
        self.default_bgcolor = self.theme.fills.get_fill("control_fill_default")
        self.bgcolor = self.default_bgcolor
        self.actions_visible = actions_visible
        self._action = None
        self.is_password = password

        # padding based on actions and prefix/suffix
        right_padding = 40 if password else 10
        left_padding = 10

        self.prefix_text = None
        if prefix:
            self.prefix_text = ft.Text(
                value=prefix,
                size=text_size,
                color=self.theme.colors.get_color("text_tertiary"),
                weight=ft.FontWeight.W_400,
            )
            left_padding = (
                len(prefix) * (text_size * 0.6) + 15
            )  # Approximate character width

        self.suffix_text = None
        if suffix:
            self.suffix_text = ft.Text(
                value=suffix,
                size=text_size,
                color=self.theme.colors.get_color("text_tertiary"),
                weight=ft.FontWeight.W_400,
            )
            right_padding += (
                len(suffix) * (text_size * 0.6) + 5
            )  # Approximate character width

        # Create the text field with modified hint style
        self.textfield = ft.TextField(
            border=ft.InputBorder.NONE,
            height=height,
            text_size=text_size,
            password=password,
            bgcolor=ft.colors.TRANSPARENT,
            color=self.theme.colors.get_color("text_primary"),
            cursor_color=self.theme.colors.get_color("text_primary"),
            cursor_height=16,
            cursor_width=1,
            hint_text=placeholder,
            hint_style=ft.TextStyle(
                color=self.theme.colors.get_color("text_tertiary"),
                size=text_size,
                weight=ft.FontWeight.W_400,
            ),
            on_focus=self._handle_focus,
            on_blur=self._handle_blur,
            content_padding=ft.padding.only(
                left=left_padding, right=right_padding, bottom=7
            ),
            **textfield_kwargs
        )

        # Create the bottom border
        self.bottom_border = ft.Container(
            width=width,
            height=1,
            bgcolor=self.theme.colors.get_color("text_tertiary"),
        )

        # Add password visibility toggle or actions if provided
        self.actions_row = ft.Row(spacing=4, visible=self.actions_visible)
        self.actions_container = ft.Container(
            content=self.actions_row,
            right=4,
            top=0,
        )

        # Create stack controls list
        stack_controls = [
            ft.Container(
                content=self.textfield,
                width=width,
                height=height,
            ),
            ft.Container(
                content=self.bottom_border,
                bottom=0,
                width=width,
            ),
            self.actions_container,
        ]

        # Add prefix label if provided
        if self.prefix_text:
            stack_controls.append(
                ft.Container(
                    content=self.prefix_text,
                    left=10,
                    top=(height - text_size) / 2 - 2,
                )
            )

        # Add suffix label if provided
        if self.suffix_text:
            stack_controls.append(
                ft.Container(
                    content=self.suffix_text,
                    right=(40 if password else 10),
                    top=(height - text_size) / 2 - 2,
                )
            )

        if password:
            self.button = Button(
                design_system=self.design_system,
                content=self._get_button_icon(),
                variant=ButtonVariant.HYPERLINK,
                width=28,
                height=28,
                on_click=self._handle_button_click,
            )
            self.actions_row.controls.append(self.button)

        # Setup container properties
        self.content = ft.Stack(controls=stack_controls)
        self.width = width
        self.bgcolor = self.default_bgcolor
        self.border_radius = self.design_system.control_properties.control_corner_radius
        self.padding = 0

    def _get_button_icon(self):
        if self.is_password:
            return FluentIcon(
                name=(
                    FluentIcons.EYE_HIDE
                    if self.textfield.password
                    else FluentIcons.EYE_SHOW
                ),
                size=16,
                color=self.theme.colors.get_color("text_primary"),
            )
        return FluentIcon(
            name=FluentIcons.SEARCH,
            size=16,
            color=self.theme.colors.get_color("text_primary"),
        )

    def _handle_button_click(self, e):
        if self.is_password:
            self.textfield.password = not self.textfield.password
            self.button.content = self._get_button_icon()
            self.update()
        elif self._action:
            self._action(e)

    def _handle_focus(self, e):
        self.bgcolor = self.theme.fills.get_fill("control_fill_input_active")
        self.bottom_border.bgcolor = self.theme.colors.get_color("accent_default")
        self.bottom_border.height = 1.5
        # Update hint text color when focused
        self.textfield.hint_style.color = self.theme.colors.get_color("text_tertiary")
        self.textfield.hint_style.opacity = 1.0
        if not self.actions_visible:
            self.actions_row.visible = True
            self.actions_row.update()
        self.update()

    def _handle_blur(self, e):
        self.bgcolor = self.default_bgcolor
        self.bottom_border.bgcolor = self.theme.colors.get_color("text_tertiary")
        self.bottom_border.height = 1
        # Update hint text color when blurred
        self.textfield.hint_style.color = self.theme.colors.get_color("text_secondary")
        self.textfield.hint_style.opacity = 0.8
        if not self.actions_visible:
            self.actions_row.visible = False
            self.actions_row.update()
        self.update()

    def add_action(self, icon: FluentIcons, on_click=None, tooltip: str = None):
        """Add an action button to the textbox."""
        button = Button(
            design_system=self.design_system,
            content=FluentIcon(
                name=icon, size=16, color=self.theme.colors.get_color("text_primary")
            ),
            variant=ButtonVariant.HYPERLINK,
            width=28,
            height=28,
            on_click=on_click,
            tooltip=tooltip,
        )
        self.actions_row.controls.append(button)
        if self.page:
            self.update()
        return button

    def clear_actions(self):
        """Remove all action buttons except password toggle if present."""
        if self.is_password and self.button in self.actions_row.controls:
            self.actions_row.controls = [self.button]
        else:
            self.actions_row.controls = []
        if self.page:
            self.update()

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, func):
        self._action = func

    @property
    def value(self):
        return self.textfield.value

    @value.setter
    def value(self, value):
        self.textfield.value = value
        self.update()
