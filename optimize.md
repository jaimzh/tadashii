Absolutely. Here’s what each optimization means in the context of your backend.

## 1. Reusing HTTP connections

Currently, each call to Jikan uses:

```python
requests.get(...)
```

Imagine making several phone calls to the same person but hanging up and reconnecting before every sentence. Each new HTTPS connection may require:

- Finding the server
- Opening a TCP connection
- Performing TLS security negotiation
- Sending the request
- Closing or discarding the connection

A `requests.Session` can reuse an existing connection:

```python
session = requests.Session()

session.get(...)
session.get(...)
session.get(...)
```

The later requests may avoid some connection setup work.

For Tadashii, this is worthwhile because one recommendation can trigger many requests to the same Jikan server. It’s an easy, relatively safe improvement, but it probably won’t create the largest speedup by itself.

## 2. Concurrent Jikan searches

This is likely your biggest opportunity.

Your backend currently does something equivalent to:

```text
Search Naruto       → wait 0.8 seconds
Search underdog     → wait 1.1 seconds
Search friendship   → wait 0.9 seconds
Search training     → wait 1.0 seconds
Search emotional    → wait 0.7 seconds
```

Total: approximately `4.5 seconds`.

These searches don’t depend on one another, so they could run concurrently:

```text
Search Naruto      ─┐
Search underdog    ─┤
Search friendship  ─┼─ wait for all
Search training    ─┤
Search emotional   ─┘
```

If they all begin together, the total could be closer to the slowest request—perhaps `1.1 seconds`—instead of the sum of every request.

However, we shouldn’t launch 18 requests simultaneously. That could:

- Trigger API rate limits
- Overload the external service
- Produce more `429 Too Many Requests` responses
- Make retries worse

I would use bounded concurrency, probably three or four simultaneous Jikan requests.

There is another opportunity here: title retrieval and intent retrieval are also independent after Gemini produces the suggestions, so those two groups can overlap.

## 3. Caching repeated searches

Caching means remembering a result temporarily so we don’t request it again.

Suppose someone searches for:

```text
An emotional underdog who becomes stronger
```

The backend might search Jikan for:

```text
underdog
emotional
training
friendship
```

Another user might submit a similar prompt five minutes later. Without caching, Tadashii calls Jikan again for the same terms. With caching:

```text
Search cache for "underdog"
        ↓
Result found
        ↓
Return it immediately
```

Possible cached items include:

- Jikan keyword search results
- Jikan title search results
- Anime details by `mal_id`
- Trailer URLs
- Anime quotes
- Possibly complete recommendation responses

A basic in-memory cache is easiest:

```text
"underdog" → results, expires in 30 minutes
```

Its limitations are:

- It disappears when the backend restarts.
- Each server worker gets its own cache.
- It uses application memory.

That’s still perfectly reasonable for your current project. Redis would only become necessary when deploying multiple backend instances or needing durable/shared caching.

Anime details are particularly good cache candidates because information such as an anime’s Japanese title, studio, and trailer rarely changes.

## 4. Reducing the Gemini ranking payload

The ranking service currently sends up to 30 full `AnimeCandidate` objects to Gemini.

Those objects contain fields such as:

- Titles
- Synopsis
- Genres
- Themes
- Demographics
- Studios
- Status
- Season
- Year
- Rating
- Image URL
- MyAnimeList URL
- Trailer URL
- Other metadata

Gemini doesn’t need all of this to decide whether an anime matches the prompt. For example, an image URL contributes nothing to story matching.

A smaller ranking payload might contain only:

```json
{
  "mal_id": 20,
  "title": "Naruto",
  "synopsis": "...",
  "genres": ["Action", "Adventure"],
  "themes": ["Martial Arts"],
  "demographics": ["Shounen"],
  "type": "TV",
  "year": 2002
}
```

Benefits:

- Less data sent over the network
- Fewer Gemini input tokens
- Potentially faster responses
- Lower API costs
- Less irrelevant information distracting the model

This is a fairly safe optimization because the full anime objects remain in your backend. Gemini receives the smaller version for ranking, and the response builder reconnects the ranking to the complete object using `mal_id`.

## 5. Combining Gemini calls

You currently have three Gemini stages:

```text
User prompt
    ↓
Gemini: parse intent
    ↓
Gemini: suggest titles
    ↓
Jikan retrieval
    ↓
Gemini: rank candidates
```

The first two calls could potentially become one:

```text
User prompt
    ↓
Gemini returns:
{
  "intent": {...},
  "suggested_anime": [...]
}
```

That removes one entire network round trip.

If each Gemini call takes around two seconds, eliminating one could save roughly two seconds.

The tradeoff is architectural:

- The combined prompt becomes more complex.
- Intent parsing and suggestions become coupled.
- Testing each responsibility separately becomes slightly harder.
- If the response is malformed, both results fail together.

I think combining these two stages is reasonable because both are interpretations of the same user prompt. Ranking should remain separate because it needs candidates from Jikan first.

## 6. Optimizing Japanese-title enrichment

After ranking, this function runs:

```python
add_missing_japanese_titles(results)
```

For every recommendation without a Japanese title, it makes another Jikan detail request.

For example:

```text
Result 1 missing Japanese title → request → wait
Result 2 missing Japanese title → request → wait
Result 3 missing Japanese title → request → wait
Result 4 missing Japanese title → request → wait
```

If each request takes one second, four missing titles add approximately four seconds at the very end—even though the recommendations are already complete.

Possible solutions include:

### Cache anime details

Once anime ID `20` has been fetched, remember its details. Future requests become nearly instant.

### Fetch missing titles concurrently

Request several missing titles simultaneously, with a concurrency limit.

### Make enrichment optional

Return recommendations immediately without Japanese titles and load missing details from the frontend afterward.

This would improve perceived speed, but it adds frontend complexity and might cause text to change after cards appear.

### Stop fetching missing Japanese titles

If Japanese titles are decorative rather than essential, use only what the original search results contain. This is fastest but means some recommendations won’t show Japanese names.

My preference is caching plus bounded concurrency. It retains the feature without unnecessarily delaying every item sequentially.

## 7. Smarter retry and timeout behavior

Currently, each Jikan request can:

- Wait up to 10 seconds
- Retry twice
- Sleep between retries

In a worst-case failure:

```text
Attempt 1 → waits 10 seconds
Sleep     → 1 second
Attempt 2 → waits 10 seconds
Sleep     → 2 seconds
Attempt 3 → waits 10 seconds
```

One search could consume over 30 seconds. If multiple searches encounter problems sequentially, the total becomes painful.

We could improve this with:

- Separate connection and response timeouts
- Fewer retries for nonessential requests
- Exponential backoff
- Respect for a `Retry-After` header
- A total time budget for the recommendation request
- Different behavior for required and optional data

For example:

```python
timeout=(3, 7)
```

This means:

- Allow up to 3 seconds to establish the connection
- Allow up to 7 seconds waiting for response data

Trailer and Japanese-title lookups are optional, so failure there should happen quickly and should never fail the entire recommendation.

## What I would do in order

```text
1. Add timing logs
        ↓
2. Run several real prompts
        ↓
3. Identify the measured bottleneck
        ↓
4. Add Session connection reuse
        ↓
5. Add bounded Jikan concurrency
        ↓
6. Cache searches and anime details
        ↓
7. Reduce the Gemini ranking payload
        ↓
8. Evaluate combining the first two Gemini calls
```

The logging should also time individual Jikan requests—not only the overall retrieval stage. Otherwise, we’ll know retrieval took eight seconds but won’t know whether that was caused by one slow query, too many queries, rate limiting, or retries.

My expectation is that sequential Jikan requests and Japanese-title enrichment are the largest avoidable delays. The logs will confirm whether that’s actually true.



1. Return exactly 10 ranked results
2. Send Gemini a smaller ranking payload
3. Benchmark
4. Add search time budgets/retry limits
5. Investigate balanced selection instead of arbitrary first 30
6. Consider combining intent parsing and suggestions