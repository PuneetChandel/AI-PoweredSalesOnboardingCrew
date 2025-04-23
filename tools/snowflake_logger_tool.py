from crewai.tools import BaseTool
import os
import json
import snowflake.connector

class SnowflakeLoggerTool(BaseTool):
    name: str = "Snowflake Logger Tool"
    description: str = "Logs structured task output into a Snowflake table"

    def _run(self, input: dict) -> dict:
        print("Snowflake Logger received raw input:", input)

        if isinstance(input, str):
            try:
                input = json.loads(input)
            except Exception:
                return {"status": "error", "error": "Input is not valid JSON string"}

        for _ in range(3):
            if isinstance(input, dict) and any(k in input for k in ("input", "description")):
                for key in ("input", "description"):
                    if isinstance(input.get(key), dict):
                        input = input[key]
                        break
            else:
                break

        step = input.get("step", "unspecified")
        payload = input.get("payload", input)  # fallback to whole input

        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception:
                return {"status": "error", "error": "Payload is not valid JSON"}

        print("📦 Step:", step)
        print("📥 Payload to Snowflake:", payload)

        try:
            conn = snowflake.connector.connect(
                user=os.getenv("SNOWFLAKE_USER"),
                password=os.getenv("SNOWFLAKE_PASSWORD"),
                account=os.getenv("SNOWFLAKE_ACCOUNT"),
                warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
                database=os.getenv("SNOWFLAKE_DATABASE"),
                schema=os.getenv("SNOWFLAKE_SCHEMA"),
            )

            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO agent_logs (step, payload_json)
                SELECT %s, PARSE_JSON(%s)
            """, (step, json.dumps(payload)))
            conn.commit()
            return {"status": "success", "message": f"Logged step '{step}' to Snowflake"}

        except Exception as e:
            return {"status": "error", "error": str(e)}

