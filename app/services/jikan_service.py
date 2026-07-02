import requests

BASE_URL = "https://api.jikan.moe/v4"

def jikan_search_anime(query: str):
    response = requests.get(
        f"{BASE_URL}/anime",
        params={"q": query, "limit": 10}
    )

    data = response.json()

    return data.get("data", [])



def search_multiple_titles(titles):

    results = []

    for title in titles["suggested_anime"]:
        anime = jikan_search_anime(title)

        if anime:
            results.extend(anime)

    return results