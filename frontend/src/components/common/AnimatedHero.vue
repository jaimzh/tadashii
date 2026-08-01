<script setup>
import heroSvg from '@/assets/Group 5.svg'
</script>

<template>
  <section class="animated-hero">
    <!-- <img src="http://localhost:3000/cdn/testss.png" alt=""> -->
    <img :src="heroSvg" alt="" class="hero-image" />

    <p class="hero-subtitle">
      Let's find the right story for you! <br />
      Describe what you're in the mood for
    </p>
    <!-- <div class="hero-glow"></div> -->
  </section>
</template>

<style scoped>
.animated-hero {
  width: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  padding: 24px 24px;
  overflow: hidden;
}


.hero-subtitle {
  font-size: var(--font-size-lg);
  color: var(--text-muted);
  margin: 0 0 32px;
  background: linear-gradient(
    90deg,
    var(--text-muted),
    color-mix(in srgb, var(--accent) 30%, white),
    var(--text-muted)
  );
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  opacity: 90%;
}
</style>
