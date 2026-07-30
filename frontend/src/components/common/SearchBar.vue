<script setup>
import { ref } from 'vue'
import { PhMagnifyingGlass } from '@phosphor-icons/vue'

const query = ref('')

function handleSubmit() {
  if (query.value.trim()) {
    // TODO: navigate to results or trigger search
  }
}
</script>

<template>
  <form class="search-container" @submit.prevent="handleSubmit">
    <input
      v-model="query"
      type="text"
      autocomplete="off"
      class="search-input"
      placeholder="What do you feel like watching?"
    />
    <button
      type="submit"
      class="search-button"
      :disabled="!query.trim()"
      aria-label="Search"
    >
      <PhMagnifyingGlass :size="22" weight="bold" />
    </button>
  </form>
</template>

<style scoped>
@keyframes trail {
  0% { offset-distance: 0%; }
  100% { offset-distance: 100%; }
}

.search-container {
  position: relative;
  display: flex;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  border-radius: 50px;
  padding: 1px;
  overflow: hidden;
   background: color-mix(in srgb, var(--border-color) 50%, transparent);
  transition: background 0.3s ease;
}

.search-container:focus-within {
  background: color-mix(in srgb, var(--accent) 50%, transparent);

}

.search-container::before,
.search-container::after {
  content: "";
  position: absolute;
  width: 100px;
  aspect-ratio: 1;
  background: radial-gradient(100% 100% at right, transparent, white 5%, color-mix(in srgb, var(--accent) 40%, white) 25%, transparent 70%);
  offset-path: border-box;
  offset-anchor: 100% 50%;
  filter: blur(8px);
  pointer-events: none;
  animation: trail 8s linear infinite;
  
}

.search-container::before {
  z-index: 1;
}

.search-container::after {
  z-index: 2;
  animation-delay: -4s;
  opacity: 0.5;
}

.search-input,
.search-button {
  position: relative;
  z-index: 3;
}

.search-input {
  flex: 1;
  padding: 20px 28px;
  border: none;
  border-radius: 50px 0 0 50px;
  font-size: 1.25rem;
  outline: none;
  background: var(--bg-base);
  color: var(--text-main);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.search-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 32px;
  background: var(--bg-base);
  color: var(--text-muted);
  border: none;
  border-radius: 0 50px 50px 0;
  cursor: pointer;
  transition: color 0.2s ease;
}

.search-button:disabled {
  cursor: default;
}

.search-button:not(:disabled) {
  
  color: var(--accent);
}

.search-button:not(:disabled):hover {
  color: color-mix(in srgb, var(--accent) 80%, white);
}
</style>