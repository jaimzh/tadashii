from fastapi import APIRouter
from app.models.request_models import RecommendRequest
from app.services.jikan_service import jikan_search_anime, search_multiple_titles


from app.services.ai_intent_service import analyze_prompt
from app.services.ai_suggest import suggest_anime
from app.services.filter_service import filter_results
from app.services.merge_service import merge_results

from app.services.merge_service import merge_results
from app.services.filter_service import filter_results
from app.services.ranking_service import rank_anime
from app.services.franchise_service import remove_spinoffs

router = APIRouter()


# @router.post("/recommend")
# def recommend(data: RecommendRequest):

#     intent = analyze_prompt(data.prompt)

#     keyword_results = search_anime(" ".join(intent["search_keywords"]))
#     suggested_titles = suggest_anime(intent)
#     suggested_results = search_multiple_titles(suggested_titles)

#     merged = merge_results(keyword_results, suggested_results)
#     filtered = filter_results(merged)

#     # ranked = rank_anime(data.prompt, intent, filtered)

#     rank_input = []

#     for anime in filtered:
#         rank_input.append(
#             {
#                 "mal_id": anime["mal_id"],
#                 "title": anime["title"],
#                 "synopsis": anime.get("synopsis"),
#                 "genres": [g["name"] for g in anime.get("genres", [])],
#                 "themes": [t["name"] for t in anime.get("themes", [])],
#                 "score": anime.get("score"),
#                 "episodes": anime.get("episodes"),
#             }
#         )
#     ranked = rank_anime(data.prompt, intent, rank_input)

#     return {"input": data.prompt, "intent": intent, "results": ranked, "debug": {"keyword_results": keyword_results, "suggested_results": suggested_results, "rank_input": rank_input}}


@router.post("/recommend")
def recommend(data: RecommendRequest):

    intent = analyze_prompt(data.prompt)

    # AI FIRST (strong signal)
    ai_suggested_titles = suggest_anime(intent)
    searched_suggested_results = search_multiple_titles(ai_suggested_titles)

    # JIKAN SECOND (weak/broad signal) now i feel like this is unnecessary 
    keyword_results = jikan_search_anime(
        " ".join(intent["search_keywords"])
    )[:5]

    # MERGE (dedupe)
    merged = merge_results(keyword_results, searched_suggested_results)

    # FILTER (remove junk types)
    filtered = filter_results(merged)

    # CLEAN (remove movies/ovas if desired)
    cleaned = remove_spinoffs(filtered)

    # FINAL RANK
    ranked = rank_anime(
        data.prompt,
        intent,
        cleaned
    )

    return {
        "input": data.prompt,
        "intent": intent,
        "results": ranked
    }