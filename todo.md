# Tadashii TODO

Quick place to save ideas so they do not get forgotten.

## Features

- [ ] Add bookmarks / saved anime list.
- [ ] Add "Shazam for anime" recognition using the trace.moe API.
- [ ] Show rotating Animechan quotes while recommendations are loading.

## Backend and infrastructure

- [ ] Add backend response caching.
- [ ] Add API rate limiting.
- [ ] Cache Animechan quote batches to protect the daily request allowance.
- [ ] Proxy third-party API calls through FastAPI so credentials stay private.

## Anime quote loading experience

- [ ] Request a batch of approximately 20 quotes from Animechan.
- [ ] Store quotes in local storage with a timestamp and expiration time.
- [ ] Rotate to a new quote every five seconds while recommendations load.
- [ ] Stop and clean up the quote timer when loading finishes.
- [ ] Fall back to the normal loading animation if the quote API fails.
- [ ] Review the Animechan documentation before implementation.

## Notes and future ideas

- [ ] Add new idea here.
