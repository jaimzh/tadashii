<script setup>
import { computed } from 'vue'
import {
  PhArrowSquareOut,
  PhBookmarkSimple,
  PhList,
  PhPlay,
  PhStar,
  PhX,
} from '@phosphor-icons/vue'
import { useWatchLater } from '@/composables/useWatchLater.js'

const props = defineProps({
  result: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['close'])
const { isSaved, toggleSaved } = useWatchLater()
const savedForLater = computed(() => isSaved(props.result.id))

const genres = computed(() =>
  (props.result.genres || '')
    .split(',')
    .map((genre) => genre.trim())
    .filter(Boolean),
)

function yearFromDate(value) {
  const match = /^(\d{4})/.exec(value || '')
  return match?.[1] || ''
}

const airedLabel = computed(() => {
  const startYear = yearFromDate(props.result.airedFrom) || props.result.year || ''
  const endYear = yearFromDate(props.result.airedTo)

  if (!startYear) return ''
  if (endYear && endYear !== startYear) return `${startYear}–${endYear}`
  if (!endYear && props.result.status === 'Currently Airing') {
    return `${startYear}–Present`
  }

  return startYear
})
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <article class="modal-shell" role="dialog" aria-modal="true" :aria-label="result.title">
      <button class="close-btn" @click="emit('close')" aria-label="Close details">
        <PhX :size="18" weight="bold" />
      </button>

      <div class="modal-content">
        <div class="modal-poster">
          <img v-if="result.image" :src="result.image" :alt="`${result.title} poster`" />
          <div v-else class="poster-placeholder">Poster unavailable</div>
        </div>

        <div class="modal-info">
          <header class="modal-header">
            <div class="title-block">
              <h2 class="modal-title">{{ result.title }}</h2>
              <p v-if="result.romajiName" class="alternate-title">
                <span class="title-label">Romaji</span>
                {{ result.romajiName }}
              </p>
              <p v-if="result.japaneseName" class="alternate-title">
                <span class="title-label">Japanese</span>
                {{ result.japaneseName }}
              </p>
            </div>
          </header>

          <p v-if="result.synopsis" class="synopsis">{{ result.synopsis }}</p>

          <div class="quick-stats">
            <span>
              <PhStar :size="17" weight="fill" class="star-icon" />
              {{ result.rating }}
            </span>
            <span>
              <PhList :size="17" weight="bold" />
              {{ result.episodes }} eps
            </span>
          </div>

          <dl class="details-grid">
            <div class="detail-item">
              <dt>Aired</dt>
              <dd>{{ airedLabel || (result.trailerLoading ? 'Loading…' : 'N/A') }}</dd>
            </div>
            <div class="detail-item">
              <dt>Status</dt>
              <dd>{{ result.status || (result.trailerLoading ? 'Loading…' : 'N/A') }}</dd>
            </div>
            <div v-if="result.type" class="detail-item">
              <dt>Format</dt>
              <dd>{{ result.type }}</dd>
            </div>
            <div v-if="result.studio" class="detail-item detail-wide">
              <dt>Studio</dt>
              <dd>{{ result.studio }}</dd>
            </div>
            <div v-if="genres.length" class="detail-item detail-wide genre-detail">
              <dt>Genres</dt>
              <dd class="genre-list">
                <span v-for="genre in genres" :key="genre" class="genre-chip">
                  {{ genre }}
                </span>
              </dd>
            </div>
          </dl>

          <div v-if="result.reason" class="reason">
            <span class="reason-label">Why it matches</span>
            <p>{{ result.reason }}</p>
          </div>

          <div class="modal-actions">
            <button
              type="button"
              class="watch-btn watch-later-btn"
              :class="{ 'is-saved': savedForLater }"
              :aria-pressed="savedForLater"
              @click="toggleSaved(result)"
            >
              <PhBookmarkSimple :size="16" :weight="savedForLater ? 'fill' : 'bold'" />
              {{ savedForLater ? 'Saved' : 'Watch later' }}
            </button>

            <a
              v-if="result.url"
              class="watch-btn secondary-btn"
              :href="result.url"
              target="_blank"
              rel="noreferrer"
            >
              <PhArrowSquareOut :size="16" weight="bold" />
              View anime
            </a>

            <a
              v-if="result.trailerUrl"
              class="watch-btn trailer-btn"
              :href="result.trailerUrl"
              target="_blank"
              rel="noreferrer"
            >
              <PhPlay :size="16" weight="fill" />
              Watch trailer
            </a>

            <span v-else-if="result.trailerLoading" class="trailer-loading">
              Finding trailer…
            </span>

          </div>
        </div>
      </div>
    </article>
  </div>
</template>

<style scoped>
.modal-overlay {
  --modal-surface: color-mix(in srgb, var(--bg-base) 96%, var(--bg-light));
  --modal-elevated: color-mix(in srgb, var(--bg-light) 82%, var(--bg-base));
  --modal-text: var(--text-main);
  --modal-muted: color-mix(in srgb, var(--text-muted) 88%, var(--text-main));
  --modal-border: var(--border-color);

  position: fixed;
  inset: 0;
  z-index: 200;
  display: grid;
  place-items: center;
  padding: 1.5rem;
  background: color-mix(in srgb, var(--bg-dark) 78%, transparent);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
}

.modal-shell {
  position: relative;
  width: min(100%, 880px);
  max-height: min(86vh, 680px);
  overflow-y: auto;
  scrollbar-gutter: stable;
  padding: 2rem;
  border: 1px solid var(--modal-border);
  border-radius: 20px;
  background: var(--modal-surface);
  color: var(--modal-text);
  box-shadow:
    0 22px 58px rgba(0, 0, 0, 0.38),
    0 0 0 1px color-mix(in srgb, var(--text-main) 3%, transparent) inset;
  animation: modal-in 220ms ease-out;
}

.modal-shell::-webkit-scrollbar-track {
  margin-block: 12px;
}

@keyframes modal-in {
  from {
    opacity: 0;
    transform: translateY(14px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 2;
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border: 0;
  border-radius: 50%;
  background: color-mix(in srgb, var(--text-main) 8%, transparent);
  color: var(--modal-muted);
  cursor: pointer;
  transition: background 160ms ease, color 160ms ease, transform 160ms ease;
}

.close-btn:hover {
  background: color-mix(in srgb, var(--text-main) 14%, transparent);
  color: var(--modal-text);
  transform: rotate(4deg);
}

.modal-content {
  display: grid;
  grid-template-columns: minmax(210px, 270px) minmax(0, 1fr);
  gap: clamp(1.75rem, 3.5vw, 3rem);
}

.modal-poster {
  width: 100%;
  aspect-ratio: 2 / 3;
  overflow: hidden;
  border-radius: 16px;
  background: var(--modal-elevated);
}

.modal-poster img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.poster-placeholder {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  padding: 1rem;
  color: var(--modal-muted);
  background: linear-gradient(145deg, var(--modal-elevated), var(--modal-surface));
}

.modal-info {
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 0.25rem 0;
}

.modal-header {
  padding-right: 2rem;
}

.title-block {
  min-width: 0;
}

.modal-title {
  font-size: clamp(1.35rem, 2.6vw, 2rem);
  font-weight: 650;
  line-height: 1.15;
  letter-spacing: -0.025em;
  color: var(--modal-text);
}

.alternate-title {
  margin-top: 0.45rem;
  font-size: var(--font-size-sm);
  color: var(--modal-muted);
}

.alternate-title + .alternate-title {
  margin-top: 0.2rem;
}

.title-label {
  display: inline-block;
  min-width: 4.8rem;
  margin-right: 0.35rem;
  color: var(--modal-text);
  font-size: var(--font-size-xs);
  font-weight: 650;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.quick-stats {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  font-size: var(--font-size-sm);
  color: var(--modal-text);
}

.quick-stats span {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.star-icon {
  color: var(--accent);
}

.synopsis {
  max-width: 68ch;
  color: var(--modal-muted);
  font-size: var(--font-size-sm);
  line-height: 1.7;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem 2rem;
}

.detail-item {
  display: flex;
  align-items: baseline;
  gap: 0.45rem;
  min-width: 0;
}

.detail-wide {
  grid-column: 1 / -1;
}

.detail-item dt {
  flex: 0 0 auto;
  font-size: var(--font-size-sm);
  font-weight: 700;
  color: var(--modal-text);
}

.detail-item dd {
  min-width: 0;
  color: var(--modal-muted);
  font-size: var(--font-size-sm);
}

.genre-detail {
  align-items: center;
}

.genre-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.genre-chip {
  padding: 0.32rem 0.7rem;
  border: 1px solid var(--modal-border);
  border-radius: 999px;
  color: var(--modal-text);
  background: var(--modal-elevated);
  font-size: var(--font-size-xs);
}

.reason {
  padding: 0.9rem 1rem;
  border-radius: 10px;
  background: color-mix(in srgb, var(--text-main) 4%, transparent);
}

.reason-label {
  font-size: var(--font-size-xs);
  font-weight: 700;
  color: var(--modal-text);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.reason p {
  margin-top: 0.35rem;
  color: var(--modal-muted);
  font-size: var(--font-size-sm);
  line-height: 1.55;
}

.modal-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.65rem;
}

.watch-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  padding: 0.65rem 1.1rem;
  border-radius: 999px;
  background: var(--text-main);
  color: var(--bg-base);
  font-size: var(--font-size-sm);
  font-weight: 650;
  text-decoration: none;
  transition: transform 160ms ease, background 160ms ease;
}

.watch-later-btn {
  border: 1px solid var(--modal-border);
  background: var(--modal-elevated);
  color: var(--modal-text);
  font-family: inherit;
  cursor: pointer;
}

.watch-later-btn:hover {
  border-color: color-mix(in srgb, var(--accent) 45%, var(--modal-border));
  background: color-mix(in srgb, var(--accent) 9%, var(--modal-elevated));
}

.watch-later-btn.is-saved {
  border-color: color-mix(in srgb, var(--accent) 55%, var(--modal-border));
  background: color-mix(in srgb, var(--accent) 14%, var(--modal-elevated));
  color: var(--accent);
}

.trailer-btn {
  background: var(--accent);
  color: white;
}

.trailer-btn:hover {
  background: color-mix(in srgb, var(--accent) 86%, white);
}

.secondary-btn {
  background: var(--text-main);
  color: var(--bg-base);
}

.trailer-loading {
  color: var(--modal-muted);
  font-size: var(--font-size-xs);
}

.watch-btn:hover {
  transform: translateY(-2px);
}

.secondary-btn:hover {
  background: color-mix(in srgb, var(--text-main) 92%, var(--bg-base));
}

@media (max-width: 720px) {
  .modal-overlay {
    align-items: start;
    padding: 0.75rem;
  }

  .modal-shell {
    max-height: calc(100vh - 1.5rem);
    padding: 1.25rem;
    border-radius: 20px;
  }

  .modal-content {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .modal-poster {
    width: min(68vw, 260px);
    justify-self: center;
  }

  .modal-header {
    padding-right: 1.75rem;
  }
}

@media (max-width: 440px) {
  .details-grid {
    grid-template-columns: 1fr;
  }

  .detail-wide {
    grid-column: auto;
  }
}
</style>
