import flet as ft
import time
from fluentflet.components import Button, ButtonVariant
from fluentflet.utils.fluent_design_system import FluentDesignSystem


class Dialog(ft.Container):
    def __init__(self, title="Dialog Title", content=None, actions=None):
        super().__init__()
        self.theme = FluentDesignSystem().dark_theme
        self.dialog_width = 400
        self.title_text = title
        self._content = content or ft.Text("Some text")
        self.actions = actions or [
            Button("Action", variant=ButtonVariant.ACCENT, expand=True),
            Button("Close", on_click=lambda e: self.close_dialog(), expand=True),
        ]

        # Initialize base container
        self.expand = False
        self.opacity = 0
        self.bgcolor = ft.Colors.with_opacity(0.3, "#000000")
        # self.blur = ft.Blur(5, 5, ft.BlurTileMode.REPEATED)
        self.alignment = ft.alignment.center
        self.animate_opacity = ft.animation.Animation(
            200, ft.AnimationCurve.EASE_IN_OUT
        )

    def did_mount(self):
        """Called when the control is added to the page"""
        self.initialize_dialog()

    def close_dialog(self, e=None):
        self.dialog_window.opacity = 0
        self.dialog_window.scale = 0.95
        self.dialog_window.update()

        self.opacity = 0
        self.update()

        def remove_dialog(e):
            if self in self.page.overlay:
                self.page.overlay.remove(self)

        self.on_animation_end = remove_dialog
        self.page.update()

    def show(self):
        time.sleep(0.05)
        self.opacity = 1
        self.update()
        self.dialog_window.opacity = 1
        self.dialog_window.scale = 1
        self.dialog_window.update()

    def initialize_dialog(self):
        # Create main content column
        content_column = ft.Column(
            spacing=0,
            controls=[
                # Title area
                ft.Container(
                    padding=ft.padding.only(left=24, right=24, top=24, bottom=12),
                    content=ft.Text(
                        self.title_text, size=24, weight=ft.FontWeight.W_500
                    ),
                ),
                # Content area
                ft.Container(
                    padding=ft.padding.symmetric(horizontal=24),
                    expand=True,
                    content=self._content,
                ),
                # Actions row at bottom
                ft.Container(
                    padding=ft.padding.all(24),
                    margin=ft.margin.only(top=24),
                    bgcolor=self.theme.get("solid_background_base"),
                    border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[ft.Row(self.actions, spacing=10, expand=True)],
                    ),
                ),
            ],
        )

        # Main dialog container
        self.dialog_window = ft.Container(
            width=self.dialog_width,
            bgcolor="#292929",
            border_radius=8,
            content=content_column,
            top=self.page.window.height / 3,
            opacity=0,
            border=ft.border.all(0.5, "#757575"),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.colors.with_opacity(0.3, "black"),
                offset=ft.Offset(0, 4),
            ),
            animate=ft.animation.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            animate_scale=ft.animation.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
            animate_opacity=ft.animation.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
        )

        # Add click handler to background
        self.on_click = self.close_dialog

        # Stack for the dialog
        dialog_stack = ft.Stack([self.dialog_window], width=self.dialog_width)
        self.content = dialog_stack
