import reflex as rx
from typing import Any
from app.state import ServiceCategory
from app.services.firebase_service import get_app_settings, save_app_settings


class AdminSettingsState(rx.State):
    """State for managing app settings in the admin dashboard."""

    app_settings: dict[str, str | list[ServiceCategory]] = {}

    @rx.event
    async def initialize_settings(self):
        settings = await get_app_settings()
        if settings:
            self.app_settings = settings
        else:
            self.app_settings = {
                "app_name": "Urban Hand",
                "hero_title": "Connecting Local Hands to Local Needs.",
                "hero_subtitle": "Find trusted local service providers in your city, with just a few clicks.",
                "get_listed_text": "Get Listed",
                "accent_color": "#14b8a6",
                "service_categories": [
                    {"id": "1", "name": "Electrician", "icon": "zap", "enabled": True},
                    {"id": "2", "name": "Plumber", "icon": "droplet", "enabled": True},
                    {"id": "3", "name": "Tailor", "icon": "scissors", "enabled": True},
                    {"id": "4", "name": "Carpenter", "icon": "hammer", "enabled": True},
                    {
                        "id": "5",
                        "name": "Tiffin",
                        "icon": "utensils-crossed",
                        "enabled": True,
                    },
                    {"id": "6", "name": "Tutor", "icon": "book-user", "enabled": True},
                    {
                        "id": "7",
                        "name": "Photographer",
                        "icon": "camera",
                        "enabled": True,
                    },
                    {"id": "8", "name": "Others", "icon": "ellipsis", "enabled": True},
                ],
            }
            await save_app_settings(self.app_settings)
        await self.sync_ui_state()

    @rx.event
    def handle_setting_change(self, key: str, value: str | list[ServiceCategory]):
        """Update a setting in the local state."""
        self.app_settings[key] = value

    @rx.event
    async def save_settings(self):
        await save_app_settings(self.app_settings)
        await self.sync_ui_state()

    @rx.event
    async def sync_ui_state(self):
        from app.state import UIState
        from app.services.firebase_service import get_providers

        ui_state = await self.get_state(UIState)
        ui_state.app_settings = self.app_settings
        retrieved_categories = self.app_settings.get("service_categories", [])
        if isinstance(retrieved_categories, list):
            ui_state.service_categories = retrieved_categories
        db_providers = await get_providers()
        if db_providers:
            ui_state.providers = db_providers