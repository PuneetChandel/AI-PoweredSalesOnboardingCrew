from crewai.tools import BaseTool
from schemas.lead import Lead
import json
from pydantic import ValidationError

class CalendlyLinkGeneratorTool(BaseTool):
    name: str = "Calendly Link Generator"
    description: str = "Generates a personalized Calendly link with pre-filled email and name"

    def _run(self, input: dict) -> dict:
        print("🔍 Calendly Tool received raw input:", input)

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

        calendly_base_url = "https://calendly.com/pcchan/intro-call"

        try:
            lead = Lead(**input)
            link = f"{calendly_base_url}?name={lead.name}&email={lead.email}"
            return {
                "status": "success",
                "calendly_link": link,
                "input_data": lead.dict()
            }
        except Exception as e:
            return {
                "status": "fallback",
                "calendly_link": calendly_base_url,
                "error": f"Failed to personalize link: {str(e)}",
                "raw_input": input
            }
