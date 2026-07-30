<script setup>
import { onMounted } from 'vue';
import { useTheme } from '@/coposables/useTheme';
import { PhSun, PhMoon, PhQuestion } from '@phosphor-icons/vue';

const { theme, toggleTheme, initTheme } = useTheme();

onMounted(() => {
  initTheme();
});
</script>

<template>
  <header class="app-header">
    <div>
      <span class="app-name">🔥</span>
      <span class="app-name">Tadashii</span>
    </div>
   

    <div class="actions">
      <button @click="toggleTheme" class="icon-btn" aria-label="Toggle theme">
        <PhSun v-if="theme === 'dark'" :size="22" weight="bold" />
        <PhMoon v-else :size="20"  />
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
  transition: background-color 0.3s ease, border-color 0.3s ease;
  position: sticky;
  top: 0;
  z-index: 100;
}

.app-name {
  font-weight: bold;
  font-size: 1.25rem;
  color: var(--text-main);
}

.actions {
  display: flex;
  gap: 0.5rem;
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
