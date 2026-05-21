# app/services/ranking_service.py

from google import genai
import os
import json

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def rank_anime(prompt: str, intent: dict, anime_list: list):

    prompt_payload = f"""
You are an anime ranking engine.

Your job is to score how well each anime matches the user's intent.

USER PROMPT:
{prompt}

INTENT:
{json.dumps(intent, indent=2)}

ANIME LIST:
{json.dumps(anime_list[:30], indent=2)}

Return ONLY valid JSON:

[
  {{
    "mal_id": 0,
    "title": "",
    "prompt_match": 0-100,
    "reason": "",
    "emotion_tags": []
  }}
]

Rules:
- Score based on STORY + THEMES + CHARACTER ARC + SYNOPSIS
- NOT popularity or rating
- Be strict and reasoning-based
- Keep reason under 20 words
- Return sorted highest match first
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt_payload
    )

    return json.loads(response.text)