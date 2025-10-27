import reflex as rx
from app.state import UIState, ServiceCategory
from app.components import header, footer, provider_card


def search_filters() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Filters", class_name="text-lg font-semibold text-gray-800 mb-4"),
        rx.el.div(
            rx.el.label(
                "Search by name or location",
                class_name="text-sm font-medium text-gray-700",
            ),
            rx.el.input(
                placeholder="e.g. Ramesh, Malviya Nagar...",
                on_change=UIState.set_search_query,
                default_value=UIState.search_query,
                class_name="mt-1 w-full rounded-lg border-gray-300 shadow-sm text-sm",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label("Category", class_name="text-sm font-medium text-gray-700"),
            rx.el.select(
                rx.el.option("All", value="All"),
                rx.foreach(
                    UIState.service_categories,
                    lambda category: rx.el.option(
                        category["name"], value=category["name"]
                    ),
                ),
                on_change=UIState.set_category_filter,
                default_value=UIState.category_filter,
                class_name="mt-1 w-full rounded-lg border-gray-300 shadow-sm text-sm",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                f"Minimum Rating: {UIState.rating_filter.to_string()}",
                class_name="text-sm font-medium text-gray-700",
            ),
            rx.el.input(
                type="range",
                min=0,
                max=5,
                step=0.1,
                on_change=UIState.set_rating_filter.throttle(50),
                default_value=UIState.rating_filter,
                key=UIState.rating_filter,
                class_name="mt-1 w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-teal-500",
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                rx.el.input(
                    type="checkbox",
                    on_change=UIState.set_open_now_filter,
                    checked=UIState.open_now_filter,
                    class_name="h-4 w-4 rounded border-gray-300 text-teal-600 focus:ring-teal-500",
                ),
                rx.el.span("Open Now", class_name="ml-2 text-sm text-gray-600"),
                class_name="flex items-center",
            ),
            class_name="mb-4",
        ),
        class_name="w-full md:w-1/4 lg:w-1/5 p-6 bg-white rounded-xl border border-gray-200 shadow-sm h-fit sticky top-24",
    )


def search_results() -> rx.Component:
    return rx.el.div(
        rx.el.h2("Search Results", class_name="text-2xl font-bold text-gray-800 mb-6"),
        rx.el.div(
            rx.foreach(UIState.filtered_providers, provider_card),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8",
        ),
        rx.cond(
            UIState.filtered_providers.length() == 0,
            rx.el.div(
                rx.icon("search-x", class_name="h-12 w-12 text-gray-400 mb-4"),
                rx.el.h3(
                    "No Providers Found",
                    class_name="text-xl font-semibold text-gray-700",
                ),
                rx.el.p(
                    "Try adjusting your search filters.",
                    class_name="text-gray-500 mt-2",
                ),
                class_name="text-center p-16 bg-gray-50 rounded-lg border-2 border-dashed border-gray-200",
            ),
            None,
        ),
        class_name="flex-1 p-6",
    )


def search_page() -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.main(
            rx.el.div(
                search_filters(),
                search_results(),
                class_name="container mx-auto flex flex-col md:flex-row gap-8 py-8 px-4",
            ),
            class_name="bg-gray-50 min-h-screen",
        ),
        footer(),
        class_name="bg-white font-['Inter']",
    )