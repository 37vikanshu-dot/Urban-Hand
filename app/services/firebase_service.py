import reflex as rx
import os
from supabase import create_client, Client
from typing import Any
import logging
import uuid


def get_supabase_client() -> Client | None:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        return None
    return create_client(url, key)


async def get_app_settings() -> dict[
    str, str | int | bool | list[dict[str, str | bool]]
]:
    supabase = get_supabase_client()
    if not supabase:
        return {}
    try:
        response = supabase.table("app_settings").select("settings").single().execute()
        return response.data.get("settings", {})
    except Exception as e:
        logging.exception(f"Error fetching settings: {e}")
        return {}


async def save_app_settings(
    settings: dict[str, str | int | bool | list[dict[str, str | bool]]],
):
    supabase = get_supabase_client()
    if not supabase:
        return
    try:
        supabase.table("app_settings").upsert({"id": 1, "settings": settings}).execute()
    except Exception as e:
        logging.exception(f"Error saving settings: {e}")


async def get_providers() -> list[dict[str, str | int | bool | float]]:
    supabase = get_supabase_client()
    if not supabase:
        return []
    try:
        response = supabase.table("providers").select("data").execute()
        return [item["data"] for item in response.data]
    except Exception as e:
        logging.exception(f"Error fetching providers: {e}")
        return []


async def save_providers(providers: list[dict[str, str | int | bool | float]]):
    supabase = get_supabase_client()
    if not supabase:
        return
    try:
        supabase.table("providers").delete().neq("id", -1).execute()
        if providers:
            supabase.table("providers").insert(
                [{"id": p["id"], "data": p} for p in providers]
            ).execute()
    except Exception as e:
        logging.exception(f"Error saving providers: {e}")


async def get_pricing_plans() -> list[dict[str, str | int | bool | list[str]]]:
    supabase = get_supabase_client()
    if not supabase:
        return []
    try:
        response = supabase.table("pricing_plans").select("data").execute()
        return [item["data"] for item in response.data]
    except Exception as e:
        logging.exception(f"Error fetching pricing plans: {e}")
        return []


async def save_pricing_plans(plans: list[dict[str, str | int | bool | list[str]]]):
    supabase = get_supabase_client()
    if not supabase:
        return
    try:
        supabase.table("pricing_plans").delete().neq("id", "").execute()
        if plans:
            supabase.table("pricing_plans").insert(
                [{"id": p["id"], "data": p} for p in plans]
            ).execute()
    except Exception as e:
        logging.exception(f"Error saving pricing plans: {e}")


async def get_payment_submissions() -> list[dict]:
    supabase = get_supabase_client()
    if not supabase:
        return []
    try:
        response = supabase.table("payment_submissions").select("data").execute()
        return [item["data"] for item in response.data]
    except Exception as e:
        logging.exception(f"Error fetching payment submissions: {e}")
        return []


async def save_payment_submissions(submissions: list[dict]):
    supabase = get_supabase_client()
    if not supabase:
        return
    try:
        supabase.table("payment_submissions").delete().neq("id", "").execute()
        if submissions:
            supabase.table("payment_submissions").insert(
                [{"id": s["id"], "data": s} for s in submissions]
            ).execute()
    except Exception as e:
        logging.exception(f"Error saving payment submissions: {e}")


async def get_business_analytics() -> list[dict]:
    supabase = get_supabase_client()
    if not supabase:
        return []
    try:
        response = supabase.table("business_analytics").select("*").execute()
        return response.data
    except Exception as e:
        logging.exception(f"Error fetching business analytics: {e}")
        return []


async def get_recent_user_activity(limit: int = 20) -> list[dict]:
    supabase = get_supabase_client()
    if not supabase:
        return []
    try:
        response = (
            supabase.table("user_analytics")
            .select("id, event_type, provider_id, timestamp")
            .order("timestamp", desc=True)
            .limit(limit)
            .execute()
        )
        return response.data
    except Exception as e:
        logging.exception(f"Error fetching recent user activity: {e}")
        return []


async def get_business_owners() -> list[dict]:
    supabase = get_supabase_client()
    if not supabase:
        return []
    try:
        response = supabase.table("business_owners").select("*").execute()
        return response.data
    except Exception as e:
        logging.exception(f"Error fetching business owners: {e}")
        return []


async def save_business_owners(owners: list[dict]):
    supabase = get_supabase_client()
    if not supabase:
        return
    try:
        supabase.table("business_owners").delete().neq(
            "id", str(uuid.uuid4())
        ).execute()
        if owners:
            supabase.table("business_owners").insert(owners).execute()
    except Exception as e:
        logging.exception(f"Error saving business owners: {e}")


async def get_owner_by_email(email: str) -> dict | None:
    supabase = get_supabase_client()
    if not supabase:
        return None
    try:
        response = (
            supabase.table("business_owners")
            .select("*")
            .eq("email", email)
            .single()
            .execute()
        )
        return response.data
    except Exception as e:
        if "PGRST116" not in str(e):
            logging.exception(f"Error fetching owner by email: {e}")
        return None


async def update_owner_password(owner_id: str, new_password_hash: str):
    supabase = get_supabase_client()
    if not supabase:
        return
    try:
        supabase.table("business_owners").update(
            {"password_hash": new_password_hash}
        ).eq("id", owner_id).execute()
    except Exception as e:
        logging.exception(f"Error updating password: {e}")