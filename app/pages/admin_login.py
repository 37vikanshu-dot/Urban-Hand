import reflex as rx
from app.states.admin_state import AdminState


def admin_login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon("shield-check", class_name="h-8 w-8 text-teal-500"),
                        rx.el.span(
                            "Urban Hand Admin",
                            class_name="font-bold text-2xl text-gray-800",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    href="/",
                ),
                rx.el.h2(
                    "Admin Panel Login",
                    class_name="mt-6 text-xl font-semibold text-gray-700",
                ),
                class_name="text-center",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Email Address",
                        class_name="block text-sm font-medium text-gray-700",
                    ),
                    rx.el.input(
                        type="email",
                        placeholder="admin@example.com",
                        name="email",
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm",
                        required=True,
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Password", class_name="block text-sm font-medium text-gray-700"
                    ),
                    rx.el.input(
                        type="password",
                        name="password",
                        class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm",
                        required=True,
                    ),
                    class_name="mb-6",
                ),
                rx.cond(
                    AdminState.error_message != "",
                    rx.el.div(
                        rx.icon("badge_alert", class_name="h-4 w-4 mr-2"),
                        AdminState.error_message,
                        class_name="flex items-center text-sm text-red-600 bg-red-50 p-3 rounded-md mb-4",
                    ),
                    None,
                ),
                rx.el.button(
                    "Login to Admin Panel",
                    type="submit",
                    class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500",
                ),
                on_submit=AdminState.handle_login_submit,
                class_name="mt-8",
            ),
            class_name="max-w-md w-full mx-auto bg-white p-8 border border-gray-200 rounded-xl shadow-sm",
        ),
        class_name="min-h-screen flex items-center justify-center bg-gray-50 font-['Inter']",
    )