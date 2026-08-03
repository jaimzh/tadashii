<script setup>
import { onMounted, ref, watch, nextTick } from 'vue';
import gsap from 'gsap';
import { useTheme } from '@/coposables/useTheme';
import { PhSun, PhMoon, PhQuestion } from '@phosphor-icons/vue';
import SearchBar from './SearchBar.vue';

const props = defineProps({
  isSearching: { type: Boolean, default: false },
  isLoading: { type: Boolean, default: false },
  query: { type: String, default: '' },
  searchOrigin: { type: Object, default: null },
});

const { theme, toggleTheme, initTheme } = useTheme();
const navSearchEl = ref(null);
const dimmed = ref(false);
const emit = defineEmits(['search']);

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
  const rect = navSearchEl.value?.$el?.getBoundingClientRect();
  emit('search', query, rect);
}

watch(
  () => props.isSearching,
  async (searching) => {
    if (!searching) {
      dimmed.value = false;
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
        scaleX: 0.8,
        scaleY: 0.8,
        duration: 0.5,
        ease: 'power2.inOut',
      }
    );
  }
);
</script>

<template>
  <header class="app-header">
    <div class="brand">
      <span class="app-name">🔥</span>
      <span class="app-name">Tadashii</span>
    </div>

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
      <button @click="toggleTheme" class="icon-btn" aria-label="Toggle theme">
        <PhSun v-if="theme === 'dark'" :size="22" weight="bold" />
        <PhMoon v-else :size="20" />
      </button>
      <button class="icon-btn" aria-label="Help">
        <PhQuestion :size="20" />
      </button>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  height: 5rem;
  background-color: var(--bg-main);
  border: 1px solid var(--border-color);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  transition: background-color 0.3s ease, border-color 0.3s ease, opacity 0.3s ease;
  position: sticky;
  top: 0;
  z-index: 100;
}

.app-name {
  font-weight: bold;
  font-size: var(--font-size-lg);
  color: var(--text-main);
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  min-width: 140px;
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
  min-width: 140px;
  justify-content: flex-end;
}

.icon-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-light);
  color: var(--text-muted);
  border: 1px solid var(--border-color);
  width: 34px;
  height: 34px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.2s ease;
}

.icon-btn:hover {
  border-color: var(--text-main);
}
</style>
