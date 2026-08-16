import { mockRecommendationResponse } from '@/data/mockRecommendations.js'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

// false = use the real FastAPI backend; true = use local UI test data.
const USE_MOCK_DATA = false
const animeDetailsCache = new Map()

async function request(path, options) {
  const response = await fetch(`${API_BASE_URL}${path}`, options)

  if (!response.ok) {
    let message = `API request failed (${response.status})`

    try {
      const body = await response.json()
      message = body.detail || body.message || message
    } catch {
      // Keep the status-based message when the API does not return JSON.
    }

    throw new Error(message)
  }

  return response.json()
}

export async function recommend(prompt) {
  if (USE_MOCK_DATA) {
    return {
      ...mockRecommendationResponse,
      input: prompt,
    }
  }

  return request('/api/recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt }),
  })
}

export async function getAnimeDetails(malId) {
  if (animeDetailsCache.has(malId)) {
    return animeDetailsCache.get(malId)
  }

  let detailsRequest

  if (USE_MOCK_DATA) {
    const recommendation = mockRecommendationResponse.results.find(
      (result) => result.anime.mal_id === malId,
    )

    detailsRequest = Promise.resolve({
      mal_id: malId,
      title: recommendation?.anime.title || null,
      title_english: recommendation?.anime.title_english || null,
      title_japanese: recommendation?.anime.title_japanese || null,
      image_url: recommendation?.anime.image || null,
      studios: recommendation?.anime.studios || [],
      synopsis: recommendation?.anime.synopsis || null,
      trailer_url: recommendation?.anime.trailer_url || null,
      year: recommendation?.anime.year || null,
      status: recommendation?.anime.status || null,
      aired_from: null,
      aired_to: null,
    })
  } else {
    detailsRequest = request(`/api/anime/${malId}/details`)
  }

  animeDetailsCache.set(malId, detailsRequest)

  try {
    return await detailsRequest
  } catch (error) {
    // Allow a temporary failure to be retried the next time the card opens.
    if (animeDetailsCache.get(malId) === detailsRequest) {
      animeDetailsCache.delete(malId)
    }
    throw error
  }
}

export async function fetchQuoteList() {
  return request('/api/quotes/list')
}
