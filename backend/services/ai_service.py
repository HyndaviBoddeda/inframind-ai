import os
import requests
from dotenv import load_dotenv

from services.log_services import analyze_log

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def analyze_with_ai(log_text: str):

    if not OPENAI_API_KEY:
        fallback_result = analyze_log(log_text)
        return {
            "mode": "fallback",
            "reason": "OpenAI API key not configured",
            "analysis": fallback_result
        }

    prompt = f"""
You are an expert Cloud Operations SRE Copilot.

Analyze this infrastructure log or incident:

{log_text}

Return:
1. Incident type
2. Severity
3. Likely root cause
4. Recommended remediation steps
5. Prevention recommendations
"""

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a senior cloud infrastructure AI copilot."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3
            },
            timeout=15
        )

        data = response.json()

        if response.status_code != 200:
            fallback_result = analyze_log(log_text)
            return {
                "mode": "fallback",
                "reason": data.get("error", {}).get("message", "OpenAI request failed"),
                "analysis": fallback_result
            }

        return {
            "mode": "openai",
            "analysis": data
        }

    except Exception as error:
        fallback_result = analyze_log(log_text)
        return {
            "mode": "fallback",
            "reason": str(error),
            "analysis": fallback_result
        }