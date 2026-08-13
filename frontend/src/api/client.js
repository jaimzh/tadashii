import { mockRecommendationResponse } from '@/data/mockRecommendations.js'

// Keep this true while designing the results UI. Set it to false to use FastAPI again.
const USE_MOCK_DATA = true

export async function recommend(prompt) {
  if (USE_MOCK_DATA) {
    await new Promise((resolve) => setTimeout(resolve, 5000))

    return {
      ...mockRecommendationResponse,
      input: prompt,
    }
  }

  const res = await fetch('/api/recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt }),
  })
  if (!res.ok) throw new Error(`API error: ${res.status}`)
  return res.json()
}

export async function getTrailer(malId) {
  if (USE_MOCK_DATA) {
    const recommendation = mockRecommendationResponse.results.find(
      (result) => result.anime.mal_id === malId,
    )

    return {
      mal_id: malId,
      trailer_url: recommendation?.anime.trailer_url || null,
    }
  }

  const res = await fetch(`/api/anime/${malId}/trailer`)
  if (!res.ok) throw new Error(`Trailer API error: ${res.status}`)
  return res.json()
}
