<template>
    <div class="anime-view">
      <!-- Навигация -->
      <nav class="navbar">
        <div class="container">
          <div class="nav-left">
            <router-link to="/" class="logo">🎌 AnimeCore</router-link>
            <div class="nav-links">
              <router-link to="/" class="nav-link">Главная</router-link>
              <router-link to="/anime" class="nav-link active">Аниме</router-link>
              <router-link to="/playlists" class="nav-link">Плейлисты</router-link>
            </div>
          </div>
          <div class="nav-right">
            <router-link to="/login" class="btn btn-outline">Войти</router-link>
          </div>
        </div>
      </nav>
  
      <!-- Контент -->
      <div class="container main-content">
        <!-- Заголовок и поиск -->
        <div class="page-header">
          <h1>Все аниме</h1>
          <div class="search-box">
            <input
              v-model="searchQuery"
              @input="handleSearch"
              type="text"
              placeholder="Поиск аниме..."
              class="search-input"
            />
            <div class="search-icon">🔍</div>
          </div>
        </div>
  
        <!-- Состояние загрузки -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Загрузка аниме...</p>
        </div>
  
        <!-- Ошибка -->
        <div v-else-if="error" class="error-state">
          <p>Ошибка: {{ error }}</p>
          <button @click="fetchAnime" class="btn btn-primary">Попробовать снова</button>
        </div>
  
        <!-- Список аниме -->
        <div v-else>
          <!-- Фильтры -->
          <div class="filters">
            <button
              v-for="status in statusFilters"
              :key="status.value"
              @click="toggleStatusFilter(status.value)"
              :class="['filter-btn', { active: activeStatusFilters.includes(status.value) }]"
            >
              {{ status.label }}
            </button>
          </div>
  
          <!-- Карточки -->
          <div v-if="filteredAnime.length === 0" class="empty-state">
            <p>Аниме не найдено</p>
          </div>
  
          <div class="anime-grid">
            <div
              v-for="item in filteredAnime"
              :key="item.id"
              class="anime-card"
              @click="goToAnimeDetail(item.id)"
            >
              <!-- Постер -->
              <div class="anime-poster">
                <div class="poster-placeholder">🎌</div>
              </div>
              
              <!-- Информация -->
              <div class="anime-info">
                <h3 class="anime-title">{{ item.title_ru || item.title_en }}</h3>
                
                <div class="anime-meta">
                  <span class="anime-year">{{ item.year }}</span>
                  <span class="anime-episodes">{{ item.episodes }} эп.</span>
                  <span :class="['anime-status', getStatusClass(item.status)]">
                    {{ getStatusText(item.status) }}
                  </span>
                </div>
                
                <p class="anime-description">{{ truncateDescription(item.description) }}</p>
                
                <!-- Жанры -->
                <div class="anime-genres">
                  <span
                    v-for="genre in item.genres.slice(0, 3)"
                    :key="genre.id"
                    class="genre-tag"
                  >
                    {{ genre.name }}
                  </span>
                  <span v-if="item.genres.length > 3" class="genre-more">
                    +{{ item.genres.length - 3 }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import apiClient from '@/api/client'
  
  const router = useRouter()
  
  // Состояние
  const animeList = ref<any[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)
  const searchQuery = ref('')
  const activeStatusFilters = ref<string[]>([])
  
  // Фильтры статусов
  const statusFilters = [
    { value: 'ongoing', label: 'Онгоинг' },
    { value: 'finished', label: 'Завершён' },
    { value: 'announced', label: 'Анонсирован' }
  ]
  
  // Загрузка аниме
  const fetchAnime = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await apiClient.get('/anime/anime/')
      animeList.value = response.data
    } catch (err: any) {
      error.value = err.message || 'Не удалось загрузить аниме'
      console.error('Ошибка загрузки аниме:', err)
    } finally {
      loading.value = false
    }
  }
  
  // Поиск
  const handleSearch = async () => {
    if (searchQuery.value.trim()) {
      loading.value = true
      try {
        const response = await apiClient.get('/anime/anime/', {
          params: { search: searchQuery.value }
        })
        animeList.value = response.data
      } catch (err) {
        console.error('Ошибка поиска:', err)
      } finally {
        loading.value = false
      }
    } else {
      fetchAnime()
    }
  }
  
  // Фильтрация по статусу
  const toggleStatusFilter = (status: string) => {
    const index = activeStatusFilters.value.indexOf(status)
    if (index === -1) {
      activeStatusFilters.value.push(status)
    } else {
      activeStatusFilters.value.splice(index, 1)
    }
  }
  
  // Фильтрованные аниме
  const filteredAnime = computed(() => {
    let filtered = animeList.value
    
    if (activeStatusFilters.value.length > 0) {
      filtered = filtered.filter(item => 
        activeStatusFilters.value.includes(item.status)
      )
    }
    
    return filtered
  })
  
  // Вспомогательные функции
  const getStatusText = (status: string) => {
    const map: Record<string, string> = {
      'ongoing': 'Онгоинг',
      'finished': 'Завершён',
      'announced': 'Анонсирован'
    }
    return map[status] || status
  }
  
  const getStatusClass = (status: string) => {
    const map: Record<string, string> = {
      'ongoing': 'status-ongoing',
      'finished': 'status-finished',
      'announced': 'status-announced'
    }
    return map[status] || ''
  }
  
  const truncateDescription = (desc: string) => {
    if (!desc) return 'Описание отсутствует'
    return desc.length > 150 ? desc.substring(0, 150) + '...' : desc
  }
  
  // Переход к деталям
  const goToAnimeDetail = (id: number) => {
    router.push(`/anime/${id}`)
  }
  
  // Загрузка при монтировании
  onMounted(() => {
    fetchAnime()
  })
  </script>
  
  <style scoped>
  .anime-view {
    min-height: 100vh;
    background-color: #f9fafb;
  }
  
  /* Основной контент */
  .main-content {
    padding: 2rem 1rem;
  }
  
  /* Заголовок страницы */
  .page-header {
    margin-bottom: 2rem;
  }
  
  .page-header h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 1rem;
  }
  
  /* Поиск */
  .search-box {
    position: relative;
    max-width: 400px;
  }
  
  .search-input {
    width: 100%;
    padding: 0.75rem 1rem 0.75rem 2.5rem;
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    font-size: 1rem;
    outline: none;
    transition: border-color 0.2s;
  }
  
  .search-input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  }
  
  .search-icon {
    position: absolute;
    left: 0.75rem;
    top: 50%;
    transform: translateY(-50%);
    color: #9ca3af;
  }
  
  /* Состояния */
  .loading-state {
    text-align: center;
    padding: 3rem;
  }
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #e5e7eb;
    border-top-color: #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .error-state {
    text-align: center;
    padding: 3rem;
    color: #dc2626;
  }
  
  .empty-state {
    text-align: center;
    padding: 3rem;
    color: #6b7280;
  }
  
  /* Фильтры */
  .filters {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
  }
  
  .filter-btn {
    padding: 0.5rem 1rem;
    border: 1px solid #d1d5db;
    border-radius: 9999px;
    background: white;
    color: #4b5563;
    font-size: 0.875rem;
    cursor: pointer;
    transition: all 0.2s;
  }
  
  .filter-btn:hover {
    background-color: #f3f4f6;
  }
  
  .filter-btn.active {
    background-color: #3b82f6;
    color: white;
    border-color: #3b82f6;
  }
  
  /* Сетка аниме */
  .anime-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
  }
  
  /* Карточка аниме */
  .anime-card {
    background: white;
    border-radius: 0.75rem;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: pointer;
  }
  
  .anime-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
  }
  
  /* Постер */
  .anime-poster {
    height: 200px;
    background: linear-gradient(135deg, #93c5fd 0%, #3b82f6 100%);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .poster-placeholder {
    font-size: 4rem;
    opacity: 0.8;
  }
  
  /* Информация об аниме */
  .anime-info {
    padding: 1rem;
  }
  
  .anime-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 0.5rem;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  
  .anime-meta {
    display: flex;
    gap: 0.75rem;
    align-items: center;
    font-size: 0.875rem;
    color: #6b7280;
    margin-bottom: 0.75rem;
  }
  
  .anime-status {
    padding: 0.125rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.75rem;
    font-weight: 500;
  }
  
  .status-ongoing {
    background-color: #dcfce7;
    color: #166534;
  }
  
  .status-finished {
    background-color: #f3f4f6;
    color: #374151;
  }
  
  .status-announced {
    background-color: #dbeafe;
    color: #1e40af;
  }
  
  .anime-description {
    font-size: 0.875rem;
    color: #4b5563;
    line-height: 1.5;
    margin-bottom: 1rem;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  
  /* Жанры */
  .anime-genres {
    display: flex;
    flex-wrap: wrap;
    gap: 0.375rem;
  }
  
  .genre-tag {
    padding: 0.25rem 0.5rem;
    background-color: #f3f4f6;
    color: #4b5563;
    border-radius: 0.25rem;
    font-size: 0.75rem;
  }
  
  .genre-more {
    font-size: 0.75rem;
    color: #9ca3af;
    align-self: center;
  }
  
  /* Адаптивность */
  @media (max-width: 640px) {
    .container {
      padding: 0 0.75rem;
    }
    
    .nav-links {
      display: none;
    }
    
    .anime-grid {
      grid-template-columns: 1fr;
    }
    
    .hero-title {
      font-size: 2rem;
    }
  }
  </style>