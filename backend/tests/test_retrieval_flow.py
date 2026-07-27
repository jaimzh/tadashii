from pathlib import Path
import sys

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BACKEND_DIR))

from app.services.filter.filter_service import filter_candidates
from app.services.intent.ai_intent_service import analyze_prompt
from app.services.normalization.normalize_service import normalize_anime_results
from app.services.retreival.ai_suggest import suggest_anime
from app.services.retreival.jikan_service import (
    search_anime_by_intent,
    search_anime_by_titles,
)
from app.services.retreival.merge_service import merge_results


def main():
    user_prompt = "I want an emotional anime about a lonely underdog who gets stronger and finds friends"

    print("USER PROMPT")
    print(user_prompt)
    print()

    intent = analyze_prompt(user_prompt)
    print("INTENT")
    print(intent)
    print()

    suggestions = suggest_anime(intent)
    print("AI SUGGESTIONS")
    print(suggestions)
    print()

    suggested_titles = suggestions.get("suggested_anime", [])

    title_results = search_anime_by_titles(suggested_titles)
    print("TITLE SEARCH RESULTS")
    print(len(title_results))
    print()

    intent_results = search_anime_by_intent(intent)
    print("INTENT SEARCH RESULTS")
    print(len(intent_results))
    print()

    merged_results = merge_results(title_results, intent_results)
    print("MERGED RESULTS")
    print(len(merged_results))
    print()

    print("FIRST 10 RAW RESULTS")
    for anime in merged_results[:10]:
        print(anime.get("mal_id"), anime.get("title"))
    print()

    normalized_results = normalize_anime_results(merged_results)
    print("NORMALIZED RESULTS")
    print(len(normalized_results))
    print()

    filtered_results = filter_candidates(normalized_results)
    print("FILTERED RESULTS")
    print(len(filtered_results))
    print()

    print("FIRST 10 FILTERED RESULTS")
    for anime in filtered_results[:10]:
        print(anime.mal_id, anime.title, anime.type, anime.episodes, anime.year, anime.genres)


if __name__ == "__main__":
    main()
