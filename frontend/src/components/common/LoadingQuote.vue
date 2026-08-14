<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useAnimeQuotes } from '@/coposables/useAnimeQuotes.js'

const QUOTE_ROTATION_MS = 10000

const currentQuote = ref(null)
const quoteLoading = ref(true)
const { loadQuotes, getNextQuote } = useAnimeQuotes()

let rotationTimer = null
let isActive = true

async function showNextQuote() {
  const quote = await getNextQuote()

  if (isActive && quote) {
    currentQuote.value = quote
  }
}

onMounted(async () => {
  const availableQuotes = await loadQuotes()
  if (!isActive) return

  quoteLoading.value = false
  if (!availableQuotes.length) return

  await showNextQuote()

  rotationTimer = window.setInterval(async () => {
    await showNextQuote()
  }, QUOTE_ROTATION_MS)
})

onBeforeUnmount(() => {
  isActive = false

  if (rotationTimer) {
    window.clearInterval(rotationTimer)
  }
})
</script>

<template>
  <p v-if="quoteLoading" class="quote-loading">Loading...</p>

  <blockquote v-else-if="currentQuote" class="loading-quote">
    <p>“{{ currentQuote.content }}”</p>
    <footer>
      <span>— {{ currentQuote.character }}</span>
      <cite>{{ currentQuote.anime }}</cite>
    </footer>
  </blockquote>
</template>

<style scoped>
.quote-loading {
  margin-top: 2.25rem;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.loading-quote {
  width: min(90vw, 560px);
  margin: 2.25rem auto 0;
  color: var(--text-main);
  text-align: center;
}

.loading-quote p {
  background: linear-gradient(
    100deg,




    var(--text-muted) 20%,
    var(--accent) 50%,
    var(--text-muted) 80%


    /* var(--text-muted) 20%,
    var(--text-main) 45%,
    var(--accent) 50%,
    var(--text-main) 55%,
    var(--text-muted) 80% */
  );
  background-size: 250% 100%;
  background-position: 100% 0;
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
  font-size: var(--font-size-base);
  line-height: 1.7;
  animation: quote-shimmer 3s linear infinite;
}

.loading-quote footer {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.35rem 0.55rem;
  margin-top: 0.8rem;
  color: var(--text-muted);
  font-size: var(--font-size-xs);
}

.loading-quote cite {
  color: var(--accent);
  font-style: normal;
}

@keyframes quote-shimmer {
  to {
    background-position: -150% 0;
  }
}

@media (max-width: 560px) {
  .loading-quote {
    width: min(84vw, 420px);
  }

  .loading-quote p {
    font-size: var(--font-size-sm);
  }
}

@media (prefers-reduced-motion: reduce) {
  .loading-quote p {
    background: none;
    color: var(--text-main);
    animation: none;
  }
}
</style>
