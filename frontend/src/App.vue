<script setup>
import { computed, ref, onUnmounted } from 'vue'
import AppHeader from '@/components/common/AppHeader.vue'
import HomeView from './views/HomeView.vue'
import ResultView from './views/ResultView.vue'
import { recommend } from './api/client.js'
import Aurora from './components/common/Aurora.vue'
import { useTheme } from '@/coposables/useTheme'

const stage = ref('home')
const searchQuery = ref('')
const searchOrigin = ref(null)
let loadTimer = null
const results = ref([])
const searchError = ref('')
const { theme } = useTheme()

const auroraColors = computed(() => {
  if (theme.value === 'light') {
    return ['#DCEEFF', '#4A9DFF', '#F7FBFF']
  }

  if (theme.value === 'zen') {
    return ['#456B8C', '#935B37', '#E5D2B4']
  }

  return ['#071A33', '#007BFF', '#182B46']
})

function toCardResult(recommendation) {
  const anime = recommendation.anime

  return {
    id: anime.mal_id,
    title: anime.title_english || anime.title,
    japaneseName: anime.title_japanese || '',
    image: anime.image || '',
    episodes: anime.episodes ? String(anime.episodes) : 'N/A',
    rating: anime.score ? String(anime.score) : 'N/A',
    type: anime.type || 'TV',
    year: anime.year ? String(anime.year) : '',
    genres: anime.genres.join(', '),
    studio: anime.studios.join(', '),
    synopsis: anime.synopsis || '',
    reason: recommendation.reason || '',
    matchScore: recommendation.match_score,
    emotionTags: recommendation.emotion_tags,
    url: anime.url || '',
  }
}

function goHome() {
  clearTimeout(loadTimer)
  stage.value = 'home'
  searchQuery.value = ''
  searchOrigin.value = null
  searchError.value = ''
}

async function handleSearch(query, rect) {
  searchQuery.value = query
  searchOrigin.value = rect
  stage.value = 'loading'
  searchError.value = ''


   try {
  const data = await recommend(query)
  const convertedResults = []

  for (const recommendation of data.results) {
    const cardResult = toCardResult(recommendation)
    convertedResults.push(cardResult)
  }

  results.value = convertedResults
  stage.value = 'results'

  console.log('API RESPONSE:', data)
  console.log('RESULTS:', results.value)
} catch (err) {
  console.error('Search failed:', err)
  searchError.value = err instanceof Error ? err.message : 'Search failed. Please try again.'
  stage.value = 'home'
}

  // clearTimeout(loadTimer)
  // loadTimer = setTimeout(() => {
  //   stage.value = 'results'
  // }, 10000)
}

onUnmounted(() => {
  clearTimeout(loadTimer)
})
</script>

<template>
  <div class="main">
     <!-- <Aurora
      class="app-aurora"
      :color-stops="auroraColors"
      :blend="0.5"
      :amplitude="1"
      :speed="0.5"
    /> -->
    <div class="wrapper">
    <AppHeader
      :is-searching="stage !== 'home'"
      :is-loading="stage === 'loading'"
      :query="searchQuery"
      :search-origin="searchOrigin"
      @search="handleSearch"
      @home="goHome"
    />
    <HomeView
      v-if="stage === 'home' || stage === 'loading'"
      :is-searching="stage === 'loading'"
      :error="searchError"
      @search="handleSearch"
    />
    <ResultView v-else-if="stage === 'results'" :results="results" />
  </div>
  </div>
  
</template>

<style>
.wrapper {
  max-width: 1120px;
  margin-left: auto;
  margin-right: auto;
  width: 100%;
  box-sizing: border-box;
  padding-left: 20px;
  padding-right: 20px;
}

.main {
  position: relative;
  isolation: isolate;
  min-height: 100vh;
}

.app-aurora {
  position: fixed;
  inset: 0;
  z-index: -1;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  pointer-events: none;
  opacity: .45;
}
</style>
