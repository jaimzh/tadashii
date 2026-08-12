<script setup>
import { ref } from 'vue'
import ResultCard from '@/components/common/ResultCard.vue'
import ResultModal from '@/components/common/ResultModal.vue'

defineProps({
  results: {
    type: Array,
    default: () => [],
  },
})

const selected = ref(null)
</script>

<template>
  <div class="result-view">
    <div class="results-grid">
      <ResultCard
        v-for="result in results"
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
