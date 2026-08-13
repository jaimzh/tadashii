<script setup>
import { ref, watch } from 'vue'
import { PhDiceFive, PhMagnifyingGlass } from '@phosphor-icons/vue'
import { surpriseQueries } from '@/data/surpriseQueries'

const props = defineProps({
  value: {
    type: String,
    default: '',
  },
  readonly: {
    type: Boolean,
    default: false,
  },
})
const emit = defineEmits(['submit'])

const query = ref(props.value)

watch(
  () => props.value,
  (v) => {
    query.value = v
  }
)

function handleSubmit() {
  if (props.readonly) return
  if (query.value.trim()) {
    emit('submit', query.value.trim())
  }
}

function surpriseMe() {
  if (props.readonly || !surpriseQueries.length) return

  const availableQueries = surpriseQueries.filter((item) => item !== query.value)
  const choices = availableQueries.length ? availableQueries : surpriseQueries
  query.value = choices[Math.floor(Math.random() * choices.length)]
}
</script>

<template>
  <form class="search-container" @submit.prevent="handleSubmit">
    <input
      v-model="query"
      type="text"
      autocomplete="off"
      class="search-input"
      :readonly="readonly"
      :placeholder="readonly ? '' : 'What do you feel like watching?'"
    />
    <div class="search-actions">
      <button
        type="button"
        class="surprise-button"
        :disabled="readonly"
        aria-label="Surprise me"
        title="Surprise me"
        @click="surpriseMe"
      >
        <PhDiceFive :size="22" weight="bold" />
      </button>
      <button
        type="submit"
        class="search-button"
        :disabled="readonly || !query.trim()"
        aria-label="Search"
      >
        <PhMagnifyingGlass :size="22" weight="bold" />
      </button>
    </div>
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
  max-width: 520px;
  margin: 0 auto;
  border-radius: 50px;
  padding: 1px;
  overflow: hidden;
  background: color-mix(in srgb, var(--border-color) 70%, transparent);
  transition: background 0.3s ease;
   box-shadow: 0 8px 6px -6px rgba(0, 0, 0, 0.4);
}

.search-container:focus-within {
  background: color-mix(in srgb, var(--accent) 50%, transparent);

}

.search-container::before,
.search-container::after {
  content: "";
  position: absolute;
  width: 150px;
  aspect-ratio: 1;
  background: radial-gradient(circle, white 10%, color-mix(in srgb, var(--accent) 40%, white) 40%, transparent 70%);
  offset-path: border-box;
  offset-anchor: 50% 50%;
  filter: blur(6px);
  pointer-events: none;
  animation: trail 5s linear infinite;
}

.search-container::before {
  z-index: 2;
}

.search-container::after {
  z-index: 1;
  animation-delay: -2.5s;
  opacity: 0.5;
}

.search-input,
.search-actions {
  position: relative;
  z-index: 3;
}

.search-input {
  flex: 1;
  min-width: 0;
  padding: 14px 20px;
  border: none;
  border-radius: 50px 0 0 50px;
  font-size: var(--font-size-base);
  outline: none;
  background: var(--bg-base);
  color: var(--text-main);
}

.search-actions {
  display: flex;
  flex: 0 0 auto;
  align-items: stretch;
  overflow: hidden;
  border-radius: 0 50px 50px 0;
  background: var(--bg-base);
}

.surprise-button,
.search-button {
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  transition: color 0.2s ease;
  
}

.surprise-button {
  padding: 14px 8px;
}

.surprise-button:not(:disabled):hover,
.search-button:not(:disabled):hover {
  color: color-mix(in srgb, var(--accent) 82%, white);
}

.surprise-button svg,
.search-button svg {
  transition: transform 0.2s ease;
}

.surprise-button:not(:disabled):hover svg {
  transform: translateY(-2px) rotate(12deg);
}

.search-button:not(:disabled):hover svg {
  transform: translateY(-2px);
}

.surprise-button:focus-visible,
.search-button:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: -4px;
}

.surprise-button:disabled,
.search-button:disabled {
  cursor: pointer;
 
}

.search-input::placeholder {
  color: var(--text-muted);
  opacity: 0.4;
}

.search-button {
  padding: 14px 16px 14px 10px;
}
</style>
