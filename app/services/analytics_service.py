import reflex as rx
import logging
from app.services.firebase_service import get_supabase_client
from typing import Any
import datetime


async def log_event(
    event_type: str,
    provider_id: int | None = None,
    category: str | None = None,
    search_query: str | None = None,
    metadata: dict | None = None,
):
    """Logs a user interaction event to the user_analytics table."""
    supabase = get_supabase_client()
    if not supabase:
        logging.warning(
            "Supabase client not available. Skipping analytics event logging."
        )
        return
    try:
        event_data = {
            "event_type": event_type,
            "provider_id": provider_id,
            "category": category,
            "search_query": search_query,
            "metadata": metadata or {},
        }
        supabase.table("user_analytics").insert(event_data).execute()
        logging.info(f"Logged analytics event: {event_type}")
    except Exception as e:
        logging.exception(f"Error logging analytics event: {e}")


async def update_business_stats(provider_id: int, stat_to_increment: str):
    """Atomically increments a statistic for a given provider."""
    supabase = get_supabase_client()
    if not supabase:
        logging.warning(
            "Supabase client not available. Skipping business stats update."
        )
        return
    try:
        response = (
            supabase.table("business_analytics")
            .select("provider_id")
            .eq("provider_id", provider_id)
            .execute()
        )
        if not response.data:
            supabase.table("business_analytics").insert(
                {"provider_id": provider_id, stat_to_increment: 1}
            ).execute()
        else:
            current_stat_resp = (
                supabase.table("business_analytics")
                .select(stat_to_increment)
                .eq("provider_id", provider_id)
                .single()
                .execute()
            )
            current_value = current_stat_resp.data.get(stat_to_increment, 0)
            supabase.table("business_analytics").update(
                {stat_to_increment: current_value + 1}
            ).eq("provider_id", provider_id).execute()
        if stat_to_increment == "total_views":
            supabase.table("business_analytics").update(
                {"last_viewed": datetime.datetime.now().isoformat()}
            ).eq("provider_id", provider_id).execute()
    except Exception as e:
        logging.exception(
            f"Error updating business stats for provider {provider_id}: {e}"
        )