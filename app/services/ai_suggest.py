import json
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def suggest_anime(intent: dict):

    prompt = f"""
You are an anime recommendation engine.

Given this user intent:
{intent}

Suggest 5–10 or as much anime titles that best match.

Rules:
- Only return anime titles that actually exist
- Focus on well-known anime first
- Return JSON only

Return format:
{{
  "suggested_anime": []
}}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return json.loads(response.text)