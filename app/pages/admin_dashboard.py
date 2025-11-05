import reflex as rx
from app.states.admin_state import AdminState
from app.states.admin_settings_state import AdminSettingsState
from app.states.admin_categories_state import AdminCategoriesState
from app.states.admin_listings_state import AdminListingsState
from app.states.admin_payment_plans_state import AdminPaymentPlansState, PricingPlan
from app.states.admin_payment_submissions_state import (
    AdminPaymentSubmissionsState,
    PaymentSubmission,
)
from app.states.admin_analytics_state import AdminAnalyticsState
from app.states.admin_business_owners_state import AdminBusinessOwnersState
from app.state import Provider
from typing import Any


def admin_sidebar() -> rx.Component:
    """The sidebar for the admin dashboard."""
    nav_items = [
        {"name": "Analytics", "icon": "bar-chart-2"},
        {"name": "App Settings", "icon": "settings"},
        {"name": "Categories", "icon": "layout-grid"},
        {"name": "Listings", "icon": "list"},
        {"name": "Payments", "icon": "banknote"},
        {"name": "Business Owners", "icon": "users"},
        {"name": "Reviews", "icon": "star"},
    ]
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon("shield-check", class_name="h-8 w-8 text-teal-500"),
                        rx.el.span(
                            "Urban Hand Admin",
                            class_name="font-bold text-xl text-gray-800",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    href="/admin/dashboard",
                ),
                class_name="flex items-center h-16 border-b px-6",
            ),
            rx.el.nav(
                rx.foreach(
                    nav_items,
                    lambda item: rx.el.a(
                        rx.icon(item["icon"], class_name="h-5 w-5"),
                        rx.el.span(item["name"]),
                        on_click=lambda: AdminState.set_current_page(item["name"]),
                        class_name=rx.cond(
                            AdminState.current_page == item["name"],
                            "flex items-center gap-3 rounded-lg bg-teal-100 px-3 py-2 text-teal-800 transition-all hover:text-teal-800 font-semibold cursor-pointer",
                            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900 cursor-pointer",
                        ),
                    ),
                ),
                class_name="flex-1 grid items-start p-4 text-sm font-medium gap-2",
            ),
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("log-out", class_name="h-5 w-5 mr-2"),
                "Logout",
                on_click=AdminState.logout,
                class_name="w-full flex items-center justify-center gap-3 rounded-lg px-3 py-3 text-red-500 transition-all hover:bg-red-50 hover:text-red-600 font-semibold",
            ),
            class_name="mt-auto p-4 border-t",
        ),
        class_name="hidden border-r bg-gray-50/75 md:flex md:flex-col min-h-screen w-64",
    )


def form_group(label: str, description: str, child: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(label, class_name="font-semibold text-gray-800"),
            rx.el.p(description, class_name="text-sm text-gray-500"),
            class_name="flex-1",
        ),
        rx.el.div(child, class_name="w-full md:w-2/3"),
        class_name="flex flex-col md:flex-row items-start gap-4 p-6 border-b",
    )


def text_content_settings() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Text Content", class_name="text-xl font-bold p-6 border-b"),
        form_group(
            "Hero Title",
            "The main headline on the home page.",
            rx.el.input(
                default_value=AdminSettingsState.app_settings.get("hero_title", "").to(
                    str
                ),
                on_change=lambda v: AdminSettingsState.handle_setting_change(
                    "hero_title", v
                ),
                placeholder="Enter hero title",
                class_name="w-full rounded-md border-gray-300 shadow-sm text-sm",
            ),
        ),
        form_group(
            "Hero Subtitle",
            "The supporting text below the main headline.",
            rx.el.textarea(
                default_value=AdminSettingsState.app_settings.get(
                    "hero_subtitle", ""
                ).to(str),
                on_change=lambda v: AdminSettingsState.handle_setting_change(
                    "hero_subtitle", v
                ),
                placeholder="Enter hero subtitle",
                class_name="w-full rounded-md border-gray-300 shadow-sm text-sm",
                rows=3,
            ),
        ),
        form_group(
            "'Get Listed' Button Text",
            "The call-to-action button in the header.",
            rx.el.input(
                default_value=AdminSettingsState.app_settings.get(
                    "get_listed_text", ""
                ).to(str),
                on_change=lambda v: AdminSettingsState.handle_setting_change(
                    "get_listed_text", v
                ),
                placeholder="Enter button text",
                class_name="w-full rounded-md border-gray-300 shadow-sm text-sm",
            ),
        ),
    )


def branding_settings() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Branding & Theme", class_name="text-xl font-bold p-6 border-b"),
        form_group(
            "Accent Color",
            "The primary color for buttons, links, and highlights.",
            rx.el.input(
                type="color",
                on_change=lambda v: AdminSettingsState.handle_setting_change(
                    "accent_color", v
                ),
                class_name="w-24 h-10 p-1 border-gray-300 rounded-md cursor-pointer",
                default_value=AdminSettingsState.app_settings.get(
                    "accent_color", "#14b8a6"
                ).to(str),
            ),
        ),
    )


def app_settings_page_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            text_content_settings(),
            branding_settings(),
            class_name="bg-white rounded-xl border border-gray-200 shadow-sm",
        )
    )


def admin_dashboard_page() -> rx.Component:
    return rx.el.div(
        admin_sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        AdminState.current_page,
                        class_name="text-2xl font-bold text-gray-900",
                    ),
                    rx.cond(
                        AdminState.current_page == "App Settings",
                        rx.el.button(
                            rx.icon("save", class_name="h-4 w-4 mr-2"),
                            "Save Changes",
                            on_click=AdminSettingsState.save_settings,
                            class_name="flex items-center bg-teal-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-teal-600 transition-colors",
                        ),
                        None,
                    ),
                    class_name="flex justify-between items-center",
                ),
                rx.el.div(
                    rx.match(
                        AdminState.current_page,
                        ("Analytics", analytics_page_content()),
                        ("App Settings", app_settings_page_content()),
                        ("Categories", categories_page_content()),
                        ("Listings", listings_page_content()),
                        ("Payments", payments_page_content()),
                        ("Business Owners", business_owners_page_content()),
                        ("Reviews", rx.el.p("Review management coming soon...")),
                        rx.el.p("Select a page from the sidebar."),
                    ),
                    class_name="mt-6",
                ),
                class_name="p-8",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen bg-gray-100 font-['Inter']",
    )


def category_management_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4 mr-2"),
                "Add New Category",
                on_click=AdminCategoriesState.open_add_modal,
                class_name="flex items-center bg-teal-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-teal-600 transition-colors",
            )
        ),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title(
                rx.cond(
                    AdminCategoriesState.modal_is_editing,
                    "Edit Category",
                    "Add New Category",
                )
            ),
            rx.el.div(
                rx.el.label("Category Name", class_name="text-sm font-medium"),
                rx.el.input(
                    placeholder="e.g. Electrician",
                    default_value=AdminCategoriesState.modal_category_name,
                    on_change=AdminCategoriesState.set_modal_category_name,
                    class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm",
                ),
                class_name="my-4",
            ),
            rx.el.div(
                rx.el.label("Icon", class_name="text-sm font-medium"),
                rx.el.div(
                    rx.foreach(
                        AdminCategoriesState.lucide_icons,
                        lambda icon: rx.el.button(
                            rx.icon(icon, class_name="h-5 w-5"),
                            on_click=lambda: AdminCategoriesState.set_modal_icon(icon),
                            class_name=rx.cond(
                                AdminCategoriesState.modal_category_icon == icon,
                                "p-2 rounded-lg bg-teal-100 text-teal-700",
                                "p-2 rounded-lg hover:bg-gray-100",
                            ),
                            variant="ghost",
                        ),
                    ),
                    class_name="grid grid-cols-6 gap-2 mt-2 border p-2 rounded-lg",
                ),
                class_name="my-4",
            ),
            rx.el.div(
                rx.el.label(
                    rx.el.input(
                        type="checkbox",
                        checked=AdminCategoriesState.modal_category_enabled,
                        on_change=AdminCategoriesState.set_modal_category_enabled,
                        class_name="h-4 w-4 rounded border-gray-300 text-teal-600 focus:ring-teal-500 mr-2",
                    ),
                    "Enabled",
                    class_name="flex items-center text-sm font-medium",
                ),
                class_name="my-4",
            ),
            rx.el.div(
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=AdminCategoriesState.close_category_modal,
                        variant="soft",
                        color_scheme="gray",
                    )
                ),
                rx.el.button(
                    "Save Category", on_click=AdminCategoriesState.save_category
                ),
                class_name="flex justify-end gap-3 mt-4",
            ),
        ),
        open=AdminCategoriesState.show_category_modal,
        on_open_change=AdminCategoriesState.set_show_category_modal,
    )


def delete_confirmation_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Confirm Deletion"),
            rx.radix.primitives.dialog.description(
                "Are you sure you want to delete this category? This action cannot be undone."
            ),
            rx.el.div(
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=AdminCategoriesState.cancel_delete,
                        variant="soft",
                        color_scheme="gray",
                    )
                ),
                rx.el.button(
                    "Delete",
                    on_click=AdminCategoriesState.confirm_delete_category,
                    color_scheme="red",
                ),
                class_name="flex justify-end gap-3 mt-4",
            ),
        ),
        open=AdminCategoriesState.show_delete_confirm,
        on_open_change=AdminCategoriesState.set_show_delete_confirm,
    )


def stat_card(
    icon: str, title: str, value: rx.Var[str | int], color: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-6 w-6 {color}"),
            class_name="p-3 bg-gray-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-bold text-gray-900"),
        ),
        class_name="flex items-center gap-4 p-4 bg-white rounded-xl border border-gray-200 shadow-sm",
    )


def analytics_page_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_card(
                "eye", "Total Views", AdminAnalyticsState.total_views, "text-blue-500"
            ),
            stat_card(
                "phone",
                "Total Calls",
                AdminAnalyticsState.total_calls,
                "text-green-500",
            ),
            stat_card(
                "message-circle",
                "WhatsApp Clicks",
                AdminAnalyticsState.total_whatsapp_clicks,
                "text-teal-500",
            ),
            stat_card(
                "share-2",
                "Total Shares",
                AdminAnalyticsState.total_shares,
                "text-indigo-500",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Top Performing Providers (by Views)",
                    class_name="text-lg font-semibold text-gray-800",
                ),
                rx.el.div(
                    rx.foreach(
                        AdminAnalyticsState.top_performing_providers,
                        lambda stat: rx.el.div(
                            rx.el.span(stat["name"], class_name="font-medium"),
                            rx.el.div(
                                rx.el.span(
                                    stat["total_views"].to_string(),
                                    class_name="font-bold text-gray-800",
                                ),
                                rx.icon("eye", class_name="h-4 w-4 text-gray-400"),
                                class_name="flex items-center gap-2",
                            ),
                            class_name="flex justify-between items-center p-3 hover:bg-gray-50 rounded-md",
                        ),
                    ),
                    class_name="mt-4 space-y-2",
                ),
                class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
            ),
            rx.el.div(
                rx.el.h3(
                    "Recent Activity", class_name="text-lg font-semibold text-gray-800"
                ),
                rx.el.div(
                    rx.foreach(
                        AdminAnalyticsState.recent_activity,
                        lambda activity: rx.el.div(
                            rx.el.div(
                                rx.icon(
                                    rx.match(
                                        activity["event_type"],
                                        ("page_view", "eye"),
                                        ("call_click", "phone"),
                                        ("whatsapp_click", "message-circle"),
                                        ("share_click", "share-2"),
                                        "alert-circle",
                                    ),
                                    class_name="h-5 w-5 text-gray-500",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        activity["event_type"]
                                        .replace("_", " ")
                                        .capitalize(),
                                        class_name="font-medium",
                                    ),
                                    rx.el.p(
                                        f"Provider: {activity['provider_name']}",
                                        class_name="text-sm text-gray-500",
                                    ),
                                ),
                            ),
                            rx.el.span(
                                activity["timestamp"],
                                class_name="text-xs text-gray-500",
                            ),
                            class_name="flex justify-between items-center p-3 hover:bg-gray-50 rounded-md",
                        ),
                    ),
                    class_name="mt-4 space-y-2",
                ),
                class_name="p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6",
        ),
        class_name="space-y-6",
        on_mount=AdminAnalyticsState.on_load,
    )


def categories_page_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Service Categories", class_name="text-xl font-bold"),
            category_management_modal(),
            class_name="flex justify-between items-center p-6 border-b",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Icon", class_name="font-semibold text-sm text-gray-600 w-16"),
                rx.el.p(
                    "Name", class_name="font-semibold text-sm text-gray-600 flex-1"
                ),
                rx.el.p(
                    "Status", class_name="font-semibold text-sm text-gray-600 w-24"
                ),
                rx.el.p(
                    "Actions",
                    class_name="font-semibold text-sm text-gray-600 w-48 text-right",
                ),
                class_name="flex items-center gap-4 px-6 py-3 bg-gray-50",
            ),
            rx.el.div(
                rx.foreach(
                    AdminCategoriesState.service_categories,
                    lambda cat, index: rx.el.div(
                        rx.icon(cat["icon"], class_name="h-6 w-6 text-gray-700 w-16"),
                        rx.el.span(cat["name"], class_name="font-medium flex-1"),
                        rx.el.div(
                            rx.el.span(
                                rx.cond(cat["enabled"], "Enabled", "Disabled"),
                                class_name=rx.cond(
                                    cat["enabled"],
                                    "px-2 py-1 text-xs font-semibold text-green-800 bg-green-100 rounded-full",
                                    "px-2 py-1 text-xs font-semibold text-red-800 bg-red-100 rounded-full",
                                ),
                            ),
                            class_name="w-24",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("arrow-up", class_name="h-4 w-4"),
                                on_click=lambda: AdminCategoriesState.move_category(
                                    index, index - 1
                                ),
                                disabled=index == 0,
                                variant="ghost",
                            ),
                            rx.el.button(
                                rx.icon("arrow-down", class_name="h-4 w-4"),
                                on_click=lambda: AdminCategoriesState.move_category(
                                    index, index + 1
                                ),
                                disabled=index
                                == AdminCategoriesState.service_categories.length() - 1,
                                variant="ghost",
                            ),
                            rx.el.button(
                                rx.icon("pencil", class_name="h-4 w-4"),
                                on_click=lambda: AdminCategoriesState.open_edit_modal(
                                    cat
                                ),
                                variant="ghost",
                            ),
                            rx.el.button(
                                rx.icon("trash-2", class_name="h-4 w-4 text-red-500"),
                                on_click=lambda: AdminCategoriesState.open_delete_confirm(
                                    cat["id"]
                                ),
                                variant="ghost",
                            ),
                            class_name="flex justify-end gap-2 w-48",
                        ),
                        class_name="flex items-center gap-4 px-6 py-4 border-b",
                    ),
                )
            ),
        ),
        delete_confirmation_dialog(),
        class_name="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden",
        on_mount=[AdminCategoriesState.load_categories],
    )


def listing_management_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4 mr-2"),
                "Add New Listing",
                on_click=AdminListingsState.open_add_modal,
                class_name="flex items-center bg-teal-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-teal-600 transition-colors",
            )
        ),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title(
                rx.cond(
                    AdminListingsState.modal_is_editing,
                    "Edit Listing",
                    "Add New Listing",
                )
            ),
            rx.el.div(
                rx.el.label("Business Name", class_name="text-sm font-medium"),
                rx.el.input(
                    default_value=AdminListingsState.modal_business_name,
                    on_change=AdminListingsState.set_modal_business_name,
                    class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm",
                ),
                class_name="my-2",
            ),
            rx.el.div(
                rx.el.label("Category", class_name="text-sm font-medium"),
                rx.el.select(
                    rx.foreach(
                        AdminCategoriesState.service_categories,
                        lambda cat: rx.el.option(cat["name"], value=cat["name"]),
                    ),
                    value=AdminListingsState.modal_category,
                    on_change=AdminListingsState.set_modal_category,
                    class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm rounded-md",
                ),
                class_name="my-2",
            ),
            rx.el.div(
                rx.el.label("Address / Location", class_name="text-sm font-medium"),
                rx.el.input(
                    default_value=AdminListingsState.modal_address,
                    on_change=AdminListingsState.set_modal_address,
                    class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm",
                ),
                class_name="my-2",
            ),
            rx.el.div(
                rx.el.label("Image URL", class_name="text-sm font-medium"),
                rx.el.input(
                    default_value=AdminListingsState.modal_image_url,
                    on_change=AdminListingsState.set_modal_image_url,
                    class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm",
                ),
                class_name="my-2",
            ),
            rx.el.div(
                rx.el.label(
                    rx.el.input(
                        type="checkbox",
                        checked=AdminListingsState.modal_featured,
                        on_change=AdminListingsState.set_modal_featured,
                        class_name="h-4 w-4 rounded border-gray-300 text-teal-600 focus:ring-teal-500 mr-2",
                    ),
                    "Featured Listing",
                    class_name="flex items-center text-sm font-medium",
                ),
                class_name="my-4",
            ),
            rx.el.div(
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=AdminListingsState.close_listing_modal,
                        variant="soft",
                        color_scheme="gray",
                    )
                ),
                rx.el.button("Save Listing", on_click=AdminListingsState.save_listing),
                class_name="flex justify-end gap-3 mt-4",
            ),
        ),
        open=AdminListingsState.show_listing_modal,
        on_open_change=AdminListingsState.set_show_listing_modal,
    )


def listings_delete_confirmation_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Confirm Deletion"),
            rx.radix.primitives.dialog.description(
                "Are you sure you want to delete this listing? This action cannot be undone."
            ),
            rx.el.div(
                rx.radix.primitives.dialog.close(
                    rx.el.button(
                        "Cancel",
                        on_click=AdminListingsState.cancel_delete,
                        variant="soft",
                        color_scheme="gray",
                    )
                ),
                rx.el.button(
                    "Delete",
                    on_click=AdminListingsState.delete_listing,
                    color_scheme="red",
                ),
                class_name="flex justify-end gap-3 mt-4",
            ),
        ),
        open=AdminListingsState.show_delete_confirm,
        on_open_change=AdminListingsState.set_show_delete_confirm,
    )


def listings_page_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Business Listings", class_name="text-xl font-bold"),
            listing_management_modal(),
            class_name="flex justify-between items-center p-6 border-b",
        ),
        rx.el.div(
            rx.el.input(
                placeholder="Search by name or location...",
                on_change=AdminListingsState.set_search_query,
                class_name="w-full md:w-1/3 rounded-md border-gray-300 shadow-sm text-sm",
            ),
            rx.el.select(
                rx.el.option("All Categories", value="All"),
                rx.foreach(
                    AdminCategoriesState.service_categories,
                    lambda cat: rx.el.option(cat["name"], value=cat["name"]),
                ),
                on_change=AdminListingsState.set_category_filter,
                class_name="rounded-md border-gray-300 shadow-sm text-sm",
            ),
            class_name="flex gap-4 p-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p("Image", class_name="font-semibold text-sm text-gray-600 w-20"),
                rx.el.p(
                    "Name", class_name="font-semibold text-sm text-gray-600 flex-1"
                ),
                rx.el.p(
                    "Category", class_name="font-semibold text-sm text-gray-600 w-32"
                ),
                rx.el.p(
                    "Location", class_name="font-semibold text-sm text-gray-600 w-48"
                ),
                rx.el.p(
                    "Actions",
                    class_name="font-semibold text-sm text-gray-600 w-32 text-right",
                ),
                class_name="flex items-center gap-4 px-6 py-3 bg-gray-50/75 border-b",
            ),
            rx.el.div(
                rx.foreach(
                    AdminListingsState.filtered_listings,
                    lambda listing: rx.el.div(
                        rx.image(
                            src=listing["image_url"],
                            class_name="h-10 w-10 rounded-md object-cover",
                        ),
                        rx.el.div(
                            rx.el.span(listing["name"], class_name="font-medium"),
                            rx.cond(
                                listing["featured"],
                                rx.el.div(
                                    rx.icon(
                                        "star",
                                        class_name="h-3 w-3 text-yellow-500 mr-1",
                                    ),
                                    "Featured",
                                    class_name="text-xs text-yellow-700 bg-yellow-100 px-2 py-0.5 rounded-full flex items-center w-fit mt-1",
                                ),
                                None,
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.span(
                            listing["category"], class_name="text-sm text-gray-600 w-32"
                        ),
                        rx.el.span(
                            listing["location"],
                            class_name="text-sm text-gray-600 w-48 truncate",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("pencil", class_name="h-4 w-4"),
                                on_click=lambda: AdminListingsState.open_edit_modal(
                                    listing
                                ),
                                variant="ghost",
                            ),
                            rx.el.button(
                                rx.icon("trash-2", class_name="h-4 w-4 text-red-500"),
                                on_click=lambda: AdminListingsState.open_delete_confirm(
                                    listing["id"].to_string()
                                ),
                                variant="ghost",
                            ),
                            class_name="flex justify-end gap-2 w-32",
                        ),
                        class_name="flex items-center gap-4 px-6 py-4 border-b hover:bg-gray-50",
                    ),
                )
            ),
            rx.cond(
                AdminListingsState.filtered_listings.length() == 0,
                rx.el.div(
                    rx.icon("search-x", class_name="h-12 w-12 text-gray-400 mb-4"),
                    rx.el.h3(
                        "No Listings Found",
                        class_name="text-xl font-semibold text-gray-700",
                    ),
                    rx.el.p(
                        "Try adjusting your search filters.",
                        class_name="text-gray-500 mt-2",
                    ),
                    class_name="text-center p-16",
                ),
                None,
            ),
        ),
        listings_delete_confirmation_dialog(),
        class_name="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden",
        on_mount=[
            AdminListingsState.load_listings,
            AdminCategoriesState.load_categories,
        ],
    )


def payments_page_content() -> rx.Component:
    return rx.radix.tabs.root(
        rx.radix.tabs.list(
            rx.radix.tabs.trigger("Payment Plans", value="plans"),
            rx.radix.tabs.trigger("Payment Submissions", value="submissions"),
        ),
        rx.el.div(
            rx.radix.tabs.content(payment_plans_tab(), value="plans"),
            rx.radix.tabs.content(payment_submissions_tab(), value="submissions"),
            class_name="mt-6",
        ),
        default_value="plans",
        class_name="w-full",
    )


def payment_plans_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(payment_configuration_section(), class_name="mb-8"),
        rx.el.div(
            rx.el.div(
                rx.el.h2("Pricing Plans", class_name="text-xl font-bold"),
                rx.el.button(
                    rx.icon("plus", class_name="mr-2"),
                    "Add New Plan",
                    on_click=AdminPaymentPlansState.open_add_modal,
                    class_name="flex items-center bg-teal-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-teal-600 transition-colors",
                ),
                class_name="flex justify-between items-center p-6 border-b",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Name", class_name="font-semibold text-sm text-gray-600 flex-1"
                    ),
                    rx.el.p(
                        "Price", class_name="font-semibold text-sm text-gray-600 w-24"
                    ),
                    rx.el.p(
                        "Duration",
                        class_name="font-semibold text-sm text-gray-600 w-24",
                    ),
                    rx.el.p(
                        "Status", class_name="font-semibold text-sm text-gray-600 w-24"
                    ),
                    rx.el.p(
                        "Actions",
                        class_name="font-semibold text-sm text-gray-600 w-32 text-right",
                    ),
                    class_name="flex items-center gap-4 px-6 py-3 bg-gray-50",
                ),
                rx.foreach(
                    AdminPaymentPlansState.pricing_plans,
                    lambda plan: rx.el.div(
                        rx.el.span(plan["name"], class_name="font-medium flex-1"),
                        rx.el.span(f"₹{plan['price']}", class_name="w-24"),
                        rx.el.span(plan["duration"], class_name="w-24"),
                        rx.el.span(
                            rx.cond(plan["active"], "Active", "Inactive"),
                            class_name=rx.cond(
                                plan["active"],
                                "w-24 px-2 py-1 text-xs font-semibold text-green-800 bg-green-100 rounded-full",
                                "w-24 px-2 py-1 text-xs font-semibold text-gray-800 bg-gray-100 rounded-full",
                            ),
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("pencil", class_name="h-4 w-4"),
                                on_click=lambda: AdminPaymentPlansState.open_edit_modal(
                                    plan
                                ),
                                variant="ghost",
                            ),
                            rx.el.button(
                                rx.icon("trash-2", class_name="h-4 w-4 text-red-500"),
                                on_click=lambda: AdminPaymentPlansState.delete_plan(
                                    plan["id"]
                                ),
                                variant="ghost",
                            ),
                            class_name="flex justify-end gap-2 w-32",
                        ),
                        class_name="flex items-center gap-4 px-6 py-4 border-b",
                    ),
                ),
            ),
            plan_editor_modal(),
        ),
        class_name="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden",
        on_mount=[AdminPaymentPlansState.load_default_plans],
    )


def plan_editor_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title(
                rx.cond(
                    AdminPaymentPlansState.modal_is_editing, "Edit Plan", "Add New Plan"
                )
            ),
            rx.el.div(
                rx.el.label("Plan Name", class_name="text-sm font-medium"),
                rx.el.input(
                    default_value=AdminPaymentPlansState.modal_plan_data["name"],
                    on_change=lambda v: AdminPaymentPlansState.handle_modal_plan_change(
                        "name", v
                    ),
                    class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm",
                ),
                class_name="my-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.label("Price (₹)", class_name="text-sm font-medium"),
                    rx.el.input(
                        default_value=AdminPaymentPlansState.modal_plan_data[
                            "price"
                        ].to_string(),
                        on_change=lambda v: AdminPaymentPlansState.handle_modal_plan_change(
                            "price", v.to(int)
                        ),
                        type="number",
                        class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm",
                    ),
                ),
                rx.el.div(
                    rx.el.label("Duration", class_name="text-sm font-medium"),
                    rx.el.select(
                        rx.foreach(
                            ["Monthly", "3 Months", "6 Months", "Yearly", "Lifetime"],
                            lambda d: rx.el.option(d, value=d),
                        ),
                        value=AdminPaymentPlansState.modal_plan_data["duration"],
                        on_change=lambda v: AdminPaymentPlansState.handle_modal_plan_change(
                            "duration", v
                        ),
                        class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm rounded-md",
                    ),
                ),
                class_name="grid grid-cols-2 gap-4 my-2",
            ),
            rx.el.div(
                rx.el.label("Features", class_name="text-sm font-medium"),
                rx.foreach(
                    AdminPaymentPlansState.modal_plan_data["features"],
                    lambda f: rx.el.div(
                        rx.el.span(f, class_name="flex-1"),
                        rx.el.button(
                            rx.icon("x", class_name="h-4 w-4"),
                            on_click=lambda: AdminPaymentPlansState.remove_feature_from_modal(
                                f
                            ),
                            variant="ghost",
                            size="1",
                        ),
                        class_name="flex items-center justify-between bg-gray-100 px-2 py-1 rounded-md",
                    ),
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Add a feature...",
                        on_change=AdminPaymentPlansState.set_modal_feature_input,
                        class_name="flex-1 rounded-l-md border-gray-300 shadow-sm text-sm",
                        default_value=AdminPaymentPlansState.modal_feature_input,
                    ),
                    rx.el.button(
                        "Add",
                        on_click=AdminPaymentPlansState.add_feature_to_modal,
                        class_name="bg-gray-200 px-4 rounded-r-md text-sm font-medium",
                    ),
                    class_name="flex mt-2",
                ),
                class_name="my-2",
            ),
            rx.el.div(
                rx.el.label(
                    rx.el.input(
                        type="checkbox",
                        checked=AdminPaymentPlansState.modal_plan_data["active"],
                        on_change=lambda v: AdminPaymentPlansState.handle_modal_plan_change(
                            "active", v
                        ),
                        class_name="h-4 w-4 rounded border-gray-300 text-teal-600 focus:ring-teal-500 mr-2",
                    ),
                    "Active Plan",
                    class_name="flex items-center text-sm font-medium",
                ),
                class_name="my-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=AdminPaymentPlansState.close_plan_modal,
                    variant="soft",
                    color_scheme="gray",
                ),
                rx.el.button("Save Plan", on_click=AdminPaymentPlansState.save_plan),
                class_name="flex justify-end gap-3 mt-4",
            ),
        ),
        open=AdminPaymentPlansState.show_plan_modal,
        on_open_change=AdminPaymentPlansState.set_show_plan_modal,
    )


def payment_configuration_section() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Payment Configuration", class_name="text-xl font-bold p-6 border-b"),
        form_group(
            "UPI ID",
            "The UPI ID to display for payments.",
            rx.el.input(
                default_value=AdminPaymentPlansState.upi_id,
                on_change=AdminPaymentPlansState.set_upi_id,
                class_name="w-full rounded-md border-gray-300 shadow-sm text-sm",
            ),
        ),
        form_group(
            "QR Code Image URL",
            "URL of the QR code image.",
            rx.el.input(
                default_value=AdminPaymentPlansState.qr_code_url,
                on_change=AdminPaymentPlansState.set_qr_code_url,
                placeholder="https://example.com/qr.png",
                class_name="w-full rounded-md border-gray-300 shadow-sm text-sm",
            ),
        ),
        form_group(
            "Payment Instructions",
            "Instructions shown to users on the payment screen.",
            rx.el.textarea(
                default_value=AdminPaymentPlansState.payment_instructions,
                on_change=AdminPaymentPlansState.set_payment_instructions,
                rows=3,
                class_name="w-full rounded-md border-gray-300 shadow-sm text-sm",
            ),
        ),
        class_name="bg-white rounded-xl border border-gray-200 shadow-sm",
    )


def payment_submissions_tab() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Payment Submissions", class_name="text-xl font-bold"),
            rx.el.select(
                rx.foreach(
                    ["All", "Pending", "Approved", "Rejected"],
                    lambda s: rx.el.option(s, value=s),
                ),
                on_change=AdminPaymentSubmissionsState.set_status_filter,
                default_value="All",
                class_name="rounded-md border-gray-300 shadow-sm text-sm",
            ),
            class_name="flex justify-between items-center p-6 border-b",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Applicant", class_name="font-semibold text-sm text-gray-600 flex-1"
                ),
                rx.el.p("Plan", class_name="font-semibold text-sm text-gray-600 w-32"),
                rx.el.p("Date", class_name="font-semibold text-sm text-gray-600 w-40"),
                rx.el.p(
                    "Status", class_name="font-semibold text-sm text-gray-600 w-32"
                ),
                rx.el.p(
                    "Actions",
                    class_name="font-semibold text-sm text-gray-600 w-24 text-right",
                ),
                class_name="flex items-center gap-4 px-6 py-3 bg-gray-50",
            ),
            rx.foreach(
                AdminPaymentSubmissionsState.filtered_submissions,
                payment_submission_row,
            ),
            rx.cond(
                AdminPaymentSubmissionsState.filtered_submissions.length() == 0,
                rx.el.div(
                    rx.icon("folder-search", class_name="h-12 w-12 text-gray-400 mb-4"),
                    rx.el.h3(
                        "No Submissions Found",
                        class_name="text-xl font-semibold text-gray-700",
                    ),
                    class_name="text-center p-16",
                ),
                None,
            ),
        ),
        payment_review_modal(),
        class_name="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden",
        on_mount=AdminPaymentSubmissionsState.on_load,
    )


def business_owners_page_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2("Business Owners", class_name="text-xl font-bold"),
            business_owner_management_modal(),
            class_name="flex justify-between items-center p-6 border-b",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "Name", class_name="font-semibold text-sm text-gray-600 flex-1"
                ),
                rx.el.p(
                    "Linked Business",
                    class_name="font-semibold text-sm text-gray-600 w-48",
                ),
                rx.el.p(
                    "Actions",
                    class_name="font-semibold text-sm text-gray-600 w-32 text-right",
                ),
                class_name="flex items-center gap-4 px-6 py-3 bg-gray-50/75 border-b",
            ),
            rx.el.div(
                rx.foreach(
                    AdminBusinessOwnersState.owners,
                    lambda owner: rx.el.div(
                        rx.el.div(
                            rx.el.span(owner["full_name"], class_name="font-medium"),
                            rx.el.span(
                                owner["email"],
                                class_name="text-xs text-gray-500 block mt-1",
                            ),
                            class_name="flex-1",
                        ),
                        rx.el.span(
                            AdminBusinessOwnersState.provider_name_map.get(
                                owner["provider_id"].to_string(), "Not Linked"
                            ),
                            class_name="text-sm text-gray-600 w-48",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon("key-round", class_name="h-4 w-4"),
                                on_click=lambda: AdminBusinessOwnersState.open_reset_password_modal(
                                    owner
                                ),
                                variant="ghost",
                            ),
                            rx.el.button(
                                rx.icon("trash-2", class_name="h-4 w-4 text-red-500"),
                                on_click=lambda: AdminBusinessOwnersState.delete_owner(
                                    owner["id"]
                                ),
                                variant="ghost",
                            ),
                            class_name="flex justify-end gap-2 w-32",
                        ),
                        class_name="flex items-center gap-4 px-6 py-4 border-b hover:bg-gray-50",
                    ),
                )
            ),
        ),
        reset_password_modal(),
        class_name="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden",
        on_mount=[AdminBusinessOwnersState.load_data],
    )


def business_owner_management_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4 mr-2"),
                "Add New Owner",
                on_click=AdminBusinessOwnersState.open_add_modal,
                class_name="flex items-center bg-teal-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-teal-600 transition-colors",
            )
        ),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Add New Business Owner"),
            rx.el.form(
                rx.el.div(
                    rx.el.label("Full Name", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="full_name",
                        class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm",
                    ),
                    class_name="my-2",
                ),
                rx.el.div(
                    rx.el.label("Email", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="email",
                        type="email",
                        class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm",
                    ),
                    class_name="my-2",
                ),
                rx.el.div(
                    rx.el.label("Password", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="password",
                        type="password",
                        class_name="mt-1 w-full rounded-md border-gray-300 shadow-sm text-sm",
                    ),
                    class_name="my-2",
                ),
                rx.el.div(
                    rx.el.label(
                        "Link to Business Listing", class_name="text-sm font-medium"
                    ),
                    rx.el.select(
                        rx.el.option("Select a business...", value="", disabled=True),
                        rx.foreach(
                            AdminBusinessOwnersState.unlinked_providers,
                            lambda p: rx.el.option(
                                p["name"], value=p["id"].to_string()
                            ),
                        ),
                        name="provider_id",
                        class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm rounded-md",
                    ),
                    class_name="my-2",
                ),
                rx.cond(
                    AdminBusinessOwnersState.error_message,
                    rx.el.p(
                        AdminBusinessOwnersState.error_message,
                        class_name="text-red-500 text-sm mt-2",
                    ),
                    None,
                ),
                rx.el.div(
                    rx.radix.primitives.dialog.close(
                        rx.el.button(
                            "Cancel", type="button", variant="soft", color_scheme="gray"
                        )
                    ),
                    rx.el.button("Create Owner Account", type="submit"),
                    class_name="flex justify-end gap-3 mt-4",
                ),
                on_submit=AdminBusinessOwnersState.create_owner_account,
            ),
        ),
        open=AdminBusinessOwnersState.show_add_modal,
        on_open_change=AdminBusinessOwnersState.set_show_add_modal,
    )


def reset_password_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Reset Password"),
            rx.cond(
                AdminBusinessOwnersState.selected_owner,
                rx.el.div(
                    rx.el.p(
                        f"Resetting password for {AdminBusinessOwnersState.selected_owner['email']}"
                    ),
                    rx.el.input(
                        placeholder="Enter new password",
                        on_change=AdminBusinessOwnersState.set_new_password,
                        type="password",
                        class_name="w-full rounded-md border-gray-300 mt-4",
                    ),
                ),
            ),
            rx.el.div(
                rx.radix.primitives.dialog.close(
                    rx.el.button("Cancel", variant="soft", color_scheme="gray")
                ),
                rx.el.button(
                    "Reset Password", on_click=AdminBusinessOwnersState.reset_password
                ),
                class_name="flex justify-end gap-3 mt-4",
            ),
        ),
        open=AdminBusinessOwnersState.show_reset_password_modal,
        on_open_change=AdminBusinessOwnersState.set_show_reset_password_modal,
    )


def payment_submission_row(submission: PaymentSubmission) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(submission["applicant_name"], class_name="font-medium"),
            rx.el.span(
                submission["business_name"], class_name="text-xs text-gray-500 block"
            ),
            class_name="flex-1",
        ),
        rx.el.span(
            f"{submission['plan_selected']} (₹{submission['amount']})",
            class_name="w-32",
        ),
        rx.el.span(submission["submit_date"], class_name="w-40"),
        rx.el.span(
            submission["status"],
            class_name=rx.match(
                submission["status"],
                (
                    "Approved",
                    "px-2 py-1 text-xs font-semibold text-green-800 bg-green-100 rounded-full",
                ),
                (
                    "Rejected",
                    "px-2 py-1 text-xs font-semibold text-red-800 bg-red-100 rounded-full",
                ),
                (
                    "Pending",
                    "px-2 py-1 text-xs font-semibold text-yellow-800 bg-yellow-100 rounded-full",
                ),
                "px-2 py-1 text-xs font-semibold text-gray-800 bg-gray-100 rounded-full",
            ),
        ),
        rx.el.div(
            rx.el.button(
                "Review",
                on_click=lambda: AdminPaymentSubmissionsState.open_review_modal(
                    submission
                ),
                size="1",
            ),
            class_name="flex justify-end gap-2 w-24",
        ),
        class_name="flex items-center gap-4 px-6 py-4 border-b hover:bg-gray-50",
    )


def payment_review_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title("Review Payment Submission"),
            rx.cond(
                AdminPaymentSubmissionsState.selected_submission,
                rx.el.div(
                    rx.el.h3("Applicant Details", class_name="font-bold mt-4 mb-2"),
                    rx.el.p(
                        f"Name: {AdminPaymentSubmissionsState.selected_submission['applicant_name']}"
                    ),
                    rx.el.p(
                        f"Business: {AdminPaymentSubmissionsState.selected_submission['business_name']}"
                    ),
                    rx.el.h3("Payment Details", class_name="font-bold mt-4 mb-2"),
                    rx.el.p(
                        f"Plan: {AdminPaymentSubmissionsState.selected_submission['plan_selected']}"
                    ),
                    rx.el.p(
                        f"Amount: ₹{AdminPaymentSubmissionsState.selected_submission['amount']}"
                    ),
                    rx.el.h3("Screenshot", class_name="font-bold mt-4 mb-2"),
                    rx.image(
                        src=rx.get_upload_url(
                            AdminPaymentSubmissionsState.selected_submission[
                                "screenshot_url"
                            ]
                        ),
                        class_name="w-full max-w-sm rounded-md border",
                    ),
                    rx.cond(
                        AdminPaymentSubmissionsState.selected_submission["status"]
                        == "Pending",
                        rx.el.div(
                            rx.el.textarea(
                                placeholder="Add rejection notes (if any)...",
                                on_change=AdminPaymentSubmissionsState.set_rejection_notes,
                                class_name="w-full rounded-md border-gray-300 text-sm mt-4",
                                rows=2,
                            ),
                            rx.el.div(
                                rx.el.button(
                                    "Reject",
                                    on_click=AdminPaymentSubmissionsState.reject_payment,
                                    color_scheme="red",
                                ),
                                rx.el.button(
                                    "Approve",
                                    on_click=AdminPaymentSubmissionsState.approve_payment,
                                    color_scheme="green",
                                ),
                                class_name="flex justify-end gap-3 mt-4",
                            ),
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Status: ",
                                rx.el.strong(
                                    AdminPaymentSubmissionsState.selected_submission[
                                        "status"
                                    ]
                                ),
                            ),
                            rx.el.p(
                                f"Notes: {AdminPaymentSubmissionsState.selected_submission['notes']}"
                            ),
                            class_name="mt-4 p-4 bg-gray-100 rounded-md",
                        ),
                    ),
                ),
                rx.el.p("No submission selected."),
            ),
            rx.radix.primitives.dialog.close(
                rx.el.button(
                    "Close", variant="soft", color_scheme="gray", class_name="mt-4"
                )
            ),
            max_width="560px",
        ),
        open=AdminPaymentSubmissionsState.show_review_modal,
        on_open_change=AdminPaymentSubmissionsState.set_show_review_modal,
    )