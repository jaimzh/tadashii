<script setup>
import { computed } from 'vue'
import { PhBookmarkSimple, PhCheckCircle, PhTrashSimple } from '@phosphor-icons/vue'
import { useWatchLater } from '@/composables/useWatchLater.js'

const { savedAnime, removeSaved, setWatched } = useWatchLater()

const upNext = computed(() =>
  savedAnime.value.filter((anime) => !anime.watched),
)

const watched = computed(() =>
  savedAnime.value.filter((anime) => anime.watched),
)
</script>

<template>
  <div class="watch-later-view">
    <header class="page-header">
      <div>
        <p class="eyebrow">Your list</p>
        <h1>Watch Later</h1>
      </div>
      <span v-if="savedAnime.length" class="saved-total">
        {{ savedAnime.length }} saved
      </span>
    </header>

    <section v-if="!savedAnime.length" class="empty-state">
      <span class="empty-icon">
        <PhBookmarkSimple :size="30" weight="duotone" />
      </span>
      <h2>Nothing saved yet</h2>
      <p>Bookmark an anime from its expanded card and it will appear here.</p>
    </section>

    <div v-else class="watch-sections">
      <section class="watch-section" aria-labelledby="up-next-heading">
        <div class="section-heading">
          <h2 id="up-next-heading">Up Next</h2>
          <span>{{ upNext.length }}</span>
        </div>

        <p v-if="!upNext.length" class="section-empty">
          Everything on your list has been watched.
        </p>

        <div v-else class="watch-list">
          <article v-for="anime in upNext" :key="anime.malId" class="watch-item">
            <img
              v-if="anime.image"
              :src="anime.image"
              :alt="`${anime.title} poster`"
              loading="lazy"
              decoding="async"
            />
            <div v-else class="poster-placeholder">No image</div>

            <div class="item-copy">
              <h3>{{ anime.title }}</h3>
              <p v-if="anime.englishName" class="japanese-title">
                {{ anime.englishName }}
              </p>
              <p v-if="anime.romajiName" class="japanese-title">
                {{ anime.romajiName }}
              </p>
              <p v-if="anime.japaneseName" class="japanese-title">
                {{ anime.japaneseName }}
              </p>
              <p class="item-meta">
                {{ [anime.type, anime.year].filter(Boolean).join(' · ') || 'Details unavailable' }}
              </p>
            </div>

            <label class="watched-toggle">
              <input
                type="checkbox"
                :checked="anime.watched"
                @change="setWatched(anime.malId, $event.target.checked)"
              />
              <span>Watched</span>
            </label>

            <button
              type="button"
              class="remove-btn"
              :aria-label="`Remove ${anime.title} from Watch Later`"
              @click="removeSaved(anime.malId)"
            >
              <PhTrashSimple :size="18" />
            </button>
          </article>
        </div>
      </section>

      <section v-if="watched.length" class="watch-section watched-section" aria-labelledby="watched-heading">
        <div class="section-heading">
          <h2 id="watched-heading">Watched</h2>
          <span>{{ watched.length }}</span>
        </div>

        <div class="watch-list">
          <article v-for="anime in watched" :key="anime.malId" class="watch-item is-watched">
            <img
              v-if="anime.image"
              :src="anime.image"
              :alt="`${anime.title} poster`"
              loading="lazy"
              decoding="async"
            />
            <div v-else class="poster-placeholder">No image</div>

            <div class="item-copy">
              <h3>{{ anime.title }}</h3>
              <p v-if="anime.englishName" class="japanese-title">
                {{ anime.englishName }}
              </p>
              <p v-if="anime.romajiName" class="japanese-title">
                {{ anime.romajiName }}
              </p>
              <p v-if="anime.japaneseName" class="japanese-title">
                {{ anime.japaneseName }}
              </p>
              <p class="item-meta">
                {{ [anime.type, anime.year].filter(Boolean).join(' · ') || 'Details unavailable' }}
              </p>
            </div>

            <label class="watched-toggle">
              <input
                type="checkbox"
                :checked="anime.watched"
                @change="setWatched(anime.malId, $event.target.checked)"
              />

              <span>Watched</span>
            </label>

            <button
              type="button"
              class="remove-btn"
              :aria-label="`Remove ${anime.title} from Watch Later`"
              @click="removeSaved(anime.malId)"
            >
              <PhTrashSimple :size="18" />
            </button>
          </article>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.watch-later-view {
  width: min(100%, 880px);
  margin: 0 auto;
  padding: 3.5rem 0 4rem;
}

.page-header,
.section-heading,
.watch-item,
.watched-toggle {
  display: flex;
  align-items: center;
}

.page-header {
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 2rem;
}

.eyebrow {
  margin-bottom: 0.3rem;
  color: var(--accent);
  font-size: var(--font-size-xs);
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

h1 {
  color: var(--text-main);
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  line-height: 1.1;
}

.saved-total,
.section-heading span {
  border: 1px solid var(--border-color);
  border-radius: 999px;
  color: var(--text-muted);
  background: var(--bg-light);
  font-size: var(--font-size-xs);
}

.saved-total {
  padding: 0.45rem 0.8rem;
}

.empty-state {
  display: grid;
  justify-items: center;
  padding: clamp(3rem, 10vw, 6rem) 1.5rem;
  border: 1px dashed var(--border-color);
  border-radius: 18px;
  text-align: center;
  background: color-mix(in srgb, var(--bg-light) 65%, transparent);
}

.empty-icon {
  display: grid;
  place-items: center;
  width: 58px;
  height: 58px;
  margin-bottom: 1rem;
  border-radius: 50%;
  color: var(--accent);
  background: color-mix(in srgb, var(--accent) 12%, transparent);
}

.empty-state h2 {
  color: var(--text-main);
  font-size: var(--font-size-xl);
}

.empty-state p {
  max-width: 42ch;
  margin-top: 0.5rem;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.watch-sections,
.watch-list {
  display: grid;
}

.watch-sections {
  gap: 2.5rem;
}

.watch-list {
  gap: 0.75rem;
}

.section-heading {
  gap: 0.6rem;
  margin-bottom: 0.9rem;
}

.section-heading h2 {
  color: var(--text-main);
  font-size: var(--font-size-lg);
}

.section-heading span {
  min-width: 24px;
  padding: 0.2rem 0.45rem;
  text-align: center;
}

.section-empty {
  padding: 1.25rem;
  border: 1px dashed var(--border-color);
  border-radius: 12px;
  color: var(--text-muted);
  font-size: var(--font-size-sm);
}

.watch-item {
  min-width: 0;
  gap: 1rem;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 14px;
  background: var(--bg-light);
  transition: border-color 160ms ease, background 160ms ease;
}

.watch-item:hover {
  border-color: color-mix(in srgb, var(--accent) 24%, var(--border-color));
}

.watch-item > img,
.poster-placeholder {
  flex: 0 0 54px;
  width: 54px;
  height: 76px;
  border-radius: 8px;
}

.watch-item > img {
  object-fit: cover;
}

.poster-placeholder {
  display: grid;
  place-items: center;
  padding: 0.35rem;
  color: var(--text-muted);
  background: var(--bg-base);
  font-size: 0.55rem;
  text-align: center;
}

.item-copy {
  min-width: 0;
  flex: 1;
}

.item-copy h3 {
  overflow: hidden;
  color: var(--text-main);
  font-size: var(--font-size-base);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.japanese-title,
.item-meta {
  overflow: hidden;
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  text-overflow: ellipsis;
  white-space: nowrap;
}

.japanese-title {
  margin-top: 0.18rem;
}

.item-meta {
  margin-top: 0.4rem;
}

.watched-toggle {
  flex: 0 0 auto;
  gap: 0.4rem;
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  cursor: pointer;
}

.watched-toggle input {
  width: 16px;
  height: 16px;
  accent-color: var(--accent);
  cursor: pointer;
}

.watched-toggle svg {
  color: var(--accent);
}

.remove-btn {
  flex: 0 0 auto;
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border: 0;
  border-radius: 50%;
  color: var(--text-muted);
  background: transparent;
  cursor: pointer;
  transition: color 160ms ease, background 160ms ease;
}

.remove-btn:hover,
.remove-btn:focus-visible {
  color: #dc5a5a;
  background: color-mix(in srgb, #dc5a5a 10%, transparent);
  outline: none;
}

.is-watched {
  background: color-mix(in srgb, var(--bg-light) 75%, transparent);
}

.is-watched .item-copy {
  opacity: 0.62;
}

@media (max-width: 620px) {
  .watch-later-view {
    padding-top: 2rem;
  }

  .watch-item {
    display: grid;
    grid-template-columns: 54px minmax(0, 1fr) auto;
  }

  .watched-toggle {
    grid-column: 2;
  }

  .remove-btn {
    grid-column: 3;
    grid-row: 1;
  }
}
</style>
