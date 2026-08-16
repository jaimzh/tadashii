<script setup>
import TadashiiLogo from '@/components/common/TadashiiLogo.vue'
</script>

<template>
  <section class="animated-hero">
    <TadashiiLogo class="hero-image" />

    <h1 class="sr-only">Anime recommendations that match your mood</h1>
    <!-- <p class="hero-subtitle">
      Describe what you feel like watching. Tadashii will help you find the right story.
    </p> -->


    <p class="hero-subtitle">
      Let's find the right story for you!
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
  gap: 1.25rem;
  padding: 16px;
  overflow: hidden;
}

.hero-image {
  width: min(100%, 320px);
}

.hero-subtitle {
  max-width: 44ch;
  font-size: var(--font-size-sm);
  line-height: 1.55;
  text-align: center;
  color: var(--text-muted);
  margin: 0 0 20px;
  background: linear-gradient(
    90deg,
    var(--text-muted),
    color-mix(in srgb, var(--accent-glow) 70%, white),
    var(--text-muted)
  );
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  opacity: 90%;
}

.hero-title {
  margin: -0.25rem 0 -0.65rem;
  color: var(--text-main);
  font-size: clamp(var(--font-size-lg), 3vw, var(--font-size-xl));
  line-height: 1.25;
  text-align: center;
}
</style>
