import reflex as rx
from app.services.analytics_service import log_event, update_business_stats


class AnalyticsState(rx.State):
    """State for handling analytics and user event tracking."""

    @rx.event(background=True)
    async def track_page_view(self, provider_id: int):
        """Track a view event for a business profile."""
        async with self:
            await log_event(event_type="page_view", provider_id=provider_id)
            await update_business_stats(provider_id, "total_views")

    @rx.event(background=True)
    async def track_call_click(self, provider_id: int):
        """Track a 'Call Now' button click."""
        async with self:
            await log_event(event_type="call_click", provider_id=provider_id)
            await update_business_stats(provider_id, "total_calls")

    @rx.event(background=True)
    async def track_whatsapp_click(self, provider_id: int):
        """Track a 'Chat on WhatsApp' button click."""
        async with self:
            await log_event(event_type="whatsapp_click", provider_id=provider_id)
            await update_business_stats(provider_id, "total_whatsapp")

    @rx.event(background=True)
    async def track_share_click(self, provider_id: int):
        """Track a 'Share Profile' button click."""
        async with self:
            await log_event(event_type="share_click", provider_id=provider_id)
            await update_business_stats(provider_id, "total_shares")