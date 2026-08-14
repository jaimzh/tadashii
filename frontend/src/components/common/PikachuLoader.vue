<script setup>
import { onBeforeUnmount, ref } from 'vue'

defineProps({
  text: {
    type: String,
    default: 'Loading...',
  },
})

const cursorVisible = ref(false)
const cursorPosition = ref({ x: 0, y: 0 })
const clickParticles = ref([])
let particleId = 0
const particleTimers = new Set()

function moveCursor(event) {
  const bounds = event.currentTarget.getBoundingClientRect()
  cursorPosition.value = {
    x: event.clientX - bounds.left,
    y: event.clientY - bounds.top,
  }
  cursorVisible.value = true
}

function addClickParticle(event) {
  const bounds = event.currentTarget.getBoundingClientRect()
  const id = particleId++

  clickParticles.value.push({
    id,
    x: event.clientX - bounds.left,
    y: event.clientY - bounds.top,
  })

  const timer = window.setTimeout(() => {
    clickParticles.value = clickParticles.value.filter((particle) => particle.id !== id)
    particleTimers.delete(timer)
  }, 650)

  particleTimers.add(timer)
}

onBeforeUnmount(() => {
  particleTimers.forEach((timer) => window.clearTimeout(timer))
})
</script>

<template>
  <div
    class="pikachu-loader"
    role="status"
    :aria-label="text"
    @pointermove="moveCursor"
    @pointerenter="cursorVisible = true"
    @pointerleave="cursorVisible = false"
    @click="addClickParticle"
  >
    <div class="pikachu-loader__content">
      <div class="pikachu-loader__frame">
        <iframe
          src="https://giphy.com/embed/kuWN0iF9BLQKk"
          class="giphy-embed"
          title="Running Pikachu loading animation"
          frameborder="0"
          allowfullscreen
        ></iframe>
      </div>
      <p class="pikachu-loader__credit">
        <a
          href="https://giphy.com/stickers/pokemon-running-kuWN0iF9BLQKk"
          target="_blank"
          rel="noreferrer"
        >
          via GIPHY
        </a>
      </p>
      <span class="pikachu-loader__text">{{ text }}</span>
    </div>

    <span
      v-if="cursorVisible"
      class="mouse-dot mouse-dot--cursor"
      :style="{
        left: `${cursorPosition.x}px`,
        top: `${cursorPosition.y}px`,
      }"
      aria-hidden="true"
    ></span>

    <span
      v-for="particle in clickParticles"
      :key="particle.id"
      class="mouse-dot mouse-dot--particle"
      :style="{
        left: `${particle.x}px`,
        top: `${particle.y}px`,
      }"
      aria-hidden="true"
    ></span>
  </div>
</template>

<style scoped>
.pikachu-loader {
  position: relative;
  display: grid;
  place-items: center;
  width: 100%;
  min-height: 100%;
  overflow: hidden;
  background: var(--bg-base);
}

.pikachu-loader__content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.25rem;
  padding: 1.5rem;
  text-align: center;
}

.pikachu-loader__frame {
  width: min(480px, 82vw);
  aspect-ratio: 480 / 343;
  overflow: hidden;
  border-radius: 14px;
}

.giphy-embed {
  display: block;
  width: 100%;
  height: 100%;
  border: 0;
}

.pikachu-loader__credit {
  margin-top: -0.85rem;
  font-size: var(--font-size-xs);
}

.pikachu-loader__credit a {
  color: var(--text-muted);
  text-decoration: none;
}

.pikachu-loader__credit a:hover {
  color: var(--accent);
}

.pikachu-loader__text {
  background: linear-gradient(
    100deg,
    var(--text-muted) 20%,
    var(--text-main) 48%,
    var(--accent) 52%,
    var(--text-muted) 80%
  );
  background-size: 250% 100%;
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  font-size: var(--font-size-md);
  animation: loading-text 2.4s linear infinite;
}

.mouse-dot {
  position: absolute;
  z-index: 2;
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background: #fff782;
  pointer-events: none;
  transform: translate(-50%, -50%);
}

.mouse-dot--cursor {
  animation: mouse-pulse 0.5s ease-in-out infinite alternate;
}

.mouse-dot--particle {
  animation: click-particle 0.65s ease-out forwards;
}

@keyframes mouse-pulse {
  to {
    width: 15px;
    height: 15px;
  }
}

@keyframes click-particle {
  to {
    opacity: 0;
    transform: translate(-50%, -50%) scale(2.2);
  }
}

@keyframes loading-text {
  from {
    background-position: 100% 0;
  }
  to {
    background-position: -150% 0;
  }
}

@media (hover: hover) and (pointer: fine) {
  .pikachu-loader,
  .pikachu-loader * {
    cursor: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .pikachu-loader__text,
  .mouse-dot--cursor,
  .mouse-dot--particle {
    animation: none;
  }

  .pikachu-loader__text {
    background: none;
    color: var(--text-main);
  }
}
</style>
