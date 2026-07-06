from fastapi import APIRouter

from app.models.request_models import RecommendRequest
from app.services.filter.filter_service import filter_candidates
from app.services.intent.ai_intent_service import analyze_prompt
from app.services.normalization.normalize_service import normalize_anime_results
from app.services.ranking.ranking_service import rank_anime
from app.services.response.response_builder_service import build_recommendation_results
from app.services.retreival.ai_suggest import suggest_anime
from app.services.retreival.jikan_service import search_anime_by_intent, search_anime_by_titles
from app.services.retreival.merge_service import merge_results

router = APIRouter()


@router.post("/recommend")
def recommend(data: RecommendRequest):
    intent = analyze_prompt(data.prompt)

    ai_suggestions = suggest_anime(intent)
    suggested_titles = ai_suggestions.get("suggested_anime", [])

    title_results = search_anime_by_titles(suggested_titles)
    intent_results = search_anime_by_intent(intent)

    merged_results = merge_results(title_results, intent_results)
    normalized_results = normalize_anime_results(merged_results)
    filtered_results = filter_candidates(normalized_results)

    rankings = rank_anime(data.prompt, intent, filtered_results)
    results = build_recommendation_results(rankings, filtered_results)

    return {
        "input": data.prompt,
        "intent": intent,
        "results": results,
    }
