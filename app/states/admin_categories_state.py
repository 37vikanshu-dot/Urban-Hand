import reflex as rx
from typing import Any, cast
from app.state import ServiceCategory
from app.states.admin_settings_state import AdminSettingsState
import uuid


class AdminCategoriesState(rx.State):
    """State for managing service categories in the admin dashboard."""

    service_categories: list[ServiceCategory] = []
    show_category_modal: bool = False
    modal_is_editing: bool = False
    modal_category_id: str = ""
    modal_category_name: str = ""
    modal_category_icon: str = ""
    modal_category_enabled: bool = True
    lucide_icons: list[str] = [
        "zap",
        "droplet",
        "scissors",
        "hammer",
        "utensils-crossed",
        "book-user",
        "camera",
        "wrench",
        "paint-roller",
        "car",
        "home",
        "briefcase",
        "heart-pulse",
        "graduation-cap",
        "music",
        "package",
        "shopping-bag",
        "ellipsis",
    ]
    show_delete_confirm: bool = False
    category_to_delete_id: str = ""

    @rx.event
    async def load_categories(self):
        """Load categories from AdminSettingsState."""
        admin_settings = await self.get_state(AdminSettingsState)
        self.service_categories = admin_settings.app_settings.get(
            "service_categories", []
        )

    @rx.event
    async def save_categories(self):
        """Save the current list of categories to AdminSettingsState."""
        from app.state import UIState

        admin_settings = await self.get_state(AdminSettingsState)
        admin_settings.app_settings["service_categories"] = self.service_categories
        yield UIState.on_load

    @rx.event
    def open_add_modal(self):
        self.modal_is_editing = False
        self.modal_category_id = ""
        self.modal_category_name = ""
        self.modal_category_icon = "zap"
        self.modal_category_enabled = True
        self.show_category_modal = True

    @rx.event
    def open_edit_modal(self, category: ServiceCategory):
        self.modal_is_editing = True
        self.modal_category_id = category.get("id", "")
        self.modal_category_name = category["name"]
        self.modal_category_icon = category["icon"]
        self.modal_category_enabled = category.get("enabled", True)
        self.show_category_modal = True

    @rx.event
    def close_category_modal(self):
        self.show_category_modal = False

    @rx.event
    def save_category(self):
        if self.modal_is_editing:
            index_to_update = -1
            for i, cat in enumerate(self.service_categories):
                if cat.get("id") == self.modal_category_id:
                    index_to_update = i
                    break
            if index_to_update != -1:
                self.service_categories[index_to_update] = {
                    "id": self.modal_category_id,
                    "name": self.modal_category_name,
                    "icon": self.modal_category_icon,
                    "enabled": self.modal_category_enabled,
                }
        else:
            new_category: ServiceCategory = {
                "id": str(uuid.uuid4()),
                "name": self.modal_category_name,
                "icon": self.modal_category_icon,
                "enabled": self.modal_category_enabled,
            }
            self.service_categories.append(new_category)
        self.close_category_modal()
        return AdminCategoriesState.save_categories

    @rx.event
    def confirm_delete_category(self):
        self.service_categories = [
            cat
            for cat in self.service_categories
            if cat.get("id") != self.category_to_delete_id
        ]
        self.show_delete_confirm = False
        self.category_to_delete_id = ""
        return AdminCategoriesState.save_categories

    @rx.event
    def open_delete_confirm(self, category_id: str):
        self.category_to_delete_id = category_id
        self.show_delete_confirm = True

    @rx.event
    def cancel_delete(self):
        self.show_delete_confirm = False

    @rx.event
    def move_category(self, from_index: int, to_index: int):
        if 0 <= from_index < len(self.service_categories) and 0 <= to_index < len(
            self.service_categories
        ):
            item = self.service_categories.pop(from_index)
            self.service_categories.insert(to_index, item)
            return AdminCategoriesState.save_categories

    @rx.event
    def toggle_enabled(self, category_id: str, enabled: bool):
        for cat in self.service_categories:
            if cat.get("id") == category_id:
                cat["enabled"] = enabled
                break
        return AdminCategoriesState.save_categories

    @rx.event
    def set_modal_icon(self, icon: str):
        self.modal_category_icon = icon