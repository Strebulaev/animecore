<template>
  <nav class="bg-white shadow-sm py-4 sticky top-0 z-50">
    <div class="container flex justify-between items-center">
      <div class="flex items-center gap-8">
        <router-link to="/" class="text-2xl font-bold text-blue-600 no-underline">🎌 Анимяшка</router-link>
        <div class="hidden md:flex gap-6">
          <router-link to="/" class="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md transition-colors no-underline" :class="{ 'text-blue-600 font-semibold': $route.path === '/' }">
            Главная
          </router-link>
          <router-link to="/anime" class="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md transition-colors no-underline" :class="{ 'text-blue-600 font-semibold': $route.path.startsWith('/anime') }">
            Аниме
          </router-link>
          <router-link to="/playlists" class="text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md transition-colors no-underline" :class="{ 'text-blue-600 font-semibold': $route.path.startsWith('/playlists') }">
            Плейлисты
          </router-link>
        </div>
      </div>

      <div class="flex items-center gap-4">
        <!-- Для неавторизованных пользователей -->
        <template v-if="!authStore.isAuthenticated">
          <router-link to="/login" class="hidden md:inline-block text-gray-600 border border-gray-300 bg-white hover:bg-gray-50 px-4 py-2 rounded-md transition-colors no-underline">Войти</router-link>
          <router-link to="/register" class="hidden md:inline-block bg-blue-600 text-white border border-blue-600 hover:bg-blue-700 px-4 py-2 rounded-md transition-colors no-underline">Регистрация</router-link>
        </template>

        <!-- Для авторизованных пользователей -->
        <template v-else>
          <router-link to="/profile" class="hidden md:inline-block text-gray-600 hover:text-blue-600 px-3 py-2 rounded-md transition-colors no-underline" :class="{ 'text-blue-600 font-semibold': $route.path === '/profile' }">
            Аккаунт
          </router-link>
          <button @click="handleLogout" class="hidden md:inline-block text-red-600 border border-red-600 bg-white hover:bg-red-50 px-4 py-2 rounded-md transition-colors">
            Выйти
          </button>
        </template>

        <!-- Hamburger menu button -->
        <button
          class="md:hidden flex flex-col justify-center items-center w-8 h-8 bg-transparent border-none cursor-pointer"
          @click="toggleMobileMenu"
          :class="{ 'open': isMobileMenuOpen }"
          aria-label="Toggle menu"
        >
          <span class="w-full h-0.5 bg-gray-600 mb-1 transition-transform"></span>
          <span class="w-full h-0.5 bg-gray-600 mb-1 transition-opacity"></span>
          <span class="w-full h-0.5 bg-gray-600 transition-transform"></span>
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <div class="md:hidden absolute top-full left-0 right-0 bg-white shadow-md transform transition-transform" :class="{ '-translate-y-full opacity-0 pointer-events-none': !isMobileMenuOpen, 'translate-y-0 opacity-100': isMobileMenuOpen }">
      <div class="px-4 py-6">
        <div class="space-y-2">
          <router-link to="/" class="block text-gray-600 hover:text-blue-600 py-3 px-4 rounded-md transition-colors no-underline" @click="closeMobileMenu" :class="{ 'text-blue-600 bg-gray-50': $route.path === '/' }">
            Главная
          </router-link>
          <router-link to="/anime" class="block text-gray-600 hover:text-blue-600 py-3 px-4 rounded-md transition-colors no-underline" @click="closeMobileMenu" :class="{ 'text-blue-600 bg-gray-50': $route.path.startsWith('/anime') }">
            Аниме
          </router-link>
          <router-link to="/playlists" class="block text-gray-600 hover:text-blue-600 py-3 px-4 rounded-md transition-colors no-underline" @click="closeMobileMenu" :class="{ 'text-blue-600 bg-gray-50': $route.path.startsWith('/playlists') }">
            Плейлисты
          </router-link>
        </div>

        <div class="mt-6 pt-4 border-t border-gray-200 space-y-3">
          <!-- Для неавторизованных пользователей -->
          <template v-if="!authStore.isAuthenticated">
            <router-link to="/login" class="block text-center text-gray-600 border border-gray-300 bg-white hover:bg-gray-50 py-3 px-4 rounded-md transition-colors no-underline" @click="closeMobileMenu">Войти</router-link>
            <router-link to="/register" class="block text-center bg-blue-600 text-white border border-blue-600 hover:bg-blue-700 py-3 px-4 rounded-md transition-colors no-underline" @click="closeMobileMenu">Регистрация</router-link>
          </template>

          <!-- Для авторизованных пользователей -->
          <template v-else>
            <router-link to="/profile" class="block text-gray-600 hover:text-blue-600 py-3 px-4 rounded-md transition-colors no-underline" @click="closeMobileMenu" :class="{ 'text-blue-600 bg-gray-50': $route.path === '/profile' }">
              Аккаунт
            </router-link>
            <button @click="handleLogoutAndClose" class="block w-full text-center text-red-600 border border-red-600 bg-white hover:bg-red-50 py-3 px-4 rounded-md transition-colors">
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
@media (min-width: 768px) {
  .container {
    padding: 0 4rem;
  }
}

@media (min-width: 1200px) {
  .container {
    padding: 0 6rem;
  }
}

@media (min-width: 1600px) {
  .container {
    padding: 0 8rem;
  }
}

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