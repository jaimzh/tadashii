import { mockRecommendationResponse } from '@/data/mockRecommendations.js'

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || '').replace(/\/$/, '')

// false = use the real FastAPI backend; true = use local UI test data.
const USE_MOCK_DATA = true

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

export async function getTrailer(malId) {
  if (USE_MOCK_DATA) {
    const recommendation = mockRecommendationResponse.results.find(
      (result) => result.anime.mal_id === malId,
    )

    return {
      mal_id: malId,
      trailer_url: recommendation?.anime.trailer_url || null,
      title_japanese: recommendation?.anime.title_japanese || null,
    }
  }

  return request(`/api/anime/${malId}/trailer`)
}
