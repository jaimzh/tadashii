import json
import unittest
from unittest.mock import Mock, patch

from app.services.ranking import ranking_service


class RankingServiceTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
