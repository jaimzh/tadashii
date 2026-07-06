import requests

from app.config import JIKAN_BASE_URL, JIKAN_SEARCH_LIMIT


def jikan_search_anime(query: str):
    response = requests.get(
        f"{JIKAN_BASE_URL}/anime",
        params={"q": query, "limit": JIKAN_SEARCH_LIMIT}
    )

    data = response.json()

    return data.get("data", [])


#our main boy 1
def search_anime_by_titles(titles: list[str]):
    results = []

    for title in titles:
        anime = jikan_search_anime(title)

        if anime:
            results.extend(anime)

    return results


def search_multiple_titles(titles):
    suggested_titles = titles.get("suggested_anime", [])

    return search_anime_by_titles(suggested_titles)


def search_anime_by_keywords(keywords: list[str]):
    results = []

    for keyword in keywords:
        anime = jikan_search_anime(keyword)

        if anime:
            results.extend(anime)

    return results


#our main boy2
def search_anime_by_intent(intent: dict):
    search_terms = []

    search_terms.extend(intent.get("search_keywords", []))
    search_terms.extend(intent.get("themes", []))
    search_terms.extend(intent.get("semantic_tags", []))

    mood = intent.get("mood")
    character_arc = intent.get("character_arc")

    if mood:
        search_terms.append(mood)

    if character_arc:
        search_terms.append(character_arc)

    return search_anime_by_keywords(search_terms)
