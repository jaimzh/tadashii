<script setup>
import { PhStar } from '@phosphor-icons/vue'

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
  >
    <div class="card-image">
      <img v-if="image" :src="image" alt="" />
      <span v-else class="image-placeholder" />
    </div>

    <div class="card-body">
      <h3 class="card-title">{{ title }}</h3>

      <div class="card-meta">
        <span class="meta-item">{{ episodes }} episodes</span>
        <span class="meta-item rating">
          <PhStar :size="16" weight="fill" class="star-icon" />
          {{ rating }}
        </span>
      </div>
    </div>
  </article>
</template>

<style scoped>
.result-card {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  padding: 1rem;
  background: var(--bg-light);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
  overflow: hidden;
  cursor: pointer;
}

.result-card:hover {
  border-color: color-mix(in srgb, var(--accent) 50%, transparent);
  box-shadow: var(--ambient-glow);
  transform: translateY(-2px);
}

.result-card:active {
  transform: translateY(0);
}

.card-image {
  width: 88px;
  height: 120px;
  flex-shrink: 0;
  border-radius: 8px;
  overflow: hidden;
  background: var(--bg-dark);
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.image-placeholder {
  display: block;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    135deg,
    color-mix(in srgb, var(--accent) 25%, transparent),
    transparent
  );
}

.card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 0.5rem;
  min-width: 0;
}

.card-title {
  font-size: var(--font-size-md);
  font-weight: 600;
  color: var(--text-main);
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: var(--font-size-sm);
  color: var(--text-muted);
}

.rating .star-icon {
  color: var(--accent);
}
</style>
