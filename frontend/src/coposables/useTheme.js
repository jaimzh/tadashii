// src/composables/useTheme.js
import { ref } from 'vue'

const theme = ref('dark')

export function useTheme() {
  const applyTheme = (newTheme) => {
    theme.value = newTheme
    document.documentElement.setAttribute('data-theme', newTheme)
    localStorage.setItem('user-theme', newTheme)
  }

  const toggleTheme = () => {
    let nextTheme

    if (theme.value === 'dark') {
      nextTheme = 'light'
    } else {
      nextTheme = 'dark'
    }
    applyTheme(nextTheme)
  }

  
  const initTheme = () => {
    const savedTheme = localStorage.getItem('user-theme')

    if (savedTheme) {
      applyTheme(savedTheme)
    } else {
      const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches
      applyTheme(prefersLight ? 'light' : 'dark')
    }
  }

  return {
    theme,
    toggleTheme,
    initTheme,
  }
}
