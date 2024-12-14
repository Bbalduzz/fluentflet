import flet as ft
from fluentflet.utils.fluent_design_system import FluentDesignSystem


class ProgressRing(ft.ProgressRing):
    def __init__(self, **kwargs):
        self.theme = FluentDesignSystem().dark_theme
        super().__init__(
            stroke_width=kwargs.get("stroke_width", 3),
            color=self.theme.colors.get_color("accent_default"),
            stroke_cap=ft.StrokeCap.ROUND,
            **kwargs
        )
