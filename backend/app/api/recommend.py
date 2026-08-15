from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.models.schema import RecommendRequest, TrailerResponse
from app.observability.pipeline_timing import logger, timed_stage
from app.services.filter.filter_service import filter_candidates
from app.services.intent.ai_intent_service import analyze_prompt
from app.services.normalization.normalize_service import normalize_anime_results
from app.services.ranking.ranking_service import rank_anime
from app.services.response.response_builder_service import build_recommendation_results
from app.services.retreival.ai_suggest import suggest_anime
from app.services.retreival.jikan_service import (
    get_anime_trailer,
    search_anime_by_intent,
    search_anime_by_titles,
)
from app.services.retreival.merge_service import merge_results

router = APIRouter()


def _analyze_prompt(request_id: str, prompt: str) -> dict:
    with timed_stage(request_id, "intent_parsing"):
        return analyze_prompt(prompt)


def _suggest_anime(request_id: str, prompt: str) -> dict:
    with timed_stage(request_id, "anime_suggestions") as stage:
        suggestions = suggest_anime(prompt)
        stage["count"] = len(suggestions.get("suggested_anime") or [])
        return suggestions


def _retrieve_by_titles(
    request_id: str,
    suggested_titles: list[str],
) -> list[dict]:
    with timed_stage(request_id, "title_retrieval") as stage:
        results = search_anime_by_titles(
            suggested_titles,
            request_id=request_id,
        )
        stage["count"] = len(results)
        return results


def _retrieve_by_intent(request_id: str, intent: dict) -> list[dict]:
    with timed_stage(request_id, "intent_retrieval") as stage:
        results = search_anime_by_intent(
            intent,
            request_id=request_id,
        )
        stage["count"] = len(results)
        return results


@router.get("/anime/{mal_id}/trailer", response_model=TrailerResponse)
def anime_trailer(mal_id: int):
    try:
        trailer_url = get_anime_trailer(mal_id)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    return TrailerResponse(
        mal_id=mal_id,
        trailer_url=trailer_url,
    )


@router.post("/recommend")
def recommend(data: RecommendRequest):
    request_id = f"rec-{uuid4().hex[:8]}"
    request_started_at = perf_counter()
    logger.info("request=%s pipeline=recommendation status=started", request_id)

    try:
        executor = ThreadPoolExecutor(max_workers=2)
        intent_future = executor.submit(
            _analyze_prompt,
            request_id,
            data.prompt,
        )
        suggestions_future = executor.submit(
            _suggest_anime,
            request_id,
            data.prompt,
        )

        try:
            intent = intent_future.result()
        except Exception as exc:
            executor.shutdown(wait=False, cancel_futures=True)
            raise HTTPException(
                status_code=503,
                detail="The recommendation AI is temporarily unavailable.",
            ) from exc

        if not intent.get("is_valid_prompt", False):
            executor.shutdown(wait=False, cancel_futures=True)
            reason = intent.get("validation_reason") or (
                "Enter an understandable anime request with a genre, mood, "
                "theme, story idea, or anime title."
            )
            raise HTTPException(status_code=422, detail=reason)

        try:
            ai_suggestions = suggestions_future.result()
        except Exception as exc:
            raise HTTPException(
                status_code=503,
                detail="The recommendation AI is temporarily unavailable.",
            ) from exc
        finally:
            executor.shutdown(wait=True, cancel_futures=True)

        suggested_titles = ai_suggestions.get("suggested_anime", [])

        try:
            with ThreadPoolExecutor(max_workers=2) as retrieval_executor:
                title_future = retrieval_executor.submit(
                    _retrieve_by_titles,
                    request_id,
                    suggested_titles,
                )
                intent_results_future = retrieval_executor.submit(
                    _retrieve_by_intent,
                    request_id,
                    intent,
                )
                title_results = title_future.result()
                intent_results = intent_results_future.result()
        except RuntimeError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc

        with timed_stage(request_id, "merge") as stage:
            merged_results = merge_results(title_results, intent_results)
            stage["count"] = len(merged_results)

        if not merged_results:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No anime matches were found. Try a clearer request with "
                    "a genre, mood, theme, or anime title."
                ),
            )

        with timed_stage(request_id, "normalize") as stage:
            normalized_results = normalize_anime_results(merged_results)
            stage["count"] = len(normalized_results)

        with timed_stage(request_id, "filter") as stage:
            filtered_results = filter_candidates(normalized_results)
            stage["before"] = len(normalized_results)
            stage["after"] = len(filtered_results)

        if not filtered_results:
            raise HTTPException(
                status_code=404,
                detail=(
                    "No usable anime matches were found. Try changing the "
                    "genre, mood, theme, or example title in your request."
                ),
            )

        try:
            with timed_stage(request_id, "ranking") as stage:
                rankings = rank_anime(
                    data.prompt,
                    intent,
                    filtered_results,
                    request_id=request_id,
                )
                stage["count"] = len(rankings)
        except Exception as exc:
            raise HTTPException(
                status_code=503,
                detail="The recommendation AI is temporarily unavailable.",
            ) from exc

        with timed_stage(request_id, "response_building") as stage:
            results = build_recommendation_results(rankings, filtered_results)
            stage["count"] = len(results)

    except Exception:
        duration = perf_counter() - request_started_at
        logger.error(
            "request=%s stage=total duration_s=%.3f status=error",
            request_id,
            duration,
        )
        raise

    duration = perf_counter() - request_started_at
    logger.info(
        "request=%s stage=total duration_s=%.3f status=ok results=%d",
        request_id,
        duration,
        len(results),
    )

    return {
        "input": data.prompt,
        "intent": intent,
        "results": results,
    }

