from fastapi import APIRouter
from app.models.request_models import RecommendRequest
from app.services.jikan_service import search_anime, search_multiple_titles


from app.services.ai_intent_service import analyze_prompt
from app.services.ai_suggest import suggest_anime
from app.services.filter_service import filter_results
from app.services.merge_service import merge_results

from app.services.merge_service import merge_results
from app.services.filter_service import filter_results
from app.services.ranking_service import rank_anime

router = APIRouter()




@router.post("/recommend")
def recommend(data: RecommendRequest):

    intent = analyze_prompt(data.prompt)

    keyword_results = search_anime(" ".join(intent["search_keywords"]))
    suggested_titles = suggest_anime(intent)
    suggested_results = search_multiple_titles(suggested_titles)

    merged = merge_results(keyword_results, suggested_results)
    filtered = filter_results(merged)

    ranked = rank_anime(data.prompt, intent, filtered)

    return {
        "input": data.prompt,
        "intent": intent,
        "results": ranked
    }