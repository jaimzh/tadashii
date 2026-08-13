import random

import requests

from app.config import ANIMECHAN_BASE_URL, ANIMECHAN_TIMEOUT_SECONDS

CURATED_ANIME = [
    "Tengen Toppa Gurren Lagann",
    "Naruto",
    "Shingeki no Kyojin",
    "Vinland Saga",
    "One Piece",
    "Fullmetal Alchemist: Brotherhood",
    "Hunter x Hunter",
    "Cowboy Bebop",
    "Death Note",
    "Steins;Gate",
    "Code Geass",
    "Kimetsu no Yaiba",
    "Mob Psycho 100",
    "Boku no Hero Academia",
    "Jujutsu Kaisen",
]

QUOTES_PER_LIST = 5


def _name(value) -> str | None:
    if isinstance(value, str):
        return value.strip() or None

    if isinstance(value, dict):
        name = value.get("name")
        if isinstance(name, str):
            return name.strip() or None

    return None


def _quote_items(payload) -> list[dict]:
    if isinstance(payload, list):
        return payload

    if not isinstance(payload, dict):
        return []

    data = payload.get("data")
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        return [data]

    return []


def _normalize_quotes(payload, fallback_anime: str) -> list[dict]:
    quotes = []
    seen = set()

    for raw_quote in _quote_items(payload):
        if not isinstance(raw_quote, dict):
            continue

        content = raw_quote.get("content") or raw_quote.get("quote")
        if not isinstance(content, str):
            continue

        content = content.strip()
        key = content.casefold()
        if not content or key in seen:
            continue

        character = _name(raw_quote.get("character"))
        anime = _name(raw_quote.get("anime")) or fallback_anime
        if not character:
            continue

        quotes.append(
            {
                "content": content,
                "character": character,
                "anime": anime,
            }
        )
        seen.add(key)

        if len(quotes) == QUOTES_PER_LIST:
            break

    return quotes


def get_quote_list() -> dict:
    anime = random.choice(CURATED_ANIME)

    try:
        response = requests.get(
            f"{ANIMECHAN_BASE_URL.rstrip('/')}/quotes",
            params={"anime": anime},
            timeout=ANIMECHAN_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        quotes = _normalize_quotes(response.json(), anime)
    except (requests.RequestException, ValueError) as exc:
        raise RuntimeError(str(exc)) from exc

    if not quotes:
        raise RuntimeError(f"Animechan returned no usable quotes for {anime}")

    return {"anime": anime, "quotes": quotes}
