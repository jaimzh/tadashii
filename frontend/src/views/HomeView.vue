<script setup>
import AnimatedHero from '@/components/common/AnimatedHero.vue'
import SearchBar from '@/components/common/SearchBar.vue'
</script>

<template>
  <div class="home-view">
    <div class="wrapper">
<AnimatedHero />
        <SearchBar />
      
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

.wrapper {
  flex: 1;
  flex-direction: column;
  display: flex;
  align-items: center;
  justify-content: center;

}


</style>
