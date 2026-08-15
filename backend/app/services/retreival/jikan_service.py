from concurrent.futures import ThreadPoolExecutor
from functools import partial
import re
import time
from time import perf_counter
import unicodedata
from difflib import SequenceMatcher

import requests

from app.config import (
    INTENT_SEARCH_TERM_LIMIT,
    JIKAN_BASE_URL,
    JIKAN_MAX_CONCURRENCY,
    JIKAN_RETRY_COUNT,
    JIKAN_SEARCH_LIMIT,
    JIKAN_TITLE_MATCH_LIMIT,
    JIKAN_TITLE_SEARCH_SCAN_LIMIT,
    JIKAN_TIMEOUT_SECONDS,
    SEARCH_QUERY_MAX_LENGTH,
)
from app.observability.pipeline_timing import logger

MAL_REWRITE_ATTRIBUTION = re.compile(
    r"\s*\[Written by MAL Rewrite\]\s*$",
    flags=re.IGNORECASE,
)


def clean_synopsis(synopsis: str | None) -> str | None:
    if not synopsis:
        return synopsis

    return MAL_REWRITE_ATTRIBUTION.sub("", synopsis).rstrip()


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
    aired = anime.get("aired") or {}
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
        "aired_from": aired.get("from"),
        "aired_to": aired.get("to"),
        "synopsis": clean_synopsis(anime.get("synopsis")),
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


def add_missing_japanese_titles(
    recommendations: list,
    stats: dict | None = None,
) -> list:
    """Complete missing Japanese titles and optionally report enrichment counts."""
    enrichment_stats = {
        "total": len(recommendations),
        "already_present": 0,
        "lookups": 0,
        "enriched": 0,
        "lookup_failed": 0,
        "still_missing": 0,
    }

    for recommendation in recommendations:
        anime = getattr(recommendation, "anime", None)

        if not anime:
            enrichment_stats["still_missing"] += 1
            continue

        if anime.title_japanese:
            enrichment_stats["already_present"] += 1
            continue

        enrichment_stats["lookups"] += 1

        try:
            details = get_anime_details(anime.mal_id)
        except RuntimeError:
            # Missing optional metadata should not fail the recommendation request.
            enrichment_stats["lookup_failed"] += 1
            enrichment_stats["still_missing"] += 1
            continue

        anime.title_japanese = details.get("title_japanese")

        if anime.title_japanese:
            enrichment_stats["enriched"] += 1
        else:
            enrichment_stats["still_missing"] += 1

    if stats is not None:
        stats.update(enrichment_stats)

    return recommendations


def normalize_search_terms(terms: list) -> list[str]:
    normalized = []
    seen = set()

    for term in terms or []:
        if isinstance(term, dict):
            term = term.get("title") or term.get("name")

        if not isinstance(term, str):
            continue

        term = term.strip()

        if not term or len(term) > SEARCH_QUERY_MAX_LENGTH:
            continue

        key = term.lower()
        if key in seen:
            continue

        normalized.append(term)
        seen.add(key)

    return normalized


def _normalize_title(value: str | None) -> str:
    if not value:
        return ""

    value = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"\w+", value, flags=re.UNICODE))


def _anime_title_variants(anime: dict) -> list[str]:
    values = [
        anime.get("title"),
        anime.get("title_english"),
        anime.get("title_japanese"),
        *(anime.get("title_synonyms") or []),
    ]
    return list(dict.fromkeys(filter(None, values)))


def _title_match_score(query: str, anime: dict) -> tuple[float, float]:
    normalized_query = _normalize_title(query)
    query_tokens = set(normalized_query.split())
    best_score = 0.0
    best_sequence_score = 0.0

    for variant in _anime_title_variants(anime):
        normalized_variant = _normalize_title(variant)
        if not normalized_variant:
            continue

        sequence_score = SequenceMatcher(
            None, normalized_query, normalized_variant
        ).ratio()
        variant_tokens = set(normalized_variant.split())
        token_score = (
            len(query_tokens & variant_tokens) / len(query_tokens | variant_tokens)
            if query_tokens and variant_tokens
            else 0.0
        )

        if normalized_query == normalized_variant:
            score = 3.0
        elif (
            normalized_variant.startswith(f"{normalized_query} ")
            or normalized_query.startswith(f"{normalized_variant} ")
        ):
            score = 2.0 + max(sequence_score, token_score)
        else:
            score = max(sequence_score, token_score)

        if (score, sequence_score) > (best_score, best_sequence_score):
            best_score = score
            best_sequence_score = sequence_score

    return best_score, best_sequence_score


def select_best_title_matches(
    query: str,
    anime_results: list[dict],
    limit: int = JIKAN_TITLE_MATCH_LIMIT,
) -> list[dict]:
    """Keep the Jikan results whose known titles most closely match the query."""
    indexed_results = list(enumerate(anime_results))
    indexed_results.sort(
        key=lambda item: (*_title_match_score(query, item[1]), -item[0]),
        reverse=True,
    )
    return [anime for _, anime in indexed_results[:limit]]


def jikan_search_anime(
    query: str,
    request_id: str | None = None,
    result_limit: int = JIKAN_SEARCH_LIMIT,
):
    started_at = perf_counter()
    last_error = None
    attempts = 0

    for attempt in range(JIKAN_RETRY_COUNT + 1):
        attempts = attempt + 1

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

            adapted_results = [
                adapt_anime_result(anime)
                for anime in results[:result_limit]
            ]
            logger.info(
                "request=%s service=jikan query=%r duration_s=%.3f "
                "status=ok attempts=%d count=%d",
                request_id or "untracked",
                query,
                perf_counter() - started_at,
                attempts,
                len(adapted_results),
            )
            return adapted_results
        except requests.RequestException as exc:
            last_error = str(exc)
            time.sleep(1 + attempt)

    error_message = last_error or f"Jikan search failed for query '{query}'"
    logger.warning(
        "request=%s service=jikan query=%r duration_s=%.3f "
        "status=error attempts=%d error=%r",
        request_id or "untracked",
        query,
        perf_counter() - started_at,
        attempts,
        error_message,
    )
    raise RuntimeError(error_message)


def search_terms_concurrently(
    terms: list[str],
    request_id: str | None = None,
    search_function=None,
) -> list:
    if not terms:
        return []

    search = partial(
        search_function or jikan_search_anime,
        request_id=request_id,
    )
    max_workers = min(JIKAN_MAX_CONCURRENCY, len(terms))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        result_groups = executor.map(search, terms)
        return [anime for group in result_groups for anime in group]


#our main boy 1
def search_anime_by_titles(
    titles: list[str],
    request_id: str | None = None,
):
    terms = normalize_search_terms(titles)

    def search_title(query: str, request_id: str | None = None) -> list[dict]:
        results = jikan_search_anime(
            query,
            request_id=request_id,
            result_limit=JIKAN_TITLE_SEARCH_SCAN_LIMIT,
        )
        return select_best_title_matches(query, results)

    return search_terms_concurrently(
        terms,
        request_id=request_id,
        search_function=search_title,
    )


def search_anime_by_keywords(
    keywords: list[str],
    request_id: str | None = None,
):
    terms = normalize_search_terms(keywords)[:INTENT_SEARCH_TERM_LIMIT]
    return search_terms_concurrently(terms, request_id=request_id)


#our main boy2
def search_anime_by_intent(intent: dict, request_id: str | None = None):
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

    return search_anime_by_keywords(search_terms, request_id=request_id)
