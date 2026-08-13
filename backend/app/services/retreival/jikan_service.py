import time

import requests

from app.config import JIKAN_BASE_URL, JIKAN_SEARCH_LIMIT

MAX_INTENT_SEARCH_TERMS = 8
MAX_QUERY_LENGTH = 80
JIKAN_TIMEOUT_SECONDS = 10
JIKAN_RETRY_COUNT = 2


def _named_items(items: list | None) -> list[dict]:
    normalized = []

    for item in items or []:
        if isinstance(item, str):
            normalized.append({"name": item})
        elif isinstance(item, dict):
            normalized.append(item)

    return normalized


def adapt_anime_result(anime: dict) -> dict:
    """Convert a jikan-edge search item to the Jikan v4 shape used downstream."""
    if "malId" not in anime:
        return anime

    edge_images = anime.get("images") or {}
    image_url = (
        edge_images.get("large")
        or edge_images.get("medium")
        or anime.get("imageUrl")
    )

    trailer = anime.get("trailer") or {}
    titles = anime.get("titles") or []

    def title_by_type(title_type: str) -> str | None:
        for item in titles:
            if isinstance(item, dict) and item.get("type") == title_type:
                return item.get("title")

        return None

    return {
        "mal_id": anime.get("malId"),
        "url": anime.get("url"),
        "title": anime.get("title"),
        "title_english": anime.get("titleEnglish") or title_by_type("English"),
        "title_japanese": (
            anime.get("titleJapanese")
            or anime.get("title_japanese")
            or title_by_type("Japanese")
        ),
        "title_synonyms": anime.get("titleSynonyms") or [],
        "type": anime.get("type"),
        "source": anime.get("source"),
        "episodes": anime.get("episodes"),
        "status": anime.get("status"),
        "airing": anime.get("airing"),
        "synopsis": anime.get("synopsis"),
        "background": anime.get("background"),
        "season": anime.get("season"),
        "year": anime.get("year"),
        "rating": anime.get("rating"),
        "score": anime.get("score"),
        "genres": _named_items(anime.get("genres")),
        "explicit_genres": _named_items(anime.get("explicitGenres")),
        "themes": _named_items(anime.get("themes")),
        "demographics": _named_items(anime.get("demographics")),
        "studios": _named_items(anime.get("studios")),
        "images": {"jpg": {"image_url": anime.get("imageUrl"), "large_image_url": image_url}},
        "trailer": {"url": trailer.get("url") or anime.get("trailerUrl")},
        "data_source": "jikan-edge",
    }


def get_anime_details(mal_id: int) -> dict:
    last_error = None

    for attempt in range(JIKAN_RETRY_COUNT + 1):
        try:
            response = requests.get(
                f"{JIKAN_BASE_URL.rstrip('/')}/anime/{mal_id}",
                timeout=JIKAN_TIMEOUT_SECONDS,
            )

            if response.status_code == 429 or response.status_code >= 500:
                last_error = f"Jikan returned {response.status_code} for anime {mal_id}"
                time.sleep(1 + attempt)
                continue

            response.raise_for_status()
            anime = response.json().get("data")

            if not isinstance(anime, dict):
                raise RuntimeError("Anime API returned an invalid detail response")

            return adapt_anime_result(anime)
        except requests.RequestException as exc:
            last_error = str(exc)
            time.sleep(1 + attempt)

    raise RuntimeError(last_error or f"Jikan detail lookup failed for anime {mal_id}")


def get_anime_trailer(mal_id: int) -> str | None:
    anime = get_anime_details(mal_id)
    trailer = anime.get("trailer") or {}
    return trailer.get("url")


def normalize_search_terms(terms: list) -> list[str]:
    normalized = []
    seen = set()

    for term in terms or []:
        if isinstance(term, dict):
            term = term.get("title") or term.get("name")

        if not isinstance(term, str):
            continue

        term = term.strip()

        if not term or len(term) > MAX_QUERY_LENGTH:
            continue

        key = term.lower()
        if key in seen:
            continue

        normalized.append(term)
        seen.add(key)

    return normalized


def jikan_search_anime(query: str):
    last_error = None

    for attempt in range(JIKAN_RETRY_COUNT + 1):
        try:
            response = requests.get(
                f"{JIKAN_BASE_URL.rstrip('/')}/anime",
                params={"q": query},
                timeout=JIKAN_TIMEOUT_SECONDS,
            )

            if response.status_code == 429 or response.status_code >= 500:
                last_error = f"Jikan returned {response.status_code} for query '{query}'"
                time.sleep(1 + attempt)
                continue

            response.raise_for_status()
            payload = response.json()
            results = payload.get("data")

            if not isinstance(results, list):
                raise RuntimeError("Anime API returned an invalid search response")

            return [adapt_anime_result(anime) for anime in results[:JIKAN_SEARCH_LIMIT]]
        except requests.RequestException as exc:
            last_error = str(exc)
            time.sleep(1 + attempt)

    raise RuntimeError(last_error or f"Jikan search failed for query '{query}'")


#our main boy 1
def search_anime_by_titles(titles: list[str]):
    results = []

    for title in normalize_search_terms(titles):
        anime = jikan_search_anime(title)

        if anime:
            results.extend(anime)

    return results


def search_anime_by_keywords(keywords: list[str]):
    results = []

    for keyword in normalize_search_terms(keywords)[:MAX_INTENT_SEARCH_TERMS]:
        anime = jikan_search_anime(keyword)

        if anime:
            results.extend(anime)

    return results


#our main boy2
def search_anime_by_intent(intent: dict):
    search_terms = []

    search_terms.extend(intent.get("search_keywords", []))
    search_terms.extend(intent.get("genres", []))
    search_terms.extend(intent.get("themes", []))
    search_terms.extend(intent.get("semantic_tags", []))

    mood = intent.get("mood")
    character_arc = intent.get("character_arc")

    if mood:
        search_terms.append(mood)

    if character_arc:
        search_terms.append(character_arc)

    return search_anime_by_keywords(search_terms)
