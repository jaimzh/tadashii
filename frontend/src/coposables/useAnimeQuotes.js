import { ref } from 'vue'
import { fetchQuoteList } from '@/api/client.js'

const CACHE_KEY = 'tadashii-anime-quotes-v2'
const CACHE_DURATION_MS = 24 * 60 * 60 * 1000

const quotes = ref([])
const currentIndex = ref(0)
const expiresAt = ref(0)
const isLoading = ref(false)
const error = ref('')

function isValidQuote(quote) {
  return (
    quote &&
    typeof quote.content === 'string' &&
    quote.content.trim() &&
    typeof quote.character === 'string' &&
    quote.character.trim() &&
    typeof quote.anime === 'string' &&
    quote.anime.trim()
  )
}

function normalizeQuotes(items) {
  const seen = new Set()

  return (Array.isArray(items) ? items : []).filter((quote) => {
    if (!isValidQuote(quote)) return false

    const key = quote.content.trim().toLowerCase()
    if (seen.has(key)) return false

    seen.add(key)
    return true
  })
}

function readCache() {
  try {
    const cached = JSON.parse(localStorage.getItem(CACHE_KEY))
    const cachedQuotes = normalizeQuotes(cached?.quotes)
    const cachedIndex = Number.isInteger(cached?.currentIndex) ? cached.currentIndex : 0
    const cachedExpiry = Number(cached?.expiresAt) || 0

    if (
      cachedExpiry <= Date.now() ||
      !cachedQuotes.length ||
      cachedIndex < 0 ||
      cachedIndex >= cachedQuotes.length
    ) {
      return null
    }

    return {
      quotes: cachedQuotes,
      currentIndex: cachedIndex,
      expiresAt: cachedExpiry,
    }
  } catch {
    return null
  }
}

function writeCache() {
  try {
    localStorage.setItem(
      CACHE_KEY,
      JSON.stringify({
        quotes: quotes.value,
        currentIndex: currentIndex.value,
        expiresAt: expiresAt.value,
      }),
    )
  } catch {
    // Quotes are optional, so storage failures should not affect recommendations.
  }
}

function clearQuoteCache() {
  quotes.value = []
  currentIndex.value = 0
  expiresAt.value = 0
  error.value = ''

  try {
    localStorage.removeItem(CACHE_KEY)
  } catch {
    // Ignore unavailable browser storage.
  }
}

async function loadQuotes() {
  if (expiresAt.value > Date.now() && currentIndex.value < quotes.value.length) {
    return quotes.value
  }

  const cached = readCache()
  if (cached) {
    quotes.value = cached.quotes
    currentIndex.value = cached.currentIndex
    expiresAt.value = cached.expiresAt
    return quotes.value
  }

  isLoading.value = true
  error.value = ''

  try {
    const response = await fetchQuoteList()
    const fetchedQuotes = normalizeQuotes(response?.quotes)

    if (!fetchedQuotes.length) {
      throw new Error('The quote API returned no usable quotes.')
    }

    quotes.value = fetchedQuotes
    currentIndex.value = 0
    expiresAt.value = Date.now() + CACHE_DURATION_MS
    writeCache()

    return quotes.value
  } catch (requestError) {
    error.value = requestError instanceof Error ? requestError.message : 'Could not load quotes.'
    return []
  } finally {
    isLoading.value = false
  }
}

async function getNextQuote() {
  if (
    expiresAt.value > Date.now() &&
    quotes.value.length &&
    currentIndex.value >= quotes.value.length
  ) {
    clearQuoteCache()
  }

  await loadQuotes()

  const quote = quotes.value[currentIndex.value]
  if (!quote) return null

  currentIndex.value += 1
  writeCache()

  return quote
}

export function useAnimeQuotes() {
  return {
    quotes,
    currentIndex,
    isLoading,
    error,
    loadQuotes,
    getNextQuote,
    clearQuoteCache,
  }
}
