<template>
  <div class="profile-page">
    <!-- Навигация -->
    <NavBar />

    <div class="container profile-container">
      <div class="profile-header">
        <div class="user-avatar-large">
          {{ getUserInitials }}
        </div>
        <div class="user-info">
          <h1 class="user-name">{{ authStore.user?.username }}</h1>
          <p class="user-email">{{ authStore.user?.email }}</p>
          <div class="user-stats">
            <span class="stat-item">
              <strong>{{ userJoinDate }}</strong> в сообществе
            </span>
          </div>
        </div>
      </div>

      <div class="profile-content">
        <div class="profile-section">
          <h2>Информация об аккаунте</h2>
          <div class="info-grid">
            <div class="info-item">
              <label>Имя пользователя</label>
              <span>{{ authStore.user?.username }}</span>
            </div>
            <div class="info-item">
              <label>Email</label>
              <span>{{ authStore.user?.email }}</span>
            </div>
            <div class="info-item">
              <label>Статус email</label>
              <span :class="['status-badge', authStore.user?.email_verified ? 'verified' : 'unverified']">
                {{ authStore.user?.email_verified ? 'Подтверждён' : 'Не подтверждён' }}
              </span>
            </div>
            <div class="info-item">
              <label>Дата регистрации</label>
              <span>{{ userJoinDate }}</span>
            </div>
          </div>
        </div>

        <div class="profile-section">
          <h2>Действия</h2>
          <div class="actions-grid">
            <button class="btn btn-outline" @click="changePassword">
              Изменить пароль
            </button>
            <button class="btn btn-outline" @click="editProfile">
              Редактировать профиль
            </button>
            <button class="btn btn-danger" @click="deleteAccount">
              Удалить аккаунт
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import NavBar from '@/components/NavBar.vue'

const authStore = useAuthStore()

const getUserInitials = computed(() => {
  if (!authStore.user?.username) return '?'
  return authStore.user.username.charAt(0).toUpperCase()
})

const userJoinDate = computed(() => {
  if (!authStore.user?.created_at) return 'Неизвестно'
  return new Date(authStore.user.created_at).toLocaleDateString('ru-RU')
})

const changePassword = () => {
  // TODO: Реализовать изменение пароля
  alert('Функция изменения пароля будет добавлена позже')
}

const editProfile = () => {
  // TODO: Реализовать редактирование профиля
  alert('Функция редактирования профиля будет добавлена позже')
}

const deleteAccount = () => {
  if (confirm('Вы действительно хотите удалить аккаунт? Это действие нельзя отменить.')) {
    // TODO: Реализовать удаление аккаунта
    alert('Функция удаления аккаунта будет добавлена позже')
  }
}
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background-color: #f9fafb;
  padding-bottom: 2rem;
}

.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.profile-header {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 2rem;
}

.user-avatar-large {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.user-email {
  font-size: 1.1rem;
  color: #6b7280;
  margin-bottom: 1rem;
}

.user-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  font-size: 0.9rem;
  color: #6b7280;
}

.profile-content {
  display: grid;
  gap: 2rem;
}

.profile-section {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.profile-section h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item label {
  font-size: 0.9rem;
  font-weight: 500;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-item span {
  font-size: 1rem;
  color: #1f2937;
  font-weight: 500;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.verified {
  background-color: #d1fae5;
  color: #065f46;
}

.status-badge.unverified {
  background-color: #fee2e2;
  color: #dc2626;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.btn-danger {
  background-color: #dc2626;
  color: white;
  border-color: #dc2626;
}

.btn-danger:hover {
  background-color: #b91c1c;
}

.logout-btn {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
}

/* Адаптивность */
@media (max-width: 768px) {
  .profile-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .user-avatar-large {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }

  .user-name {
    font-size: 1.5rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>