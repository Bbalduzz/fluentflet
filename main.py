import flet as ft
from fluentflet import (
    Button,
    ButtonVariant,
    Checkbox,
    CheckState,
    Slider,
    SliderOrientation,
    Radio,
    RadioGroup,
    TreeView,
    DictTreeViewModel,
    JSONTreeViewModel,
    TextBox,
    ToolTip,
    Calendar,
    Toggle,
    Expander,
    Dropdown,
    ListItem,
    ProgressRing,
    Dialog,
)
from fluentflet import FluentWindow, Titlebar, NavigationType
from fluentflet import FluentIcon, FluentIcons, FluentIconStyle
from fluentflet.__version__ import VERSION

print(VERSION)

from datetime import datetime
from pathlib import Path
import inspect


class DisplayGroup(ft.Container):
    def __init__(self, title: str, widgets: list = None, **kwargs):
        # Extract widget path from the first widget if available
        widget_path = "fluentflet.components"

        # Create header with title and path
        header = ft.Column(
            [
                ft.Text(
                    value=title, size=32, weight=ft.FontWeight.BOLD, color="#ffffff"
                ),
                ft.Text(value=widget_path, size=14, color="#808080"),
            ],
            spacing=5,
        )

        # Create content column for widgets
        self.content_column = ft.Column(
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            expand=True,
            scroll=ft.ScrollMode.ALWAYS,
        )

        if widgets:
            self.content_column.controls.extend(widgets)

        # Combine header and content
        main_column = ft.Column([header, self.content_column], spacing=20)

        super().__init__(
            content=main_column,
            padding=ft.padding.symmetric(horizontal=30, vertical=20),
            border_radius=8,
            expand=True,
            **kwargs,
        )

    def add(self, item):
        """Add a widget to the group"""
        self.content_column.controls.append(item)
        self.update()

    def remove(self, item):
        """Remove a widget from the group"""
        self.content_column.controls.remove(item)
        self.update()

    def clear(self):
        """Remove all widgets"""
        self.content_column.controls.clear()
        self.update()


class DisplayItem(ft.Container):
    def __init__(self, title: str = "", content: ft.Control = None, **kwargs):
        self.title = ft.Text(
            value=title, size=14, weight=ft.FontWeight.NORMAL, color="#ffffff"
        )

        """
        source_code = self._get_source_code(content) if content else ""

        ft.Container(
            content=ft.Text(
                value="", #source_code,
                color=ft.colors.WHITE70,
                size=12,
                selectable=True
            ),
            padding=ft.padding.only(top=8)
        )
        """

        # Create main content with source code section
        main_content = ft.Column(
            [
                # Widget display
                (
                    ft.Container(
                        content=ft.Row([content]),
                        bgcolor=ft.Colors.with_opacity(0.6, "#1e1e1e"),
                        padding=20,
                        border_radius=ft.border_radius.only(top_left=8, top_right=8),
                        expand=True,
                    )
                    if content
                    else None
                ),
                # Source code section
                (
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text("Source code", color="#808080"),
                                        Button(
                                            FluentIcon(
                                                FluentIcons.COPY,
                                                size=14,
                                                color="#ffffff",
                                            ),
                                            variant=ButtonVariant.HYPERLINK,
                                            # on_click=lambda _: self.copy_source_code(source_code)
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                            ]
                        ),
                        bgcolor=ft.Colors.with_opacity(0.6, "#2d2d2d"),
                        padding=ft.padding.symmetric(horizontal=10, vertical=8),
                        border_radius=ft.border_radius.only(
                            bottom_left=8, bottom_right=8
                        ),
                    )
                    if content
                    else None
                ),
            ],
            spacing=1,
        )

        super().__init__(
            content=ft.Column(
                [self.title, main_content] if content else [self.title],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.padding.symmetric(horizontal=0, vertical=10),
            border_radius=8,
            **kwargs,
        )

    def _get_source_code(self, content) -> str:
        if content is None:
            return "None"

        # Get class name and signature
        class_name = content.__class__.__name__
        sig = inspect.signature(content.__class__.__init__)

        # List of attributes we want to skip
        skip_attrs = {"design_system", "page", "parent", "_build", "_created", "_id"}

        # Separate positional and keyword parameters
        pos_params = []
        kw_params = []

        for param_name, param in sig.parameters.items():
            if param_name == "self" or param_name in skip_attrs:
                continue

            actual_value = getattr(content, param_name, None)
            # Skip None values and complex objects
            if actual_value is not None and not hasattr(actual_value, "__dict__"):
                # If parameter is positional-only or has no default value
                if param.kind == param.POSITIONAL_ONLY or (
                    param.kind == param.POSITIONAL_OR_KEYWORD
                    and param.default == param.empty
                ):
                    pos_params.append(repr(actual_value))
                else:
                    kw_params.append(f"{param_name}={repr(actual_value)}")

        # Combine all parameters
        all_params = pos_params + kw_params
        return f"{class_name}({', '.join(all_params)})"


def main(page: ft.Page):
    page.title = "Fluent Flet"
    page.icon = Path("fluentflet", "static", "fluentflet.png")
    page.window.width = 800
    page.accepts_drops = True

    window = FluentWindow(
        page=page,
        window_titlebar=Titlebar(
            title="Fluent Flet Components",
            icon=ft.Image(src="fluentflet/static/fluentflet.png", width=18, height=18),
        ),
        nav_type=NavigationType.OVERLAY,
        navigation_items=[
            {"icon": FluentIcons.HOME, "label": "Home", "route": "/home"},
            {"icon": FluentIcons.SYMBOLS, "label": "Fluent icons", "route": "/icons"},
            {"type": "divider"},
            {
                "icon": FluentIcons.CONTROL_BUTTON,
                "label": "Button",
                "route": "/components/button",
            },
            {
                "icon": FluentIcons.CHECKBOX_CHECKED,
                "label": "Checkbox",
                "route": "/components/checkbox",
            },
            {
                "icon": FluentIcons.RADIO_BUTTON,
                "label": "Radio",
                "route": "/components/radio",
            },
            {
                "icon": FluentIcons.TOGGLE_LEFT,
                "label": "Toggle",
                "route": "/components/toggle",
            },
            {
                "icon": FluentIcons.TEXT_FIELD,
                "label": "TextBox",
                "route": "/components/textbox",
            },
            {
                "icon": FluentIcons.COMMENT,
                "label": "Dropdown",
                "route": "/components/dropdown",
            },
            {
                "icon": FluentIcons.ARROW_AUTOFIT_WIDTH,
                "label": "Slider",
                "route": "/components/slider",
            },
            {
                "icon": FluentIcons.CALENDAR_EMPTY,
                "label": "Calendar",
                "route": "/components/calendar",
            },
            {
                "icon": FluentIcons.LIST,
                "label": "ListItem",
                "route": "/components/listitem",
            },
            {
                "icon": FluentIcons.CHEVRON_DOWN,
                "label": "Expander",
                "route": "/components/expander",
            },
            {
                "icon": FluentIcons.ARROW_SYNC_CIRCLE,
                "label": "Progress",
                "route": "/components/progress",
            },
            {
                "icon": FluentIcons.TEXT_BULLET_LIST_TREE,
                "label": "Treeview",
                "route": "/components/treeview",
            },
            {
                "icon": FluentIcons.RECTANGLE_LANDSCAPE,
                "label": "Dialog",
                "route": "/components/dialog",
            },
        ],
        bottom_navigation_items=[
            {"type": "divider"},
            {"icon": FluentIcons.SETTINGS, "label": "Settings", "route": "/settings"},
        ],
        colors={
            "nav_bg": "#1F1F1F",
            "content_bg": "#282828",
        },
    )

    # Home View
    @window.route("/")
    def home():
        return DisplayGroup(
            title="home",
            widgets=[
                DisplayItem(
                    title="Welcome to Fluent Flet Components",
                    content=ft.Column(
                        [
                            ft.Text(
                                "A showcase of individual Fluent Flet widgets",
                                size=20,
                                color="white",
                            ),
                            ft.Text(
                                "Select a component from the navigation menu to see detailed examples.",
                                color="#808080",
                                size=16,
                            ),
                            # ft.Text("Current fluentflet version:", VERSION_STRING)
                        ]
                    ),
                )
            ],
        )

    # Slider Page
    @window.route("/components/slider")
    def slider():
        return DisplayGroup(
            title="Slider",
            widgets=[
                DisplayItem(
                    title="Horizontal Slider",
                    content=Slider(
                        value=50,
                        min=0,
                        max=100,
                        on_change=lambda e: print(f"Value: {round(e.current_value)}"),
                    ),
                ),
                DisplayItem(
                    title="Vertical Slider",
                    content=ft.Container(
                        content=Slider(
                            value=50,
                            orientation=SliderOrientation.VERTICAL,
                        ),
                        height=220,
                    ),
                ),
            ],
        )

    # Button Page
    @window.route("/components/button")
    def button():
        return DisplayGroup(
            title="Button",
            widgets=[
                DisplayItem(
                    title="Standard Button",
                    content=Button(
                        content=ft.Text("Standard"),
                        on_click=lambda e: print("Button clicked"),
                    ),
                ),
                DisplayItem(
                    title="Accent Button",
                    content=Button("Accent", variant=ButtonVariant.ACCENT),
                ),
                DisplayItem(
                    title="Toggle Button",
                    content=Button("Toggle", variant=ButtonVariant.TOGGLE),
                ),
                DisplayItem(
                    title="Icon Button",
                    content=Button(content=FluentIcon(name=FluentIcons.ADD, size=15)),
                ),
                DisplayItem(
                    title="Hyperlink Button",
                    content=Button("Hyperlink", variant=ButtonVariant.HYPERLINK),
                ),
                DisplayItem(
                    title="Disabled Button",
                    content=Button(content=ft.Text("Standard"), disabled=True),
                ),
                DisplayItem(
                    title="Disabled Accent Button",
                    content=Button(
                        content=ft.Text("Accent"),
                        variant=ButtonVariant.ACCENT,
                        disabled=True,
                    ),
                ),
                DisplayItem(
                    title="Disabled Toggle Button",
                    content=Button(
                        "Toggle", variant=ButtonVariant.TOGGLE, disabled=True
                    ),
                ),
                DisplayItem(
                    title="Disabled Icon Button",
                    content=Button(
                        content=FluentIcon(name=FluentIcons.ADD, size=15), disabled=True
                    ),
                ),
                DisplayItem(
                    title="Disabled Hyperlink Button",
                    content=Button(
                        content=ft.Text("Hyperlink"),
                        variant=ButtonVariant.HYPERLINK,
                        disabled=True,
                    ),
                ),
            ],
        )

    # Checkbox Page
    @window.route("/components/checkbox")
    def checkbox():
        return DisplayGroup(
            title="Checkbox",
            widgets=[
                DisplayItem(
                    title="Two-state Checkbox",
                    content=Checkbox(
                        label="Two-state Checkbox", on_change=lambda state: print(state)
                    ),
                ),
                DisplayItem(
                    title="Three-state Checkbox",
                    content=Checkbox(
                        label="Three-state Checkbox",
                        three_state=True,
                        on_change=lambda state: print(state),
                    ),
                ),
                DisplayItem(
                    title="Initially Checked Three-state Checkbox",
                    content=Checkbox(
                        label="Three-state (Initially Checked)",
                        state=CheckState.CHECKED,
                        three_state=True,
                    ),
                ),
                DisplayItem(
                    title="Initially Indeterminate Three-state Checkbox",
                    content=Checkbox(
                        label="Three-state (Initially Indeterminate)",
                        state=CheckState.INDETERMINATE,
                        three_state=True,
                    ),
                ),
                DisplayItem(
                    title="Disabled Checkbox",
                    content=Checkbox(label="Disabled", disabled=True),
                ),
                DisplayItem(
                    title="Disabled Checked Checkbox",
                    content=Checkbox(
                        label="Disabled Checked",
                        state=CheckState.CHECKED,
                        disabled=True,
                    ),
                ),
                DisplayItem(
                    title="Disabled Indeterminate Checkbox",
                    content=Checkbox(
                        label="Disabled Indeterminate",
                        state=CheckState.INDETERMINATE,
                        disabled=True,
                    ),
                ),
            ],
        )

    # Radio Page
    @window.route("/components/radio")
    def radio():
        return DisplayGroup(
            title="Radio",
            widgets=[
                DisplayItem(
                    title="Radio Group",
                    content=RadioGroup(
                        content=ft.Column(
                            [
                                Radio(value="radio1", label="Option 1"),
                                Radio(value="radio2", label="Option 2"),
                                Radio(value="radio3", label="Option 3", disabled=True),
                            ]
                        ),
                        # value="option1",
                        on_change=lambda value: print("Radio changed:", value),
                    ),
                ),
                DisplayItem(
                    title="Standard Radio Button",
                    content=Radio(value="option1", label="Option 1"),
                ),
                DisplayItem(
                    title="Disabled Radio Button",
                    content=Radio(
                        value="option4", label="Disabled Option", disabled=True
                    ),
                ),
            ],
        )

    # Toggle Page
    @window.route("/components/toggle")
    def toggle():
        return DisplayGroup(
            title="Toggle",
            widgets=[
                DisplayItem(
                    title="Standard Toggle", content=Toggle(label="Standard Toggle")
                ),
                DisplayItem(
                    title="Custom Label Toggle",
                    content=Toggle(label={"on_content": "ON", "off_content": "OFF"}),
                ),
                DisplayItem(
                    title="Initially On Toggle",
                    content=Toggle(label="Initially On", value=True),
                ),
                DisplayItem(
                    title="Disabled Toggle",
                    content=Toggle(label="Disabled Toggle", disabled=True),
                ),
            ],
        )

    textbox_test = TextBox(
        placeholder="TextBox", width=300, on_change=lambda e: print(e.control.value)
    )

    textbox_test.add_action(
        icon=FluentIcons.SEARCH,
        on_click=lambda e: print(f"Searching: {textbox_test.value}"),
        tooltip="Search",
    )
    textbox_test.add_action(
        icon=FluentIcons.DISMISS,
        on_click=lambda e: setattr(textbox_test, "value", ""),
        tooltip="Clear",
    )

    # TextBox Page
    @window.route("/components/textbox")
    def textbox():
        return DisplayGroup(
            title="TextBox",
            widgets=[
                DisplayItem(title="Standard TextBox", content=textbox_test),
                DisplayItem(
                    title="Password TextBox",
                    content=TextBox(
                        placeholder="Password TextBox", width=300, password=True
                    ),
                ),
                DisplayItem(
                    title="TextBox with prefix and suffix",
                    content=TextBox(
                        placeholder="Enter domain name",
                        prefix="https://",
                        suffix=".com",
                        width=300,
                    ),
                ),
            ],
        )

    # Dropdown Page
    @window.route("/components/dropdown")
    def dropdown():
        return DisplayGroup(
            title="Dropdown",
            widgets=[
                DisplayItem(
                    title="Standard Dropdown",
                    content=Dropdown(
                        options=["Option 1", "Option 2", "Option 3"],
                        initial_value="Option 1",
                    ),
                )
            ],
        )

    # Calendar Page
    @window.route("/components/calendar")
    def calendar():
        return DisplayGroup(
            title="Calendar",
            widgets=[
                DisplayItem(
                    title="Standard Calendar",
                    content=Calendar(
                        on_select=lambda date: print(
                            f"Selected: {date.strftime('%Y-%m-%d') if date else 'None'}"
                        )
                    ),
                ),
                DisplayItem(
                    title='Calendar with "blackout" dates',
                    content=Calendar(
                        blackout_dates=[datetime(2024, 12, 7), datetime(2024, 12, 9)],
                        on_select=lambda date: print(
                            f"Selected: {date.strftime('%Y-%m-%d') if date else 'None'}"
                        ),
                    ),
                ),
            ],
        )

    # ListItem Page
    @window.route("/components/listitem")
    def listitem():
        return DisplayGroup(
            title="List Item",
            widgets=[
                DisplayItem(
                    title="Basic ListItem",
                    content=ListItem(content=ft.Text("Standard List Item")),
                ),
                DisplayItem(
                    title="ListView",
                    content=ft.Column(
                        spacing=2,
                        controls=[
                            ListItem(content=ft.Text("Kendall Collins")),
                            ListItem(content=ft.Text("Henry Ross")),
                            ListItem(content=ft.Text("Nicole Wagner")),
                        ],
                    ),
                ),
            ],
        )

    # Expander Page
    @window.route("/components/expander")
    def expander():
        return DisplayGroup(
            title="Expander",
            widgets=[
                DisplayItem(
                    title="Basic Expander",
                    content=Expander(
                        header="Basic String Header",
                        content=ft.Column(
                            [
                                ft.Text("This is some content"),
                                Button(
                                    ft.Text("Click me"), variant=ButtonVariant.DEFAULT
                                ),
                            ]
                        ),
                    ),
                ),
                DisplayItem(
                    title="Expander with Icon Header",
                    content=Expander(
                        header=ft.Row(
                            [
                                FluentIcon(
                                    name=FluentIcons.EDIT_SETTINGS,
                                    style=FluentIconStyle.FILLED,
                                    size=15,
                                    color="#ffffff",
                                ),
                                ft.Text("Header with Icon"),
                            ]
                        ),
                        content=ft.Text("Content with fancy header"),
                    ),
                ),
                DisplayItem(
                    title="Expander with Interactive Header",
                    content=Expander(
                        header=ft.Row([Checkbox(), ft.Text("Header with Action")]),
                        content=ft.Text("Content with fancy header"),
                    ),
                ),
            ],
        )

    # treeview Page
    @window.route("/components/treeview")
    def treeview():
        return DisplayGroup(
            title="Treeview",
            widgets=[
                DisplayItem(
                    title="Tree View from dict",
                    content=TreeView(
                        data={
                            "Root": {
                                "Level_1": {
                                    "Item_1": 1.10,
                                    "Item_2": 1.20,
                                    "Item_3": 1.30,
                                },
                                "Level_2": {
                                    "SubLevel_1": {
                                        "SubLevel_1_item1": 2.11,
                                        "SubLevel_1_Item2": 2.12,
                                        "SubLevel_1_Item3": 2.13,
                                    },
                                    "SubLevel_2": {
                                        "SubLevel_2_Item1": 2.21,
                                        "SubLevel_2_Item2": 2.22,
                                        "SubLevel_2_Item3": 2.23,
                                    },
                                },
                                "Level_3": {
                                    "Item_1": 3.10,
                                    "Item_2": 3.20,
                                    "Item_3": 3.30,
                                },
                            }
                        },
                        model=DictTreeViewModel(),
                        is_dark_mode=True,
                    ),
                )
            ],
        )

    @window.route("/components/progress")
    def progress():
        def create_progress_view():
            progress_ring = ProgressRing(value=0.3)

            def update_progress(e):
                try:
                    value = float(e.control.value)
                    value = max(0, min(100, value))
                    progress_ring.value = value
                    progress_ring.update()
                except ValueError:
                    progress_ring.value = 0
                    progress_ring.update()

            # Create TextBox with progress control
            progress_control = TextBox(
                placeholder="Enter progress (0-100)",
                width=120,
                value=0.3,
                on_change=update_progress,
            )

            def increment_progress(e):
                current_value = progress_ring.value
                new_value = min(1, current_value + 0.1)  # Increment by 0.1, max at 1
                progress_control.value = f"{new_value:.1f}"  # Format to 1 decimal place
                progress_ring.value = new_value
                progress_ring.update()
                progress_control.update()

            def decrement_progress(e):
                current_value = progress_ring.value
                new_value = max(0, current_value - 0.1)  # Decrement by 0.1, min at 0
                progress_control.value = f"{new_value:.1f}"  # Format to 1 decimal place
                progress_ring.value = new_value
                progress_ring.update()
                progress_control.update()

            # Add increment action
            progress_control.add_action(
                icon=FluentIcons.CHEVRON_UP,
                on_click=increment_progress,
                tooltip="Increment by 10",
            )

            # Add decrement action
            progress_control.add_action(
                icon=FluentIcons.CHEVRON_DOWN,
                on_click=decrement_progress,
                tooltip="Decrement by 10",
            )

            return ft.Row([progress_ring, progress_control], spacing=20)

        return DisplayGroup(
            title="Progress Ring",
            widgets=[
                DisplayItem(
                    title="Indeterminate progress ring", content=ProgressRing()
                ),
                DisplayItem(
                    title="Determiante progress ring", content=create_progress_view()
                ),
            ],
        )

    @window.route("/components/dialog")
    def dialog():
        def show_dialog(e):
            dialog = Dialog()
            page.overlay.append(dialog)
            page.update()
            dialog.show()

        def show_custom_dialog(e):
            # Example of custom content and actions
            custom_content = ft.Column(
                [
                    ft.Text("This is a custom content example"),
                    TextBox(placeholder="Enter something"),
                    Checkbox(label="Check this box"),
                ]
            )

            custom_actions = [
                Button(
                    "Save",
                    variant=ButtonVariant.ACCENT,
                    expand=True,
                    on_click=lambda e: print("Save clicked"),
                ),
                Button(
                    "Don't Save", expand=True, on_click=lambda e: dialog.close_dialog()
                ),
                Button("Cancel", expand=True, on_click=lambda e: dialog.close_dialog()),
            ]

            dialog = Dialog(
                title="Custom Dialog", content=custom_content, actions=custom_actions
            )
            page.overlay.append(dialog)
            page.update()
            dialog.show()

        return DisplayGroup(
            title="Dialog",
            widgets=[
                DisplayItem(
                    title="Basic Dialog",
                    content=Button("Open Dialog", on_click=show_dialog),
                ),
                DisplayItem(
                    title="Custom Dialog",
                    content=Button("Open Dialog", on_click=show_custom_dialog),
                ),
            ],
        )

    @window.route("/icons")
    def create_icons_browser():
        # Use a dataclass for better performance and cleaner code
        from dataclasses import dataclass

        @dataclass
        class SelectedIcon:
            value: str = None
            name: str = None
            python_enum: str = None

        selected_icon = SelectedIcon()
        icon_availability_cache = {}

        # pre-calculate common styles
        TILE_PADDING = ft.padding.only(top=15, bottom=10, right=15, left=15)
        COMMON_BGCOLOR = ft.Colors.with_opacity(0.578, "#1e1e1e")
        DETAILS_BGCOLOR = ft.Colors.with_opacity(0.578, "#1a1a1a")

        def show_icon_details(icon: FluentIcons, style: FluentIconStyle):
            if not details_panel.visible:
                details_panel.visible = True

            # update selected icon data all at once
            selected_icon.value = icon.value
            selected_icon.name = icon.name
            selected_icon.python_enum = f"FluentIcons.{icon.name}"

            # batch updates for better performance
            updates = []
            icon_text = details_panel.content.controls[0]
            icon_previews = details_panel.content.controls[1]
            details = details_panel.content.controls[2]

            icon_text.value = icon.value

            # update previews using cached availability
            for preview, icon_style, label in [
                (icon_previews.controls[0], FluentIconStyle.REGULAR, "Regular"),
                (icon_previews.controls[1], FluentIconStyle.FILLED, "Filled"),
            ]:
                cache_key = (icon.value, icon_style)
                if cache_key not in icon_availability_cache:
                    try:
                        FluentIcon(icon, style=icon_style)
                        icon_availability_cache[cache_key] = True
                    except FileNotFoundError:
                        icon_availability_cache[cache_key] = False

                if icon_availability_cache[cache_key]:
                    preview.content = ft.Column(
                        [
                            FluentIcon(icon, style=icon_style, size=48),
                            ft.Text(label, size=12, color="#666666"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                else:
                    preview.content = ft.Text("Not available", size=12, color="#666666")

            details.controls[1].controls[0].value = icon.value
            details.controls[3].controls[0].value = icon.name
            details.controls[5].controls[0].value = selected_icon.python_enum

            details_panel.update()

        def select_icon(event, icon: FluentIcons, style: FluentIconStyle):
            [
                setattr(container, "border", None)
                for container in icon_grid.controls
                if container
            ]
            event.control.border = ft.border.all(2, "#62cdfe")

            icon_grid.update()
            show_icon_details(icon, style)

        def create_icon_tile(icon: FluentIcons, style: FluentIconStyle) -> ft.Container:
            cache_key = (icon.value, style)
            if cache_key not in icon_availability_cache:
                try:
                    FluentIcon(icon, style=style)
                    icon_availability_cache[cache_key] = True
                except FileNotFoundError:
                    icon_availability_cache[cache_key] = False
                    return None

            if not icon_availability_cache[cache_key]:
                return None

            return ft.Container(
                content=ft.Column(
                    [
                        FluentIcon(icon, style=style),
                        ft.Text(icon.value, size=12, text_align=ft.TextAlign.CENTER),
                    ],
                    spacing=5,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=TILE_PADDING,
                bgcolor=COMMON_BGCOLOR,
                border_radius=4,
                on_click=lambda e: select_icon(e, icon, style),
            )

        def filter_icons(e):
            search_term = e.control.value.lower()
            [
                setattr(
                    container,
                    "visible",
                    search_term in container.content.controls[1].value.lower(),
                )
                for container in icon_grid.controls
                if container
            ]
            icon_grid.update()

        search_box = TextBox(
            placeholder="Search icons", width=1000, on_change=filter_icons
        )

        icon_grid = ft.GridView(
            expand=True,
            max_extent=100,
            spacing=10,
            run_spacing=10,
        )

        # create panels with pre-calculated styles
        left_panel = ft.Column(
            [
                ft.Text("Icons", size=30, weight=ft.FontWeight.BOLD),
                search_box,
                icon_grid,
            ],
            expand=True,
        )

        details_panel = ft.Container(
            content=ft.Column(
                [
                    ft.Text("", size=24, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            ft.Container(
                                padding=20,
                                bgcolor=COMMON_BGCOLOR,
                                border_radius=4,
                                width=100,
                                height=100,
                            ),
                            ft.Container(
                                padding=20,
                                bgcolor=COMMON_BGCOLOR,
                                border_radius=4,
                                width=100,
                                height=100,
                            ),
                        ],
                        spacing=20,
                    ),
                    ft.Column(
                        [
                            ft.Text("Icon name", color="#666666"),
                            ft.Row(
                                [
                                    ft.Text("", size=16),
                                    Button(
                                        content=FluentIcon(
                                            name=FluentIcons.COPY,
                                            size=16,
                                            color="#ffffff",
                                        ),
                                        variant=ButtonVariant.DEFAULT,
                                        on_click=lambda _: page.set_clipboard(
                                            selected_icon.value
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text("Python enum name", color="#666666", size=14),
                            ft.Row(
                                [
                                    ft.Text("", size=16),
                                    Button(
                                        content=FluentIcon(
                                            name=FluentIcons.COPY,
                                            size=16,
                                            color="#ffffff",
                                        ),
                                        variant=ButtonVariant.DEFAULT,
                                        on_click=lambda _: page.set_clipboard(
                                            selected_icon.name
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            ft.Text("Python", color="#666666", size=14),
                            ft.Row(
                                [
                                    ft.Text("", size=16),
                                    Button(
                                        content=FluentIcon(
                                            name=FluentIcons.COPY,
                                            size=16,
                                            color="#ffffff",
                                        ),
                                        variant=ButtonVariant.DEFAULT,
                                        on_click=lambda _: page.set_clipboard(
                                            selected_icon.python_enum
                                        ),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ],
                        spacing=20,
                    ),
                ],
                spacing=30,
            ),
            width=400,
            bgcolor=DETAILS_BGCOLOR,
            padding=30,
            border_radius=4,
            visible=False,
        )

        icons = [
            create_icon_tile(icon, FluentIconStyle.REGULAR) for icon in FluentIcons
        ]
        icon_grid.controls = [icon for icon in icons if icon is not None]

        return ft.Row([left_panel, details_panel], expand=True)

    # Set initial route
    window.navigate("/home")


ft.app(target=main)
