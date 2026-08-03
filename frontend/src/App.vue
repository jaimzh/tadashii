<script setup>
import { ref, onUnmounted } from 'vue'
import AppHeader from '@/components/common/AppHeader.vue'
import HomeView from './views/HomeView.vue'
import ResultView from './views/ResultView.vue'

const stage = ref('home')
const searchQuery = ref('')
const searchOrigin = ref(null)
let loadTimer = null

function handleSearch(query, rect) {
  searchQuery.value = query
  searchOrigin.value = rect
  stage.value = 'loading'

  clearTimeout(loadTimer)
  loadTimer = setTimeout(() => {
    stage.value = 'results'
  }, 10000)
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
    <ResultView v-else-if="stage === 'results'" />
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
