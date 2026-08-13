<script setup>
defineProps({
  text: {
    type: String,
    required: true,
  },
  position: {
    type: String,
    default: 'top',
  },
})
</script>

<template>
  <span class="text-hint" :class="`text-hint--${position}`">
    <slot />
    <span class="text-hint__message" role="tooltip">{{ text }}</span>
  </span>
</template>

<style scoped>
.text-hint {
  position: relative;
  display: inline-flex;
  align-items: stretch;
}

.text-hint__message {
  position: absolute;
  z-index: 1000;
  width: max-content;
  padding: 0.4rem 0.65rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-light);
  color: var(--text-main);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  font-size: var(--font-size-xs);
  pointer-events: none;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.15s ease;
}

.text-hint:hover .text-hint__message {
  opacity: 1;
  visibility: visible;
}

.text-hint--top .text-hint__message {
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
}

.text-hint--bottom .text-hint__message {
  top: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
}

.text-hint--left .text-hint__message {
  top: 50%;
  right: calc(100% + 8px);
  transform: translateY(-50%);
}

.text-hint--right .text-hint__message {
  top: 50%;
  left: calc(100% + 8px);
  transform: translateY(-50%);
}
</style>
