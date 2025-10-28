import reflex as rx
from typing import TypedDict, Any
import uuid
from app.services.firebase_service import get_pricing_plans, save_pricing_plans


class PricingPlan(TypedDict):
    id: str
    name: str
    price: int
    duration: str
    features: list[str]
    active: bool


class AdminPaymentPlansState(rx.State):
    """State for managing pricing plans and payment settings."""

    pricing_plans: list[PricingPlan] = []
    upi_id: str = "urbanhand@upi"
    qr_code_url: str = ""
    payment_instructions: str = (
        "Please make the payment using the UPI details and upload a screenshot."
    )
    show_plan_modal: bool = False
    modal_is_editing: bool = False
    modal_plan_data: PricingPlan = {
        "id": "",
        "name": "",
        "price": 0,
        "duration": "Monthly",
        "features": [],
        "active": True,
    }
    modal_feature_input: str = ""

    @rx.event
    async def load_default_plans(self):
        plans = await get_pricing_plans()
        if plans:
            self.pricing_plans = plans
        elif not self.pricing_plans:
            self.pricing_plans = [
                {
                    "id": str(uuid.uuid4()),
                    "name": "Basic",
                    "price": 0,
                    "duration": "Lifetime",
                    "features": [
                        "Appear in normal search results",
                        "Customers can call/WhatsApp",
                        "Can get reviews",
                    ],
                    "active": True,
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "Featured",
                    "price": 199,
                    "duration": "Monthly",
                    "features": [
                        "Appears at top of category & home screen",
                        "Verified badge",
                        "Highlighted card design",
                    ],
                    "active": True,
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "Premium Partner",
                    "price": 499,
                    "duration": "3 Months",
                    "features": [
                        "All Featured benefits",
                        "Social media promotion once a month",
                        "'Verified Partner' tag",
                    ],
                    "active": True,
                },
            ]
            await save_pricing_plans(self.pricing_plans)

    def _get_plan_index_by_id(self, plan_id: str) -> int:
        for i, plan in enumerate(self.pricing_plans):
            if plan["id"] == plan_id:
                return i
        return -1

    @rx.event
    def open_add_modal(self):
        self.modal_is_editing = False
        self.modal_plan_data = {
            "id": str(uuid.uuid4()),
            "name": "",
            "price": 0,
            "duration": "Monthly",
            "features": [],
            "active": True,
        }
        self.show_plan_modal = True

    @rx.event
    def open_edit_modal(self, plan: PricingPlan):
        self.modal_is_editing = True
        self.modal_plan_data = plan.copy()
        self.show_plan_modal = True

    @rx.event
    def close_plan_modal(self):
        self.show_plan_modal = False

    @rx.event
    def handle_modal_plan_change(self, field: str, value: Any):
        self.modal_plan_data[field] = value

    @rx.event
    def add_feature_to_modal(self):
        if self.modal_feature_input:
            self.modal_plan_data["features"].append(self.modal_feature_input)
            self.modal_feature_input = ""

    @rx.event
    def remove_feature_from_modal(self, feature: str):
        self.modal_plan_data["features"] = [
            f for f in self.modal_plan_data["features"] if f != feature
        ]

    @rx.event
    async def save_plan(self):
        if self.modal_is_editing:
            index = self._get_plan_index_by_id(self.modal_plan_data["id"])
            if index != -1:
                self.pricing_plans[index] = self.modal_plan_data
        else:
            self.pricing_plans.append(self.modal_plan_data)
        await save_pricing_plans(self.pricing_plans)
        self.close_plan_modal()

    @rx.event
    def toggle_plan_status(self, plan_id: str):
        index = self._get_plan_index_by_id(plan_id)
        if index != -1:
            self.pricing_plans[index]["active"] = not self.pricing_plans[index][
                "active"
            ]

    @rx.event
    async def delete_plan(self, plan_id: str):
        self.pricing_plans = [p for p in self.pricing_plans if p["id"] != plan_id]
        await save_pricing_plans(self.pricing_plans)