import reflex as rx
from app.components import (
    header,
    hero_section,
    service_categories_grid,
    featured_providers_section,
    top_rated_providers_section,
    footer,
)
from app.pages.search import search_page
from app.pages.business_detail import business_detail_page
from app.pages.get_listed import get_listed_page
from app.pages.admin_login import admin_login_page
from app.pages.admin_dashboard import admin_dashboard_page
from app.pages.owner.login import owner_login_page
from app.pages.owner.dashboard import owner_dashboard_page
from app.state import UIState
from app.states.admin_state import AdminState
from app.states.business_owner_auth_state import BusinessOwnerAuthState


def index() -> rx.Component:
    """The main page of the Urban Hand app."""
    return rx.el.div(
        header(),
        rx.el.main(
            hero_section(),
            service_categories_grid(),
            featured_providers_section(),
            top_rated_providers_section(),
        ),
        footer(),
        class_name="bg-white font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="teal"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
from app.states.analytics_state import AnalyticsState

app.add_page(index, on_load=UIState.load_initial_data)
app.add_page(search_page, route="/search")
app.add_page(
    business_detail_page,
    route="/business/[id]",
    on_load=lambda: AnalyticsState.track_page_view(UIState.current_provider["id"]),
)
app.add_page(get_listed_page, route="/get-listed")
app.add_page(admin_login_page, route="/admin/login")
app.add_page(
    admin_dashboard_page,
    route="/admin/dashboard",
    on_load=AdminState.on_load_check_auth,
)
app.add_page(owner_login_page, route="/owner/login")
app.add_page(
    owner_dashboard_page,
    route="/owner/dashboard",
    on_load=BusinessOwnerAuthState.check_auth,
)