<script setup>
import { ref } from 'vue'
import AnimatedHero from '@/components/common/AnimatedHero.vue'
import SearchBar from '@/components/common/SearchBar.vue'
import Loader from '@/components/common/Loader.vue'

const isDarkMode = ref(true)
const isSearching = ref(false)

function handleSearch() {
  isSearching.value = true
}
</script>

<template>
  <div class="home-view">
    <div class="wrapper">
      <Loader v-if="isSearching" />
      <AnimatedHero v-else />
      <SearchBar @submit="handleSearch" />
      <div class="hero-glow"></div>
    </div>
  </div>
</template>

<style scoped>
.home-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  margin-top:-4rem ;

  
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
  border: 1px solid red;

}


</style>
