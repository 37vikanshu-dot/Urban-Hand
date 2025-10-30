import reflex as rx
from firebase_admin import auth
from typing import Any


class AdminState(rx.State):
    is_authenticated: bool = False
    email: str = ""
    password: str = ""
    error_message: str = ""
    current_page: str = "App Settings"

    @rx.var
    def is_admin_page(self) -> bool:
        return self.router.page.path.startswith("/admin") and (
            not self.router.page.path.endswith("/login")
        )

    @rx.event
    async def on_load_check_auth(self):
        if (
            self.router.page.path.startswith("/admin")
            and (not self.router.page.path.endswith("/login"))
            and (not self.is_authenticated)
        ):
            return rx.redirect("/admin/login")
        from app.states.admin_settings_state import AdminSettingsState

        settings_state = await self.get_state(AdminSettingsState)
        await settings_state.initialize_settings()
        if not self.current_page:
            self.current_page = "App Settings"

    @rx.event
    def handle_login_submit(self, form_data: dict[str, str]):
        self.email = form_data.get("email", "")
        self.password = form_data.get("password", "")
        return AdminState.login

    @rx.event
    def login(self):
        if self.email == "admin@urbanhand.com" and self.password == "admin123":
            self.is_authenticated = True
            self.error_message = ""
            return rx.redirect("/admin/dashboard")
        else:
            self.error_message = "Invalid email or password."
            self.is_authenticated = False

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.email = ""
        self.password = ""
        return rx.redirect("/admin/login")

    @rx.event
    def set_current_page(self, page_name: str):
        self.current_page = page_name