import { fileURLToPath, URL } from 'node:url'
import { readFileSync } from 'node:fs'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

const siteConfig = JSON.parse(
  readFileSync(fileURLToPath(new URL('./site.config.json', import.meta.url)), 'utf8'),
)
const siteUrl = siteConfig.url.replace(/\/$/, '')

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    {
      name: 'tadashii-site-config',
      transformIndexHtml(html) {
        return html.replaceAll('__SITE_URL__', siteUrl)
      },
    },
    vue(),
    vueDevTools(),
  ],
  server: {
    proxy:{
      '/api':{
      target: 'http://localhost:8000',
      changeOrigin: true,

      }
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
