import flet as ft
from fluentflet.components.button import Button, ButtonVariant
from typing import List, Union, Callable, Optional


class Dropdown(ft.Container):
    def __init__(
        self,
        options: List[Union[str, ft.Control]],
        max_width: int = 150,
        theme_mode: ft.ThemeMode = ft.ThemeMode.DARK,
        on_select: Optional[Callable] = None,
        animated: bool = True,
        initial_value: Optional[str] = None,
        **kwargs
    ):
        # Initialize container properties
        super().__init__(width=max_width, height=35, **kwargs)

        # Initialize dropdown properties
        self.options = options
        self.max_width = max_width
        self.on_select = on_select
        self.animated = animated
        self.selected_value = initial_value

        # State management
        self.is_open = False
        self._cached_position = None
        self.dropdown_overlay = None

        # Constants
        self.ANIMATION_DURATION = 300
        self.DROPDOWN_OFFSET = 5
        self.ITEM_HEIGHT = 35

        # Initialize the dropdown UI
        self._setup_dropdown()

    def _setup_dropdown(self):
        """Initialize the dropdown UI components"""
        self.dropdown_icon = ft.Icon(
            name=ft.icons.ARROW_DROP_DOWN_ROUNDED, color=ft.colors.WHITE, size=16
        )

        self.dropdown_button = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap_down=self.toggle_dropdown,
            content=Button(
                content=ft.Row(
                    [
                        ft.Text(self.selected_value or "Select an option"),
                        self.dropdown_icon,
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ),
        )
        self.content = self.dropdown_button
        self.padding = ft.padding.only(right=30)

    def _create_dropdown_item(self, option: Union[str, ft.Control]) -> ft.Container:
        """Create a styled dropdown item"""
        text = option if isinstance(option, str) else option.value

        def handle_item_click(e):
            self.selected_value = text
            self.dropdown_button.content.content.controls[0].value = text
            self.close_dropdown()
            if self.on_select:
                self.on_select(text)
            self.update()

        return ft.Container(
            content=ft.Text(
                text,
                color=ft.colors.with_opacity(1, "#ffffff"),
                size=14,
                no_wrap=True,
                overflow=ft.TextOverflow.ELLIPSIS,
            ),
            padding=ft.padding.only(left=15, top=8, bottom=8),
            border_radius=4,
            height=self.ITEM_HEIGHT,
            on_hover=lambda e: self._handle_item_hover(e),
            on_click=handle_item_click,
        )

    def _handle_item_hover(self, e: ft.HoverEvent) -> None:
        """Handle hover states for dropdown items"""
        container = e.control
        is_hover = e.data == "true"
        container.bgcolor = ft.colors.with_opacity(0.7, "#37393b") if is_hover else None
        container.content.color = (
            ft.colors.with_opacity(1, "#ffffff")
            if is_hover
            else ft.colors.with_opacity(1, "#ffffff")
        )
        container.update()

    def _create_dropdown_list(self) -> ft.Container:
        """Create the main dropdown container"""
        items = [self._create_dropdown_item(option) for option in self.options]

        return ft.Container(
            content=ft.ListView(items, spacing=2),
            # bgcolor=ft.colors.with_opacity(0.061, "#ffffff"),
            bgcolor="#2d2d2d",
            border=ft.border.all(1, ft.colors.with_opacity(0.8, ft.colors.BLACK)),
            border_radius=8,
            padding=5,
            width=self.max_width,
            shadow=ft.BoxShadow(
                spread_radius=-1,
                blur_radius=3,
                color=ft.colors.with_opacity(0.2, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
            animate=ft.animation.Animation(
                self.ANIMATION_DURATION, ft.AnimationCurve.EASE_OUT
            ),
            opacity=1,
        )

    def _calculate_position(self, e: ft.TapEvent) -> tuple:
        """Calculate dropdown position based on button position"""
        if not self._cached_position:
            self._cached_position = (
                e.global_x - e.local_x,
                e.global_y - e.local_y + self.DROPDOWN_OFFSET + self.height,
            )
        return self._cached_position

    def toggle_dropdown(self, e: ft.TapEvent) -> None:
        """Toggle dropdown state"""
        if self.is_open:
            self.close_dropdown()
        else:
            self._show_dropdown(e)

    def _show_dropdown(self, e: ft.TapEvent) -> None:
        """Show dropdown and calculate position"""
        position = self._calculate_position(e)
        dropdown = self._create_dropdown_list()
        dropdown.top = position[1]
        dropdown.left = position[0]

        if self.animated:
            dropdown.height = len(self.options) * self.ITEM_HEIGHT + 20  # 20px padding
            dropdown.opacity = 1

        # Create overlay for dropdown
        self.dropdown_overlay = ft.Stack([dropdown])
        self.page.overlay.append(self.dropdown_overlay)
        self.is_open = True
        self._update_dropdown_icon(True)
        self.page.update()

    def close_dropdown(self) -> None:
        """Close dropdown and clean up"""
        if self.dropdown_overlay:
            self.page.overlay.remove(self.dropdown_overlay)
            self.dropdown_overlay = None
        self.is_open = False
        self._update_dropdown_icon(False)
        self.page.update()

    def _update_dropdown_icon(self, is_open: bool) -> None:
        """Update dropdown icon state"""
        self.dropdown_icon.name = (
            ft.icons.ARROW_DROP_UP_ROUNDED
            if is_open
            else ft.icons.ARROW_DROP_DOWN_ROUNDED
        )
        self.dropdown_icon.update()
