# app/services/merge_service.py

def merge_results(keyword_results, suggested_results):

    seen = set()
    merged = []

    for anime in keyword_results + suggested_results:

        anime_id = anime["mal_id"]

        if anime_id not in seen:
            merged.append(anime)
            seen.add(anime_id)

    return merged