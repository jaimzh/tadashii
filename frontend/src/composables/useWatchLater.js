import { computed, ref } from 'vue'

const STORAGE_KEY = 'tadashii-watch-later-v1'

function loadSavedAnime() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    const parsed = stored ? JSON.parse(stored) : []
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

const savedAnime = ref(loadSavedAnime())

function saveWatchLaterList() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(savedAnime.value))
}

function isSaved(malId) {
  return savedAnime.value.some((anime) => anime.malId === malId)
}

function removeSaved(malId) {
  const existingIndex = savedAnime.value.findIndex(
    (anime) => anime.malId === malId,
  )

  if (existingIndex < 0) return false

  savedAnime.value.splice(existingIndex, 1)
  saveWatchLaterList()
  return true
}

function setWatched(malId, watched) {
  const anime = savedAnime.value.find((item) => item.malId === malId)

  if (!anime) return false

  anime.watched = watched
  saveWatchLaterList()
  return true
}

function toggleSaved(result) {
  const existingIndex = savedAnime.value.findIndex(
    (anime) => anime.malId === result.id,
  )

  if (existingIndex >= 0) {
    removeSaved(result.id)
    return false
  }

  savedAnime.value.push({
    malId: result.id,
    title: result.title,
    englishName: result.englishName || '',
    romajiName: result.romajiName || '',
    japaneseName: result.japaneseName || '',
    image: result.image || '',
    type: result.type || '',
    year: result.year || '',
    watched: false,
    addedAt: new Date().toISOString(),
  })
  saveWatchLaterList()
  return true
}

export function useWatchLater() {
  return {
    savedAnime,
    savedCount: computed(() => savedAnime.value.length),
    isSaved,
    removeSaved,
    setWatched,
    toggleSaved,
  }
}
