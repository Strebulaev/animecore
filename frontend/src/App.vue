<template>
  <div id="app">
    <NavBar />
    <router-view />
    <BottomNavigation />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import NavBar from '@/components/NavBar.vue'
import BottomNavigation from '@/components/BottomNavigation.vue'

// Пока без auth store
onMounted(() => {
  console.log('App mounted')
})
</script>

<style>
/* Глобальные стили */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background-color: #f9fafb;
  width: 100%;
}

/* CSS Variables for spacing */
:root {
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  --space-xl: 4rem;
}

#app {
  min-height: 100vh;
  /* Add bottom padding for mobile navigation */
  padding-bottom: 80px;
}

/* Adjust padding on larger screens */
@media (min-width: 768px) {
  #app {
    padding-bottom: 0;
  }
}

/* Global container styles for consistent layout */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (min-width: 768px) {
  .container {
    padding: 0 4rem;
  }
}

@media (min-width: 1200px) {
  .container {
    max-width: 1400px;
    padding: 0 6rem;
  }
}

@media (min-width: 1600px) {
  .container {
    max-width: 1600px;
    padding: 0 8rem;
  }
}

/* Hide NavBar on mobile screens */
@media (max-width: 767px) {
  .navbar {
    display: none;
  }
}
</style>