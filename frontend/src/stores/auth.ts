import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/api/client'

interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  phone_number?: string
  avatar?: string
  bio?: string
  email_verified: boolean
  phone_verified: boolean
  created_at: string
  updated_at: string
}

interface AuthTokens {
  access: string
  refresh: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isAuthenticated = computed(() => !!user.value)

  const login = async (username: string, password: string) => {
    try {
      console.log('Auth Store: Attempting login for', username)
      const response = await apiClient.post('/users/login/', {
        username,
        password
      })

      const { user: userData, tokens } = response.data
      console.log('Auth Store: Login successful, user:', userData)
      user.value = userData

      localStorage.setItem('access_token', tokens.access)
      localStorage.setItem('refresh_token', tokens.refresh)

      // Устанавливаем токен в заголовки для будущих запросов
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${tokens.access}`

      console.log('Auth Store: User set to', user.value)
      console.log('Auth Store: isAuthenticated =', isAuthenticated.value)

      return { success: true }
    } catch (error) {
      console.error('Auth Store: Login failed', error)
      return { success: false, error }
    }
  }

  const register = async (data: {
    username: string
    email?: string
    phone_number?: string
    first_name?: string
    last_name?: string
    password: string
    password_confirm: string
  }) => {
    try {
      await apiClient.post('/users/register/', data)
      return { success: true }
    } catch (error) {
      return { success: false, error }
    }
  }

  const googleLogin = async (idToken: string) => {
    try {
      const response = await apiClient.post('/users/google/', {
        id_token: idToken
      })

      const { user: userData, tokens } = response.data
      user.value = userData

      localStorage.setItem('access_token', tokens.access)
      localStorage.setItem('refresh_token', tokens.refresh)

      return { success: true }
    } catch (error) {
      return { success: false, error }
    }
  }

  const verifyPhone = async (phoneNumber: string, action: 'send' | 'verify', code?: string) => {
    try {
      const response = await apiClient.post('/users/verify/phone/', {
        phone_number: phoneNumber,
        action,
        ...(code && { code })
      })
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error }
    }
  }

  const verifyEmail = async (email: string, action: 'send' | 'verify', code?: string) => {
    try {
      const response = await apiClient.post('/users/verify/email/', {
        email,
        action,
        ...(code && { code })
      })
      return { success: true, data: response.data }
    } catch (error) {
      return { success: false, error }
    }
  }

  const logout = async () => {
    try {
      await apiClient.post('/users/logout/')
    } catch (error) {
      console.error('Logout error:', error)
    }

    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    delete apiClient.defaults.headers.common['Authorization']
    user.value = null
  }

  const fetchUser = async () => {
    try {
      console.log('Auth Store: fetchUser called')
      const response = await apiClient.get('/users/profile/')
      console.log('Auth Store: fetchUser successful, user data:', response.data)
      user.value = response.data
      console.log('Auth Store: user set to:', user.value)
    } catch (error: any) {
      console.error('Auth Store: fetchUser failed:', error)
      console.error('Auth Store: error response:', error.response)
      // Если токен истек, очищаем
      if (error.response?.status === 401) {
        console.log('Auth Store: Token expired, logging out')
        logout()
      }
    }
  }

  const updateProfile = async (data: Partial<User>) => {
    try {
      const response = await apiClient.patch('/users/profile/', data)
      user.value = response.data
      return { success: true }
    } catch (error) {
      return { success: false, error }
    }
  }

  const passwordReset = async (email: string) => {
    try {
      await apiClient.post('/users/password-reset/', { email })
      return { success: true }
    } catch (error) {
      return { success: false, error }
    }
  }

  // Проверяем токен при инициализации
  const checkAuth = () => {
    const token = localStorage.getItem('access_token')
    console.log('Auth Store: checkAuth called, token exists:', !!token)
    if (token) {
      // Устанавливаем токен в заголовки
      apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
      fetchUser()
    } else {
      console.log('Auth Store: No token found in localStorage')
    }
  }

  return {
    user,
    isAuthenticated,
    login,
    register,
    googleLogin,
    verifyPhone,
    verifyEmail,
    logout,
    fetchUser,
    updateProfile,
    passwordReset,
    checkAuth
  }
})