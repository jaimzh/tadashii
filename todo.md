# Tadashii TODO

Quick place to save ideas so they do not get forgotten.

## Features

- [x] Add bookmarks / saved anime list.
<!-- - [ ] Add "Shazam for anime" recognition using the trace.moe API. -->
- [x] Show rotating Animechan quotes while recommendations are loading.

## Backend and infrastructure

- [ ] Add backend response caching.
- [x] Add API rate limiting.
- [ ] Add shared backend caching for Animechan quote batches. Browser caching already exists.
- [x] Proxy third-party API calls through FastAPI so credentials stay private.

## Anime quote loading experience

- [x] Request a batch of approximately 20 quotes from Animechan.
- [x] Store quotes in local storage with a timestamp and expiration time.
- [x] Stop and clean up the quote timer when loading finishes.
- [x] Fall back to the normal loading animation if the quote API fails.
- [ ] Review the Animechan documentation before implementation.

## Notes and future ideas

- [ ] Observability clean up
- [ ] Watchlist negative exclusion: let users request recommendations that exclude anime already in their Watch Later list (e.g. "recommend stuff that does not exist in my watchlist").
- [ ] Multi-catalog plugins: grow Tadashii beyond anime to other catalogs (Netflix shows, Amazon Prime, cartoons, live-action). Plugin per service = read its catalog -> normalize into a neutral catalog shape (not AnimeCandidate - rename to a generic base, e.g. TitleCandidate/CatalogEntry; anime becomes one catalog). Also make candidate ID namespace generic (mal_id -> catalog-qualified ID like netflix:81198901) so the response builder can join across catalogs. Reuse existing intent/ranking/response pipeline. Matches README roadmap item on service-based discovery.
