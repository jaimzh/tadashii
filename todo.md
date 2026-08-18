# Tadashii TODO

Quick place to save ideas so they do not get forgotten.

## Features

- [x] Add bookmarks / saved anime list.
- [ ] Add "Shazam for anime" recognition using the trace.moe API.
- [x] Show rotating Animechan quotes while recommendations are loading.

## Backend and infrastructure

- [ ] Add backend response caching.
- [x] Add API rate limiting.
- [ ] Add shared backend caching for Animechan quote batches. Browser caching already exists.
- [x] Proxy third-party API calls through FastAPI so credentials stay private.

## Anime quote loading experience

- [x] Request a batch of approximately 20 quotes from Animechan.
- [x] Store quotes in local storage with a timestamp and expiration time.
- [ ] Rotate to a new quote every five seconds while recommendations load. Currently 10 seconds.
- [x] Stop and clean up the quote timer when loading finishes.
- [x] Fall back to the normal loading animation if the quote API fails.
- [ ] Review the Animechan documentation before implementation.

## Notes and future ideas

- [ ] Observability clean up
