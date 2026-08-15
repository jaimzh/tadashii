# app/services/ai_intent_service.py

import json
from google import genai

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GEMINI_TIMEOUT_MS,
    INTENT_KEYWORD_LIMIT,
)
from app.models.schema import IntentAnalysis

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={
        "timeout": GEMINI_TIMEOUT_MS,
        "retry_options": {"attempts": 1},
    },
)


def analyze_prompt(user_prompt: str):

    prompt = f"""
You are an anime intent parser for a recommendation system.

Analyze the user request and return ONLY valid JSON.

User prompt:
{json.dumps(user_prompt)}

Return:

{{
  "is_valid_prompt": true,
  "validation_reason": "",
  "search_keywords": [],
  "semantic_tags": [],
  "themes": [],
  "mood": "",
  "genres": [],
  "character_arc": ""
}}

Rules:

- is_valid_prompt:
  true only when the prompt is understandable and can reasonably be used to
  recommend or discover anime. Short but meaningful requests such as
  "romance anime", "something like Naruto", or "sad found-family story" are valid.
  Random characters, gibberish, unrelated requests, and text with no
  understandable anime preference are invalid.

- validation_reason:
  Empty when valid. When invalid, briefly explain what the user should provide.

- When is_valid_prompt is false, return empty search fields.

- search_keywords:
  Short searchable anime terms only.
  Must work well with anime databases.
  Examples:
  ["underdog", "training", "revenge", "friendship"]

- semantic_tags:
  Broader concepts and meanings.
  Examples:
  ["zero to hero", "self growth"]

- genres:
  Use real anime genres only

- maximum {INTENT_KEYWORD_LIMIT} keywords

Return JSON only.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL, contents=prompt
    )

    parsed = IntentAnalysis.model_validate(json.loads(response.text)).model_dump()
    parsed["search_keywords"] = parsed["search_keywords"][:INTENT_KEYWORD_LIMIT]
    return parsed
