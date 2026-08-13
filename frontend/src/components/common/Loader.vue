<template>
  <span class="loader" role="status" aria-label="Generating recommendations"></span>
</template>

<style scoped>
.loader {
  --color-1: var(--text-main);
  --color-2: color-mix(in srgb, var(--text-main) 20%, transparent);
  --size: 0.4px;

  width: calc(16 * var(--size));
  height: calc(16 * var(--size));
  box-shadow:
    0 calc(30 * var(--size)),
    0 calc(-30 * var(--size));
  border-radius: calc(4 * var(--size));
  background: currentColor;
  display: block;
  margin: calc(-50 * var(--size)) auto 0;
  position: relative;
  z-index: 2;
  color: var(--color-1);
  transform: translateY(calc(30 * var(--size)));
  box-sizing: border-box;
  animation: animloader 2s ease infinite;
}

.loader::after,
.loader::before {
  content: '';
  box-sizing: border-box;
  width: calc(16 * var(--size));
  height: calc(16 * var(--size));
  box-shadow:
    0 calc(30 * var(--size)),
    0 calc(-30 * var(--size));
  border-radius: calc(4 * var(--size));
  background: currentColor;
  color: var(--color-1);
  position: absolute;
  left: calc(30 * var(--size));
  top: 0;
  animation: animloader 2s 0.2s ease infinite;
}

.loader::before {
  animation-delay: 0.4s;
  left: calc(60 * var(--size));
}

@keyframes animloader {
  0% {
    top: 0;
    color: var(--color-1);
  }
  50% {
    top: calc(30 * var(--size));
    color: var(--color-2);
  }
  100% {
    top: 0;
    color: var(--color-1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .loader,
  .loader::before,
  .loader::after {
    animation: none;
  }
}
</style>
