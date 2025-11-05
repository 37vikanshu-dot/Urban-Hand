import reflex as rx
from typing import TypedDict
from app.services.firebase_service import get_business_analytics, get_providers
from app.states.business_owner_auth_state import BusinessOwnerAuthState


class BusinessAnalyticsData(TypedDict):
    provider_id: int
    total_views: int
    total_calls: int
    total_whatsapp: int
    total_shares: int
    last_viewed: str


class BusinessOwnerDashboardState(rx.State):
    owner_stats: BusinessAnalyticsData | None = None
    provider_name: str = ""

    @rx.event
    async def on_load(self):
        auth_state = await self.get_state(BusinessOwnerAuthState)
        if auth_state.logged_in_owner:
            provider_id = auth_state.logged_in_owner["provider_id"]
            all_stats = await get_business_analytics()
            for stat in all_stats:
                if stat["provider_id"] == provider_id:
                    self.owner_stats = stat
                    break
            all_providers = await get_providers()
            for p in all_providers:
                if p["id"] == provider_id:
                    self.provider_name = p["name"]
                    break

    @rx.var
    def total_views(self) -> int:
        return self.owner_stats["total_views"] if self.owner_stats else 0

    @rx.var
    def total_calls(self) -> int:
        return self.owner_stats["total_calls"] if self.owner_stats else 0

    @rx.var
    def total_whatsapp_clicks(self) -> int:
        return self.owner_stats["total_whatsapp"] if self.owner_stats else 0

    @rx.var
    def total_shares(self) -> int:
        return self.owner_stats["total_shares"] if self.owner_stats else 0