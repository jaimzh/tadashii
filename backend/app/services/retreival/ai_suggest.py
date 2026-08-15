import json
from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_TIMEOUT_MS

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={
        "timeout": GEMINI_TIMEOUT_MS,
        "retry_options": {"attempts": 1},
    },
)


def suggest_anime(user_prompt: str):

    prompt = f"""
You are an anime recommendation engine.

Given this user request:
{json.dumps(user_prompt)}

Suggest 5-10 or as much anime titles that best match.

Rules:
- If the request is gibberish, unrelated to anime discovery, or not
  understandable enough to recommend anime, return an empty list
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
