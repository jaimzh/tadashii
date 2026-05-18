from fastapi import APIRouter
from app.models.request_models import RecommendRequest
from app.services.jikan_service import search_anime

router = APIRouter()

@router.post("/recommend")
def recommend(data: RecommendRequest):
    anime_results = search_anime(data.prompt)
    return {
        "input": data.prompt,
        "results": anime_results
    }