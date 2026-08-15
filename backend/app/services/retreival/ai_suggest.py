import json
from google import genai

from app.config import (
    AI_SUGGESTION_MAX_COUNT,
    AI_SUGGESTION_MIN_COUNT,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GEMINI_TIMEOUT_MS,
)

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

Suggest {AI_SUGGESTION_MIN_COUNT}-{AI_SUGGESTION_MAX_COUNT} anime titles that best match.

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

    parsed = json.loads(response.text)
    suggestions = parsed.get("suggested_anime") or []
    parsed["suggested_anime"] = suggestions[:AI_SUGGESTION_MAX_COUNT]
    return parsed
