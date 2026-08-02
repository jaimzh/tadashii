<script setup>
import { ref } from 'vue'
import AppHeader from '@/components/common/AppHeader.vue'
import HomeView from './views/HomeView.vue'
import ResultView from './views/ResultView.vue'

const isSearching = ref(false)
const searchQuery = ref('')
const searchOrigin = ref(null)

function handleSearch(query, rect) {
  searchQuery.value = query
  searchOrigin.value = rect
  isSearching.value = true
}
</script>

<template>
  <div class="wrapper">
    <AppHeader
      :is-searching="isSearching"
      :query="searchQuery"
      :search-origin="searchOrigin"
    />
    <HomeView :is-searching="isSearching" @search="handleSearch" />
    <ResultView />
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
