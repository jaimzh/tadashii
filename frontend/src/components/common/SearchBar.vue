<script setup>
import { ref } from 'vue'

const query = ref('')

function handleSubmit() {
  if (query.value.trim()) {
    // TODO: navigate to results or trigger search
  }
}
</script>

<template>
  <form class="search-bar" @submit.prevent="handleSubmit">
    <input
      v-model="query"
      type="text"
      class="search-input"
      placeholder="Describe the anime you're looking for..."
    />
    <button type="submit" class="search-button">Search</button>
  </form>
</template>

<style scoped>
.search-bar {
  display: flex;
  max-width: 640px;
  margin: 0 auto;
}

.search-input {
  flex: 1;
  padding: 14px 20px;
  border: 1px solid #ccc;
  border-radius: 999px 0 0 999px;
  font-size: 1rem;
  outline: none;
}

.search-input:focus {
  border-color: #666;
}

.search-button {
  padding: 14px 28px;
  background: #000;
  color: #fff;
  border: none;
  border-radius: 0 999px 999px 0;
  font-size: 1rem;
  cursor: pointer;
}

.search-button:hover {
  background: #222;
}
</style>
