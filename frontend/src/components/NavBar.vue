<template>
  <nav class="navbar">
    <div class="container">
      <div class="nav-left">
        <router-link to="/" class="logo">🎌 AnimeCore</router-link>
        <div class="nav-links desktop-nav">
          <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">
            Главная
          </router-link>
          <router-link to="/anime" class="nav-link" :class="{ active: $route.path.startsWith('/anime') }">
            Аниме
          </router-link>
          <router-link to="/playlists" class="nav-link" :class="{ active: $route.path.startsWith('/playlists') }">
            Плейлисты
          </router-link>
        </div>
      </div>

      <div class="nav-right">
        <!-- Для неавторизованных пользователей -->
        <template v-if="!authStore.isAuthenticated">
          <router-link to="/login" class="btn btn-outline hidden-sm-down">Войти</router-link>
          <router-link to="/register" class="btn btn-primary hidden-sm-down">Регистрация</router-link>
        </template>

        <!-- Для авторизованных пользователей -->
        <template v-else>
          <router-link to="/profile" class="nav-link hidden-sm-down" :class="{ active: $route.path === '/profile' }">
            Аккаунт
          </router-link>
          <button @click="handleLogout" class="btn btn-outline logout-btn hidden-sm-down">
            Выйти
          </button>
        </template>

        <!-- Hamburger menu button -->
        <button
          class="hamburger-btn hidden-md-up"
          @click="toggleMobileMenu"
          :class="{ active: isMobileMenuOpen }"
          aria-label="Toggle menu"
        >
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
          <span class="hamburger-line"></span>
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <div class="mobile-menu" :class="{ open: isMobileMenuOpen }">
      <div class="mobile-menu-content">
        <div class="mobile-nav-links">
          <router-link to="/" class="mobile-nav-link" @click="closeMobileMenu" :class="{ active: $route.path === '/' }">
            Главная
          </router-link>
          <router-link to="/anime" class="mobile-nav-link" @click="closeMobileMenu" :class="{ active: $route.path.startsWith('/anime') }">
            Аниме
          </router-link>
          <router-link to="/playlists" class="mobile-nav-link" @click="closeMobileMenu" :class="{ active: $route.path.startsWith('/playlists') }">
            Плейлисты
          </router-link>
        </div>

        <div class="mobile-auth">
          <!-- Для неавторизованных пользователей -->
          <template v-if="!authStore.isAuthenticated">
            <router-link to="/login" class="mobile-btn btn-outline" @click="closeMobileMenu">Войти</router-link>
            <router-link to="/register" class="mobile-btn btn-primary" @click="closeMobileMenu">Регистрация</router-link>
          </template>

          <!-- Для авторизованных пользователей -->
          <template v-else>
            <router-link to="/profile" class="mobile-nav-link" @click="closeMobileMenu" :class="{ active: $route.path === '/profile' }">
              Аккаунт
            </router-link>
            <button @click="handleLogoutAndClose" class="mobile-btn btn-outline logout">
              Выйти
            </button>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isMobileMenuOpen = ref(false)

// Управление мобильным меню
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}

// Выход из аккаунта
const handleLogout = async () => {
  await authStore.logout()
  // Можно добавить редирект на главную
}

const handleLogoutAndClose = async () => {
  await handleLogout()
  closeMobileMenu()
}

// Закрытие меню при клике вне его (для мобильных)
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement
  if (!target.closest('.navbar') && isMobileMenuOpen.value) {
    closeMobileMenu()
  }
}

// Инициализация
onMounted(() => {
  console.log('NavBar: Component mounted')
  // Проверяем аутентификацию при загрузке
  authStore.checkAuth()
  console.log('NavBar: isAuthenticated =', authStore.isAuthenticated)
  console.log('NavBar: user =', authStore.user)

  // Добавляем слушатель для кликов вне меню
  document.addEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #3b82f6;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  color: #4b5563;
  text-decoration: none;
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  transition: background-color 0.2s;
}

.nav-link:hover {
  background-color: #f3f4f6;
}

.nav-link.active {
  color: #3b82f6;
  font-weight: 600;
}

.nav-right {
  display: flex;
  gap: 0.75rem;
  align-items: center;
}

/* Кнопки */
.btn {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  text-decoration: none;
  display: inline-block;
  transition: all 0.2s;
  border: 1px solid transparent;
  cursor: pointer;
}

.btn-outline {
  color: #4b5563;
  border-color: #d1d5db;
  background: white;
}

.btn-outline:hover {
  background-color: #f9fafb;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.btn-primary:hover {
  background-color: #2563eb;
}

/* Кнопка выхода */
.logout-btn {
  color: #dc2626;
  border-color: #dc2626;
}

.logout-btn:hover {
  background-color: #fef2f2;
}

/* Hamburger menu button */
.hamburger-btn {
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 30px;
  height: 30px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1001;
}

.hamburger-line {
  width: 100%;
  height: 3px;
  background: #4b5563;
  border-radius: 2px;
  transition: all 0.3s ease;
  transform-origin: center;
}

.hamburger-btn.active .hamburger-line:nth-child(1) {
  transform: rotate(45deg) translate(6px, 6px);
}

.hamburger-btn.active .hamburger-line:nth-child(2) {
  opacity: 0;
}

.hamburger-btn.active .hamburger-line:nth-child(3) {
  transform: rotate(-45deg) translate(6px, -6px);
}

/* Mobile menu */
.mobile-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transform: translateY(-100%);
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
  z-index: 1000;
}

.mobile-menu.open {
  transform: translateY(0);
  opacity: 1;
  visibility: visible;
}

.mobile-menu-content {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.mobile-nav-links {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mobile-nav-link {
  color: #4b5563;
  text-decoration: none;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  transition: background-color 0.2s;
  font-size: 1rem;
}

.mobile-nav-link:hover,
.mobile-nav-link.active {
  background-color: #f3f4f6;
  color: #3b82f6;
}

.mobile-auth {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

.mobile-btn {
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  text-decoration: none;
  text-align: center;
  display: inline-block;
  transition: all 0.2s;
  border: 1px solid transparent;
  cursor: pointer;
  font-size: 1rem;
  min-height: 44px;
}

.mobile-btn.btn-outline {
  color: #4b5563;
  border-color: #d1d5db;
  background: white;
}

.mobile-btn.btn-outline:hover {
  background-color: #f9fafb;
}

.mobile-btn.btn-primary {
  background-color: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.mobile-btn.btn-primary:hover {
  background-color: #2563eb;
}

.mobile-btn.logout {
  color: #dc2626;
  border-color: #dc2626;
}

.mobile-btn.logout:hover {
  background-color: #fef2f2;
}

/* Responsive breakpoints */
@media (max-width: 768px) {
  .desktop-nav {
    display: none;
  }

  .hamburger-btn {
    display: flex;
  }

  .navbar {
    padding: 0.75rem 0;
    position: relative;
  }

  .container {
    padding: 0 0.75rem;
  }

  .nav-left {
    gap: 1rem;
  }

  .logo {
    font-size: 1.25rem;
  }

  .nav-right {
    gap: 0.5rem;
  }

  .btn {
    padding: 0.4rem 0.75rem;
    font-size: 0.875rem;
  }
}

@media (max-width: 480px) {
  .navbar {
    padding: 0.5rem 0;
  }

  .container {
    padding: 0 0.5rem;
  }

  .nav-left {
    gap: 0.75rem;
  }

  .logo {
    font-size: 1.125rem;
  }

  .nav-right {
    gap: 0.375rem;
  }

  .btn {
    padding: 0.375rem 0.625rem;
    font-size: 0.8rem;
  }

  .mobile-menu-content {
    padding: 0.75rem;
    gap: 1rem;
  }

  .mobile-nav-link,
  .mobile-btn {
    padding: 0.625rem 0.875rem;
    font-size: 0.95rem;
  }
}
</style>