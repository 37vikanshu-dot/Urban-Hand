import reflex as rx
import bcrypt
from typing import TypedDict, Any
from app.services.firebase_service import get_owner_by_email


class BusinessOwner(TypedDict):
    id: str
    provider_id: int
    email: str
    password_hash: str
    full_name: str


class BusinessOwnerAuthState(rx.State):
    logged_in_owner: BusinessOwner | None = None
    error_message: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return self.logged_in_owner is not None

    @rx.event
    async def handle_login(self, form_data: dict[str, Any]):
        email = form_data.get("email")
        password = form_data.get("password")
        if not email or not password:
            self.error_message = "Email and password are required."
            return
        owner = await get_owner_by_email(email)
        if owner and bcrypt.checkpw(password.encode(), owner["password_hash"].encode()):
            self.logged_in_owner = owner
            self.error_message = ""
            return rx.redirect("/owner/dashboard")
        else:
            self.error_message = "Invalid email or password."
            self.logged_in_owner = None

    @rx.event
    def logout(self):
        self.logged_in_owner = None
        return rx.redirect("/owner/login")

    @rx.event
    def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/owner/login")