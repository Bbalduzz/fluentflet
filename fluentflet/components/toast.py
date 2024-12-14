import flet as ft
from time import sleep
from enum import Enum
from fluentflet.components import Button, ButtonVariant


class ToastPosition(Enum):
    TOP_LEFT = "top-left"
    TOP_RIGHT = "top-right"
    TOP_CENTER = "top-center"
    BOTTOM_LEFT = "bottom-left"
    BOTTOM_RIGHT = "bottom-right"
    BOTTOM_CENTER = "bottom-center"


class ToastVariant(Enum):
    SINGLE_LINE = "single-line"
    MULTI_LINE = "multi-line"


class ToastSeverity(Enum):
    INFORMATIONAL = "informational"
    SUCCESS = "success"
    WARNING = "warning"
    CRITICAL = "critical"


class ToastActionType(Enum):
    NONE = "none"
    HYPERLINK = "hyperlink"
    DEFAULT = "default"


class ToastColors(Enum):
    INFORMATIONAL = {
        "light": {
            "bgcolor": "#f1f8fe",
            "border_color": "#d5e0fa",
            "text_color": "#3572d5",
        },
        "dark": {
            "bgcolor": ft.Colors.with_opacity(0.03, "#ffffff"),
            "border_color": ft.Colors.with_opacity(0.1, "#000000"),
            "text_color": ft.Colors.WHITE,
            "icon_color": "#3572d5",
        },
    }
    SUCCESS = {
        "light": {
            "bgcolor": "#effdf3",
            "border_color": "#dbfce6",
            "text_color": "#3c883b",
        },
        "dark": {
            "bgcolor": ft.Colors.with_opacity(1, "#383c1a"),
            "border_color": ft.Colors.with_opacity(0.1, "#000000"),
            "text_color": ft.Colors.WHITE,
            "icon_color": "#3c883b",
        },
    }
    CRITICAL = {
        "light": {
            "bgcolor": "#fcf0f0",
            "border_color": "#fae2e1",
            "text_color": "#d22d1d",
        },
        "dark": {
            "bgcolor": ft.Colors.with_opacity(1, "#452827"),
            "border_color": ft.Colors.with_opacity(0.1, "#000000"),
            "text_color": ft.Colors.WHITE,
            "icon_color": "#d22d1d",
        },
    }
    WARNING = {
        "light": {
            "bgcolor": "#fefcf1",
            "border_color": "#fbf7db",
            "text_color": "#d3863e",
        },
        "dark": {
            "bgcolor": ft.Colors.with_opacity(1, "#433519"),
            "border_color": ft.Colors.with_opacity(0.1, "#000000"),
            "text_color": ft.Colors.WHITE,
            "icon_color": "#d3863e",
        },
    }


class Toast(ft.Container):
    def __init__(
        self,
        title=None,
        message=None,
        severity: ToastSeverity | str = ToastSeverity.INFORMATIONAL,
        variant: ToastVariant | str = ToastVariant.SINGLE_LINE,
        action_type: ToastActionType | str = ToastActionType.NONE,
        action_text: str = None,
        action_url: str = None,
        on_action=None,
        position: ToastPosition | str = ToastPosition.TOP_RIGHT,
        **kwargs
    ):
        # Convert string enums to enum types if needed
        if isinstance(severity, str):
            severity = ToastSeverity(severity)
        if isinstance(variant, str):
            variant = ToastVariant(variant)
        if isinstance(action_type, str):
            action_type = ToastActionType(action_type)

        # Get colors based on severity
        colors = self.get_colors(severity)

        # Create content based on variant and action type
        content = self.create_content(
            severity,
            variant,
            title,
            message,
            colors,
            action_type,
            action_text,
            action_url,
            on_action,
        )

        # Set height based on variant
        height = kwargs.get(
            "height", 50 if variant == ToastVariant.SINGLE_LINE else None
        )
        animate_pos, offset = self.get_animation_config(position)

        super().__init__(
            content=content,
            bgcolor=colors["bgcolor"],
            border=ft.border.all(1, colors["border_color"]),
            border_radius=4,
            width=kwargs.get("width", 460),
            height=height,
            offset=offset,  # Initial offset based on position
            animate_offset=ft.animation.Animation(400, "decelerate"),
            opacity=0,  # Start fully transparent
            animate_opacity=ft.animation.Animation(200, "decelerate"),
            scale=kwargs.get("initial_scale", 0.95),  # Start slightly scaled down
            animate_scale=ft.animation.Animation(200, "decelerate"),
        )
        # Store animation values for later use
        self.final_offset = ft.Offset(0, 0)
        self.initial_offset = offset

    @staticmethod
    def get_colors(severity):
        return ToastColors[severity.name].value["dark"]

    def create_action_button(self, action_type, text, url, on_action, colors):
        if action_type == ToastActionType.NONE:
            return None

        if action_type == ToastActionType.HYPERLINK:
            return ft.TextButton(
                text=text,
                url=url,
                style=ft.ButtonStyle(
                    color=colors["text_color"],
                ),
            )

        return ft.TextButton(
            text=text,
            on_click=on_action,
            style=ft.ButtonStyle(
                color=colors["text_color"],
            ),
        )

    def create_content(
        self,
        severity,
        variant,
        title,
        message,
        colors,
        action_type,
        action_text,
        action_url,
        on_action,
    ):
        # Create severity icon
        icon = self.get_severity_icon(severity)
        icon_widget = (
            ft.Icon(
                name=icon,
                size=20,
                color=colors["icon_color"],
            )
            if icon
            else None
        )

        # Create close button
        close_button = Button(
            content=ft.Icon(name=ft.icons.CLOSE, size=16, color="#ffffff"),
            variant=ButtonVariant.HYPERLINK,
            on_click=lambda e: print("Close clicked"),
        )

        # Create text content
        text_content = (
            ft.Container(
                ft.Column(
                    controls=[
                        ft.Text(
                            title,
                            color=colors["text_color"],
                            size=14,
                            weight=ft.FontWeight.W_500,
                        ),
                        (
                            ft.Text(
                                message,
                                color=colors["text_color"],
                                size=14,
                            )
                            if message
                            else None
                        ),
                    ],
                    spacing=4,
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.padding.only(top=12, bottom=12),
            )
            if variant == ToastVariant.MULTI_LINE
            else ft.Row(
                controls=[
                    ft.Text(
                        title,
                        color=colors["text_color"],
                        size=14,
                        weight=ft.FontWeight.W_500,
                    ),
                    (
                        ft.Text(
                            message,
                            color=colors["text_color"],
                            size=14,
                        )
                        if message
                        else None
                    ),
                ],
                spacing=12,
                alignment=ft.MainAxisAlignment.START,
            )
        )

        return ft.Row(
            controls=[
                ft.Container(
                    icon_widget,
                    padding=ft.padding.only(left=12),
                ),
                ft.Container(
                    content=text_content,
                    expand=True,
                    padding=ft.padding.only(left=13),
                ),
                ft.Container(close_button, margin=ft.margin.only(right=12)),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

    def get_severity_icon(self, severity):
        icons = {
            ToastSeverity.INFORMATIONAL: ft.Icons.INFO_OUTLINE_ROUNDED,
            ToastSeverity.SUCCESS: ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
            ToastSeverity.WARNING: ft.Icons.WARNING_AMBER_ROUNDED,
            ToastSeverity.CRITICAL: ft.Icons.ERROR_OUTLINE_ROUNDED,
        }
        return icons.get(severity)

    def get_animation_config(self, position):
        """Returns the appropriate animation configuration based on position"""
        if not position:
            return ft.Offset(0, 0), ft.Offset(0, 0)

        animations = {
            "top-left": (ft.Offset(-1, 0), ft.Offset(-1, 0)),  # Slide from left
            "top-right": (ft.Offset(1, 0), ft.Offset(1, 0)),  # Slide from right
            "top-center": (ft.Offset(0, -1), ft.Offset(0, -1)),  # Slide from top
            "bottom-left": (ft.Offset(-1, 0), ft.Offset(-1, 0)),  # Slide from left
            "bottom-right": (ft.Offset(1, 0), ft.Offset(1, 0)),  # Slide from right
            "bottom-center": (ft.Offset(0, 1), ft.Offset(0, 1)),  # Slide from bottom
        }
        return animations.get(position, (ft.Offset(0, 0), ft.Offset(0, 0)))

    def animate_entrance(self):
        """Trigger the entrance animation"""
        self.offset = self.final_offset
        self.opacity = 1
        self.scale = 1
        self.update()

    def animate_exit(self):
        """Trigger the exit animation"""
        self.offset = self.initial_offset
        self.opacity = 0
        self.scale = 0.95
        self.update()


class Toaster:
    def __init__(
        self,
        page,
        expand=False,
        position: ToastPosition | str = ToastPosition.TOP_RIGHT,
        theme: str = "dark",
        default_toast_duration=3,
        default_offset=20,
    ):
        self.theme = theme
        self.page = page
        self.default_position = (
            position.value if isinstance(position, ToastPosition) else position
        )
        self.default_toast_duration = default_toast_duration
        self.default_offset = default_offset
        self.is_hovered = False
        self.is_expanded = expand

        # Dictionary to store position-specific stacks and toasts
        self.position_stacks = {}
        self.position_toasts = {}

        # Initialize default stack
        self.initialize_position_stack(self.default_position)

        self.page.on_resized = self.handle_resize

    def initialize_position_stack(self, position):
        """Create a new stack for a specific position if it doesn't exist"""
        if position not in self.position_stacks:
            stack = ft.Stack(
                width=self.page.window.width,
                height=self.page.window.height,
                expand=True,
            )
            self.position_stacks[position] = stack
            self.position_toasts[position] = []
            self.page.overlay.append(stack)

    def show_toast(
        self,
        title=None,
        message=None,
        severity: ToastSeverity | str = ToastSeverity.INFORMATIONAL,
        variant: ToastVariant | str = ToastVariant.SINGLE_LINE,
        action_type: ToastActionType | str = ToastActionType.NONE,
        action_text: str = None,
        action_url: str = None,
        on_action=None,
        position: ToastPosition | str = None,
        duration=3,
        toast=None,
        **kwargs
    ):
        # Convert position to string value if it's an enum
        if isinstance(position, ToastPosition):
            position = position.value
        position = position or self.default_position

        # Initialize stack for this position if it doesn't exist
        self.initialize_position_stack(position)

        # Create or use provided toast
        toast = (
            toast
            if toast
            else Toast(
                title=title,
                message=message,
                severity=severity,
                variant=variant,
                action_type=action_type,
                action_text=action_text,
                action_url=action_url,
                on_action=on_action,
                position=position,  # Pass position to Toast
                **kwargs
            )
        )

        # Get the position-specific stack and toasts list
        stack = self.position_stacks[position]
        toasts = self.position_toasts[position]

        # Position and add the toast
        self.set_toast_position(toast, 0, position)
        stack.controls.append(toast)
        toasts.insert(0, toast)
        self.reposition_toasts(position)
        self.page.update()

        # Trigger entrance animation after a brief delay
        def trigger_animation():
            sleep(0.05)  # Small delay to ensure the toast is rendered
            toast.animate_entrance()

        self.page.run_thread(trigger_animation)

        if duration > 0:

            def __remove_toast():
                sleep(duration)
                if toast in stack.controls:
                    # Trigger exit animation
                    toast.animate_exit()
                    sleep(0.4)  # Wait for animation to complete
                    self.remove_toast(toast, position)

            self.page.run_thread(__remove_toast)

    def update_toast(
        self,
        toast,
        message,
        description,
        severity,
        position,
        variant=ToastVariant.SINGLE_LINE,
        action_type=ToastActionType.NONE,
        action_text=None,
        action_url=None,
        on_action=None,
    ):
        colors = ToastColors[severity.name].value["dark"]
        toast.content = toast.create_content(
            severity,
            variant,
            message,
            description,
            colors,
            action_type,
            action_text,
            action_url,
            on_action,
        )
        toast.bgcolor = colors["bgcolor"]
        toast.border = ft.border.all(1, colors["border_color"])
        self.page.update()
        sleep(3)
        self.remove_toast(toast, position)

    def remove_toast(self, toast, position):
        stack = self.position_stacks[position]
        toasts = self.position_toasts[position]

        if toast in stack.controls:
            stack.controls.remove(toast)
            toasts.remove(toast)
            self.reposition_toasts(position)
            self.page.update()

    def reposition_toasts(self, position):
        toasts = self.position_toasts[position]
        for i, toast in enumerate(toasts):
            if self.is_hovered or self.is_expanded:
                self.set_toast_position(toast, i, position)
            else:
                self.set_toast_position(toast, i, position)

    def set_toast_position(self, toast, index, position, as_column=True):
        base_offset = self.default_offset
        spacing = 10

        if as_column:
            if "top" in position:
                toast.top = base_offset + (index * 60)
                toast.bottom = None
            elif "bottom" in position:
                toast.bottom = base_offset + (index * 60)
                toast.top = None
            toast.scale = 1
        else:
            if "top" in position:
                toast.top = base_offset + (index * 10)
                toast.bottom = None
            else:
                toast.bottom = base_offset + (index * 10)
                toast.top = None
            toast.scale = 1 - (0.05 * index)

        # Handle horizontal positioning
        toast_width = toast.width or 300
        if "left" in position:
            toast.left = base_offset
            toast.right = None
        elif "right" in position:
            toast.right = base_offset
            toast.left = None
        elif "center" in position:
            toast.left = (self.page.window.width - toast_width) / 2
            toast.right = None

        # Only the top toast in each position stack handles hover events
        if index == 0 and not self.is_expanded:
            toast.on_hover = lambda e: self.on_hover(e, position)
        else:
            toast.on_hover = None

    def on_hover(self, e, position):
        self.is_hovered = e.data == "true"
        self.reposition_toasts(position)
        self.page.update()

    def handle_resize(self, e):
        # Update all stacks
        for position, stack in self.position_stacks.items():
            stack.width = self.page.window.width
            stack.height = self.page.window.height
            self.reposition_toasts(position)
        self.page.update()
