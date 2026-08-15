# app/services/ranking_service.py

from google import genai
from google.genai.errors import ServerError
import json
from time import sleep

from app.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GEMINI_RANKING_RETRY_DELAY_SECONDS,
    GEMINI_TIMEOUT_MS,
)
from app.observability.pipeline_timing import logger

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={
        "timeout": GEMINI_TIMEOUT_MS,
        "retry_options": {"attempts": 1},
    },
)
TARGET_RECOMMENDATION_COUNT = 10
RANKING_MAX_ATTEMPTS = 2


def build_rank_payload(anime_list: list):
    payload = []

    for anime in anime_list[:30]:
        if hasattr(anime, "model_dump"):
            payload.append(anime.model_dump())
        else:
            payload.append(anime)

    return payload


def _generate_rankings(prompt_payload: str, request_id: str | None):
    for attempt in range(1, RANKING_MAX_ATTEMPTS + 1):
        try:
            return client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt_payload,
            )
        except ServerError as exc:
            should_retry = exc.code == 503 and attempt < RANKING_MAX_ATTEMPTS

            if not should_retry:
                raise

            logger.warning(
                "request=%s service=gemini stage=ranking status=retry "
                "http_status=503 attempt=%d next_attempt=%d delay_s=%.1f",
                request_id or "untracked",
                attempt,
                attempt + 1,
                GEMINI_RANKING_RETRY_DELAY_SECONDS,
            )
            sleep(GEMINI_RANKING_RETRY_DELAY_SECONDS)


def rank_anime(
    prompt: str,
    intent: dict,
    anime_list: list,
    request_id: str | None = None,
):
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

    response = _generate_rankings(prompt_payload, request_id)

    rankings = json.loads(response.text)

    if not isinstance(rankings, list):
        raise ValueError("Ranking model returned a non-list response")

    return rankings[:requested_count]
