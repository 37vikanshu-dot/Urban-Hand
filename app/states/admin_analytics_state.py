import reflex as rx
from typing import TypedDict
from app.services.firebase_service import (
    get_business_analytics,
    get_recent_user_activity,
    get_providers,
)
import datetime


class BusinessAnalyticsData(TypedDict):
    provider_id: int
    total_views: int
    total_calls: int
    total_whatsapp: int
    total_shares: int
    last_viewed: str


class UserActivity(TypedDict):
    id: int
    event_type: str
    provider_id: int
    timestamp: str
    provider_name: str


class AdminAnalyticsState(rx.State):
    """State for the admin analytics dashboard."""

    business_stats: list[BusinessAnalyticsData] = []
    recent_activity: list[UserActivity] = []
    provider_map: dict[int, str] = {}
    time_range: str = "all_time"

    @rx.event
    async def on_load(self):
        """Load all analytics data from the database."""
        providers = await get_providers()
        self.provider_map = {p["id"]: p["name"] for p in providers}
        stats_data = await get_business_analytics()
        self.business_stats = stats_data
        activity_data = await get_recent_user_activity(limit=20)
        for activity in activity_data:
            activity["provider_name"] = self.provider_map.get(
                activity.get("provider_id"), "Unknown"
            )
        self.recent_activity = activity_data

    @rx.var
    def total_views(self) -> int:
        return sum((stat.get("total_views", 0) for stat in self.business_stats))

    @rx.var
    def total_calls(self) -> int:
        return sum((stat.get("total_calls", 0) for stat in self.business_stats))

    @rx.var
    def total_whatsapp_clicks(self) -> int:
        return sum((stat.get("total_whatsapp", 0) for stat in self.business_stats))

    @rx.var
    def total_shares(self) -> int:
        return sum((stat.get("total_shares", 0) for stat in self.business_stats))

    @rx.var
    def top_performing_providers(self) -> list[dict]:
        """Providers sorted by total views."""
        sorted_stats = sorted(
            self.business_stats, key=lambda x: x.get("total_views", 0), reverse=True
        )[:10]
        return [
            {**stat, "name": self.provider_map.get(stat["provider_id"], "Unknown")}
            for stat in sorted_stats
        ]

    @rx.var
    def engagement_chart_data(self) -> list[dict]:
        """Data formatted for the recharts bar chart."""
        return [
            {
                "name": self.provider_map.get(stat["provider_id"], "Unknown"),
                "Views": stat.get("total_views", 0),
                "Calls": stat.get("total_calls", 0),
                "WhatsApp": stat.get("total_whatsapp", 0),
                "Shares": stat.get("total_shares", 0),
            }
            for stat in self.business_stats
        ]