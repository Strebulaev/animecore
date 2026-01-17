<template>
    <div class="auth-page">
      <nav class="navbar">
        <div class="container">
          <router-link to="/" class="logo">🎌 AnimeCore</router-link>
        </div>
      </nav>
  
      <div class="container auth-container">
        <div class="auth-card">
          <h2>Вход в аккаунт</h2>
          <p class="auth-subtitle">Войдите чтобы использовать все возможности</p>
          
          <form @submit.prevent="handleLogin" class="auth-form">
            <div class="form-group">
              <label for="username">Имя пользователя</label>
              <input
                v-model="form.username"
                type="text"
                id="username"
                placeholder="Введите имя пользователя"
                required
              />
            </div>
            
            <div class="form-group">
              <label for="password">Пароль</label>
              <input
                v-model="form.password"
                type="password"
                id="password"
                placeholder="Введите пароль"
                required
              />
            </div>
            
            <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
              {{ loading ? 'Вход...' : 'Войти' }}
            </button>
          </form>
          
          <div class="auth-footer">
            <p>Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link></p>
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
    password: ''
  })
  
  const handleLogin = async () => {
    loading.value = true
    // TODO: Реализовать логику входа
    setTimeout(() => {
      loading.value = false
      router.push('/')
    }, 1000)
  }
  </script>
  
  <style scoped>
  .auth-page {
    min-height: 100vh;
    background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  }
  
  .auth-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 64px);
    padding: 2rem 1rem;
  }
  
  .auth-card {
    background: white;
    padding: 2rem;
    border-radius: 1rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    width: 100%;
    max-width: 400px;
  }
  
  .auth-card h2 {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 0.5rem;
  }
  
  .auth-subtitle {
    color: #6b7280;
    margin-bottom: 1.5rem;
  }
  
  .auth-form {
    margin-bottom: 1.5rem;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  .form-group label {
    display: block;
    font-size: 0.875rem;
    font-weight: 500;
    color: #374151;
    margin-bottom: 0.375rem;
  }
  
  .form-group input {
    width: 100%;
    padding: 0.625rem 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    font-size: 1rem;
    transition: border-color 0.2s;
  }
  
  .form-group input:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  .btn-block {
    width: 100%;
    padding: 0.75rem;
    font-size: 1rem;
  }
  
  .auth-footer {
    text-align: center;
    padding-top: 1rem;
    border-top: 1px solid #e5e7eb;
  }
  
  .auth-footer p {
    color: #6b7280;
    margin-bottom: 1rem;
  }
  
  .auth-footer a {
    color: #3b82f6;
    text-decoration: none;
  }
  
  .back-link {
    display: inline-block;
    color: #6b7280;
    text-decoration: none;
    font-size: 0.875rem;
  }
  </style>