import unittest

from app.services.retrieval.merge_service import merge_results


class MergeServiceTests(unittest.TestCase):
    def test_takes_turns_between_branches_and_removes_duplicates(self):
        title_results = [
            {"mal_id": 1, "title": "Title 1"},
            {"mal_id": 2, "title": "Title 2"},
            {"mal_id": 3, "title": "Title 3"},
        ]
        intent_results = [
            {"mal_id": 4, "title": "Intent 1"},
            {"mal_id": 2, "title": "Duplicate"},
            {"mal_id": 5, "title": "Intent 3"},
        ]

        results = merge_results(title_results, intent_results)

        self.assertEqual(
            [anime["mal_id"] for anime in results],
            [1, 4, 2, 3, 5],
        )


if __name__ == "__main__":
    unittest.main()
