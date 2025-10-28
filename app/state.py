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
    providers: list[Provider] = [
        {
            "id": 1,
            "name": "Ramesh Electricals",
            "category": "Electrician",
            "location": "A-Block, Malviya Nagar",
            "rating": 4.8,
            "reviews": 120,
            "image_url": "https://api.dicebear.com/9.x/notionists/svg?seed=ramesh&backgroundColor=c0aede,b6e3f4,d1d4f9",
            "featured": True,
        },
        {
            "id": 2,
            "name": "Sita's Kitchen",
            "category": "Tiffin",
            "location": "Sector 15, Pratapgarh",
            "rating": 4.9,
            "reviews": 250,
            "image_url": "https://api.dicebear.com/9.x/notionists/svg?seed=sita&backgroundColor=c0aede,b6e3f4,d1d4f9",
            "featured": True,
        },
        {
            "id": 3,
            "name": "Modern Tailors",
            "category": "Tailor",
            "location": "Gandhi Chowk",
            "rating": 4.7,
            "reviews": 88,
            "image_url": "https://api.dicebear.com/9.x/notionists/svg?seed=modern&backgroundColor=c0aede,b6e3f4,d1d4f9",
            "featured": False,
        },
        {
            "id": 4,
            "name": "Prakash Plumbers",
            "category": "Plumber",
            "location": "Near Bus Stand",
            "rating": 4.6,
            "reviews": 95,
            "image_url": "https://api.dicebear.com/9.x/notionists/svg?seed=prakash&backgroundColor=c0aede,b6e3f4,d1d4f9",
            "featured": True,
        },
        {
            "id": 5,
            "name": "Anil Photography",
            "category": "Photographer",
            "location": "Civil Lines",
            "rating": 4.9,
            "reviews": 150,
            "image_url": "https://api.dicebear.com/9.x/notionists/svg?seed=anil&backgroundColor=c0aede,b6e3f4,d1d4f9",
            "featured": False,
        },
        {
            "id": 6,
            "name": "Guru Coaching",
            "category": "Tutor",
            "location": "Shastri Nagar",
            "rating": 4.8,
            "reviews": 75,
            "image_url": "https://api.dicebear.com/9.x/notionists/svg?seed=guru&backgroundColor=c0aede,b6e3f4,d1d4f9",
            "featured": True,
        },
    ]
    search_query: str = ""
    category_filter: str = "All"
    rating_filter: float = 0.0
    open_now_filter: bool = False
    new_review_text: str = ""
    new_review_rating: int = 0
    app_settings: dict[str, str | list[ServiceCategory]] = {}

    @rx.event
    async def on_load(self):
        from app.states.admin_settings_state import AdminSettingsState
        from app.services.firebase_service import get_providers

        settings_state = await self.get_state(AdminSettingsState)
        yield settings_state.initialize_settings
        self.app_settings = settings_state.app_settings
        retrieved_categories = self.app_settings.get("service_categories", [])
        if isinstance(retrieved_categories, list):
            self.service_categories = retrieved_categories
        db_providers = await get_providers()
        if db_providers:
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