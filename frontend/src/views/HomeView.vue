<script setup>
import { ref } from 'vue'
import AnimatedHero from '@/components/common/AnimatedHero.vue'
import SearchBar from '@/components/common/SearchBar.vue'

const isDarkMode = ref(true)
</script>

<template>
  <div class="home-view">
    <div class="wrapper">
<AnimatedHero />
        <SearchBar />
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

}


</style>
