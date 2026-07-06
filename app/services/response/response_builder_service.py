from app.models.request_models import AnimeCandidate, RecommendationResult


def build_recommendation_results(
    rankings: list[dict],
    candidates: list[AnimeCandidate]
) -> list[RecommendationResult]:
    candidates_by_id = {}

    for anime in candidates:
        candidates_by_id[anime.mal_id] = anime

    results = []

    for ranking in rankings:
        mal_id = ranking.get("mal_id")
        anime = candidates_by_id.get(mal_id)

        if not anime:
            continue

        result = RecommendationResult(
            anime=anime,
            match_score=ranking.get("match_score") or ranking.get("prompt_match", 0),
            reason=ranking.get("reason", ""),
            emotion_tags=ranking.get("emotion_tags") or [],
        )

        results.append(result)

    return results
