<script setup>
import ResultCard from '@/components/common/ResultCard.vue'

const placeholderResults = Array.from({ length: 9 }, (_, i) => ({
  id: i + 1,
  title: `Placeholder Title ${i + 1}`,
  image: '',
  episodes: String((i + 1) * 12),
  rating: (3.5 + (i % 3) * 0.5).toFixed(1),
}))
</script>

<template>
  <div class="result-view">
    <div class="results-grid">
      <ResultCard
        v-for="result in placeholderResults"
        :key="result.id"
        :title="result.title"
        :image="result.image"
        :episodes="result.episodes"
        :rating="result.rating"
      />
    </div>
  </div>
</template>

<style scoped>
.result-view {
  width: 100%;
  padding: 2rem 0;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}
</style>
