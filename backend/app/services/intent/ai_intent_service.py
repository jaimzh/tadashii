# app/services/ai_intent_service.py

import json
from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)


def analyze_prompt(user_prompt: str):

    prompt = f"""
You are an anime intent parser for a recommendation system.

Analyze the user request and return ONLY valid JSON.

User prompt:
"{user_prompt}"

Return:

{{
  "search_keywords": [],
  "semantic_tags": [],
  "themes": [],
  "mood": "",
  "genres": [],
  "character_arc": ""
}}

Rules:

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

- maximum 5 keywords

Return JSON only.
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL, contents=prompt
    )

    return json.loads(response.text)
