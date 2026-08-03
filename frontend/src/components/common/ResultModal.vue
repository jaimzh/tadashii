<script setup>
import { PhStar, PhX, PhPlay } from '@phosphor-icons/vue'

defineProps({
  result: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['close'])
</script>

<template>
  <div class="modal-overlay" @click.self="emit('close')">
    <div class="modal-shell">
      <button class="close-btn" @click="emit('close')" aria-label="Close">
        <PhX :size="22" />
      </button>

      <div class="modal-content">
        <div class="modal-poster">
          <img v-if="result.image" :src="result.image" alt="" />
          <span v-else class="poster-placeholder" />
        </div>

        <div class="modal-info">
          <h2 class="modal-title">{{ result.title }}</h2>
          <p v-if="result.japaneseName" class="japanese-name">
            {{ result.japaneseName }}
          </p>

          <div class="modal-meta-row">
            <span v-if="result.year" class="chip">{{ result.year }}</span>
            <span v-if="result.duration" class="chip">{{ result.duration }}</span>
            <span v-if="result.genres" class="chip">{{ result.genres }}</span>
            <span v-if="result.studio" class="chip">{{ result.studio }}</span>
          </div>

          <div class="rating-row">
            <PhStar :size="18" weight="fill" class="star-icon" />
            <span class="rating-value">{{ result.rating }}</span>
            <span v-if="result.episodes" class="episode-count">
              · {{ result.episodes }} episodes
            </span>
          </div>

          <p v-if="result.synopsis" class="synopsis">{{ result.synopsis }}</p>

          <div v-if="result.reason" class="reason">
            <span class="reason-label">Why this one:</span>
            <p>{{ result.reason }}</p>
          </div>

          <button class="watch-btn">
            <PhPlay :size="18" weight="fill" />
            Watch
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
  padding: 1rem;
}

.modal-shell {
  position: relative;
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  max-width: 760px;
  width: 100%;
  max-height: 85vh;
  overflow-y: auto;
  animation: modal-in 0.25s ease;
}

@keyframes modal-in {
  from {
    opacity: 0;
    transform: scale(0.92);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.close-btn {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 1px solid var(--border-color);
  background: var(--bg-light);
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
}

.close-btn:hover {
  color: var(--text-main);
  border-color: var(--text-main);
}

.modal-content {
  display: flex;
  flex-direction: row;
  gap: 1.5rem;
  padding: 1.5rem;
}

.modal-poster {
  flex-shrink: 0;
  width: 200px;
  height: 280px;
  border-radius: 10px;
  overflow: hidden;
  background: var(--bg-dark);
}

.modal-poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.poster-placeholder {
  display: block;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--accent) 30%, transparent),
    transparent
  );
}

.modal-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.modal-title {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.2;
}

.japanese-name {
  font-size: var(--font-size-sm);
  color: var(--text-muted);
}

.modal-meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.chip {
  padding: 0.25rem 0.6rem;
  border-radius: 50px;
  border: 1px solid var(--border-color);
  background: var(--bg-base);
  font-size: var(--font-size-xs);
  color: var(--text-muted);
}

.rating-row {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.star-icon {
  color: var(--accent);
}

.rating-value {
  color: var(--text-main);
  font-weight: 600;
}

.episode-count {
  margin-left: 0.25rem;
}

.synopsis {
  font-size: var(--font-size-sm);
  color: var(--text-muted);
  line-height: 1.6;
}

.reason {
  padding: 0.75rem;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  background: var(--bg-base);
}

.reason-label {
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.reason p {
  margin-top: 0.35rem;
  font-size: var(--font-size-sm);
  color: var(--text-muted);
  line-height: 1.5;
}

.watch-btn {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 50px;
  background: var(--accent);
  color: white;
  font-size: var(--font-size-md);
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  transition: filter 0.2s ease;
}

.watch-btn:hover {
  filter: brightness(1.1);
}
</style>
