import threading
import time
import unittest
from unittest.mock import Mock, patch

from app.services.retreival import jikan_service


class JikanEdgeAdapterTests(unittest.TestCase):
    def test_removes_trailing_mal_rewrite_attribution_from_synopsis(self):
        result = jikan_service.adapt_anime_result(
            {
                "malId": 19,
                "title": "Monster",
                "synopsis": (
                    "A doctor pursues the consequences of a life-saving decision.\n\n"
                    "[Written by MAL Rewrite]"
                ),
            }
        )

        self.assertEqual(
            result["synopsis"],
            "A doctor pursues the consequences of a life-saving decision.",
        )

    def test_preserves_non_attribution_bracketed_synopsis_text(self):
        synopsis = "A tournament begins. [The final round is omitted]"
        result = jikan_service.adapt_anime_result(
            {"malId": 1, "title": "Test", "synopsis": synopsis}
        )

        self.assertEqual(result["synopsis"], synopsis)

    def test_concurrent_search_preserves_term_order_and_worker_limit(self):
        active = 0
        max_active = 0
        lock = threading.Lock()
        delays = {"first": 0.04, "second": 0.03, "third": 0.02, "fourth": 0.01}

        def fake_search(query, request_id=None):
            nonlocal active, max_active

            with lock:
                active += 1
                max_active = max(max_active, active)

            time.sleep(delays[query])

            with lock:
                active -= 1

            return [{"mal_id": query, "request_id": request_id}]

        with (
            patch.object(jikan_service, "JIKAN_MAX_CONCURRENCY", 3),
            patch.object(jikan_service, "jikan_search_anime", side_effect=fake_search),
        ):
            results = jikan_service.search_terms_concurrently(
                ["first", "second", "third", "fourth"],
                request_id="rec-test",
            )

        self.assertEqual(
            [result["mal_id"] for result in results],
            ["first", "second", "third", "fourth"],
        )
        self.assertTrue(all(result["request_id"] == "rec-test" for result in results))
        self.assertEqual(max_active, 3)

    def test_concurrent_search_takes_turns_between_query_result_groups(self):
        def fake_search(query, request_id=None):
            return [
                {"mal_id": f"{query}-{position}"}
                for position in range(1, 4)
            ]

        with patch.object(
            jikan_service,
            "jikan_search_anime",
            side_effect=fake_search,
        ):
            results = jikan_service.search_terms_concurrently(["a", "b", "c"])

        self.assertEqual(
            [result["mal_id"] for result in results],
            [
                "a-1", "b-1", "c-1",
                "a-2", "b-2", "c-2",
                "a-3", "b-3", "c-3",
            ],
        )

    def test_keyword_search_normalizes_deduplicates_and_caps_terms(self):
        keywords = ["One", " one ", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]

        with patch.object(
            jikan_service,
            "search_terms_concurrently",
            return_value=[],
        ) as search:
            jikan_service.search_anime_by_keywords(
                keywords,
                request_id="rec-test",
            )

        search.assert_called_once_with(
            ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight"],
            request_id="rec-test",
        )

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
                "year": 2002,
                "status": "Finished Airing",
                "aired": {"from": "2002-10-03", "to": "2007-02-08"},
                "genres": ["Action", {"name": "Adventure"}],
            }
        )

        self.assertEqual(result["mal_id"], 20)
        self.assertEqual(result["title_english"], "Naruto")
        self.assertEqual(result["title_japanese"], "ナルト")
        self.assertEqual(result["aired_from"], "2002-10-03")
        self.assertEqual(result["aired_to"], "2007-02-08")
        self.assertEqual(result["status"], "Finished Airing")
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

    def test_title_search_scans_past_default_limit_and_keeps_best_matches(self):
        search_results = [
            {"mal_id": anime_id, "title": f"Naruto Movie {anime_id}"}
            for anime_id in range(12)
        ]
        search_results.extend(
            [
                {"mal_id": 20, "title": "Naruto"},
                {"mal_id": 1735, "title": "Naruto: Shippuden"},
            ]
        )

        with patch.object(
            jikan_service,
            "jikan_search_anime",
            return_value=search_results,
        ) as search:
            results = jikan_service.search_anime_by_titles(["Naruto"])

        self.assertEqual(results[0]["mal_id"], 20)
        self.assertLessEqual(len(results), jikan_service.JIKAN_TITLE_MATCH_LIMIT)
        search.assert_called_once_with(
            "Naruto",
            request_id=None,
            result_limit=jikan_service.JIKAN_TITLE_SEARCH_SCAN_LIMIT,
        )

    def test_title_matching_prefers_exact_hajime_no_ippo_title(self):
        results = jikan_service.select_best_title_matches(
            "Hajime no Ippo",
            [
                {"mal_id": 6213, "title": "Hajime no Ippo: New Challenger"},
                {"mal_id": 18689, "title": "Hajime no Ippo: Rising"},
                {"mal_id": 263, "title": "Hajime no Ippo"},
                {"mal_id": 34403, "title": "Hajimete no Gal"},
            ],
            limit=3,
        )

        self.assertEqual(results[0]["mal_id"], 263)
        self.assertNotIn(34403, [anime["mal_id"] for anime in results])

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
        stats = {}

        with patch.object(
            jikan_service,
            "get_anime_details",
            return_value={"title_japanese": "ナルト"},
        ):
            results = jikan_service.add_missing_japanese_titles(
                [recommendation], stats=stats
            )

        self.assertEqual(results[0].anime.title_japanese, "ナルト")

        self.assertEqual(stats["lookups"], 1)
        self.assertEqual(stats["enriched"], 1)
        self.assertEqual(stats["still_missing"], 0)

    def test_keeps_existing_japanese_title_without_detail_request(self):
        anime = Mock(mal_id=20, title_japanese="ナルト")
        recommendation = Mock(anime=anime)

        stats = {}

        with patch.object(jikan_service, "get_anime_details") as get_details:
            jikan_service.add_missing_japanese_titles(
                [recommendation], stats=stats
            )

        get_details.assert_not_called()
        self.assertEqual(stats["already_present"], 1)
        self.assertEqual(stats["lookups"], 0)


if __name__ == "__main__":
    unittest.main()
