import reflex as rx
from app.state import UIState
from app.components import header, footer


def business_detail_page() -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.main(
            rx.cond(
                UIState.current_provider,
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.image(
                                src=UIState.current_provider["image_url"],
                                class_name="w-full h-96 object-cover rounded-xl border border-gray-200",
                            ),
                            rx.el.h1(
                                UIState.current_provider["name"],
                                class_name="text-4xl font-extrabold text-gray-900 mt-6",
                            ),
                            rx.cond(
                                UIState.current_provider["featured"],
                                rx.el.div(
                                    rx.icon(
                                        "star",
                                        class_name="h-5 w-5 text-yellow-500 mr-2",
                                    ),
                                    "Featured Business",
                                    class_name="mt-2 w-fit flex items-center bg-yellow-100 text-yellow-800 text-sm font-semibold px-3 py-1 rounded-full",
                                ),
                                None,
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "tag", class_name="h-5 w-5 text-indigo-500"
                                    ),
                                    rx.el.p(
                                        UIState.current_provider["category"],
                                        class_name="text-lg text-gray-700",
                                    ),
                                    class_name="flex items-center gap-3",
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "map-pin", class_name="h-5 w-5 text-gray-500"
                                    ),
                                    rx.el.p(
                                        UIState.current_provider["location"],
                                        class_name="text-lg text-gray-700",
                                    ),
                                    class_name="flex items-center gap-3",
                                ),
                                class_name="flex flex-col gap-3 mt-4 text-gray-600",
                            ),
                            class_name="w-full lg:w-2/3",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.button(
                                    rx.icon("phone", class_name="h-5 w-5 mr-2"),
                                    "Call Now",
                                    class_name="w-full flex items-center justify-center bg-blue-500 text-white px-6 py-3 rounded-lg text-md font-semibold hover:bg-blue-600 transition-colors",
                                ),
                                rx.el.button(
                                    rx.icon(
                                        "message-circle", class_name="h-5 w-5 mr-2"
                                    ),
                                    "Chat on WhatsApp",
                                    class_name="w-full flex items-center justify-center bg-green-500 text-white px-6 py-3 rounded-lg text-md font-semibold hover:bg-green-600 transition-colors",
                                ),
                                rx.el.button(
                                    rx.icon("map", class_name="h-5 w-5 mr-2"),
                                    "View Location",
                                    class_name="w-full flex items-center justify-center bg-gray-200 text-gray-800 px-6 py-3 rounded-lg text-md font-semibold hover:bg-gray-300 transition-colors",
                                ),
                                rx.el.button(
                                    rx.icon("share-2", class_name="h-5 w-5 mr-2"),
                                    "Share Profile",
                                    class_name="w-full flex items-center justify-center bg-gray-200 text-gray-800 px-6 py-3 rounded-lg text-md font-semibold hover:bg-gray-300 transition-colors",
                                ),
                                class_name="space-y-4",
                            ),
                            class_name="w-full lg:w-1/3 p-6 bg-white rounded-xl border border-gray-200 shadow-sm h-fit lg:sticky top-24",
                        ),
                        class_name="flex flex-col lg:flex-row gap-12",
                    ),
                    class_name="container mx-auto py-12 px-4",
                ),
                rx.el.div(
                    rx.icon(
                        "flag_triangle_right", class_name="h-16 w-16 text-red-500 mb-4"
                    ),
                    rx.el.h2(
                        "Provider Not Found",
                        class_name="text-2xl font-bold text-gray-800",
                    ),
                    rx.el.p(
                        "The provider you are looking for does not exist.",
                        class_name="text-gray-600 mt-2",
                    ),
                    rx.el.a(
                        "Go back to search",
                        href="/search",
                        class_name="mt-6 text-teal-600 font-semibold hover:underline",
                    ),
                    class_name="flex flex-col items-center justify-center h-[50vh] text-center",
                ),
            )
        ),
        footer(),
        class_name="bg-gray-50 font-['Inter'] min-h-screen",
    )