<template>
    <div class="anime-view">
      <!-- Навигация -->
      <NavBar />
  
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
            <AnimeCard
              v-for="item in filteredAnime"
              :key="item.id"
              :anime="item"
              @click="goToAnimeDetail"
            />
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import apiClient from '@/api/client'
  import NavBar from '@/components/NavBar.vue'
  import AnimeCard from '@/components/AnimeCard.vue'
  
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
  const goToAnimeDetail = (anime: any) => {
    router.push(`/anime/${anime.id}`)
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
  
  /* Адаптивность */
  @media (max-width: 640px) {
    .main-content {
      padding: 1rem 0.5rem;
    }

    .page-header {
      margin-bottom: 1.5rem;
    }

    .page-header h1 {
      font-size: 1.75rem;
    }

    .search-box {
      max-width: 100%;
    }

    .filters {
      gap: 0.375rem;
      margin-bottom: 1rem;
    }

    .filter-btn {
      padding: 0.375rem 0.75rem;
      font-size: 0.8125rem;
    }

    .anime-grid {
      grid-template-columns: 1fr;
      gap: 1rem;
    }
  }

  @media (max-width: 480px) {
    .main-content {
      padding: 0.75rem 0.25rem;
    }

    .page-header h1 {
      font-size: 1.5rem;
    }

    .filters {
      justify-content: center;
    }

    .filter-btn {
      padding: 0.375rem 0.625rem;
      font-size: 0.75rem;
    }

    .anime-grid {
      gap: 0.75rem;
    }
  }
  </style>