#it accepts any number of list so merge_results(title_results, intent_results)
def merge_results(*result_lists):
    seen = set()
    merged = []

    for results in result_lists:
        for anime in results:
            anime_id = anime.get("mal_id")

            if not anime_id:
                continue

            if anime_id not in seen:
                merged.append(anime)
                seen.add(anime_id)

    return merged
