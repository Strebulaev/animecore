<template>
    <div class="auth-page">
      <nav class="navbar">
        <div class="container">
          <router-link to="/" class="logo">🎌 AnimeCore</router-link>
        </div>
      </nav>
  
      <div class="container auth-container">
        <div class="auth-card">
          <h2>Регистрация</h2>
          <p class="auth-subtitle">Создайте аккаунт чтобы начать</p>
          
          <form @submit.prevent="handleRegister" class="auth-form">
            <div class="form-group">
              <label for="username">Имя пользователя</label>
              <input
                v-model="form.username"
                type="text"
                id="username"
                placeholder="Придумайте имя пользователя"
                required
              />
            </div>
            
            <div class="form-group">
              <label for="email">Email</label>
              <input
                v-model="form.email"
                type="email"
                id="email"
                placeholder="Введите email"
                required
              />
            </div>
            
            <div class="form-group">
              <label for="password">Пароль</label>
              <input
                v-model="form.password"
                type="password"
                id="password"
                placeholder="Придумайте пароль"
                required
              />
            </div>
            
            <div class="form-group">
              <label for="confirmPassword">Подтверждение пароля</label>
              <input
                v-model="form.confirmPassword"
                type="password"
                id="confirmPassword"
                placeholder="Повторите пароль"
                required
              />
            </div>
            
            <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
              {{ loading ? 'Регистрация...' : 'Зарегистрироваться' }}
            </button>
          </form>
          
          <div class="auth-footer">
            <p>Уже есть аккаунт? <router-link to="/login">Войти</router-link></p>
            <router-link to="/" class="back-link">← На главную</router-link>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  const loading = ref(false)
  const form = ref({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  })
  
  const handleRegister = async () => {
    if (form.value.password !== form.value.confirmPassword) {
      alert('Пароли не совпадают')
      return
    }
    
    loading.value = true
    // TODO: Реализовать регистрацию
    setTimeout(() => {
      loading.value = false
      router.push('/login')
    }, 1000)
  }
  </script>
  
  <style scoped>
  /* Стили такие же как в LoginView */
  </style>