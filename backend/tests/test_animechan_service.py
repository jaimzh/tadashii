import unittest
from unittest.mock import Mock, patch

from app.services.quotes import animechan_service


class AnimechanServiceTests(unittest.TestCase):
    def test_get_quote_list_combines_quotes_from_multiple_anime(self):
        selected_anime = ["Naruto", "One Piece", "Death Note", "Cowboy Bebop"]

        def response_for_request(*_args, **kwargs):
            anime = kwargs["params"]["anime"]
            response = Mock()
            response.json.return_value = {
                "status": "success",
                "data": [
                    {
                        "content": f"A quote from {anime}",
                        "anime": {"name": anime},
                        "character": {"name": f"{anime} character"},
                    }
                ],
            }
            return response

        with (
            patch.object(animechan_service.random, "sample", return_value=selected_anime),
            patch.object(animechan_service.random, "shuffle"),
            patch.object(
                animechan_service.requests,
                "get",
                side_effect=response_for_request,
            ) as get,
        ):
            result = animechan_service.get_quote_list()

        self.assertEqual(len(result["quotes"]), 4)
        self.assertEqual(get.call_count, 4)
        self.assertEqual(
            {quote["anime"] for quote in result["quotes"]},
            set(selected_anime),
        )

    def test_get_quote_list_raises_when_all_selected_anime_return_empty(self):
        empty_response = Mock()
        empty_response.json.return_value = {"status": "success", "data": []}
        selected_anime = ["Naruto", "One Piece", "Death Note", "Cowboy Bebop"]

        with (
            patch.object(animechan_service.random, "sample", return_value=selected_anime),
            patch.object(animechan_service.requests, "get", return_value=empty_response) as get,
        ):
            with self.assertRaisesRegex(RuntimeError, "no usable quotes"):
                animechan_service.get_quote_list()

        self.assertEqual(get.call_count, 4)

    def test_get_quote_list_keeps_quotes_when_one_selected_anime_fails(self):
        selected_anime = ["Naruto", "One Piece", "Death Note", "Cowboy Bebop"]

        def response_for_request(*_args, **kwargs):
            anime = kwargs["params"]["anime"]
            if anime == "Naruto":
                raise animechan_service.requests.ConnectionError("Unavailable")

            response = Mock()
            response.json.return_value = {
                "data": [
                    {
                        "content": f"A quote from {anime}",
                        "character": {"name": "Character"},
                    }
                ]
            }
            return response

        with (
            patch.object(animechan_service.random, "sample", return_value=selected_anime),
            patch.object(animechan_service.random, "shuffle"),
            patch.object(
                animechan_service.requests,
                "get",
                side_effect=response_for_request,
            ),
        ):
            result = animechan_service.get_quote_list()

        self.assertEqual(len(result["quotes"]), 3)
        self.assertNotIn("Naruto", {quote["anime"] for quote in result["quotes"]})

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
