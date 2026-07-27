<script setup>
</script>

<template>
  <section class="animated-hero">
    <div class="hero-inner">
      <slot />
    </div>
  </section>
</template>

<style scoped>
.animated-hero {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px 24px;
}

.hero-inner {
  text-align: center;
  max-width: 720px;
}
</style>
