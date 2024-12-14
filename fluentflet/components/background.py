import flet as ft
import flet.canvas as cv
import math
from dataclasses import dataclass
from typing import Optional


class Background:
    """Background decorations for Flet pages"""

    @staticmethod
    def DOTS(
        spacing: float = 15,
        radius: float = 0.5,
        color: str = "#20283a",
        opacity: float = 0.1,
        width: int = 800,
        height: int = 800,
    ) -> ft.Row:

        rows = math.ceil(height / spacing)
        cols = math.ceil(width / spacing)

        # Create dots
        dots = []
        for row in range(rows):
            for col in range(cols):
                x = col * spacing
                y = row * spacing
                dots.append(
                    cv.Circle(
                        x,
                        y,
                        radius,  # x, y, radius
                        paint=ft.Paint(color=color, style=ft.PaintingStyle.FILL),
                    )
                )

        # Create canvas for background
        return cv.Canvas(dots, width=float("inf"), expand=True)
