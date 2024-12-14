import flet as ft
from fluentflet.window import FluentWindow, FluentState
from fluentflet.utils import FluentIcons
from fluentflet.components import Button

"""
# you can create subclasses of FluentState and use the public methods: set and get
# example:
class AppState(FluentState):
    def _load_initial_state(self):
        visits = self._page.session.get("visits")
        if visits is None:
            visits = 0

        self._state = {
            "visits": visits,
            "theme": "light",
            "selected_user": None
        }
    
    def increment_visits(self):
        visits = self.get("visits", 0) 
        self.set("visits", visits + 1, persist=True)

    def get_visits(self):
        return self.get("visits", 0)
"""


def main(page: ft.Page):
    page.title = "fluentwindow routing"
    window = FluentWindow(
        page,
        navigation_items=[
            {"icon": FluentIcons.HOME, "label": "Home", "route": "/"},
            {"icon": FluentIcons.PEOPLE, "label": "Users", "route": "/users"},
        ],
    )

    users = {
        "1": {"name": "Alice Smith", "role": "Admin"},
        "2": {"name": "Bob Jones", "role": "User"},
        "3": {"name": "Carol Davis", "role": "Editor"},
    }

    @window.route("/")
    def home_view():
        visits = window.state.get("visits", 0)
        window.state.set("visits", visits + 1, persist=True)

        return ft.Column(
            controls=[
                ft.Text("Welcome!", size=32, weight=ft.FontWeight.BOLD),
                ft.Text(f"You've visited {visits} times", size=16),
                ft.Text("This is a demo of FluentWindow routing.", size=20),
                Button(
                    content=ft.Text("View Users"),
                    on_click=lambda _: window.navigate("/users"),
                ),
            ]
        )

    @window.route("/users")
    def users_list_view():
        def create_user_item(user_id, user_data):
            def handle_like():
                likes = window.state.get(f"user_likes_{user_id}", 0)
                window.state.set(f"user_likes_{user_id}", likes + 1, persist=True)
                like_text.value = f"Likes: {likes + 1}"
                like_text.update()

            like_text = ft.Text(
                f"Likes: {window.state.get(f'user_likes_{user_id}', 0)}"
            )

            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(user_data["name"], size=20),
                        ft.Text(f"Role: {user_data['role']}", size=16, color="grey"),
                        like_text,
                        ft.Row(
                            controls=[
                                Button(
                                    content=ft.Text("Like"),
                                    on_click=lambda _: handle_like(),
                                ),
                                Button(
                                    content=ft.Text("View Profile"),
                                    on_click=lambda _: window.navigate(
                                        f"/users/{user_id}"
                                    ),
                                ),
                            ]
                        ),
                    ]
                ),
                padding=10,
                bgcolor=ft.Colors.with_opacity(0.1, "white"),
                border_radius=8,
                margin=ft.margin.only(bottom=10),
            )

        return ft.Column(
            controls=[
                ft.Text("Users", size=32, weight=ft.FontWeight.BOLD),
                *[create_user_item(uid, data) for uid, data in users.items()],
            ]
        )

    @window.route("/users/:user_id", is_template=True)
    def user_profile_view(user_id=None):
        if not user_id or user_id not in users:
            return ft.Column(
                controls=[
                    ft.Text("User not found!", size=32, color="red"),
                    Button(
                        content=ft.Text("Back to Users"),
                        on_click=lambda _: window.navigate("/users"),
                    ),
                ]
            )

        user = users[user_id]
        likes = window.state.get(f"user_likes_{user_id}", 0)

        return ft.Column(
            controls=[
                ft.Text(f"Profile: {user['name']}", size=32, weight=ft.FontWeight.BOLD),
                ft.Text(f"Role: {user['role']}", size=20),
                ft.Text(f"Total Likes: {likes}", size=16),
                Button(
                    content=ft.Text("Back to Users"),
                    on_click=lambda _: window.navigate("/users"),
                ),
            ]
        )

    window.navigate("/")


ft.app(target=main)
