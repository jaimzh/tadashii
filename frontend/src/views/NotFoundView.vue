<template>
  <section class="not-found" aria-labelledby="not-found-heading">
    <p class="error-code">404</p>
    <h1 id="not-found-heading">This page could not be found</h1>
    <p>The address may be incorrect, or the page may have moved.</p>
    <RouterLink to="/">Return home</RouterLink>
  </section>
</template>

<style scoped>
.not-found {
  display: grid;
  justify-items: center;
  min-height: calc(100vh - 8rem);
  align-content: center;
  padding: 3rem 1rem;
  text-align: center;
}

.error-code {
  color: var(--accent);
  font-size: var(--font-size-xs);
  font-weight: 700;
  letter-spacing: 0.12em;
}

h1 {
  margin-top: 0.5rem;
  color: var(--text-main);
  font-size: clamp(1.75rem, 5vw, 2.5rem);
}

.not-found > p:not(.error-code) {
  margin-top: 0.65rem;
  color: var(--text-muted);
}

a {
  margin-top: 1.25rem;
  color: var(--accent);
  font-weight: 700;
}
</style>
