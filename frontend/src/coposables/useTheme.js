// src/composables/useTheme.js
import { ref } from 'vue'

const themes = ['dark', 'light', 'zen']
const faviconByTheme = {
  dark: '/favicons/favicon_io%20dark/favicon.ico',
  light: '/favicons/favicon_io%20light/favicon.ico',
  zen: '/favicons/favicon_io%20zen/favicon.ico',
}
const theme = ref('dark')
let themeTransitionTimer
let activeViewTransition = null

function updateFavicon(newTheme) {
  const favicon = document.querySelector('#app-favicon')
  if (favicon) favicon.setAttribute('href', faviconByTheme[newTheme])
}

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
    updateFavicon(newTheme)
  }

  const toggleTheme = async (event) => {
    const currentIndex = themes.indexOf(theme.value)
    const nextTheme = themes[(currentIndex + 1) % themes.length]

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (!document.startViewTransition || reduceMotion) {
      applyTheme(nextTheme)
      if (!reduceMotion) playThemeTransition()
      return
    }

    const buttonRect = event?.currentTarget?.getBoundingClientRect()
    const viewport = window.visualViewport
    const width = viewport?.width ?? window.innerWidth
    const height = viewport?.height ?? window.innerHeight
    const x = buttonRect ? buttonRect.left + buttonRect.width / 2 : width / 2
    const y = buttonRect ? buttonRect.top + buttonRect.height / 2 : height / 2
    const radius = Math.max(
      Math.hypot(x, y),
      Math.hypot(width - x, y),
      Math.hypot(x, height - y),
      Math.hypot(width - x, height - y),
    ) + 16

    activeViewTransition?.skipTransition()
    const transition = document.startViewTransition(() => applyTheme(nextTheme))
    activeViewTransition = transition

    try {
      await transition.ready
      const reveal = document.documentElement.animate(
        {
          clipPath: [
            `circle(0px at ${x}px ${y}px)`,
            `circle(${radius}px at ${x}px ${y}px)`,
          ],
        },
        {
          duration: 1050,
          easing: 'cubic-bezier(.16, 1, .3, 1)',
          fill: 'both',
          pseudoElement: '::view-transition-new(root)',
        },
      )
      await reveal.finished
    } catch {
      // A newer theme click can intentionally interrupt this transition.
    } finally {
      if (activeViewTransition === transition) activeViewTransition = null
    }
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
