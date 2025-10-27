import reflex as rx
from app.components import header, footer
from app.state import UIState, ProviderApplication
from typing import Any


class RegistrationState(rx.State):
    form_data: ProviderApplication = {
        "full_name": "",
        "business_name": "",
        "category": "",
        "phone_number": "",
        "whatsapp_number": "",
        "address": "",
        "city": "",
        "description": "",
        "plan": "basic",
    }
    payment_screenshot: list[str] = []
    form_submitted: bool = False

    @rx.event
    def handle_form_change(self, field: str, value: str):
        self.form_data[field] = value

    @rx.event
    async def handle_screenshot_upload(self, files: list[rx.UploadFile]):
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.name
            with outfile.open("wb") as f:
                f.write(upload_data)
            self.payment_screenshot.append(file.name)

    @rx.event
    async def submit_application(self, form_data: dict[str, Any]):
        screenshot_file = self.payment_screenshot[0] if self.payment_screenshot else ""
        if self.form_data["plan"] != "basic":
            from app.states.admin_payment_submissions_state import (
                AdminPaymentSubmissionsState,
            )

            submission_state = await self.get_state(AdminPaymentSubmissionsState)
            submission_state.add_submission(self.form_data, screenshot_file)
        else:
            from app.states.admin_listings_state import AdminListingsState

            listing_state = await self.get_state(AdminListingsState)
            listing_data = {
                "id": len(listing_state.all_listings) + 1,
                "name": self.form_data["business_name"],
                "category": self.form_data["category"],
                "location": self.form_data["address"],
                "rating": 0.0,
                "reviews": 0,
                "image_url": f"https://api.dicebear.com/9.x/notionists/svg?seed={self.form_data['business_name'].replace(' ', '')}",
                "featured": False,
            }
            listing_state.all_listings.append(listing_data)
            await listing_state.sync_ui_state_providers()
        self.form_submitted = True


def form_field(
    label: str, name: str, placeholder: str, type: str = "text"
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700"),
        rx.el.input(
            name=name,
            placeholder=placeholder,
            type=type,
            on_change=lambda val: RegistrationState.handle_form_change(name, val),
            class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm",
        ),
        class_name="col-span-12 sm:col-span-6",
    )


def pricing_card(
    plan_name: str, price: str, features: list[str], plan_id: str
) -> rx.Component:
    is_selected = RegistrationState.form_data["plan"] == plan_id
    return rx.el.div(
        rx.el.div(
            rx.el.h3(plan_name, class_name="text-xl font-bold text-gray-800"),
            rx.el.p(price, class_name="mt-2 text-3xl font-extrabold text-gray-900"),
            rx.el.ul(
                rx.foreach(
                    features,
                    lambda feature: rx.el.li(
                        rx.icon(
                            "check_check", class_name="h-5 w-5 text-green-500 mr-2"
                        ),
                        feature,
                        class_name="flex items-center text-gray-600",
                    ),
                ),
                class_name="mt-6 space-y-3",
            ),
        ),
        on_click=lambda: RegistrationState.handle_form_change("plan", plan_id),
        class_name=rx.cond(
            is_selected,
            "p-6 bg-white rounded-xl border-2 border-teal-500 shadow-lg cursor-pointer transform scale-105",
            "p-6 bg-white rounded-xl border border-gray-200 shadow-sm cursor-pointer hover:shadow-md transition-shadow",
        ),
    )


def get_listed_page() -> rx.Component:
    return rx.el.div(
        header(),
        rx.el.main(
            rx.el.section(
                rx.el.div(
                    rx.el.h1(
                        "Get Your Business Listed on Urban Hand",
                        class_name="text-4xl font-extrabold text-gray-900 tracking-tight",
                    ),
                    rx.el.p(
                        "Reach more local customers. List your service today and grow your business.",
                        class_name="mt-4 text-lg text-gray-600 max-w-3xl mx-auto",
                    ),
                    class_name="text-center py-12 md:py-16",
                )
            ),
            rx.el.section(
                rx.el.div(
                    rx.el.h2(
                        "Choose Your Plan",
                        class_name="text-3xl font-bold text-center text-gray-800 mb-10",
                    ),
                    rx.el.div(
                        pricing_card(
                            "Basic",
                            "₹0 Free",
                            [
                                "Appear in normal search results",
                                "Customers can call/WhatsApp",
                                "Can get reviews",
                            ],
                            "basic",
                        ),
                        pricing_card(
                            "Featured",
                            "₹199 / month",
                            [
                                "Appears at top of category & home screen",
                                "Verified badge",
                                "Highlighted card design",
                                "Shared on Urban Hand Instagram",
                            ],
                            "featured",
                        ),
                        pricing_card(
                            "Premium Partner",
                            "₹499 / 3 months",
                            [
                                "All Featured benefits",
                                "Social media promotion once a month",
                                "'Verified Partner' tag",
                                "Direct link in city spotlight",
                            ],
                            "premium",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto",
                    ),
                    class_name="py-16 bg-gray-50",
                )
            ),
            rx.el.section(
                rx.el.div(
                    rx.el.h2(
                        "Tell Us About Your Business",
                        class_name="text-3xl font-bold text-center text-gray-800 mb-10",
                    ),
                    rx.el.form(
                        rx.el.div(
                            form_field("Full Name", "full_name", "e.g. Suresh Sharma"),
                            form_field(
                                "Business Name",
                                "business_name",
                                "e.g. Sharma Electricals",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Category",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.select(
                                    rx.el.option(
                                        "Select Category", value="", disabled=True
                                    ),
                                    rx.foreach(
                                        UIState.service_categories,
                                        lambda cat: rx.el.option(
                                            cat["name"], value=cat["name"]
                                        ),
                                    ),
                                    on_change=lambda val: RegistrationState.handle_form_change(
                                        "category", val
                                    ),
                                    name="category",
                                    class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm rounded-md",
                                ),
                                class_name="col-span-12 sm:col-span-6",
                            ),
                            form_field(
                                "Phone Number",
                                "phone_number",
                                "e.g. 9876543210",
                                type="tel",
                            ),
                            form_field(
                                "WhatsApp Number",
                                "whatsapp_number",
                                "e.g. 9876543210",
                                type="tel",
                            ),
                            form_field("Address", "address", "e.g. 123, Main Market"),
                            form_field(
                                "City / Area", "city", "e.g. Malviya Nagar, Jaipur"
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Description of Services",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.textarea(
                                    name="description",
                                    placeholder="Tell customers about what you do...",
                                    on_change=lambda val: RegistrationState.handle_form_change(
                                        "description", val
                                    ),
                                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm",
                                    rows=4,
                                ),
                                class_name="col-span-12",
                            ),
                            rx.el.div(
                                rx.el.label(
                                    "Business Photo",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.upload.root(
                                    rx.el.div(
                                        rx.el.p("Drag and drop or click to upload"),
                                        border="1px dotted rgb(107,114,128)",
                                        padding="2em",
                                        class_name="text-center mt-1",
                                    )
                                ),
                                class_name="col-span-12",
                            ),
                            class_name="grid grid-cols-12 gap-6",
                        ),
                        rx.cond(
                            RegistrationState.form_data["plan"] != "basic",
                            rx.el.div(
                                rx.el.h3(
                                    "Complete Your Payment",
                                    class_name="text-2xl font-bold text-gray-800 mt-12 mb-4",
                                ),
                                rx.el.p(
                                    "To activate your premium plan, please make the payment using the UPI details below and upload a screenshot of the transaction.",
                                    class_name="text-gray-600 mb-6",
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.icon(
                                            "qr-code",
                                            class_name="h-24 w-24 text-gray-400",
                                        ),
                                        class_name="w-48 h-48 mx-auto border border-dashed rounded-lg flex items-center justify-center bg-white",
                                    ),
                                    rx.el.p(
                                        "UPI ID: ",
                                        rx.el.strong("urbanhand@upi"),
                                        class_name="text-center mt-4 font-medium text-gray-700",
                                    ),
                                    class_name="p-6 bg-gray-50 rounded-lg",
                                ),
                                rx.el.div(
                                    rx.el.label(
                                        "Upload Payment Screenshot",
                                        class_name="block text-sm font-medium text-gray-700 mt-6",
                                    ),
                                    rx.upload.root(
                                        rx.el.div(
                                            rx.el.p(
                                                "Drag and drop or click to upload screenshot"
                                            ),
                                            border="1px dotted rgb(107,114,128)",
                                            padding="2em",
                                            class_name="text-center mt-1",
                                        ),
                                        id="screenshot-upload",
                                        on_drop=RegistrationState.handle_screenshot_upload,
                                        multiple=False,
                                    ),
                                    rx.foreach(
                                        RegistrationState.payment_screenshot,
                                        lambda s: rx.el.p(f"Uploaded: {s}"),
                                    ),
                                    class_name="mt-4",
                                ),
                            ),
                            None,
                        ),
                        rx.el.div(
                            rx.el.button(
                                "Submit Application",
                                type="submit",
                                class_name="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-teal-600 hover:bg-teal-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-500",
                            ),
                            class_name="mt-8",
                        ),
                        on_submit=RegistrationState.submit_application,
                        class_name="max-w-3xl mx-auto",
                    ),
                    class_name="py-16",
                )
            ),
            rx.cond(
                RegistrationState.form_submitted,
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Application Submitted!",
                            class_name="text-2xl font-bold text-green-700",
                        ),
                        rx.el.p(
                            "Thank you for registering. Our team will review your application and you will be notified upon approval.",
                            class_name="mt-2 text-gray-600",
                        ),
                        class_name="p-8 bg-green-50 rounded-xl border border-green-200 text-center",
                    ),
                    class_name="fixed top-0 left-0 w-screen h-screen bg-black/50 flex items-center justify-center z-50",
                ),
                None,
            ),
        ),
        footer(),
        class_name="bg-white font-['Inter']",
    )