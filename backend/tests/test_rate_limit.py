import unittest
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


if __name__ == "__main__":
    unittest.main()
