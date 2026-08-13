<script setup>
import TadashiiLogo from '@/components/common/TadashiiLogo.vue'
</script>

<template>
  <section class="animated-hero">
    <TadashiiLogo class="hero-image" />

    <p class="hero-subtitle">
      Let's find the right story for you! <br />
     
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
  font-size: var(--font-size-md);
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
</style>
