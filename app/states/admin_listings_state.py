import reflex as rx
from typing import Any
from app.state import Provider, UIState, ServiceCategory
from app.states.admin_categories_state import AdminCategoriesState
from app.services.firebase_service import get_providers, save_providers
import uuid


class AdminListingsState(rx.State):
    """State for managing business listings in the admin dashboard."""

    all_listings: list[Provider] = []
    search_query: str = ""
    category_filter: str = "All"
    status_filter: str = "All"
    plan_filter: str = "All"
    show_listing_modal: bool = False
    modal_is_editing: bool = False
    modal_listing_id: str = ""
    modal_business_name: str = ""
    modal_category: str = ""
    modal_full_name: str = ""
    modal_phone: str = ""
    modal_whatsapp: str = ""
    modal_address: str = ""
    modal_city: str = ""
    modal_description: str = ""
    modal_status: str = "Pending"
    modal_plan: str = "basic"
    modal_featured: bool = False
    modal_image_url: str = ""
    show_delete_confirm: bool = False
    listing_to_delete_id: str = ""

    @rx.event
    async def load_listings(self):
        self.all_listings = await get_providers()
        yield AdminListingsState.sync_ui_state_providers

    @rx.event
    def open_add_modal(self):
        self.modal_is_editing = False
        self.modal_listing_id = str(uuid.uuid4())
        self.modal_business_name = ""
        self.modal_category = ""
        self.modal_full_name = ""
        self.modal_phone = ""
        self.modal_whatsapp = ""
        self.modal_address = ""
        self.modal_city = ""
        self.modal_description = ""
        self.modal_status = "Pending"
        self.modal_plan = "basic"
        self.modal_featured = False
        self.modal_image_url = ""
        self.show_listing_modal = True

    @rx.event
    def open_edit_modal(self, listing: Provider):
        self.modal_is_editing = True
        self.modal_listing_id = str(listing["id"])
        self.modal_business_name = listing["name"]
        self.modal_category = listing["category"]
        self.modal_full_name = "Unknown User"
        self.modal_phone = "1234567890"
        self.modal_whatsapp = "1234567890"
        self.modal_address = listing["location"]
        self.modal_city = "Unknown City"
        self.modal_description = "A brief description of the service."
        self.modal_status = "Approved"
        self.modal_plan = "basic"
        self.modal_featured = listing["featured"]
        self.modal_image_url = listing["image_url"]
        self.show_listing_modal = True

    @rx.event
    def close_listing_modal(self):
        self.show_listing_modal = False

    @rx.event
    async def save_listing(self):
        listing_data = {
            "id": int(self.modal_listing_id)
            if self.modal_is_editing
            else len(self.all_listings) + 2,
            "name": self.modal_business_name,
            "category": self.modal_category,
            "location": self.modal_address,
            "rating": 0.0,
            "reviews": 0,
            "image_url": self.modal_image_url
            or f"https://api.dicebear.com/9.x/notionists/svg?seed={self.modal_business_name.replace(' ', '')}&backgroundColor=c0aede,b6e3f4,d1d4f9",
            "featured": self.modal_featured,
        }
        if self.modal_is_editing:
            index_to_update = -1
            for i, p in enumerate(self.all_listings):
                if str(p["id"]) == self.modal_listing_id:
                    index_to_update = i
                    break
            if index_to_update != -1:
                self.all_listings[index_to_update] = listing_data
        else:
            self.all_listings.append(listing_data)
        await save_providers(self.all_listings)
        self.close_listing_modal()
        yield AdminListingsState.sync_ui_state_providers

    @rx.event
    def open_delete_confirm(self, listing_id: str):
        self.listing_to_delete_id = listing_id
        self.show_delete_confirm = True

    @rx.event
    def cancel_delete(self):
        self.show_delete_confirm = False

    @rx.event
    async def delete_listing(self):
        self.all_listings = [
            p for p in self.all_listings if str(p["id"]) != self.listing_to_delete_id
        ]
        await save_providers(self.all_listings)
        self.cancel_delete()
        yield AdminListingsState.sync_ui_state_providers

    @rx.var
    def filtered_listings(self) -> list[Provider]:
        query = self.search_query.lower()
        return [
            p
            for p in self.all_listings
            if (query in p["name"].lower() or query in p["location"].lower())
            and (self.category_filter == "All" or p["category"] == self.category_filter)
        ]

    @rx.event
    async def sync_ui_state_providers(self):
        ui_state = await self.get_state(UIState)
        ui_state.providers = self.all_listings