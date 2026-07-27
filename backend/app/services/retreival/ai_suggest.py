import json
from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)


    def suggest_anime(intent: dict):

    prompt = f"""
You are an anime recommendation engine.

Given this user intent:
{intent}

Suggest 5-10 or as much anime titles that best match.

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
        model=GEMINI_MODEL,
        contents=prompt
    )

    return json.loads(response.text)
