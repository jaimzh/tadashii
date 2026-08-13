// src/composables/useTheme.js
import { ref } from 'vue'

const themes = ['dark', 'light', 'zen']
const theme = ref('dark')

export function useTheme() {
  const applyTheme = (newTheme) => {
    theme.value = newTheme
    document.documentElement.setAttribute('data-theme', newTheme)
    localStorage.setItem('user-theme', newTheme)
  }

  const toggleTheme = () => {
    const currentIndex = themes.indexOf(theme.value)
    const nextTheme = themes[(currentIndex + 1) % themes.length]
    applyTheme(nextTheme)
  }

  
  const initTheme = () => {
    const savedTheme = localStorage.getItem('user-theme')

    if (themes.includes(savedTheme)) {
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
