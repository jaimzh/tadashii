# app/services/filter_service.py

def filter_results(results):

    filtered=[]

    blocked=["Music","Hentai"]

    for anime in results:

        if anime["type"] in blocked:
            continue

        filtered.append(anime)

    return filtered