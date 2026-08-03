<script setup>
import { ref, watch } from 'vue'
import { PhMagnifyingGlass } from '@phosphor-icons/vue'

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
    <button
      type="submit"
      class="search-button"
      :disabled="readonly || !query.trim()"
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
.search-button {
  position: relative;
  z-index: 3;
}

.search-input {
  flex: 1;
  padding: 20px 28px;
  border: none;
  border-radius: 50px 0 0 50px;
  font-size: var(--font-size-lg);
  outline: none;
  background: var(--bg-base);
  color: var(--text-main);
}

.search-input::placeholder {
  color: var(--text-muted);
  opacity: 0.4;
}

.search-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 32px;
  
  background: var(--bg-base);
  color: color-mix(in srgb, var(--text-muted) 42%, white);
  border: none;
  border-radius: 0 50px 50px 0;
  cursor: pointer;
  transition: color 0.2s ease;
}

.search-button:disabled {
  cursor: default;
}

.search-button:not(:disabled) {
  
  color: color-mix(in srgb, var(--accent) 42%, white);

  
}

.search-button:not(:disabled):hover {
  color: color-mix(in srgb, var(--accent) 82%, white);
}
</style>