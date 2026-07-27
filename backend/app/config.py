import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")
JIKAN_BASE_URL = os.getenv("JIKAN_BASE_URL", "https://api.jikan.moe/v4")
JIKAN_SEARCH_LIMIT = int(os.getenv("JIKAN_SEARCH_LIMIT", "10"))
