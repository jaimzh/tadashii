from fastapi import APIRouter
from app.models.request_models import RecommendRequest, RecommendResponse

router = APIRouter()

@router.post("/recommend", response_model=RecommendResponse)
def recommend(data: RecommendRequest):
    return {
        "input": data.prompt,
        "results": [
            {
                "title": "Naruto",
                "match_score": 95,
                "reason": "Underdog story that matches emotional growth"
            }
        ]
    }