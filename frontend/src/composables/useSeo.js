import { watch } from 'vue'
import { useRoute } from 'vue-router'
import siteConfig from '../../site.config.json'

function setMeta(name, content, attribute = 'name') {
  let element = document.head.querySelector(`meta[${attribute}="${name}"]`)

  if (!element) {
    element = document.createElement('meta')
    element.setAttribute(attribute, name)
    document.head.appendChild(element)
  }

  element.setAttribute('content', content)
}

function setCanonical(url) {
  let element = document.head.querySelector('link[rel="canonical"]')

  if (!element) {
    element = document.createElement('link')
    element.setAttribute('rel', 'canonical')
    document.head.appendChild(element)
  }

  element.setAttribute('href', url)
}

function routeUrl(path) {
  return new URL(path, `${siteConfig.url.replace(/\/$/, '')}/`).toString()
}

export function useSeo() {
  const route = useRoute()

  watch(
    [
      () => route.fullPath,
      () => route.meta.title,
      () => route.meta.description,
      () => route.meta.canonical,
      () => route.meta.noindex,
    ],
    () => {
      const title = route.meta.title || siteConfig.name
      const description = route.meta.description || siteConfig.description
      const canonicalUrl = routeUrl(route.meta.canonical || route.path)
      const robots = route.meta.noindex ? 'noindex, nofollow' : 'index, follow'
      const socialImage = routeUrl(siteConfig.socialImage)

      document.title = title
      setCanonical(canonicalUrl)
      setMeta('description', description)
      setMeta('robots', robots)
      setMeta('og:title', title, 'property')
      setMeta('og:description', description, 'property')
      setMeta('og:url', canonicalUrl, 'property')
      setMeta('og:image', socialImage, 'property')
      setMeta('twitter:title', title)
      setMeta('twitter:description', description)
      setMeta('twitter:image', socialImage)
    },
    { immediate: true },
  )
}
