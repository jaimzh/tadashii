from app.config import (
    BLOCKED_ANIME_GENRES,
    BLOCKED_ANIME_RATINGS,
    BLOCKED_ANIME_TYPES,
    SHORT_FORM_MAX_EPISODES,
    SHORT_FORM_TYPES,
)
from app.models.schema import AnimeCandidate


def has_blocked_genre(anime: AnimeCandidate) -> bool:
    all_genres = anime.genres + anime.explicit_genres

    for genre in all_genres:
        if genre in BLOCKED_ANIME_GENRES:
            return True

    return False


def is_short_extra(anime: AnimeCandidate) -> bool:
    if anime.type not in SHORT_FORM_TYPES:
        return False

    if anime.episodes is None:
        return True

    return anime.episodes <= SHORT_FORM_MAX_EPISODES


def should_keep_anime(anime: AnimeCandidate) -> bool:
    if anime.type in BLOCKED_ANIME_TYPES:
        return False

    if anime.rating in BLOCKED_ANIME_RATINGS:
        return False

    if has_blocked_genre(anime):
        return False

    if is_short_extra(anime):
        return False

    if not anime.synopsis:
        return False

    return True


def filter_candidates(candidates: list[AnimeCandidate]) -> list[AnimeCandidate]:
    filtered = []

    for anime in candidates:
        if should_keep_anime(anime):
            filtered.append(anime)

    return filtered

