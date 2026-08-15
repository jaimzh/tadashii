def merge_results(*result_lists):
    """Deduplicate result lists while taking turns between retrieval branches."""
    seen = set()
    merged = []
    max_list_size = max((len(results) for results in result_lists), default=0)

    for index in range(max_list_size):
        # Title and intent retrieval each get a turn before either gets another.
        for results in result_lists:
            if index >= len(results):
                continue

            anime = results[index]
            anime_id = anime.get("mal_id")

            if not anime_id or anime_id in seen:
                continue

            merged.append(anime)
            seen.add(anime_id)

    return merged
