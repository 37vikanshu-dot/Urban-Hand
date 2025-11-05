import reflex as rx
import bcrypt
import uuid
from typing import TypedDict, Any
from app.services.firebase_service import (
    get_business_owners,
    save_business_owners,
    get_providers,
    update_owner_password,
)


class BusinessOwner(TypedDict):
    id: str
    provider_id: int
    email: str
    password_hash: str
    full_name: str


class AdminBusinessOwnersState(rx.State):
    owners: list[BusinessOwner] = []
    providers: list[dict] = []
    provider_map: dict[int, str] = {}
    show_add_modal: bool = False
    show_reset_password_modal: bool = False
    selected_owner: BusinessOwner | None = None
    new_password: str = ""
    error_message: str = ""

    @rx.event
    async def load_data(self):
        self.owners = await get_business_owners()
        self.providers = await get_providers()
        self.provider_map = {p["id"]: p["name"] for p in self.providers}

    @rx.var
    def unlinked_providers(self) -> list[dict]:
        linked_provider_ids = {owner["provider_id"] for owner in self.owners}
        return [p for p in self.providers if p["id"] not in linked_provider_ids]

    @rx.event
    def open_add_modal(self):
        self.show_add_modal = True
        self.error_message = ""

    @rx.event
    def open_reset_password_modal(self, owner: BusinessOwner):
        self.selected_owner = owner
        self.new_password = ""
        self.show_reset_password_modal = True

    @rx.event
    async def create_owner_account(self, form_data: dict[str, str]):
        if not all(
            [
                form_data.get(k)
                for k in ["full_name", "email", "password", "provider_id"]
            ]
        ):
            self.error_message = "All fields are required."
            return
        hashed_password = bcrypt.hashpw(
            form_data["password"].encode(), bcrypt.gensalt()
        ).decode()
        new_owner = {
            "id": str(uuid.uuid4()),
            "full_name": form_data["full_name"],
            "email": form_data["email"],
            "password_hash": hashed_password,
            "provider_id": int(form_data["provider_id"]),
        }
        self.owners.append(new_owner)
        await save_business_owners(self.owners)
        self.show_add_modal = False

    @rx.event
    async def reset_password(self):
        if self.selected_owner and self.new_password:
            hashed_password = bcrypt.hashpw(
                self.new_password.encode(), bcrypt.gensalt()
            ).decode()
            await update_owner_password(self.selected_owner["id"], hashed_password)
            self.show_reset_password_modal = False

    @rx.event
    async def delete_owner(self, owner_id: str):
        self.owners = [o for o in self.owners if o["id"] != owner_id]
        await save_business_owners(self.owners)

    @rx.var
    def provider_name_map(self) -> dict[int, str]:
        return {p["id"]: p["name"] for p in self.providers}