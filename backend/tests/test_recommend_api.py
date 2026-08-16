import unittest
from threading import Barrier, Event
from time import perf_counter
from unittest.mock import patch

from fastapi import HTTPException
from pydantic import ValidationError

from app.api.recommend import anime_details, recommend
from app.models.schema import RecommendRequest


VALID_INTENT = {
    "is_valid_prompt": True,
    "validation_reason": "",
    "search_keywords": ["thriller"],
    "semantic_tags": [],
    "themes": [],
    "mood": "dark",
    "genres": ["Thriller"],
    "character_arc": "",
}


class RecommendApiTests(unittest.TestCase):
    def test_anime_details_returns_full_synopsis_and_trailer(self):
        with patch(
            "app.api.recommend.get_anime_details",
            return_value={
                "title": "Monster",
                "title_english": "Monster",
                "title_japanese": "MONSTER",
                "images": {
                    "jpg": {
                        "image_url": "https://cdn.example/monster.jpg",
                        "large_image_url": "https://cdn.example/monster-large.jpg",
                    }
                },
                "studios": [{"name": "Madhouse"}],
                "synopsis": "The complete synopsis from the detail response.",
                "trailer": {"url": "https://youtube.com/watch?v=test"},
                "year": 2004,
                "status": "Finished Airing",
                "aired_from": "2004-04-07",
                "aired_to": "2005-09-28",
            },
        ):
            result = anime_details(19)

        self.assertEqual(result.mal_id, 19)
        self.assertEqual(result.title, "Monster")
        self.assertEqual(result.title_english, "Monster")
        self.assertEqual(result.title_japanese, "MONSTER")
        self.assertEqual(
            result.image_url,
            "https://cdn.example/monster-large.jpg",
        )
        self.assertEqual(result.studios, ["Madhouse"])
        self.assertEqual(
            result.synopsis,
            "The complete synopsis from the detail response.",
        )
        self.assertEqual(
            result.trailer_url,
            "https://youtube.com/watch?v=test",
        )
        self.assertEqual(result.year, 2004)
        self.assertEqual(result.status, "Finished Airing")
        self.assertEqual(result.aired_from, "2004-04-07")
        self.assertEqual(result.aired_to, "2005-09-28")

    def test_intent_and_suggestions_run_concurrently(self):
        both_started = Barrier(2)

        def analyze(_prompt):
            both_started.wait(timeout=1)
            return VALID_INTENT

        def suggest(_prompt):
            both_started.wait(timeout=1)
            return {"suggested_anime": []}

        with (
            patch("app.api.recommend.analyze_prompt", side_effect=analyze),
            patch("app.api.recommend.suggest_anime", side_effect=suggest),
            patch("app.api.recommend.search_anime_by_titles", return_value=[]),
            patch("app.api.recommend.search_anime_by_intent", return_value=[]),
        ):
            with self.assertRaises(HTTPException) as raised:
                recommend(RecommendRequest(prompt="dark thriller anime"))

        self.assertEqual(raised.exception.status_code, 404)

    def test_invalid_prompt_stops_before_jikan(self):
        release_suggestion = Event()
        invalid_intent = {
            **VALID_INTENT,
            "is_valid_prompt": False,
            "validation_reason": "Enter an understandable anime preference.",
            "search_keywords": [],
            "genres": [],
        }

        def slow_suggestion(_prompt):
            release_suggestion.wait(timeout=2)
            return {"suggested_anime": []}

        started_at = perf_counter()

        try:
            with (
                patch("app.api.recommend.analyze_prompt", return_value=invalid_intent),
                patch("app.api.recommend.suggest_anime", side_effect=slow_suggestion),
                patch("app.api.recommend.search_anime_by_titles") as title_search,
                patch("app.api.recommend.search_anime_by_intent") as intent_search,
                patch("app.api.recommend.rank_anime") as rank,
            ):
                with self.assertRaises(HTTPException) as raised:
                    recommend(RecommendRequest(prompt="caahdhdhdhfdj"))
        finally:
            release_suggestion.set()

        self.assertEqual(raised.exception.status_code, 422)
        self.assertIn("understandable", raised.exception.detail)
        self.assertLess(perf_counter() - started_at, 1)
        title_search.assert_not_called()
        intent_search.assert_not_called()
        rank.assert_not_called()

    def test_title_and_intent_retrieval_run_concurrently(self):
        both_started = Barrier(2)

        def title_search(_titles, request_id=None):
            both_started.wait(timeout=1)
            return []

        def intent_search(_intent, request_id=None):
            both_started.wait(timeout=1)
            return []

        with (
            patch("app.api.recommend.analyze_prompt", return_value=VALID_INTENT),
            patch(
                "app.api.recommend.suggest_anime",
                return_value={"suggested_anime": ["Monster"]},
            ),
            patch(
                "app.api.recommend.search_anime_by_titles",
                side_effect=title_search,
            ),
            patch(
                "app.api.recommend.search_anime_by_intent",
                side_effect=intent_search,
            ),
        ):
            with self.assertRaises(HTTPException) as raised:
                recommend(RecommendRequest(prompt="dark thriller anime"))

        self.assertEqual(raised.exception.status_code, 404)

    def test_retrieval_failure_returns_service_unavailable(self):
        with (
            patch("app.api.recommend.analyze_prompt", return_value=VALID_INTENT),
            patch(
                "app.api.recommend.suggest_anime",
                return_value={"suggested_anime": ["Monster"]},
            ),
            patch(
                "app.api.recommend.search_anime_by_titles",
                side_effect=RuntimeError("Jikan unavailable"),
            ),
            patch("app.api.recommend.search_anime_by_intent", return_value=[]),
        ):
            with self.assertRaises(HTTPException) as raised:
                recommend(RecommendRequest(prompt="dark thriller anime"))

        self.assertEqual(raised.exception.status_code, 503)
        self.assertEqual(raised.exception.detail, "Jikan unavailable")

    def test_zero_jikan_results_stop_before_ranking(self):
        with (
            patch("app.api.recommend.analyze_prompt", return_value=VALID_INTENT),
            patch(
                "app.api.recommend.suggest_anime",
                return_value={"suggested_anime": ["Monster"]},
            ),
            patch("app.api.recommend.search_anime_by_titles", return_value=[]),
            patch("app.api.recommend.search_anime_by_intent", return_value=[]),
            patch("app.api.recommend.rank_anime") as rank,
        ):
            with self.assertRaises(HTTPException) as raised:
                recommend(RecommendRequest(prompt="an unknown anime idea"))

        self.assertEqual(raised.exception.status_code, 404)
        self.assertIn("No anime matches", raised.exception.detail)
        rank.assert_not_called()

    def test_blank_prompt_is_rejected_by_request_schema(self):
        with self.assertRaises(ValidationError):
            RecommendRequest(prompt="   ")


if __name__ == "__main__":
    unittest.main()
