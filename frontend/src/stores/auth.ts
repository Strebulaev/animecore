import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/api/client'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isAuthenticated = computed(() => !!user.value)
  
  const login = async (username: string, password: string) => {
    try {
      const response = await apiClient.post('/auth/login/', {
        username,
        password
      })
      
      const { access, refresh } = response.data
      localStorage.setItem('access_token', access)
      localStorage.setItem('refresh_token', refresh)
      
      // Получаем данные пользователя
      await fetchUser()
      
      return { success: true }
    } catch (error) {
      return { success: false, error }
    }
  }
  
  const register = async (username: string, email: string, password: string) => {
    try {
      await apiClient.post('/auth/register/', {
        username,
        email,
        password
      })
      return { success: true }
    } catch (error) {
      return { success: false, error }
    }
  }
  
  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    user.value = null
  }
  
  const fetchUser = async () => {
    try {
      const response = await apiClient.get('/auth/user/')
      user.value = response.data
    } catch (error) {
      console.error('Ошибка загрузки пользователя:', error)
    }
  }
  
  // Проверяем токен при инициализации
  const checkAuth = () => {
    const token = localStorage.getItem('access_token')
    if (token) {
      fetchUser()
    }
  }
  
  return {
    user,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUser,
    checkAuth
  }
})