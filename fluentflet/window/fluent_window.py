'''
You can also navigate programmatically from anywhere:
def handle_button_click(e):
    window.navigate("settings")

home_view = ft.Column(
    controls=[
        ft.Text("Home View", size=30, color="white"),
        ft.ElevatedButton("Go to Settings", on_click=handle_button_click),
    ],
)
Or create a more complex routing system:
def HomeView(ft.UserControl):
    def __init__(self, window: FluentWindow):
        super().__init__()
        self.window = window
    
    def build(self):
        return ft.Column(
            controls=[
                ft.Text("Home View", size=30, color="white"),
                ft.ElevatedButton(
                    "Go to Profile",
                    on_click=lambda _: self.window.navigate("profile")
                ),
            ],
        )

def main(page: ft.Page):
    window = FluentWindow(
        page,
        navigation_items=[
            {"icon": FluentIcons.HOME, "label": "Home"},
            {"icon": FluentIcons.PERSON, "label": "Profile"},
            {"icon": FluentIcons.SETTINGS, "label": "Settings"},
        ],
    )
    
    # Create views with access to the window
    window.add_route("home", HomeView(window))
    window.add_route("profile", ProfileView(window))
    window.add_route("settings", SettingsView(window))
    
    # Start at home
    window.navigate("home")

ft.app(target=main)
You could even add route parameters:
# Usage:
def user_profile(user_id: str = None):
    return ft.Column(
        controls=[
            ft.Text(f"Profile for user {user_id}", size=30, color="white"),
        ],
    )

window.add_route("user_profile", user_profile)
window.navigate("user_profile", user_id="123")
'''

import flet as ft
from pathlib import Path
from fluentflet.components import ListItem, Button, ButtonVariant, ToolTip
from fluentflet.utils import FluentIcon, FluentIcons
from typing import Optional, Any, Callable, Union, Dict

class NavigationDivider(ft.Container):
    def __init__(self):
        super().__init__(
            height=.5,
            margin=ft.margin.symmetric(vertical=8),
            bgcolor="#393939",
            width=180
        )

class Titlebar(ft.Container):
    def __init__(
        self,
        content: ft.Control | None = None,
        title: str = "fluent flet",
        icon: str | ft.Control | None = None,
        title_style: dict | None = None,
        show_window_controls: bool = True,
        window_controls_style: dict | None = None,
        layout: dict | None = None,
        on_minimize: Callable | None = None,
        on_maximize: Callable | None = None,
        on_close: Callable | None = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        # Store configuration
        self.custom_content = content
        self.show_window_controls = show_window_controls
        
        # Default title configuration
        self.title_config = {
            "text": title,
            "size": 14,
            "weight": ft.FontWeight.NORMAL,
            "color": "white",
            "font_family": None,
            "text_align": ft.TextAlign.LEFT,
            **(title_style or {})
        }
        
        # Default icon configuration
        self.icon = (
            icon if isinstance(icon, ft.Control)
            else ft.Image(src=icon, width=15, height=15) if icon
            else ft.Image("fluentflet/static/fluentflet.png", width=15, height=15)
        )
        
        # Default window controls configuration
        self.window_controls_config = {
            "icon_size": 16,
            "icon_color": "#ffffff",
            "button_variant": ButtonVariant.HYPERLINK,
            "hover_color": "#c42b1c",
            "icons": {
                "minimize": ft.icons.REMOVE,
                "maximize": ft.icons.CROP_SQUARE,
                "close": ft.icons.CLOSE
            },
            **(window_controls_style or {})
        }
        
        # Default layout configuration
        self.layout_config = {
            "alignment": ft.MainAxisAlignment.SPACE_BETWEEN,
            "spacing": 0,
            "expand": True,
            "title_spacing": 10,
            **(layout or {})
        }
        
        # Event handlers
        self.on_minimize = on_minimize or self.minimize_window
        self.on_maximize = on_maximize or self.toggle_maximize_window
        self.on_close = on_close or self.close_window
        
        # Set default container properties
        self.height = kwargs.get('height', 50)
        self.padding = kwargs.get('padding', ft.padding.only(left=20, right=8))
        self.bgcolor = kwargs.get('bgcolor', "transparent")
        
        # Initialize the titlebar content
        self.content = self.build_titlebar()
    
    def build_title_section(self) -> ft.Control:
        """Build the title section with icon and text"""
        return ft.Row(
            controls=[
                self.icon,
                ft.Text(
                    self.title_config["text"],
                    size=self.title_config["size"],
                    weight=self.title_config["weight"],
                    color=self.title_config["color"],
                    font_family=self.title_config["font_family"],
                    text_align=self.title_config["text_align"]
                )
            ],
            spacing=self.layout_config["title_spacing"]
        )
    
    def build_window_controls(self) -> ft.Control:
        """Build the window control buttons"""
        cfg = self.window_controls_config
        return ft.Row(
            controls=[
                Button(
                    content=ft.Icon(cfg["icons"]["minimize"], 
                                  color=cfg["icon_color"], 
                                  size=cfg["icon_size"]),
                    variant=cfg["button_variant"],
                    on_click=lambda _: self.on_minimize(),
                ),
                Button(
                    content=ft.Icon(cfg["icons"]["maximize"], 
                                  color=cfg["icon_color"], 
                                  size=cfg["icon_size"]),
                    variant=cfg["button_variant"],
                    on_click=lambda _: self.on_maximize(),
                ),
                Button(
                    content=ft.Icon(cfg["icons"]["close"], 
                                  color=cfg["icon_color"], 
                                  size=cfg["icon_size"]),
                    variant=cfg["button_variant"],
                    on_click=lambda _: self.on_close(),
                    on_hover=self.handle_close_hover,
                )
            ],
            spacing=0,
        )
    
    def build_titlebar(self) -> ft.Control:
        """Build the complete titlebar layout"""
        controls = []
        
        # Add title section if no custom content
        if not self.custom_content:
            controls.append(self.build_title_section())
        else:
            controls.append(self.custom_content)
        
        # Add window controls if enabled
        if self.show_window_controls:
            if self.layout_config["expand"]:
                controls.append(ft.Container(expand=True))
            controls.append(self.build_window_controls())
        
        return ft.Row(
            controls=controls,
            alignment=self.layout_config["alignment"],
            spacing=self.layout_config["spacing"]
        )
    
    def update_title(self, new_title: str):
        """Update the title text"""
        self.title_config["text"] = new_title
        if not self.custom_content:
            self.content = self.build_titlebar()
            if self.page:
                self.update()
    
    def update_content(self, new_content: ft.Control):
        """Update the custom content"""
        self.custom_content = new_content
        self.content = self.build_titlebar()
        if self.page:
            self.update()
    
    def handle_close_hover(self, e):
        """Handle hover effect on close button"""
        container = e.control
        container.bgcolor = (self.window_controls_config["hover_color"] 
                           if e.data == "true" else None)
        container.update()
    
    def minimize_window(self):
        """Default minimize handler"""
        self.page.window.minimized = True
    
    def toggle_maximize_window(self):
        """Default maximize handler"""
        self.page.window.maximized = not self.page.window.maximized
    
    def close_window(self):
        """Default close handler"""
        self.page.window.close()

class FluentState:
   def __init__(self):
       self._page = None
       self._subscribers = {}
       self._state = {}

   def _init_page(self, page: ft.Page):
       self._page = page
       self._load_initial_state()

   def _load_initial_state(self):
       for key in self._page.session.get_keys():
           self._state[key] = self._page.session.get(key)

   def set(self, key: str, value: any, persist: bool = False):
       self._state[key] = value
       if persist:
           self._page.session.set(key, value)
       if key in self._subscribers:
           for callback in self._subscribers[key]:
               callback(value)

   def get(self, key: str, default=None):
       return self._state.get(key, default)
           
   def subscribe(self, key: str, callback: callable):
       if key not in self._subscribers:
           self._subscribers[key] = []
       self._subscribers[key].append(callback)
       if key in self._state:
           callback(self._state[key])

class FluentWindow:
    def __init__(
        self,
        page: ft.Page,
        navigation_items=None,
        bottom_navigation_items=None,
        selected_index=0,
        window_titlebar: Union[str, Titlebar] = "Fluent Flet",
        colors=None,
        nav_width_collapsed=50,
        nav_width_expanded=200,
        animation_duration=100,
        show_back_button=True,
        nav_item_spacing=2,
        state_manager: FluentState = FluentState
    ):
        self._page = page
        self._page.window.title_bar_hidden = True
        self._page.window.title_bar_buttons_hidden = True
        self._page.fonts = {
            "Segoe UI": str(Path("fluentflet/static/fonts/Segoe UI/Segoe UI.ttf")),
            "Segoe UI Bold": str(Path("fluentflet/static/fonts/Segoe UI/Segoe UI Bold.ttf")),
            "Segoe UI Italic": str(Path("fluentflet/static/fonts/Segoe UI/Segoe UI Italic.ttf")),
            "Segoe UI Bold Italic": str(Path("fluentflet/static/fonts/Segoe UI/Segoe UI Bold Italic.ttf"))
        }
        self._page.theme = ft.Theme(scrollbar_theme=ft.ScrollbarTheme(thickness=0.0), font_family="Segoe UI")
        self._page.accepts_drops = True
        self._page.blur_effect = True
        self._page.padding = 0
        
        self.nav_item_spacing = nav_item_spacing
        
        self.colors = {
            "nav_bg": "#1F1F1F",
            "content_bg": "#282828",
            "title_bar_bg": "#1F1F1F",
            "icon_color": "white",
            "text_color": "white",
            "hover_color": "#c42b1c"
        }
        if colors:
            self.colors.update(colors)
        if self._page.blur_effect:
            self.colors["content_bg"] = ft.colors.with_opacity(0.3, self.colors["content_bg"])
            self.colors["nav_bg"] = ft.colors.with_opacity(0.3, self.colors["nav_bg"])
        
        self._page.bgcolor = self.colors["nav_bg"]
        
        # Initialize main layout components
        self.navigation_items = navigation_items or [{"icon": FluentIcons.HOME, "label": "Home"}]
        self.bottom_navigation_items = bottom_navigation_items or [{"icon": FluentIcons.SETTINGS, "label": "Settings"},]
        
        # Handle window_title based on type
        self.titlebar = (window_titlebar if isinstance(window_titlebar, Titlebar) 
                        else Titlebar(title=str(window_titlebar)))
        
        # Create the main layout
        self.create_layout(
            nav_width_collapsed=nav_width_collapsed,
            nav_width_expanded=nav_width_expanded,
            animation_duration=animation_duration,
            show_back_button=show_back_button,
            selected_index=selected_index
        )
        
        # Set up window event handling
        self._page.window.on_event = self._handle_window_event

        self.routes = {}
        self.current_route = None
        self.route_to_nav_index = {}
        self.template_routes = {}

        if navigation_items:
            for idx, item in enumerate(navigation_items):
                if "label" in item:
                    route = item.get("route", "/" + item["label"].lower().replace(" ", "-"))
                    self.route_to_nav_index[route] = idx

        self._page.on_route_change = self._handle_route_change

        self.state = state_manager()
        self.state._init_page(page)

    def route(self, path: str, is_template: bool = False):
        """Decorator for registering routes
        
        Args:
            path: Route path (e.g., "/users" or "/users/:id")
            is_template: Whether this is a template route with parameters
        """
        def decorator(view_func):
            self.add_route(path, view_func, is_template)
            return view_func
        return decorator

    def add_route(self, route: str, view_builder: Callable[..., ft.Control], is_template: bool = False):
        """
        Add a route with a view builder that can accept parameters.
        
        Args:
            route: The route pattern (e.g., "/user" or "/user/:id" for templates)
            view_builder: Function that returns a Control, can accept route parameters
            is_template: Whether this is a template route with parameters
        """
        if is_template:
            self.template_routes[route] = view_builder
        else:
            self.routes[route] = view_builder

    def navigate(self, route: str, **params):
        """
        Navigate to a route with optional parameters.
        Updates browser history 
        and triggers route change handling.
        Args:
            route: The route to navigate to
            **params: Optional route parameters
        """
        # Construct full route with parameters if needed
        full_route = route
        if params:
            # Replace template parameters in route
            for key, value in params.items():
                full_route = full_route.replace(f":{key}", str(value))
        
        # Update page route (this will trigger route change handler)
        self._page.route = full_route
        self._page.update()

    def add_navigation_divider(self, after_index: int):
        """Add a divider after the specified navigation item index"""
        if 0 <= after_index < len(self.nav_items):
            divider = NavigationDivider()
            self.nav_items.insert(after_index + 1, divider)
            self._nav_item_intern.insert(after_index + 1, divider)

    def create_nav_item(self, item: Dict, index: int) -> ft.Control:
        """Create either a navigation item or a divider based on the item type"""
        if item.get("type") == "divider":
            return NavigationDivider()
        else:
            _item = self.create_nav_row(item["icon"], item["label"])
            list_item = ListItem(
                content=_item,
                on_click=lambda e, i=index: self.handle_nav_click(i),
                is_dark_mode=True,
            )
            self._nav_item_intern.append(_item)
            return list_item

    def create_layout(self, nav_width_collapsed, nav_width_expanded, 
                    animation_duration, show_back_button, selected_index):
        """Create the main layout"""
        # Create navigation items
        self.nav_items = []
        self._nav_item_intern = []
        
        # Track the actual index (excluding dividers) for navigation
        self.nav_index_map = {}
        actual_index = 0
        
        # Create top navigation items
        for idx, item in enumerate(self.navigation_items):
            nav_item = self.create_nav_item(item, actual_index)
            self.nav_items.append(nav_item)
            
            if item.get("type") != "divider":
                self.nav_index_map[actual_index] = idx
                actual_index += 1

        # Create navigation rail with scrollable list
        nav_top_controls = []
        if show_back_button:
            nav_top_controls.extend([
                ft.Container(
                    content=Button(
                        content=FluentIcon(
                            FluentIcons.ARROW_LEFT,
                            size=18,
                            color=self.colors["icon_color"],
                        ),
                        variant=ButtonVariant.HYPERLINK,
                        # on_click=self.go_back,
                        disabled=False
                    ),
                    margin=ft.margin.only(top=10)
                ),
                ft.Container(height=20),
            ])
        
        nav_top_controls.append(
            ft.Container(
                content=Button(
                    content=FluentIcon(
                        FluentIcons.TEXT_ALIGN_JUSTIFY,
                        size=18,
                        color=self.colors["icon_color"]
                    ),
                    on_click=lambda e: self.toggle_navigation_panel(e),
                    variant=ButtonVariant.HYPERLINK,
                    is_dark_mode=True,
                ),
                margin=ft.margin.only(top=10 if not show_back_button else 0, bottom=10)
            )
        )
        
        # Create bottom navigation items
        bottom_nav_items = []
        for idx, item in enumerate(self.bottom_navigation_items):
            nav_item = self.create_nav_item(item, actual_index + idx)
            bottom_nav_items.append(nav_item)

        # Create the navigation rail with top, scrollable middle, and bottom sections
        self.nav_rail = ft.Container(
            content=ft.Column(
                controls=[
                    # Top section with back button and menu toggle
                    ft.Container(
                        ft.Column(
                            controls=nav_top_controls,
                            spacing=self.nav_item_spacing,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                        margin=ft.margin.only(left=5)
                    ),
                    # Middle section with scrollable navigation
                    ft.Container(
                        content=ft.Column(
                            controls=self.nav_items,
                            spacing=self.nav_item_spacing,
                            scroll=ft.ScrollMode.HIDDEN,  # Enable scrolling
                        ),
                        expand=True,
                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,  # Clip overflow content
                    ),
                    # Bottom section
                    ft.Column(
                        controls=bottom_nav_items,
                        spacing=self.nav_item_spacing,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ) if bottom_nav_items else None
                ],
                spacing=0,
                expand=True
            ),
            width=nav_width_collapsed,
            padding=ft.padding.only(left=5, right=5, bottom=10),
            bgcolor=self.colors["nav_bg"],
            animate=ft.animation.Animation(animation_duration, "easeOut"),
        )

        # Create content area
        self.content_container = ft.Container(
            expand=True,
            bgcolor=self.colors["content_bg"],
            border_radius=ft.border_radius.only(top_left=10),
            content=ft.Column(
                controls=[],
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            padding=10,
        )

        # Set initial selection
        self.selected_index = selected_index
        self.is_nav_expanded = False
        self.nav_width_collapsed = nav_width_collapsed
        self.nav_width_expanded = nav_width_expanded

        # Create main layout
        self.main_layout = ft.Row(
            controls=[
                self.nav_rail,
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        controls=[
                            ft.WindowDragArea(self.titlebar),
                            self.content_container,
                        ],
                        spacing=0,
                        expand=True,
                    ),
                ),
            ],
            expand=True,
            spacing=0,
        )

        # Add to page
        self._page.add(self.main_layout)
        self.select_nav_item(selected_index)

    def create_nav_row(self, icon, label):
        return ft.Row(
            controls=[
                FluentIcon(
                    icon,
                    size=18,
                    color=self.colors["icon_color"]
                ),
                ft.Text(
                    label,
                    color=self.colors["text_color"],
                    size=14,
                    opacity=0,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=12,
        )

    def toggle_navigation_panel(self, e=None):
        self.is_nav_expanded = not self.is_nav_expanded
        
        if self.is_nav_expanded:
            self.nav_rail.width = self.nav_width_expanded
            self.nav_rail.content.horizontal_alignment = ft.CrossAxisAlignment.START
            
            for item in self._nav_item_intern:
                if isinstance(item, ft.Row):  # Skip dividers
                    item.controls[1].opacity = 1
                    item.alignment = ft.MainAxisAlignment.START
                    item.update()
        else:
            self.nav_rail.width = self.nav_width_collapsed
            self.nav_rail.content.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            
            for item in self._nav_item_intern:
                if isinstance(item, ft.Row):  # Skip dividers
                    item.controls[1].opacity = 0
                    item.alignment = ft.MainAxisAlignment.CENTER
                    item.update()
        
        self.nav_rail.update()

    def select_nav_item(self, index: int):
        """Select a navigation item, accounting for dividers"""
        # Clear all selections
        for item in self.nav_items:
            if isinstance(item, ListItem):
                item.selected = False  # Using the new selected property
        
        # Find the actual item to select
        actual_idx = self.nav_index_map.get(index)
        if actual_idx is not None:
            item = self.nav_items[actual_idx]
            if isinstance(item, ListItem):
                item.selected = True  # Using the new selected property
                self.selected_index = index

    def handle_nav_click(self, index: int):
        """Handle navigation item click and route change"""
        self.select_nav_item(index)
        
        # Get the actual route from the navigation item
        actual_idx = self.nav_index_map.get(index)
        if actual_idx is not None:
            nav_item = self.navigation_items[actual_idx]
            if "route" in nav_item:  # Use the route defined in the nav item
                self.navigate(nav_item["route"])
            else:  # Fallback to the old behavior
                route = nav_item["label"].lower()
                self.navigate(route)
        
        # Update navigation items' visual state
        for item in self.nav_items:
            if isinstance(item, ListItem):
                item.update()

    def _handle_route_change(self, e):
        """Handle route changes from both navigation and browser history"""
        route = e.route
        
        # First try exact routes
        if route in self.routes:
            view = self.routes[route]()
        else:
            # Try template routes
            matched_builder = None
            matched_params = {}
            
            for template, builder in self.template_routes.items():
                # Simple template matching (can be enhanced with regex)
                template_parts = template.split('/')
                route_parts = route.split('/')
                
                if len(template_parts) == len(route_parts):
                    params = {}
                    matches = True
                    
                    for t_part, r_part in zip(template_parts, route_parts):
                        if t_part.startswith(':'):
                            params[t_part[1:]] = r_part
                        elif t_part != r_part:
                            matches = False
                            break
                    
                    if matches:
                        matched_builder = builder
                        matched_params = params
                        break
            
            if matched_builder:
                view = matched_builder(**matched_params)
            else:
                # Default to home route if no match
                view = self.routes.get('/', lambda: ft.Text("404 - Not Found"))()
        
        # Update the view
        self.content_container.content.controls = [view]
        self.content_container.update()
        self.current_route = route
        
        # Update navigation selection if route exists in navigation items
        if route in self.route_to_nav_index:
            idx = self.route_to_nav_index[route]
            for nav_idx, actual_idx in self.nav_index_map.items():
                if actual_idx == idx:
                    self.select_nav_item(nav_idx)
                    break

    def go(self, route: str, **params):
        """Convenience method to navigate to a route"""
        self.navigate(route, **params)

    def add(self, *controls):
        """Override add to use our content container"""
        self.content_container.content.controls = list(controls)
        for control in controls:
            if hasattr(control, 'expand') and not isinstance(control, (ft.Text, ft.Icon)):
                control.expand = True
            if hasattr(control, 'width'):
                control.width = None
        self.content_container.update()

    def _handle_window_event(self, e):
        if e.data == "close":
            self._page.window.destroy()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._page, name)