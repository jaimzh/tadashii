from fastapi import APIRouter, HTTPException

from app.models.schema import QuoteListResponse
from app.services.quotes.animechan_service import get_quote_list

router = APIRouter()


@router.get("/quotes/list", response_model=QuoteListResponse)
def quote_list():
    try:
        return get_quote_list()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
