# app/services/ranking_service.py

from google import genai
import json

from app.config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_TIMEOUT_MS

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={
        "timeout": GEMINI_TIMEOUT_MS,
        "retry_options": {"attempts": 1},
    },
)
TARGET_RECOMMENDATION_COUNT = 10


def build_rank_payload(anime_list: list):
    payload = []

    for anime in anime_list[:30]:
        if hasattr(anime, "model_dump"):
            payload.append(anime.model_dump())
        else:
            payload.append(anime)

    return payload


def rank_anime(prompt: str, intent: dict, anime_list: list):
    anime_payload = build_rank_payload(anime_list)

    if not anime_payload:
        return []

    requested_count = min(TARGET_RECOMMENDATION_COUNT, len(anime_payload))

    prompt_payload = f"""
You are an anime ranking engine.

Your job is to score how well each anime matches the user's intent.

USER PROMPT:
{prompt}

INTENT:
{json.dumps(intent, indent=2)}

ANIME LIST:
{json.dumps(anime_payload, indent=2)}

Return ONLY valid JSON:

[
  {{
    "mal_id": 0,
    "title": "",
    "prompt_match": 0,
    "reason": "",
    "emotion_tags": []
  }}
]

Rules:
- Return exactly {requested_count} recommendations
- If fewer than {TARGET_RECOMMENDATION_COUNT} candidates are provided, return every candidate
- prompt_match must be a number from 0 to 100
- Score based on STORY + THEMES + CHARACTER ARC + SYNOPSIS
- NOT popularity or rating
- Be strict and reasoning-based
- Write a specific 1-2 sentence reason explaining how the anime's story,
  themes, or character journey connects to the user's exact request
- Mention concrete details from the provided synopsis instead of generic praise
- Keep each reason under 45 words and do not reveal spoilers
- Return sorted highest match first
- Return only anime from the provided ANIME LIST
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt_payload
    )

    rankings = json.loads(response.text)

    if not isinstance(rankings, list):
        raise ValueError("Ranking model returned a non-list response")

    return rankings[:requested_count]
