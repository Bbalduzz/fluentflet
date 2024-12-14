import flet as ft
from typing import List, Optional, Callable


class FluentGridView(ft.GridView):
    def __init__(
        self,
        controls: List[ft.Control],
        multiple_select: bool = True,
        movable: bool = True,
        on_select_changed: Optional[Callable[[List[int]], None]] = None,
        on_reorder: Optional[Callable[[int, int], None]] = None,
        **kwargs
    ):
        super().__init__(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            runs_count=kwargs.pop("runs_count", 4),
            max_extent=kwargs.pop("max_extent", 400),
            spacing=kwargs.pop("spacing", 2),
            run_spacing=kwargs.pop("run_spacing", 2),
            padding=kwargs.pop("padding", 0),
            **kwargs
        )

        self.original_controls = controls
        self.multiple_select = multiple_select
        self.movable = movable
        self.on_select_changed = on_select_changed
        self.on_reorder = on_reorder
        self.selected_indices: set[int] = set()
        self.drag_src_index: Optional[int] = None
        self.original_on_clicks: dict[int, Callable] = (
            {}
        )  # Store original click handlers

        self._wrap_controls()

    def _wrap_controls(self):
        """Wraps each control in a Container with hover and selection effects."""
        for idx, control in enumerate(self.original_controls):
            # Store original click handler if it exists
            if hasattr(control, "on_click"):
                self.original_on_clicks[idx] = control.on_click

            # Set the control to expand to fill container
            wrapped = ft.Container(
                content=control,
                alignment=ft.alignment.center,  # Center content
                border_radius=ft.border_radius.all(4),  # Square corners
                padding=0,
                animate=ft.animation.Animation(50, ft.AnimationCurve.EASE_IN_OUT),
                on_click=lambda e, i=idx: self._handle_click(i),
                on_hover=lambda e, i=idx: self._handle_hover(e, i),
            )

            if self.movable:
                wrapped.drag_interval = 5
                wrapped.data = idx
                wrapped.on_long_press = lambda e, i=idx: self._handle_drag_start(e, i)
                wrapped.on_drag_update = self._handle_drag_update
                wrapped.on_drag_end = self._handle_drag_end

            self.controls.append(wrapped)

    def _handle_click(self, e, index: int):
        """Handles both selection and original click event."""
        # Handle selection
        if self.multiple_select:
            if index in self.selected_indices:
                self.selected_indices.remove(index)
                self.controls[index].border = None
            else:
                self.selected_indices.add(index)
                self.controls[index].border = ft.border.all(2, "#62cdfe")
        else:
            for idx in self.selected_indices:
                self.controls[idx].border = None
            self.selected_indices.clear()

            self.selected_indices.add(index)
            self.controls[index].border = ft.border.all(2, "#62cdfe")

        # Call selection changed callback if it exists
        if self.on_select_changed:
            self.on_select_changed(list(self.selected_indices))

        # Call original click handler if it exists
        if index in self.original_on_clicks:
            self.original_on_clicks[index](e)

        self.update()

    def _handle_hover(self, e: ft.HoverEvent, index: int):
        container = self.controls[index]
        if e.data == "true":
            container.elevation = 4
        else:
            container.elevation = 0
        container.update()

    def _handle_drag_start(self, e: ft.DragStartEvent):
        if not self.movable:
            return

        self.drag_src_index = e.control.data
        e.control.scale = 1.05
        e.control.opacity = 0.7
        e.control.update()

    def _handle_drag_update(self, e: ft.DragUpdateEvent):
        if not self.movable or self.drag_src_index is None:
            return

        # Find target position
        target_idx = None
        for i, c in enumerate(self.controls):
            if i != self.drag_src_index and c.key:
                if (
                    c.left <= e.page_x <= c.left + c.width
                    and c.top <= e.page_y <= c.top + c.height
                ):
                    target_idx = i
                    break

        if target_idx is not None and target_idx != self.drag_src_index:
            # Move the control
            control = self.controls.pop(self.drag_src_index)
            self.controls.insert(target_idx, control)

            # Update source index
            self.drag_src_index = target_idx

            if self.on_reorder:
                self.on_reorder(self.drag_src_index, target_idx)

            self.update()

    def _handle_drag_end(self, e: ft.DragEndEvent):
        if not self.movable:
            return

        e.control.scale = 1.0
        e.control.opacity = 1.0
        self.drag_src_index = None
        e.control.update()

    def _find_target_index(self, x: float, y: float) -> int:
        """Finds the target index for drag and drop based on coordinates."""
        row = int(y // (self.run_spacing + self.max_extent))
        col = int(x // (self.spacing + self.max_extent))
        target_index = row * self.runs_count + col

        if 0 <= target_index < len(self.controls):
            return target_index
        return -1
