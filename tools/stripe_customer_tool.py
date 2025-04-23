from crewai.tools import BaseTool
from schemas.lead import Lead
import stripe
import os
import json
from pydantic import ValidationError

class StripeCustomerTool(BaseTool):
    name: str = "Stripe Customer Creator"
    description: str = "Creates a Stripe customer and generates a Checkout link to collect card details"

    def _run(self, input: dict) -> dict:
        print("🔍 Stripe Tool received raw input:", input)

        if isinstance(input, str):
            try:
                input = json.loads(input)
            except json.JSONDecodeError:
                return {"status": "error", "error": "Invalid input: not valid JSON"}

        for _ in range(3):
            if isinstance(input, dict) and any(k in input for k in ("input", "description", "metadata")):
                for key in ("input", "description", "metadata"):
                    if key in input and isinstance(input[key], dict):
                        input = input[key]
                        break
            else:
                break

        input.pop("type", None)

        try:
            lead = Lead(**input)
        except ValidationError as e:
            return {
                "status": "error",
                "error": "Lead validation failed",
                "details": e.errors(),
                "raw_input": input
            }

        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

        try:
            customer = stripe.Customer.create(
                name=lead.name,
                email=lead.email,
                phone=lead.phone
            )
            session = stripe.checkout.Session.create(
                customer=customer.id,
                mode="setup",
                payment_method_types=["card"],
                success_url="https://checkout.stripe.com/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="https://checkout.stripe.com/success/cancel"
            )
            return {
                "status": "success",
                "customer_id": customer.id,
                "card_setup_link": session.url
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "input_data": lead.dict()
            }
