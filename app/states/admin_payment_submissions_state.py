import reflex as rx
from typing import TypedDict, Any
import datetime
import uuid


class PaymentSubmission(TypedDict):
    id: str
    applicant_name: str
    business_name: str
    plan_selected: str
    amount: int
    screenshot_url: str
    submit_date: str
    status: str
    notes: str
    application_data: dict


class AdminPaymentSubmissionsState(rx.State):
    """State for managing payment submissions."""

    payment_submissions: list[PaymentSubmission] = []
    status_filter: str = "All"
    show_review_modal: bool = False
    selected_submission: PaymentSubmission | None = None
    rejection_notes: str = ""

    @rx.event
    async def add_submission(self, application_data: dict, screenshot_file: str):
        from app.states.admin_payment_plans_state import AdminPaymentPlansState

        plan_name = application_data.get("plan", "basic")
        plans_state = await self.get_state(AdminPaymentPlansState)
        plan_price = 0
        for plan in plans_state.pricing_plans:
            if plan["name"].lower() == plan_name:
                plan_price = plan["price"]
                break
        submission = PaymentSubmission(
            id=str(uuid.uuid4()),
            applicant_name=application_data.get("full_name", ""),
            business_name=application_data.get("business_name", ""),
            plan_selected=plan_name.capitalize(),
            amount=plan_price,
            screenshot_url=screenshot_file,
            submit_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            status="Pending",
            notes="",
            application_data=application_data,
        )
        self.payment_submissions.append(submission)

    @rx.event
    def open_review_modal(self, submission: PaymentSubmission):
        self.selected_submission = submission
        self.rejection_notes = ""
        self.show_review_modal = True

    @rx.event
    def close_review_modal(self):
        self.show_review_modal = False
        self.selected_submission = None

    @rx.event
    async def approve_payment(self):
        if self.selected_submission:
            self.selected_submission["status"] = "Approved"
            from app.states.admin_listings_state import AdminListingsState

            listing_state = await self.get_state(AdminListingsState)
            app_data = self.selected_submission["application_data"]
            listing_data = {
                "id": len(listing_state.all_listings) + 1,
                "name": app_data["business_name"],
                "category": app_data["category"],
                "location": app_data["address"],
                "rating": 0.0,
                "reviews": 0,
                "image_url": f"https://api.dicebear.com/9.x/notionists/svg?seed={app_data['business_name'].replace(' ', '')}",
                "featured": self.selected_submission["plan_selected"] != "Basic",
            }
            listing_state.all_listings.append(listing_data)
            await listing_state.sync_ui_state_providers()
            self.close_review_modal()

    @rx.event
    def reject_payment(self):
        if self.selected_submission:
            self.selected_submission["status"] = "Rejected"
            self.selected_submission["notes"] = self.rejection_notes
            self.close_review_modal()

    @rx.var
    def filtered_submissions(self) -> list[PaymentSubmission]:
        if self.status_filter == "All":
            return self.payment_submissions
        return [
            s for s in self.payment_submissions if s["status"] == self.status_filter
        ]