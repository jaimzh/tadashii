<script setup>
import heroSvg from '@/assets/Group 5.svg'
</script>

<template>
  <section class="animated-hero">
    <img :src="heroSvg" alt="" class="hero-image" />

    <p class="hero-subtitle">
      Let's find the right story for you! <br />
      Describe what you're in the mood for
    </p>
    <div class="hero-glow"></div>
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


.hero-glow {
  margin-top: 25rem;
  position: absolute;
  width: 500px;
  height: 300px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(var(--accent-rgb), 0.3), transparent 90%);
  filter: blur(80px);
  pointer-events: none;
  z-index: 1;
}

.hero-subtitle {
  font-size: 1.3rem;
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
}
</style>
