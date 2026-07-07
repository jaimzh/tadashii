from app.models.schema import AnimeCandidate

BLOCKED_TYPES = ["Music"]
BLOCKED_RATINGS = ["Rx - Hentai"]
BLOCKED_GENRES = ["Hentai"]
SHORT_FORM_TYPES = ["Special", "OVA", "ONA"]


def has_blocked_genre(anime: AnimeCandidate) -> bool:
    all_genres = anime.genres + anime.explicit_genres

    for genre in all_genres:
        if genre in BLOCKED_GENRES:
            return True

    return False


def is_short_extra(anime: AnimeCandidate) -> bool:
    if anime.type not in SHORT_FORM_TYPES:
        return False

    if anime.episodes is None:
        return True

    return anime.episodes <= 2


def should_keep_anime(anime: AnimeCandidate) -> bool:
    if anime.type in BLOCKED_TYPES:
        return False

    if anime.rating in BLOCKED_RATINGS:
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

