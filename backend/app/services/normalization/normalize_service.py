from app.models.schema import AnimeCandidate


def get_names(items: list[dict]) -> list[str]:
    names = []

    for item in items or []:
        name = item.get("name")

        if name:
            names.append(name)

    return names


def get_image(raw_anime: dict) -> str | None:
    images = raw_anime.get("images") or {}
    jpg = images.get("jpg") or {}

    return jpg.get("large_image_url") or jpg.get("image_url")


def get_trailer_url(raw_anime: dict) -> str | None:
    trailer = raw_anime.get("trailer") or {}

    return trailer.get("url")


def normalize_anime(raw_anime: dict) -> AnimeCandidate:
    return AnimeCandidate(
        mal_id=raw_anime.get("mal_id"),
        url=raw_anime.get("url"),
        title=raw_anime.get("title"),
        title_english=raw_anime.get("title_english"),
        title_japanese=raw_anime.get("title_japanese"),
        title_synonyms=raw_anime.get("title_synonyms") or [],
        type=raw_anime.get("type"),
        source=raw_anime.get("source"),
        episodes=raw_anime.get("episodes"),
        status=raw_anime.get("status"),
        airing=raw_anime.get("airing"),
        synopsis=raw_anime.get("synopsis"),
        background=raw_anime.get("background"),
        season=raw_anime.get("season"),
        year=raw_anime.get("year"),
        rating=raw_anime.get("rating"),
        score=raw_anime.get("score"),
        genres=get_names(raw_anime.get("genres")),
        explicit_genres=get_names(raw_anime.get("explicit_genres")),
        themes=get_names(raw_anime.get("themes")),
        demographics=get_names(raw_anime.get("demographics")),
        studios=get_names(raw_anime.get("studios")),
        image=get_image(raw_anime),
        trailer_url=get_trailer_url(raw_anime),
        data_source=raw_anime.get("data_source", "jikan"),
    )


def normalize_anime_results(merged_results: list[dict]) -> list[AnimeCandidate]:
    candidates = []

    for raw_anime in merged_results:
        candidate = normalize_anime(raw_anime)
        candidates.append(candidate)

    return candidates

