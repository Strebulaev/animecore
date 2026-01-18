<template>
  <div class="playlists-view">
    <div class="container">
      <h1>Плейлисты</h1>
      <p>Здесь будут ваши плейлисты.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import NavBar from '@/components/NavBar.vue'
</script>

<style scoped>
.playlists-view {
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