import reflex as rx
from app.states.business_owner_auth_state import BusinessOwnerAuthState
from app.states.business_owner_dashboard_state import BusinessOwnerDashboardState


def owner_sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon("briefcase", class_name="h-8 w-8 text-teal-500"),
                        rx.el.span(
                            "My Dashboard", class_name="font-bold text-xl text-gray-800"
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    href="/owner/dashboard",
                ),
                class_name="flex items-center h-16 border-b px-6",
            ),
            rx.el.nav(
                rx.el.a(
                    rx.icon("bar-chart-2", class_name="h-5 w-5"),
                    rx.el.span("Analytics"),
                    class_name="flex items-center gap-3 rounded-lg bg-teal-100 px-3 py-2 text-teal-800 font-semibold cursor-pointer",
                ),
                rx.el.a(
                    rx.icon("user", class_name="h-5 w-5"),
                    rx.el.span("My Profile"),
                    class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 hover:text-gray-900 cursor-pointer",
                ),
                class_name="flex-1 grid items-start p-4 text-sm font-medium gap-2",
            ),
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("log-out", class_name="h-5 w-5 mr-2"),
                "Logout",
                on_click=BusinessOwnerAuthState.logout,
                class_name="w-full flex items-center justify-center gap-3 rounded-lg px-3 py-3 text-red-500 transition-all hover:bg-red-50 hover:text-red-600 font-semibold",
            ),
            class_name="mt-auto p-4 border-t",
        ),
        class_name="hidden border-r bg-gray-50/75 md:flex md:flex-col min-h-screen w-64",
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
            rx.el.p(value.to_string(), class_name="text-2xl font-bold text-gray-900"),
        ),
        class_name="flex items-center gap-4 p-4 bg-white rounded-xl border border-gray-200 shadow-sm",
    )


def owner_dashboard_page() -> rx.Component:
    return rx.el.div(
        owner_sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        f"Welcome, {BusinessOwnerDashboardState.provider_name}",
                        class_name="text-2xl font-bold text-gray-900",
                    ),
                    rx.el.p(
                        "Here's how your business is performing.",
                        class_name="text-gray-500",
                    ),
                ),
                rx.el.div(
                    stat_card(
                        "eye",
                        "Total Views",
                        BusinessOwnerDashboardState.total_views,
                        "text-blue-500",
                    ),
                    stat_card(
                        "phone",
                        "Total Calls",
                        BusinessOwnerDashboardState.total_calls,
                        "text-green-500",
                    ),
                    stat_card(
                        "message-circle",
                        "WhatsApp Clicks",
                        BusinessOwnerDashboardState.total_whatsapp_clicks,
                        "text-teal-500",
                    ),
                    stat_card(
                        "share-2",
                        "Total Shares",
                        BusinessOwnerDashboardState.total_shares,
                        "text-indigo-500",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6",
                ),
                class_name="p-8",
            ),
            class_name="flex-1",
            on_mount=BusinessOwnerDashboardState.on_load,
        ),
        class_name="flex min-h-screen bg-gray-100 font-['Inter']",
    )