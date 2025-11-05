import reflex as rx
from typing import TypedDict, Any


class ServiceCategory(TypedDict):
    id: str
    name: str
    icon: str
    enabled: bool


class Provider(TypedDict):
    id: int
    name: str
    category: str
    location: str
    rating: float
    reviews: int
    image_url: str
    featured: bool


class ProviderApplication(TypedDict):
    full_name: str
    business_name: str
    category: str
    phone_number: str
    whatsapp_number: str
    address: str
    city: str
    description: str
    plan: str


class UIState(rx.State):
    """The UI state for the app."""

    service_categories: list[ServiceCategory] = []
    providers: list[Provider] = []
    search_query: str = ""
    category_filter: str = "All"
    rating_filter: float = 0.0
    open_now_filter: bool = False
    new_review_text: str = ""
    new_review_rating: int = 0
    app_settings: dict[str, str | list[ServiceCategory]] = {}

    @rx.event
    async def load_initial_data(self):
        """Load initial data from the database for the main UI."""
        from app.states.admin_settings_state import AdminSettingsState
        from app.services.firebase_service import get_providers, get_app_settings

        admin_settings = await self.get_state(AdminSettingsState)
        await admin_settings.initialize_settings()
        db_settings = await get_app_settings()
        db_providers = await get_providers()
        self.app_settings = db_settings
        retrieved_categories = db_settings.get("service_categories", [])
        if isinstance(retrieved_categories, list):
            self.service_categories = retrieved_categories
        self.providers = db_providers

    @rx.var
    def featured_providers(self) -> list[Provider]:
        return [p for p in self.providers if p["featured"]]

    @rx.var
    def top_rated_providers(self) -> list[Provider]:
        return sorted(
            [p for p in self.providers if not p["featured"]],
            key=lambda x: x["rating"],
            reverse=True,
        )

    @rx.var
    def filtered_providers(self) -> list[Provider]:
        """Return a list of providers filtered by the search and filter options."""
        return [
            p
            for p in self.providers
            if (
                self.search_query.lower() in p["name"].lower()
                or self.search_query.lower() in p["location"].lower()
            )
            and (self.category_filter == "All" or p["category"] == self.category_filter)
            and (p["rating"] >= self.rating_filter)
        ]

    @rx.var
    def current_provider(self) -> Provider | None:
        """The currently viewed provider."""
        provider_id = self.router.page.params.get("id", "")
        if not provider_id:
            return None
        for p in self.providers:
            if str(p["id"]) == provider_id:
                return p
        return None