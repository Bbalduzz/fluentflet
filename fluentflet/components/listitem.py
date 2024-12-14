import flet as ft
from fluentflet.utils.fluent_design_system import FluentDesignSystem


class ListItem(ft.GestureDetector):
    instances = []

    def __init__(
        self,
        content,
        on_click=None,
        is_dark_mode: bool = True,
        selected: bool = False,
        **kwargs
    ):
        # Initialize design system
        self.design_system = FluentDesignSystem()
        self.theme = (
            self.design_system.dark_theme
            if is_dark_mode
            else self.design_system.light_theme
        )

        self.item_content = content
        self._on_click = on_click
        self.is_hovered = False
        self.is_pressed = False
        self._is_selected = False

        # Add this instance to the class instances list
        ListItem.instances.append(self)

        # Main content container
        self.content_container = ft.Container(
            content=self.item_content,
            padding=ft.padding.only(left=11, top=10, right=10, bottom=10),
        )

        # Stack allows absolute positioning of children
        self.container = ft.Container(
            content=ft.Stack(
                controls=[
                    self.content_container,
                    ft.Container(
                        width=3,
                        height=18,
                        bgcolor=self.theme.colors.get_color("accent_default"),
                        border_radius=ft.border_radius.all(4),
                        animate=ft.animation.Animation(
                            duration=100, curve=ft.AnimationCurve.ELASTIC_OUT
                        ),
                        expand=True,
                        visible=False,
                        left=0,
                        top=11,
                    ),
                ],
            ),
            border_radius=self.design_system.control_properties.control_corner_radius,
            animate=ft.animation.Animation(
                duration=self.design_system.control_properties.control_fast_duration,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
            expand=True,
        )

        # Store reference to indicator
        self.indicator = self.container.content.controls[1]

        super().__init__(
            content=self.container,
            mouse_cursor=ft.MouseCursor.BASIC,
            on_enter=self._on_enter,
            on_exit=self._on_exit,
            on_tap_down=self._on_click_down,
            on_tap_up=self._on_click_up,
            on_tap=self._on_tap,
        )

        # Set initial selected state
        if selected:
            self.selected = True

    @property
    def selected(self) -> bool:
        """Get the selected state"""
        return self._is_selected

    @selected.setter
    def selected(self, value: bool):
        """Set the selected state and update visuals"""
        if value != self._is_selected:
            if value:
                # Deselect other items first
                ListItem.deselect_all(except_item=self)

            self._is_selected = value
            self.indicator.visible = value
            self.update_color()
            self.indicator.update()

    def update_theme(self, is_dark_mode: bool):
        """Update list item theme colors"""
        self.theme = (
            self.design_system.dark_theme
            if is_dark_mode
            else self.design_system.light_theme
        )
        self.indicator.bgcolor = self.theme.colors.get_color("accent_default")
        self.update_color()

    @classmethod
    def deselect_all(cls, except_item=None):
        """Deselect all items except the specified one"""
        for item in cls.instances:
            if item != except_item and item.selected:
                item.selected = False

    def _on_enter(self, e):
        self.is_hovered = True
        self.update_color()

    def _on_exit(self, e):
        self.is_hovered = False
        self.update_color()

    def _on_click_down(self, e):
        self.is_pressed = True
        self.update_color()

    def _on_click_up(self, e):
        self.is_pressed = False
        if not self.selected:
            self.update_color()

    def _on_tap(self, e):
        self.selected = not self.selected
        if self._on_click:
            self._on_click(e)

    def update_color(self):
        if self.selected:
            self.container.bgcolor = self.theme.fills.get_fill("control_fill_secondary")
        elif self.is_pressed:
            self.container.bgcolor = self.theme.fills.get_fill("control_fill_secondary")
        elif self.is_hovered:
            self.container.bgcolor = self.theme.fills.get_fill("control_fill_tertiary")
        else:
            self.container.bgcolor = None
        self.container.update()
