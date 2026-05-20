from fastapi import APIRouter
from app.models.request_models import RecommendRequest
from app.services.jikan_service import search_anime, search_multiple_titles
from app.services.ai_intent_service import analyze_prompt
from app.services.ai_suggest import suggest_anime
from backend.app.services.filter_service import filter_results
from backend.app.services.merge_service import merge_results

router = APIRouter()


# @router.post("/recommend")
# def recommend(data: RecommendRequest):
#     #1. Analyze user prompt with Gemini to extract intent 
#     intent = analyze_prompt(data.prompt)
#     #2. Use extracted intent to search anime database
#     anime_results = search_anime(
#         " ".join(intent["search_keywords"])
#     )
#     suggested_titles = suggest_anime(intent)
#     suggested_results = search_anime(suggested_titles)
    
#     return {
#         "input": data.prompt,
#         "intent": intent,
#         "results": anime_results,
#         "suggested_titles": suggested_titles,
#         "suggested_results": suggested_results
#     }
    
    
    
@router.post("/recommend")
def recommend(data: RecommendRequest):

    intent = analyze_prompt(data.prompt)

    keyword_results = search_anime(
        " ".join(intent["search_keywords"])
    )

    suggested_titles = suggest_anime(intent)

    suggested_results = search_multiple_titles(
        suggested_titles
    )

    merged = merge_results(
        keyword_results,
        suggested_results
    )

    filtered = filter_results(
        merged
    )

    return {
        "input": data.prompt,
        "results": filtered
    }