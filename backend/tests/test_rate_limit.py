import unittest
import importlib
import sys
from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from app.rate_limit import limiter


class RecommendationRateLimitTests(unittest.TestCase):
    def setUp(self):
        limiter.reset()
        self.client = TestClient(app)

    def tearDown(self):
        limiter.reset()

    def test_eleventh_recommendation_request_is_rate_limited(self):
        response_body = {"input": "test", "intent": {}, "results": []}

        with patch("app.api.recommend.recommend", return_value=response_body):
            responses = [
                self.client.post("/api/recommend", json={"prompt": "thriller"})
                for _ in range(11)
            ]

        self.assertTrue(all(response.status_code == 200 for response in responses[:10]))
        self.assertEqual(responses[10].status_code, 429)

    def test_api_health_route_is_available(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    @patch.dict("os.environ", {"REDIS_URL": "redis://localhost:6379/0"})
    def test_rate_limiter_imports_with_redis_url(self):
        sys.modules.pop("app.rate_limit", None)
        module = importlib.import_module("app.rate_limit")

        self.assertIsNotNone(module.limiter)

    @patch.dict("os.environ", {"REDIS_URL": '"redis://localhost:6379/0"'})
    def test_rate_limiter_strips_quoted_redis_url(self):
        sys.modules.pop("app.rate_limit", None)
        module = importlib.import_module("app.rate_limit")

        self.assertEqual(
            module.RATE_LIMIT_STORAGE_URI,
            "redis://localhost:6379/0",
        )

    @patch.dict("os.environ", {"REDIS_URL": 'redis://localhost:6379"'})
    def test_rate_limiter_strips_trailing_quote_from_redis_url(self):
        sys.modules.pop("app.rate_limit", None)
        module = importlib.import_module("app.rate_limit")

        self.assertEqual(
            module.RATE_LIMIT_STORAGE_URI,
            "redis://localhost:6379",
        )


if __name__ == "__main__":
    unittest.main()
