<script setup>
import AppHeader from '@/components/common/AppHeader.vue'
import HomeView from './views/HomeView.vue'
</script>

<template>
  <div class="wrapper">
  <AppHeader />
  <HomeView />
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
