import os
from dotenv import load_dotenv

load_dotenv()


def _positive_int_env(name: str, default: int) -> int:
    return max(1, int(os.getenv(name, str(default))))


# Recommendation policy: keep product-level counts and exclusions together.
RECOMMENDATION_COUNT = _positive_int_env("RECOMMENDATION_COUNT", 10)
RANKING_CANDIDATE_LIMIT = max(
    RECOMMENDATION_COUNT,
    _positive_int_env("RANKING_CANDIDATE_LIMIT", 30),
)
AI_SUGGESTION_MIN_COUNT = _positive_int_env("AI_SUGGESTION_MIN_COUNT", 5)
AI_SUGGESTION_MAX_COUNT = max(
    AI_SUGGESTION_MIN_COUNT,
    _positive_int_env("AI_SUGGESTION_MAX_COUNT", 10),
)
INTENT_KEYWORD_LIMIT = _positive_int_env("INTENT_KEYWORD_LIMIT", 5)
INTENT_SEARCH_TERM_LIMIT = _positive_int_env("INTENT_SEARCH_TERM_LIMIT", 8)
SEARCH_QUERY_MAX_LENGTH = _positive_int_env("SEARCH_QUERY_MAX_LENGTH", 80)

BLOCKED_ANIME_TYPES = ("Music",)
BLOCKED_ANIME_RATINGS = ("Rx - Hentai",)
BLOCKED_ANIME_GENRES = ("Hentai",)
SHORT_FORM_TYPES = ("Special", "OVA", "ONA")
SHORT_FORM_MAX_EPISODES = 2

# Per-process protection for the expensive recommendation endpoint.
RECOMMENDATION_RATE_LIMIT_REQUESTS = _positive_int_env(
    "RECOMMENDATION_RATE_LIMIT_REQUESTS", 10
)
RECOMMENDATION_RATE_LIMIT_WINDOW_SECONDS = _positive_int_env(
    "RECOMMENDATION_RATE_LIMIT_WINDOW_SECONDS", 60
)
# RECOMMENDATION_RATE_LIMIT = (
#     f"{RECOMMENDATION_RATE_LIMIT_REQUESTS} per "
#     f"{RECOMMENDATION_RATE_LIMIT_WINDOW_SECONDS} seconds"
# )


# VALID syntax
# RECOMMENDATION_RATE_LIMIT = (
#     f"{RECOMMENDATION_RATE_LIMIT_REQUESTS}/{RECOMMENDATION_RATE_LIMIT_WINDOW_SECONDS}second"
# )

RECOMMENDATION_RATE_LIMIT = f"{RECOMMENDATION_RATE_LIMIT_REQUESTS}/minute"



GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
GEMINI_TIMEOUT_MS = _positive_int_env("GEMINI_TIMEOUT_MS", 30000)
GEMINI_RANKING_RETRY_DELAY_SECONDS = max(
    0.0,
    float(os.getenv("GEMINI_RANKING_RETRY_DELAY_SECONDS", "0.5")),
)
GEMINI_RANKING_MAX_ATTEMPTS = _positive_int_env(
    "GEMINI_RANKING_MAX_ATTEMPTS", 2
)
JIKAN_BASE_URL = os.getenv(
    "JIKAN_BASE_URL", "https://jikan-edge.lucas-hdo.workers.dev/v1"
)
#this should be renamed to jikan intent search limit 
JIKAN_SEARCH_LIMIT = _positive_int_env("JIKAN_SEARCH_LIMIT", 10)
JIKAN_TITLE_SEARCH_SCAN_LIMIT = _positive_int_env(
    "JIKAN_TITLE_SEARCH_SCAN_LIMIT", 50
)
JIKAN_TITLE_MATCH_LIMIT = _positive_int_env("JIKAN_TITLE_MATCH_LIMIT", 3)
JIKAN_MAX_CONCURRENCY = _positive_int_env("JIKAN_MAX_CONCURRENCY", 3)
JIKAN_TIMEOUT_SECONDS = _positive_int_env("JIKAN_TIMEOUT_SECONDS", 10)
JIKAN_RETRY_COUNT = max(0, int(os.getenv("JIKAN_RETRY_COUNT", "2")))
ANIMECHAN_BASE_URL = os.getenv("ANIMECHAN_BASE_URL", "https://api.animechan.io/v1")
ANIMECHAN_TIMEOUT_SECONDS = _positive_int_env("ANIMECHAN_TIMEOUT_SECONDS", 8)
