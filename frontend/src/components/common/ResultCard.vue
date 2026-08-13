<script setup>
import { PhList, PhStar } from '@phosphor-icons/vue'

defineProps({
  title: {
    type: String,
    default: 'Untitled',
  },
  image: {
    type: String,
    default: '',
  },
  episodes: {
    type: String,
    default: 'N/A',
  },
  rating: {
    type: String,
    default: 'N/A',
  },
  synopsis: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['select'])
</script>

<template>
  <article
    class="result-card"
    role="button"
    tabindex="0"
    @click="emit('select')"
    @keydown.enter="emit('select')"
    @keydown.space.prevent="emit('select')"
  >
    <div class="card-image">
      <img v-if="image" :src="image" :alt="`${title} poster`" />
      <div v-else class="image-placeholder" aria-hidden="true">
        <span class="placeholder-mark">正</span>
        <span class="placeholder-copy">Poster artwork</span>
      </div>
      <span class="image-sheen" aria-hidden="true" />
    </div>

    <div class="card-body">
      <div class="title-row">
        <h3 class="card-title">{{ title }}</h3>
      </div>

      <p v-if="synopsis" class="card-synopsis">{{ synopsis }}</p>

      <div class="card-meta">
        <span class="meta-item episodes">
          <PhList :size="17" weight="bold" />
          {{ episodes }} eps
        </span>
        <span class="meta-item rating">
          <PhStar :size="17" weight="fill" />
          {{ rating }}
        </span>
      </div>
    </div>
  </article>
</template>

<style scoped>
.result-card {
  width: 100%;
  min-height: 150px;
  display: flex;
  align-items: stretch;
  gap: 1rem;
  padding: 0.7rem;
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  outline: none;
  cursor: pointer;
  transition: transform 180ms ease;
}

.result-card:hover {
  transform: translateY(-2px);
  border-color: color-mix(in srgb, var(--accent) 24%, var(--border-color));
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.result-card:active {
  transform: translateY(-2px) scale(0.99);
}

.result-card:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 6px;
}

.card-image {
  position: relative;
  width: 96px;
  flex: 0 0 96px;
  aspect-ratio: 2 / 3;
  min-height: 0;
  border-radius: 9px;
  overflow: hidden;
  background: color-mix(in srgb, var(--bg-light) 88%, var(--accent));
}

.card-image img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.image-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.65rem;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    145deg,
    color-mix(in srgb, var(--accent) 30%, var(--bg-light)),
    var(--bg-light) 48%,
    color-mix(in srgb, #7c3aed 24%, var(--bg-dark))
  );
  color: var(--text-muted);
}

.placeholder-mark {
  font-size: 2.25rem;
  font-weight: 700;
  color: color-mix(in srgb, var(--text-main) 28%, transparent);
}

.placeholder-copy {
  display: none;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.image-sheen {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.08), transparent 24%, rgba(0, 0, 0, 0.12));
}

.card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 0.35rem 0.25rem 0.35rem 0;
  min-height: 0;
  min-width: 0;
}

.title-row {
  display: flex;
  align-items: center;
  min-width: 0;
}

.card-title {
  min-width: 0;
  font-size: var(--font-size-md);
  font-weight: 700;
  color: var(--text-main);
  line-height: 1.25;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.card-synopsis {
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  overflow: hidden;
}

.card-meta {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 0.5rem;
}

.meta-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  min-width: max-content;
  padding: 0.32rem 0.48rem;
  border-radius: 7px;
  background: color-mix(in srgb, var(--bg-light) 84%, transparent);
  font-size: var(--font-size-xs);
  font-weight: 600;
  color: var(--text-muted);
}

.rating svg {
  color: var(--accent);
}

@media (max-width: 560px) {
  .result-card {
    min-height: 138px;
    gap: 0.8rem;
    padding: 0.6rem;
  }

  .card-image {
    width: 84px;
    flex-basis: 84px;
  }

  .card-body {
    padding-right: 0.1rem;
  }
}
</style>
