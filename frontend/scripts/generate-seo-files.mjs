import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'

const frontendRoot = fileURLToPath(new URL('../', import.meta.url))
const publicDirectory = fileURLToPath(new URL('../public/', import.meta.url))
const siteConfig = JSON.parse(
  await readFile(new URL('../site.config.json', import.meta.url), 'utf8'),
)
const siteUrl = siteConfig.url.replace(/\/$/, '')

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>${siteUrl}/</loc>
  </url>
  <url>
    <loc>${siteUrl}/help</loc>
  </url>
</urlset>
`

const robots = `User-agent: *
Allow: /

Sitemap: ${siteUrl}/sitemap.xml
`

await mkdir(publicDirectory, { recursive: true })
await Promise.all([
  writeFile(new URL('../public/sitemap.xml', import.meta.url), sitemap),
  writeFile(new URL('../public/robots.txt', import.meta.url), robots),
])

console.log(`Generated SEO files for ${siteUrl} from ${frontendRoot}`)
