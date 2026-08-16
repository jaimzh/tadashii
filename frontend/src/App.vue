<script setup>
import { computed, ref, onUnmounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppHeader from '@/components/common/AppHeader.vue'
import AppFooter from '@/components/common/AppFooter.vue'
import { recommend } from './api/client.js'

const route = useRoute()
const router = useRouter()
const isLoading = ref(false)
const searchQuery = ref('')
const searchOrigin = ref(null)
let loadTimer = null
const results = ref([])
const searchError = ref('')
const MIN_LOADING_TIME = 0
const showHeaderSearch = computed(
  () => isLoading.value || route.name !== 'home',
)

function viewProps(routeName) {
  if (routeName === 'home') {
    return {
      isSearching: isLoading.value,
      error: searchError.value,
    }
  }

  if (routeName === 'results') {
    return { results: results.value }
  }

  return {}
}

function toCardResult(recommendation) {
  const anime = recommendation.anime
  const displayTitle = anime.title_english || anime.title

  return {
    id: anime.mal_id,
    title: displayTitle,
    englishName: anime.title_english !== displayTitle ? anime.title_english : '',
    romajiName: anime.title !== displayTitle ? anime.title : '',
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
  isLoading.value = false
  searchQuery.value = ''
  searchOrigin.value = null
  searchError.value = ''
  router.push({ name: 'home' })
}

async function handleSearch(query, rect) {
  searchQuery.value = query
  searchOrigin.value = rect
  isLoading.value = true
  searchError.value = ''
  await router.push({ name: 'home' })


   try {
  // const data = await recommend(query)
  const [data] = await Promise.all([
  recommend(query),
  new Promise((resolve) => setTimeout(resolve, MIN_LOADING_TIME)),
])
  const convertedResults = []

  for (const recommendation of data.results) {
    const cardResult = toCardResult(recommendation)
    convertedResults.push(cardResult)
  }

  results.value = convertedResults
  isLoading.value = false
  await router.push({ name: 'results' })

  console.log('API RESPONSE:', data)
  console.log('RESULTS:', results.value)
} catch (err) {
  console.error('Search failed:', err)
  searchError.value = err instanceof Error ? err.message : 'Search failed. Please try again.'
  isLoading.value = false
  await router.push({ name: 'home' })
}

  // clearTimeout(loadTimer)
  // loadTimer = setTimeout(() => {
  //   stage.value = 'results'
  // }, 10000)
}

watch(
  () => route.name,
  (routeName) => {
    if (routeName === 'results' && !results.value.length) {
      router.replace({ name: 'home' })
    }
  },
  { immediate: true },
)

onUnmounted(() => {
  clearTimeout(loadTimer)
})
</script>

<template>
  <div class="main">
    <div class="wrapper">
      <AppHeader
        :is-searching="showHeaderSearch"
        :is-loading="isLoading"
        :query="searchQuery"
        :search-origin="searchOrigin"
        @search="handleSearch"
        @home="goHome"
      />
      <RouterView v-slot="{ Component, route: activeRoute }">
        <component
          :is="Component"
          v-bind="viewProps(activeRoute.name)"
          @search="handleSearch"
        />
      </RouterView>
    </div>
    <AppFooter />
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
  display: flex;
  flex-direction: column;
}

.main > .wrapper {
  flex: 1;
}
</style>
