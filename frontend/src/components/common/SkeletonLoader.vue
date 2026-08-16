<script setup>
defineProps({
  width: {
    type: String,
    default: '5rem',
  },
  height: {
    type: String,
    default: '0.8rem',
  },
  radius: {
    type: String,
    default: '999px',
  },
})
</script>

<template>
  <span
    class="skeleton-loader"
    :style="{ width, height, borderRadius: radius }"
    aria-hidden="true"
  />
</template>

<style scoped>
.skeleton-loader {
  position: relative;
  display: inline-block;
  flex: 0 0 auto;
  max-width: 100%;
  overflow: hidden;
  background: color-mix(in srgb, var(--text-muted) 12%, transparent);
}

.skeleton-loader::after {
  position: absolute;
  inset: 0;
  content: '';
  background: linear-gradient(
    90deg,
    transparent 0%,
    color-mix(in srgb, var(--text-muted) 18%, transparent) 48%,
    transparent 100%
  );
  transform: translateX(-100%);
  animation: skeleton-shimmer 1.25s linear infinite;
}

@keyframes skeleton-shimmer {
  from {
    transform: translateX(-100%);
  }

  to {
    transform: translateX(100%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .skeleton-loader::after {
    animation: none;
  }
}
</style>
