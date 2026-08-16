<script setup>
const currentYear = new Date().getFullYear()
</script>

<template>
  <footer class="app-footer">
    <p><span lang="ja">正</span> · &copy; {{ currentYear }} Tadashii</p>
  </footer>
</template>

<style scoped>
.app-footer {
  width: min(100% - 40px, 1080px);
  margin: 0 auto;
  padding: 1.25rem 0 1.5rem;
  border-top: 1px solid color-mix(in srgb, var(--border-color) 65%, transparent);
  color: var(--text-muted);
  font-size: 0.625rem;
  letter-spacing: 0.025em;
  opacity: 0.65;
  text-align: center;
}
</style>
