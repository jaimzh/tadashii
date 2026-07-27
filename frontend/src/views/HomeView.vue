<script setup>
import AnimatedHero from '@/components/common/AnimatedHero.vue'
import SearchBar from '@/components/common/SearchBar.vue'
</script>

<template>
  <div class="home-view">
    <div class="wrapper">
      <AnimatedHero>
        <h1 class="hero-title">Find your next favorite anime</h1>
        <p class="hero-subtitle">Describe what you're in the mood for</p>
        <SearchBar />
      </AnimatedHero>
    </div>
  </div>
</template>

<style scoped>
.home-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.wrapper {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0 0 12px;
  color: #000;
}

.hero-subtitle {
  font-size: 1.1rem;
  color: #aaa;
  margin: 0 0 32px;
}
</style>
