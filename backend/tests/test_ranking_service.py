import json
import unittest
from unittest.mock import Mock, patch

from google.genai.errors import ServerError

from app.services.ranking import ranking_service


class RankingServiceTests(unittest.TestCase):
    @staticmethod
    def ranking_response(count=1):
        return Mock(
            text=json.dumps(
                [
                    {
                        "mal_id": anime_id,
                        "title": f"Anime {anime_id}",
                        "prompt_match": 90,
                        "reason": "Matches the request.",
                        "emotion_tags": [],
                    }
                    for anime_id in range(count)
                ]
            )
        )

    def test_requests_ten_rankings_and_caps_model_output(self):
        candidates = [
            {"mal_id": anime_id, "title": f"Anime {anime_id}"}
            for anime_id in range(30)
        ]
        response = Mock(
            text=json.dumps(
                [
                    {
                        "mal_id": anime_id,
                        "title": f"Anime {anime_id}",
                        "prompt_match": 90,
                        "reason": "Matches the request.",
                        "emotion_tags": [],
                    }
                    for anime_id in range(12)
                ]
            )
        )

        with patch.object(
            ranking_service.client.models,
            "generate_content",
            return_value=response,
        ) as generate:
            rankings = ranking_service.rank_anime("prompt", {}, candidates)

        self.assertEqual(len(rankings), 10)
        self.assertIn("Return exactly 10 recommendations", generate.call_args.kwargs["contents"])
        self.assertIn(
            "Return recommendations from distinct franchises",
            generate.call_args.kwargs["contents"],
        )
        self.assertIn(
            "Include at most one installment from the same franchise",
            generate.call_args.kwargs["contents"],
        )
        self.assertIn(
            "Prefer the best entry point",
            generate.call_args.kwargs["contents"],
        )

    def test_requests_every_candidate_when_fewer_than_ten_exist(self):
        candidates = [
            {"mal_id": anime_id, "title": f"Anime {anime_id}"}
            for anime_id in range(3)
        ]
        response = Mock(
            text=json.dumps(
                [
                    {
                        "mal_id": anime_id,
                        "title": f"Anime {anime_id}",
                        "prompt_match": 90,
                        "reason": "Matches the request.",
                        "emotion_tags": [],
                    }
                    for anime_id in range(3)
                ]
            )
        )

        with patch.object(
            ranking_service.client.models,
            "generate_content",
            return_value=response,
        ) as generate:
            rankings = ranking_service.rank_anime("prompt", {}, candidates)

        self.assertEqual(len(rankings), 3)
        self.assertIn("Return exactly 3 recommendations", generate.call_args.kwargs["contents"])

    def test_retries_ranking_once_after_temporary_503(self):
        unavailable = ServerError(
            503,
            {
                "error": {
                    "code": 503,
                    "message": "Model is experiencing high demand.",
                    "status": "UNAVAILABLE",
                }
            },
        )

        with (
            patch.object(
                ranking_service.client.models,
                "generate_content",
                side_effect=[unavailable, self.ranking_response()],
            ) as generate,
            patch.object(ranking_service, "sleep") as retry_delay,
        ):
            rankings = ranking_service.rank_anime(
                "prompt",
                {},
                [{"mal_id": 0, "title": "Anime 0"}],
                request_id="rec-test",
            )

        self.assertEqual(len(rankings), 1)
        self.assertEqual(generate.call_count, 2)
        retry_delay.assert_called_once_with(
            ranking_service.GEMINI_RANKING_RETRY_DELAY_SECONDS
        )

    def test_does_not_retry_non_503_server_error(self):
        server_error = ServerError(
            500,
            {"error": {"code": 500, "message": "Server error"}},
        )

        with (
            patch.object(
                ranking_service.client.models,
                "generate_content",
                side_effect=server_error,
            ) as generate,
            patch.object(ranking_service, "sleep") as retry_delay,
        ):
            with self.assertRaises(ServerError):
                ranking_service.rank_anime(
                    "prompt",
                    {},
                    [{"mal_id": 0, "title": "Anime 0"}],
                )

        generate.assert_called_once()
        retry_delay.assert_not_called()

    def test_stops_after_one_503_retry(self):
        unavailable = ServerError(
            503,
            {"error": {"code": 503, "message": "High demand"}},
        )

        with (
            patch.object(
                ranking_service.client.models,
                "generate_content",
                side_effect=[unavailable, unavailable],
            ) as generate,
            patch.object(ranking_service, "sleep") as retry_delay,
        ):
            with self.assertRaises(ServerError):
                ranking_service.rank_anime(
                    "prompt",
                    {},
                    [{"mal_id": 0, "title": "Anime 0"}],
                )

        self.assertEqual(generate.call_count, 2)
        retry_delay.assert_called_once()


if __name__ == "__main__":
    unittest.main()
