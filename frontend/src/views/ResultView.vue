<script setup>
import { ref } from 'vue'
import ResultCard from '@/components/common/ResultCard.vue'
import ResultModal from '@/components/common/ResultModal.vue'

const placeholderResults = Array.from({ length: 9 }, (_, i) => ({
  id: i + 1,
  title: `Placeholder Title ${i + 1}`,
  japaneseName: `プレースホルダー ${i + 1}`,
  image: '',
  episodes: String((i + 1) * 12),
  rating: (3.5 + (i % 3) * 0.5).toFixed(1),
  year: String(2015 + (i % 9)),
  duration: `${20 + (i % 5) * 4} min`,
  genres: (i % 2 === 0 ? ['Action', 'Adventure'] : ['Drama', 'Slice of Life']).join(', '),
  studio: `Studio ${i + 1}`,
  synopsis:
    'A placeholder synopsis describing the story, characters, and tone of this anime. This text will eventually come from the backend.',
  reason: 'This was chosen because it matches the mood you described.',
}))

const selected = ref(null)
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
        @select="selected = result"
      />
    </div>

    <ResultModal
      v-if="selected"
      :result="selected"
      @close="selected = null"
    />
  </div>
</template>

<style scoped>
@keyframes fade-up {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-view {
  width: 100%;
  padding: 2rem 0;
  animation: fade-up 0.5s ease;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}
</style>
