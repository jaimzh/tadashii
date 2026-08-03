import time

import requests

from app.config import JIKAN_BASE_URL, JIKAN_SEARCH_LIMIT

MAX_INTENT_SEARCH_TERMS = 8
MAX_QUERY_LENGTH = 80
JIKAN_TIMEOUT_SECONDS = 10
JIKAN_RETRY_COUNT = 2


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
                f"{JIKAN_BASE_URL}/anime",
                params={"q": query, "limit": JIKAN_SEARCH_LIMIT},
                timeout=JIKAN_TIMEOUT_SECONDS,
            )

            if response.status_code == 429 or response.status_code >= 500:
                last_error = f"Jikan returned {response.status_code} for query '{query}'"
                time.sleep(1 + attempt)
                continue

            response.raise_for_status()
            data = response.json()

            return data.get("data", [])
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