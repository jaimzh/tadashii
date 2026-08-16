<script setup>
import { ref } from 'vue'
import ResultCard from '@/components/common/ResultCard.vue'
import ResultModal from '@/components/common/ResultModal.vue'
import { getAnimeDetails } from '@/api/client.js'

defineProps({
  results: {
    type: Array,
    default: () => [],
  },
})

const selected = ref(null)

async function selectResult(result) {
  selected.value = {
    ...result,
    detailsLoading: true,
    trailerUrl: null,
    highResImage: null,
  }

  try {
    const details = await getAnimeDetails(result.id)

    if (selected.value?.id === result.id) {
      selected.value.englishName =
        details.title_english || selected.value.englishName
      selected.value.romajiName = details.title || selected.value.romajiName
      selected.value.japaneseName =
        details.title_japanese || selected.value.japaneseName
      selected.value.highResImage = details.image_url || null
      selected.value.studio =
        details.studios?.join(', ') || selected.value.studio
      selected.value.synopsis = details.synopsis || selected.value.synopsis
      selected.value.trailerUrl = details.trailer_url
      selected.value.year = details.year ? String(details.year) : selected.value.year
      selected.value.status = details.status || ''
      selected.value.airedFrom = details.aired_from || ''
      selected.value.airedTo = details.aired_to || ''
    }
  } catch (error) {
    console.error('Anime detail lookup failed:', error)
  } finally {
    if (selected.value?.id === result.id) {
      selected.value.detailsLoading = false
    }
  }
}
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
        :synopsis="result.synopsis"
        @select="selectResult(result)"
      />
    </div>

    <Transition name="result-modal">
      <ResultModal
        v-if="selected"
        :result="selected"
        @close="selected = null"
      />
    </Transition>
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
  padding: 1.5rem 0 2rem;
  animation: fade-up 0.5s ease;
}

.results-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: stretch;
  gap: 1rem;
}

.result-modal-leave-active {
  transition: opacity 180ms ease-in;
}

.result-modal-leave-active :deep(.modal-shell) {
  animation: none;
  transition: opacity 180ms ease-in, transform 180ms ease-in;
}

.result-modal-leave-to {
  opacity: 0;
}

.result-modal-leave-to :deep(.modal-shell) {
  opacity: 0;
  transform: translateY(8px) scale(0.96);
}

@media (max-width: 720px) {
  .results-grid {
    grid-template-columns: 1fr;
  }
}
</style>
