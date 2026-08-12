<script setup>
import { ref, onUnmounted } from 'vue'
import AppHeader from '@/components/common/AppHeader.vue'
import HomeView from './views/HomeView.vue'
import ResultView from './views/ResultView.vue'
import { recommend } from './api/client.js'

const stage = ref('home')
const searchQuery = ref('')
const searchOrigin = ref(null)
let loadTimer = null
const results = ref([])

function toCardResult(recommendation) {
  const anime = recommendation.anime

  return {
    id: anime.mal_id,
    title: anime.title_english || anime.title,
    japaneseName: anime.title_japanese || '',
    image: anime.image || '',
    episodes: anime.episodes ? String(anime.episodes) : 'N/A',
    rating: anime.score ? String(anime.score) : 'N/A',
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

async function handleSearch(query, rect) {
  searchQuery.value = query
  searchOrigin.value = rect
  stage.value = 'loading'


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
  <div class="wrapper">
    <AppHeader
      :is-searching="stage !== 'home'"
      :is-loading="stage === 'loading'"
      :query="searchQuery"
      :search-origin="searchOrigin"
      @search="handleSearch"
    />
    <HomeView
      v-if="stage === 'home' || stage === 'loading'"
      :is-searching="stage === 'loading'"
      @search="handleSearch"
    />
    <ResultView v-else-if="stage === 'results'" :results="results" />
  </div>
</template>

<style>
.wrapper {
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  width: 100%;
  box-sizing: border-box;
  padding-left: 24px;
  padding-right: 24px;
}
</style>
