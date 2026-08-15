import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
GEMINI_TIMEOUT_MS = max(1, int(os.getenv("GEMINI_TIMEOUT_MS", "30000")))
GEMINI_RANKING_RETRY_DELAY_SECONDS = max(
    0.0,
    float(os.getenv("GEMINI_RANKING_RETRY_DELAY_SECONDS", "0.5")),
)
JIKAN_BASE_URL = os.getenv(
    "JIKAN_BASE_URL", "https://jikan-edge.lucas-hdo.workers.dev/v1"
)
JIKAN_SEARCH_LIMIT = int(os.getenv("JIKAN_SEARCH_LIMIT", "10"))
JIKAN_MAX_CONCURRENCY = max(1, int(os.getenv("JIKAN_MAX_CONCURRENCY", "3")))
ANIMECHAN_BASE_URL = os.getenv("ANIMECHAN_BASE_URL", "https://api.animechan.io/v1")
ANIMECHAN_TIMEOUT_SECONDS = int(os.getenv("ANIMECHAN_TIMEOUT_SECONDS", "8"))
