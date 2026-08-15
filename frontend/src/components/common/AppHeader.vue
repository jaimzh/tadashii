<script setup>
import { onMounted, ref, watch, nextTick } from 'vue';
import gsap from 'gsap';
import { useTheme } from '@/coposables/useTheme';
import { PhBookmarkSimple, PhLeaf, PhSun, PhMoon, PhQuestion, PhList, PhX } from '@phosphor-icons/vue';
import { useWatchLater } from '@/composables/useWatchLater.js';
import SearchBar from './SearchBar.vue';
import TadashiiLogo from './TadashiiLogo.vue';
import TextHint from './TextHint.vue';

const props = defineProps({
  isSearching: { type: Boolean, default: false },
  isLoading: { type: Boolean, default: false },
  query: { type: String, default: '' },
  searchOrigin: { type: Object, default: null },
});

const { theme, toggleTheme, initTheme } = useTheme();
const { savedCount } = useWatchLater();
const navSearchEl = ref(null);
const dimmed = ref(false);
const menuOpen = ref(false);
const emit = defineEmits(['search', 'home']);

onMounted(() => {
  initTheme();
});

watch(
  () => props.isLoading,
  (loading) => {
    dimmed.value = loading;
  }
);

function onSearch(query) {
  menuOpen.value = false;
  const rect = navSearchEl.value?.$el?.getBoundingClientRect();
  emit('search', query, rect);
}

function changeTheme(event) {
  toggleTheme(event);
  menuOpen.value = false;
}

watch(
  () => props.isSearching,
  async (searching) => {
    if (!searching) {
      dimmed.value = false;
      menuOpen.value = false;
      return;
    }

    await nextTick();
    await nextTick();

    const el = navSearchEl.value?.$el;
    if (!el || !props.searchOrigin) return;

    const from = props.searchOrigin;
    const target = el.getBoundingClientRect();

    const fromCenterX = from.left + from.width / 2;
    const fromCenterY = from.top + from.height / 2;
    const targetCenterX = target.left + target.width / 2;
    const targetCenterY = target.top + target.height / 2;
    const finalScale = window.matchMedia('(max-width: 720px)').matches ? 1 : 0.8;

    gsap.killTweensOf(el);

    gsap.fromTo(
      el,
      {
        x: fromCenterX - targetCenterX,
        y: fromCenterY - targetCenterY,
        scaleX: from.width / target.width,
        scaleY: from.height / target.height,
        transformOrigin: 'center center',
      },
      {
        x: 0,
        y: 0,
        scaleX: finalScale,
        scaleY: finalScale,
        duration: 0.5,
        ease: 'power2.inOut',
      }
    );
  }
);
</script>

<template>
  <header class="app-header">
    <TextHint text="Home" position="bottom">
    <button class="brand" type="button" aria-label="Go to home" @click="emit('home')">
      <TadashiiLogo compact :animated="false" />
    </button>
    </TextHint>

    <div class="nav-search-wrap" v-if="isSearching" :class="{ dimmed }">
      <SearchBar
        ref="navSearchEl"
        :value="query"
        :readonly="isLoading"
        @submit="onSearch"
      />
    </div>

    <!-- <SearchBar/> -->
    <div class="actions">
      <TextHint text="Watch Later" position="bottom">
        <RouterLink
          to="/watch-later"
          class="icon-btn watch-later-link"
          :aria-label="`Watch Later, ${savedCount} saved`"
        >
          <PhBookmarkSimple :size="20" :weight="savedCount ? 'fill' : 'regular'" />
          <span v-if="savedCount" class="saved-badge">{{ savedCount > 99 ? '99+' : savedCount }}</span>
        </RouterLink>
      </TextHint>
      <TextHint :text="`Change theme (currently ${theme})`" position="bottom">
        <button
          @click="toggleTheme"
          class="icon-btn"
          :aria-label="`Current theme: ${theme}. Change theme`"
        >
          <PhSun v-if="theme === 'dark'" :size="22"  />
          <PhLeaf v-else-if="theme === 'light'" :size="20"  />
          <PhMoon v-else :size="20" />
        </button>
      </TextHint>
      <TextHint text="Help and information" position="bottom">
        <button class="icon-btn" aria-label="Help">
          <PhQuestion :size="20" />
        </button>
      </TextHint>
    </div>

    <div class="mobile-menu">
      <button
        class="icon-btn menu-toggle"
        type="button"
        :aria-expanded="menuOpen"
        aria-controls="mobile-header-menu"
        :aria-label="menuOpen ? 'Close menu' : 'Open menu'"
        @click="menuOpen = !menuOpen"
      >
        <PhX v-if="menuOpen" :size="20" />
        <PhList v-else :size="22" weight="bold" />
      </button>

      <div v-if="menuOpen" id="mobile-header-menu" class="mobile-menu-panel">
        <RouterLink to="/watch-later" class="menu-item" @click="menuOpen = false">
          <PhBookmarkSimple :size="20" :weight="savedCount ? 'fill' : 'regular'" />
          <span>Watch Later</span>
          <span v-if="savedCount" class="menu-count">{{ savedCount }}</span>
        </RouterLink>
        <button type="button" class="menu-item" @click="changeTheme">
          <PhSun v-if="theme === 'dark'" :size="20" />
          <PhLeaf v-else-if="theme === 'light'" :size="20" />
          <PhMoon v-else :size="20" />
          <span>Change theme</span>
        </button>
        <button type="button" class="menu-item" aria-label="Help" @click="menuOpen = false">
          <PhQuestion :size="20" />
          <span>Help</span>
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 1rem 0.75rem 1rem;
  height: 4rem;
  background-color: var(--bg-base);
  /* backdrop-filter: blur(10px); */
  -webkit-backdrop-filter: blur(10px);
  transition: background-color 0.3s ease, opacity 0.3s ease;
  position: sticky;
  top: 0;
  z-index: 100;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 110px;
  padding: 0;
  border: 0;
  background: transparent;
  color: inherit;
  cursor: pointer;
}

.brand:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 4px;
  border-radius: 4px;
}

.nav-search-wrap.dimmed {
  opacity: 0.55;
}

.nav-search-wrap {
  flex: 1;
  display: flex;
  justify-content: center;
  min-width: 0;
  padding: 0 1rem;
  transition: opacity 0.3s ease;
}

.actions {
  display: flex;
  gap: 0.5rem;
  min-width: 110px;
  justify-content: flex-end;
}

.mobile-menu {
  position: relative;
  display: none;
}

.mobile-menu-panel {
  position: absolute;
  top: calc(100% + 0.6rem);
  right: 0;
  display: grid;
  min-width: 180px;
  padding: 0.45rem;
  border: 1px solid var(--border-color);
  border-radius: 12px;
  background: var(--bg-light);
  box-shadow: 0 14px 35px rgba(0, 0, 0, 0.22);
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  width: 100%;
  padding: 0.7rem 0.75rem;
  border: 0;
  border-radius: 8px;
  background: transparent;
  color: var(--text-main);
  font: inherit;
  font-size: var(--font-size-sm);
  cursor: pointer;
}

.menu-item:hover,
.menu-item:focus-visible {
  background: color-mix(in srgb, var(--accent) 12%, transparent);
  outline: none;
}

.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-light);
  color: var(--text-muted);
  border: 1px solid var(--border-color);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
}

.watch-later-link {
  position: relative;
  text-decoration: none;
}

.watch-later-link.router-link-active {
  border-color: color-mix(in srgb, var(--accent) 55%, var(--border-color));
  color: var(--accent);
}

.saved-badge {
  position: absolute;
  top: -6px;
  right: -7px;
  min-width: 17px;
  height: 17px;
  padding: 0 4px;
  border: 2px solid var(--bg-base);
  border-radius: 999px;
  color: white;
  background: var(--accent);
  font-size: 0.58rem;
  font-weight: 700;
  line-height: 13px;
  text-align: center;
}

.menu-count {
  margin-left: auto;
  color: var(--accent);
  font-size: var(--font-size-xs);
  font-weight: 700;
}

.icon-btn:hover {
  border-color: var(--text-main);
}

@media (max-width: 720px) {
  .app-header {
    display: grid;
    grid-template-columns: 34px minmax(160px, 1fr) 34px;
    gap: 0.5rem;
    height: 3.75rem;
    padding: 1rem 0.5rem 0.65rem;
  }

  .brand {
    min-width: 0;
    width: 34px;
  }

  .nav-search-wrap {
    grid-column: 2;
    min-width: 160px;
    width: 100%;
    padding: 0;
  }

  .nav-search-wrap :deep(.search-container) {
    min-width: 160px;
    width: 100%;
  }

  .actions {
    display: none;
  }

  .mobile-menu {
    grid-column: 3;
    display: block;
  }
}

@media (max-width: 340px) {
  .app-header {
    padding-right: 0.25rem;
    padding-left: 0.25rem;
    gap: 0.35rem;
  }
}
</style>
