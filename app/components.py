import reflex as rx
from app.state import ServiceCategory, Provider, UIState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon("hand-heart", class_name="h-6 w-6 text-teal-500"),
                        rx.el.span(
                            UIState.app_settings.get("app_name", "Urban Hand"),
                            class_name="font-bold text-xl text-gray-800",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    href="/",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("search", class_name="h-5 w-5 text-gray-400"),
                    rx.el.input(
                        placeholder="Search service or area...",
                        class_name="w-full bg-transparent focus:outline-none placeholder-gray-400 text-sm",
                    ),
                    class_name="flex items-center gap-2 w-full",
                ),
                class_name="hidden md:flex items-center bg-white border border-gray-200 rounded-lg px-4 py-2 w-full max-w-sm",
            ),
            rx.el.div(
                rx.el.a(
                    rx.el.button(
                        UIState.app_settings.get("get_listed_text", "Get Listed"),
                        class_name="hidden sm:block bg-teal-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-teal-600 transition-colors",
                    ),
                    href="/get-listed",
                ),
                rx.el.button(
                    rx.icon("user", class_name="h-5 w-5 text-gray-600"),
                    variant="ghost",
                    class_name="p-2 rounded-full hover:bg-gray-100",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="container mx-auto flex items-center justify-between p-4",
        ),
        class_name="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50",
    )


def hero_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h1(
                UIState.app_settings.get(
                    "hero_title", "Connecting Local Hands to Local Needs."
                ),
                class_name="text-4xl md:text-5xl font-extrabold text-gray-800 tracking-tighter",
            ),
            rx.el.p(
                UIState.app_settings.get(
                    "hero_subtitle",
                    "Find trusted local service providers in your city, with just a few clicks.",
                ),
                class_name="mt-4 text-lg text-gray-600 max-w-2xl",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("search", class_name="h-5 w-5 text-gray-400"),
                    rx.el.input(
                        placeholder="What service are you looking for?",
                        class_name="w-full bg-transparent focus:outline-none placeholder-gray-400",
                    ),
                    class_name="flex items-center gap-2 w-full",
                ),
                rx.el.button(
                    "Search",
                    class_name="bg-indigo-600 text-white px-8 py-3 rounded-r-lg text-md font-semibold hover:bg-indigo-700 transition-colors",
                ),
                class_name="mt-8 flex items-center bg-white border border-gray-200 rounded-lg shadow-sm max-w-xl w-full pl-4",
            ),
            class_name="container mx-auto text-center py-20 md:py-28",
        ),
        class_name="bg-gray-50",
    )


def category_card(category: ServiceCategory) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(tag=category["icon"], class_name="h-8 w-8 text-indigo-500 mb-3"),
            rx.el.span(
                category["name"], class_name="font-semibold text-gray-700 text-sm"
            ),
            class_name="flex flex-col items-center justify-center p-4 bg-white rounded-xl border border-gray-200 hover:shadow-lg hover:-translate-y-1 transition-all duration-300 cursor-pointer h-32",
        ),
        href="#",
    )


def service_categories_grid() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Browse by Category",
                class_name="text-2xl font-bold text-gray-800 mb-6 text-center",
            ),
            rx.el.div(
                rx.foreach(UIState.service_categories, category_card),
                class_name="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4",
            ),
            class_name="container mx-auto py-16 px-4",
        )
    )


def provider_card(provider: Provider) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src=provider["image_url"], class_name="h-48 w-full object-cover"
                ),
                rx.cond(
                    provider["featured"],
                    rx.el.div(
                        rx.icon("star", class_name="h-4 w-4 text-yellow-400 mr-1"),
                        "Featured",
                        class_name="absolute top-2 left-2 bg-yellow-400 text-yellow-900 text-xs font-bold px-2 py-1 rounded-md flex items-center",
                    ),
                    None,
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        provider["name"],
                        class_name="font-bold text-lg text-gray-800 truncate",
                    ),
                    rx.el.div(
                        rx.icon("tag", class_name="h-4 w-4 text-indigo-500"),
                        rx.el.p(
                            provider["category"], class_name="text-sm text-gray-600"
                        ),
                        class_name="flex items-center gap-2 mt-1",
                    ),
                    rx.el.div(
                        rx.icon("map-pin", class_name="h-4 w-4 text-gray-400"),
                        rx.el.p(
                            provider["location"],
                            class_name="text-sm text-gray-500 truncate",
                        ),
                        class_name="flex items-center gap-2 mt-1",
                    ),
                    class_name="flex-1",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon("star", class_name="h-5 w-5 text-yellow-500"),
                        rx.el.span(
                            provider["rating"].to_string(),
                            class_name="font-bold text-gray-800",
                        ),
                        rx.el.span(
                            f"({provider['reviews']} reviews)",
                            class_name="text-xs text-gray-500 ml-1",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex justify-between items-center",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("message-circle", class_name="h-4 w-4 mr-2"),
                        "WhatsApp",
                        class_name="w-full flex items-center justify-center bg-green-500 text-white px-3 py-2 rounded-lg text-xs font-semibold hover:bg-green-600 transition-colors",
                    ),
                    rx.el.button(
                        rx.icon("phone", class_name="h-4 w-4 mr-2"),
                        "Call",
                        class_name="w-full flex items-center justify-center bg-blue-500 text-white px-3 py-2 rounded-lg text-xs font-semibold hover:bg-blue-600 transition-colors",
                    ),
                    class_name="mt-4 grid grid-cols-2 gap-2",
                ),
                class_name="p-4 flex flex-col h-full",
            ),
            class_name="bg-white rounded-xl shadow-md overflow-hidden border border-gray-200 flex flex-col hover:shadow-xl transition-shadow duration-300 h-full",
        ),
        href=f"/business/{provider['id']}",
    )


def featured_providers_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Featured Providers",
                class_name="text-2xl font-bold text-gray-800 mb-6 text-center",
            ),
            rx.el.div(
                rx.foreach(UIState.featured_providers, provider_card),
                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8",
            ),
            class_name="container mx-auto py-16 px-4",
        ),
        class_name="bg-indigo-50",
    )


def top_rated_providers_section() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "Top Rated Near You",
                class_name="text-2xl font-bold text-gray-800 mb-6 text-center",
            ),
            rx.el.div(
                rx.foreach(UIState.top_rated_providers, provider_card),
                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8",
            ),
            class_name="container mx-auto py-16 px-4",
        )
    )


def footer() -> rx.Component:
    return rx.el.footer(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("hand-heart", class_name="h-6 w-6 text-teal-500"),
                        rx.el.span(
                            "Urban Hand", class_name="font-bold text-xl text-gray-800"
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.p(
                        "Connecting local hands to local needs.",
                        class_name="mt-2 text-gray-500 text-sm max-w-xs",
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Services", class_name="font-semibold text-gray-800 mb-4"
                        ),
                        rx.el.a(
                            "Find a Provider",
                            href="#",
                            class_name="text-gray-500 hover:text-teal-600 text-sm block mb-2",
                        ),
                        rx.el.a(
                            "Get Listed",
                            href="#",
                            class_name="text-gray-500 hover:text-teal-600 text-sm block mb-2",
                        ),
                        rx.el.a(
                            "Pricing",
                            href="#",
                            class_name="text-gray-500 hover:text-teal-600 text-sm block mb-2",
                        ),
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Company", class_name="font-semibold text-gray-800 mb-4"
                        ),
                        rx.el.a(
                            "About Us",
                            href="#",
                            class_name="text-gray-500 hover:text-teal-600 text-sm block mb-2",
                        ),
                        rx.el.a(
                            "Contact",
                            href="#",
                            class_name="text-gray-500 hover:text-teal-600 text-sm block mb-2",
                        ),
                        rx.el.a(
                            "Terms of Service",
                            href="#",
                            class_name="text-gray-500 hover:text-teal-600 text-sm block mb-2",
                        ),
                    ),
                    rx.el.div(
                        rx.el.h3(
                            "Connect", class_name="font-semibold text-gray-800 mb-4"
                        ),
                        rx.el.div(
                            rx.el.a(
                                rx.icon("instagram"),
                                href="#",
                                class_name="text-gray-500 hover:text-teal-600",
                            ),
                            rx.el.a(
                                rx.icon("facebook"),
                                href="#",
                                class_name="text-gray-500 hover:text-teal-600",
                            ),
                            rx.el.a(
                                rx.icon("twitter"),
                                href="#",
                                class_name="text-gray-500 hover:text-teal-600",
                            ),
                            class_name="flex gap-4",
                        ),
                    ),
                    class_name="grid grid-cols-2 md:grid-cols-3 gap-8",
                ),
                class_name="grid md:grid-cols-2 gap-8",
            ),
            rx.el.div(
                rx.el.p(
                    "© 2024 Urban Hand. All rights reserved.",
                    class_name="text-sm text-gray-500",
                ),
                class_name="mt-12 pt-8 border-t border-gray-200 text-center",
            ),
            class_name="container mx-auto py-12 px-4",
        ),
        class_name="bg-white border-t border-gray-200",
    )