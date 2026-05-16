import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def analyze_with_ai(log_text: str):

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
        }
    )

    return response.json()