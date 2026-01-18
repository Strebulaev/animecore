<template>
  <div class="reactor-view">
    <div class="container">
      <h1>Reactor</h1>
      <p>Здесь будут короткие видео об аниме.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import NavBar from '@/components/NavBar.vue'
</script>

<style scoped>
.reactor-view {
  min-height: 100vh;
}

.container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

p {
  color: #6b7280;
}
</style>