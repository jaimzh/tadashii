import unittest
from unittest.mock import Mock, patch

from app.services.quotes import animechan_service


class AnimechanServiceTests(unittest.TestCase):
    def test_get_quote_list_normalizes_animechan_response(self):
        response = Mock()
        response.json.return_value = {
            "status": "success",
            "data": [
                {
                    "content": "Believe in the me that believes in you!",
                    "anime": {"id": 1, "name": "Tengen Toppa Gurren Lagann"},
                    "character": {"id": 2, "name": "Kamina"},
                },
                {
                    "content": "Kick logic out and do the impossible!",
                    "anime": {"id": 1, "name": "Tengen Toppa Gurren Lagann"},
                    "character": {"id": 2, "name": "Kamina"},
                },
            ],
        }

        with (
            patch.object(
                animechan_service.random,
                "choice",
                return_value="Tengen Toppa Gurren Lagann",
            ),
            patch.object(animechan_service.requests, "get", return_value=response) as get,
        ):
            result = animechan_service.get_quote_list()

        self.assertEqual(result["anime"], "Tengen Toppa Gurren Lagann")
        self.assertEqual(len(result["quotes"]), 2)
        self.assertEqual(result["quotes"][0]["character"], "Kamina")
        self.assertEqual(get.call_args.kwargs["params"], {"anime": result["anime"]})

    def test_get_quote_list_does_not_spend_another_request_after_empty_response(self):
        empty_response = Mock()
        empty_response.json.return_value = {"status": "success", "data": []}

        with (
            patch.object(animechan_service.random, "choice", return_value="Naruto"),
            patch.object(animechan_service.requests, "get", return_value=empty_response) as get,
        ):
            with self.assertRaisesRegex(RuntimeError, "no usable quotes"):
                animechan_service.get_quote_list()

        self.assertEqual(get.call_count, 1)

    def test_normalization_removes_duplicate_and_invalid_quotes(self):
        payload = {
            "data": [
                {"content": "Keep moving forward.", "character": {"name": "Eren"}},
                {"content": "Keep moving forward.", "character": {"name": "Eren"}},
                {"content": "", "character": {"name": "Eren"}},
                {"content": "No speaker"},
            ]
        }

        quotes = animechan_service._normalize_quotes(payload, "Shingeki no Kyojin")

        self.assertEqual(len(quotes), 1)
        self.assertEqual(quotes[0]["anime"], "Shingeki no Kyojin")


if __name__ == "__main__":
    unittest.main()
