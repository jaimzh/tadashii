<script setup>
// Header logic will go here
</script>

<template>
  <header class="app-header">
    <div class="header-inner">
      <div class="logo">
        <!-- Your tiny ink logo goes here -->
        <span>Logo</span>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background-color: #000;
  color: #fff;
  width: 100%;
}

.header-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
}

.logo {
  display: flex;
  align-items: center;
}
</style>
