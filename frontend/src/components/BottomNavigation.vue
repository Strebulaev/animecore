<template>
  <nav class="bottom-navigation">
    <router-link
      to="/"
      class="nav-item"
      :class="{ active: $route.name === 'home' }"
    >
      <div class="nav-icon">🏠</div>
      <span class="nav-label">Главная</span>
    </router-link>

    <router-link
      to="/anime"
      class="nav-item"
      :class="{ active: $route.name === 'anime' || $route.name === 'anime-detail' }"
    >
      <div class="nav-icon">🎬</div>
      <span class="nav-label">Аниме</span>
    </router-link>

    <router-link
      to="/playlists"
      class="nav-item"
      :class="{ active: $route.name === 'playlists' }"
    >
      <div class="nav-icon">📋</div>
      <span class="nav-label">Плейлисты</span>
    </router-link>

    <router-link
      to="/groups"
      class="nav-item"
      :class="{ active: $route.name === 'groups' }"
    >
      <div class="nav-icon">👥</div>
      <span class="nav-label">Группы</span>
    </router-link>

    <router-link
      to="/reactor"
      class="nav-item"
      :class="{ active: $route.name === 'reactor' }"
    >
      <div class="nav-icon">🎥</div>
      <span class="nav-label">Reactor</span>
    </router-link>

    <router-link
      to="/profile"
      class="nav-item"
      :class="{ active: $route.name === 'profile' }"
    >
      <div class="nav-icon">👤</div>
      <span class="nav-label">Профиль</span>
    </router-link>
  </nav>
</template>

<script setup lang="ts">
// No additional logic needed, using $route for active states
</script>

<style scoped>
.bottom-navigation {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #e5e7eb;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 0.5rem 0;
  z-index: 1000;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: #6b7280;
  padding: 0.25rem;
  min-width: 60px;
  transition: color 0.2s;
}

.nav-item:hover,
.nav-item.active {
  color: #3b82f6;
}

.nav-icon {
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
}

.nav-label {
  font-size: 0.75rem;
  font-weight: 500;
}

/* Hide on larger screens */
@media (min-width: 768px) {
  .bottom-navigation {
    display: none;
  }
}

/* Adjust for very small screens */
@media (max-width: 480px) {
  .nav-label {
    font-size: 0.7rem;
  }

  .nav-icon {
    font-size: 1.25rem;
  }
}
</style>