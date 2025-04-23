from crewai.tools import BaseTool
from schemas.lead import Lead
from simple_salesforce import Salesforce
from pydantic import ValidationError
import os
import json

class SalesforceAPITool(BaseTool):
    name: str = "Salesforce Account Creator"
    description: str = "Creates a Salesforce account record from lead data"

    def _run(self, input: dict) -> dict:
        print("🔍 Salesforce Tool received raw input:", input)

        if isinstance(input, str):
            try:
                input = json.loads(input)
            except json.JSONDecodeError:
                return {"status": "error", "error": "Invalid input: not a valid JSON string"}

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
                "error": "Validation failed",
                "details": e.errors(),
                "raw_input": input
            }

        access_token = os.getenv("SF_ACCESS_TOKEN")
        instance_url = os.getenv("SF_INSTANCE_URL")

        if not access_token or not instance_url:
            return {"status": "error", "error": "Missing Salesforce credentials"}

        data = {
            "Name": lead.name,
            "Phone": lead.phone,
            "Website": lead.website,
            "BillingStreet": lead.address
        }

        try:
            sf = Salesforce(instance_url=instance_url, session_id=access_token)
            result = sf.Account.create(data)
            return {
                "status": "success",
                "account_id": result.get("id"),
                "input_data": data
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "input_data": data
            }
