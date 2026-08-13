<script setup>
import { ref } from 'vue'
import AnimatedHero from '@/components/common/AnimatedHero.vue'
import SearchBar from '@/components/common/SearchBar.vue'
import Loader from '@/components/common/Loader.vue'

defineProps({
  isSearching: {
    type: Boolean,
    default: false,
  },
})
const emit = defineEmits(['search'])

const searchBarEl = ref(null)

function handleSearch(query) {
  const rect = searchBarEl.value?.$el?.getBoundingClientRect()
  emit('search', query, rect)
}
</script>

<template>
  <div class="home-view">
    <div class="wrapper">
      <Loader v-if="isSearching" />
      <AnimatedHero v-else />
      <SearchBar v-if="!isSearching" ref="searchBarEl" @submit="handleSearch" />
      <div class="hero-glow"></div>
    </div>
  </div>
</template>

<style scoped>
.home-view {
  position: relative;
  isolation: isolate;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  margin-top:-5rem ;

  
}

.hero-glow {
  margin-top: 20rem;
  position: absolute;
  width: 40vw;
  height: 20vw;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(var(--accent-rgb), 0.3), transparent 90%);
  filter: blur(80px);
  pointer-events: none;
  z-index: 1;
}

.wrapper {
  flex: 1;
  flex-direction: column;
  display: flex;
  align-items: center;
  justify-content: center;

}


</style>
