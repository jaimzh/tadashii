import unittest
from unittest.mock import Mock, patch

from app.services.retreival import jikan_service


class JikanEdgeAdapterTests(unittest.TestCase):
    def test_adapts_edge_search_result_to_internal_shape(self):
        result = jikan_service.adapt_anime_result(
            {
                "malId": 20,
                "url": "https://myanimelist.net/anime/20/Naruto",
                "title": "Naruto",
                "titleEnglish": "Naruto",
                "titles": [
                    {"type": "Default", "title": "Naruto"},
                    {"type": "Japanese", "title": "ナルト"},
                ],
                "imageUrl": "https://cdn.example/naruto.jpg",
                "synopsis": "A young ninja seeks recognition.",
                "type": "TV",
                "score": 8.0,
                "episodes": 220,
                "genres": ["Action", {"name": "Adventure"}],
            }
        )

        self.assertEqual(result["mal_id"], 20)
        self.assertEqual(result["title_english"], "Naruto")
        self.assertEqual(result["title_japanese"], "ナルト")
        self.assertEqual(result["images"]["jpg"]["large_image_url"], "https://cdn.example/naruto.jpg")
        self.assertEqual(result["genres"], [{"name": "Action"}, {"name": "Adventure"}])
        self.assertEqual(result["data_source"], "jikan-edge")

    def test_search_uses_edge_route_and_applies_configured_limit(self):
        response = Mock(status_code=200)
        response.json.return_value = {
            "data": [
                {"malId": anime_id, "title": f"Anime {anime_id}"}
                for anime_id in range(jikan_service.JIKAN_SEARCH_LIMIT + 2)
            ],
            "meta": {"cached": True},
        }

        with patch.object(jikan_service.requests, "get", return_value=response) as get:
            results = jikan_service.jikan_search_anime("friendship")

        self.assertTrue(get.call_args.args[0].endswith("/v1/anime"))
        self.assertEqual(get.call_args.kwargs["params"], {"q": "friendship"})
        self.assertEqual(len(results), jikan_service.JIKAN_SEARCH_LIMIT)
        self.assertEqual(results[0]["mal_id"], 0)

    def test_rejects_malformed_search_payload(self):
        response = Mock(status_code=200)
        response.json.return_value = {"data": {"malId": 20}}

        with patch.object(jikan_service.requests, "get", return_value=response):
            with self.assertRaisesRegex(RuntimeError, "invalid search response"):
                jikan_service.jikan_search_anime("Naruto")

    def test_keeps_legacy_jikan_v4_items_unchanged(self):
        anime = {"mal_id": 20, "title": "Naruto"}
        self.assertIs(jikan_service.adapt_anime_result(anime), anime)

    def test_gets_trailer_from_anime_detail(self):
        response = Mock(status_code=200)
        response.json.return_value = {
            "data": {
                "malId": 1735,
                "titleJapanese": "ナルト- 疾風伝",
                "trailer": {
                    "url": "https://www.youtube.com/watch?v=1dy2zPPrKD0",
                },
            }
        }

        with patch.object(jikan_service.requests, "get", return_value=response) as get:
            trailer_url = jikan_service.get_anime_trailer(1735)

        self.assertTrue(get.call_args.args[0].endswith("/v1/anime/1735"))
        self.assertEqual(trailer_url, "https://www.youtube.com/watch?v=1dy2zPPrKD0")

    def test_returns_none_when_anime_has_no_trailer(self):
        response = Mock(status_code=200)
        response.json.return_value = {"data": {"malId": 20, "trailer": None}}

        with patch.object(jikan_service.requests, "get", return_value=response):
            self.assertIsNone(jikan_service.get_anime_trailer(20))

    def test_adds_missing_japanese_title_to_final_recommendation(self):
        anime = Mock(mal_id=20, title_japanese=None)
        recommendation = Mock(anime=anime)

        with patch.object(
            jikan_service,
            "get_anime_details",
            return_value={"title_japanese": "ナルト"},
        ):
            results = jikan_service.add_missing_japanese_titles([recommendation])

        self.assertEqual(results[0].anime.title_japanese, "ナルト")

    def test_keeps_existing_japanese_title_without_detail_request(self):
        anime = Mock(mal_id=20, title_japanese="ナルト")
        recommendation = Mock(anime=anime)

        with patch.object(jikan_service, "get_anime_details") as get_details:
            jikan_service.add_missing_japanese_titles([recommendation])

        get_details.assert_not_called()


if __name__ == "__main__":
    unittest.main()
