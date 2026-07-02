# app/services/franchise_service.py

def remove_spinoffs(results):

    cleaned=[]

    blocked_words=[
        "Movie",
        "OVA",
        "Special",
        "Pilot",
        "Recap",
        "Jump Festa"
    ]

    for anime in results:

        title=anime["title"]

        if any(word in title for word in blocked_words):
            continue

        cleaned.append(anime)

    return cleaned