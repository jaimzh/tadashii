// src/composables/useTheme.js
import { ref } from 'vue'

const themes = ['dark', 'light', 'zen']
const theme = ref('dark')
let themeTransitionTimer

function playThemeTransition() {
  const root = document.documentElement

  root.classList.remove('theme-transition')
  void root.offsetWidth
  root.classList.add('theme-transition')

  clearTimeout(themeTransitionTimer)
  themeTransitionTimer = setTimeout(() => {
    root.classList.remove('theme-transition')
  }, 450)
}

export function useTheme() {
  const applyTheme = (newTheme) => {
    theme.value = newTheme
    document.documentElement.setAttribute('data-theme', newTheme)
    localStorage.setItem('user-theme', newTheme)
  }

  const toggleTheme = (event) => {
    const currentIndex = themes.indexOf(theme.value)
    const nextTheme = themes[(currentIndex + 1) % themes.length]

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (!document.startViewTransition || reduceMotion) {
      applyTheme(nextTheme)
      if (!reduceMotion) playThemeTransition()
      return
    }

    const buttonRect = event?.currentTarget?.getBoundingClientRect()
    const x = buttonRect ? buttonRect.left + buttonRect.width / 2 : window.innerWidth / 2
    const y = buttonRect ? buttonRect.top + buttonRect.height / 2 : window.innerHeight / 2
    const radius = Math.hypot(
      Math.max(x, window.innerWidth - x),
      Math.max(y, window.innerHeight - y),
    )

    const root = document.documentElement
    root.style.setProperty('--theme-reveal-x', `${x}px`)
    root.style.setProperty('--theme-reveal-y', `${y}px`)
    root.style.setProperty('--theme-reveal-radius', `${radius}px`)

    document.startViewTransition(() => applyTheme(nextTheme))
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
