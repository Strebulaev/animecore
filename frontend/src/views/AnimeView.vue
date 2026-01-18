<template>
    <div class="anime-view">
      <div class="container main-content">
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
          <div class="sort-box">
            <select v-model="ordering" @change="handleSort" class="sort-select">
              <option value="">По умолчанию</option>
              <option value="-score">По рейтингу (убыв)</option>
              <option value="-episodes">По количеству серий (убыв)</option>
              <option value="-year">По году (убыв)</option>
            </select>
          </div>
        </div>
  
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Загрузка аниме...</p>
        </div>
  
        <!-- Ошибка -->
        <div v-else-if="error" class="error-state">
          <p>Ошибка: {{ error }}</p>
          <button @click="() => fetchAnime(1)" class="btn btn-primary">Попробовать снова</button>
        </div>
  
        <!-- Список аниме -->
        <div v-else>
          <!-- Кнопка показа фильтров -->
          <div class="filters-toggle">
            <button @click="showFilters = !showFilters" class="toggle-btn">
              {{ showFilters ? 'Скрыть фильтры' : 'Показать фильтры' }}
              <span class="toggle-icon">{{ showFilters ? '▲' : '▼' }}</span>
            </button>
          </div>

          <!-- Фильтры -->
          <div v-show="showFilters" class="filters">
            <!-- Статусы -->
            <div class="filter-group">
              <h3 class="filter-title">Статус:</h3>
              <button
                v-for="status in statusFilters"
                :key="status.value"
                @click="toggleStatusFilter(status.value)"
                :class="['filter-btn', { active: activeStatusFilters.includes(status.value) }]"
              >
                {{ status.label }}
              </button>
            </div>

            <!-- Жанры -->
            <div class="filter-group">
              <h3 class="filter-title">Жанры:</h3>
              <button
                v-for="genre in genresList"
                :key="genre.id"
                @click="toggleGenreFilter(genre.id)"
                :class="['filter-btn', { active: activeGenreFilters.includes(genre.id) }]"
              >
                {{ genre.name }}
              </button>
            </div>

            <!-- Кнопка очистки -->
            <div class="filter-actions">
              <button @click="clearFilters" class="clear-btn">
                Очистить все фильтры
              </button>
            </div>
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
          <div v-if="hasNextPage && !loadingMore" class="load-more-container">
            <button @click="loadMoreAnime" class="btn btn-primary load-more-btn">
              Показать больше аниме
            </button>
          </div>
          <!-- Индикатор загрузки -->
          <div v-if="loadingMore" class="loading-more">
            <div class="spinner small"></div>
            <p>Загрузка...</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed, onMounted, nextTick } from 'vue'
  import { useRouter } from 'vue-router'
  import apiClient from '@/api/client'
  import NavBar from '@/components/NavBar.vue'
  import AnimeCard from '@/components/AnimeCard.vue'
  
  const router = useRouter()
  
  // Состояние
  const animeList = ref<any[]>([])
  const genresList = ref<any[]>([])
  const loading = ref(true)
  const loadingMore = ref(false)
  const error = ref<string | null>(null)
  const searchQuery = ref('')
  const activeStatusFilters = ref<string[]>([])
  const activeGenreFilters = ref<number[]>([])
  const showFilters = ref(false)
  const currentPage = ref(1)
  const hasNextPage = ref(true)
  const ordering = ref('')
  
  // Фильтры статусов
  const statusFilters = [
    { value: 'ongoing', label: 'Онгоинг' },
    { value: 'finished', label: 'Завершён' },
    { value: 'announced', label: 'Анонсирован' }
  ]
  


  // Загрузка жанров
  const fetchGenres = async () => {
    try {
      const response = await apiClient.get('/anime/genres/')
      genresList.value = response.data
    } catch (err: any) {
      console.error('Ошибка загрузки жанров:', err)
    }
  }
  
  // Поиск
  const handleSearch = async () => {
    fetchAnime(1) // Перезагрузка с первой страницы с учетом search
  }

  // Сортировка
  const handleSort = async () => {
    fetchAnime(1) // Перезагрузка с первой страницы с учетом sorting
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

  // Фильтрация по жанрам
  const toggleGenreFilter = (genreId: number) => {
    const index = activeGenreFilters.value.indexOf(genreId)
    if (index === -1) {
      activeGenreFilters.value.push(genreId)
    } else {
      activeGenreFilters.value.splice(index, 1)
    }
  }

  // Очистка всех фильтров
  const clearFilters = () => {
    activeStatusFilters.value = []
    activeGenreFilters.value = []
    searchQuery.value = ''
    fetchAnime(1)
  }
  
  // Фильтрованные аниме
  const filteredAnime = computed(() => {
    let filtered = animeList.value

    if (activeStatusFilters.value.length > 0) {
      filtered = filtered.filter(item =>
        activeStatusFilters.value.includes(item.status)
      )
    }

    if (activeGenreFilters.value.length > 0) {
      filtered = filtered.filter(item =>
        item.genres.some((genre: any) => activeGenreFilters.value.includes(genre.id))
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
  // Загрузка аниме (с пагинацией)
  const fetchAnime = async (page = 1) => {
    if (page === 1) {
      loading.value = true
      animeList.value = []
      currentPage.value = 1
      hasNextPage.value = true
    } else {
      loadingMore.value = true
    }

    error.value = null

    try {
      const params: any = { page, page_size: 50 }

      if (searchQuery.value.trim()) {
        params.search = searchQuery.value
      }

      if (ordering.value) {
        params.ordering = ordering.value
      }

      const response = await apiClient.get('/anime/anime/', { params })

      if (page === 1) {
        animeList.value = response.data.results || response.data
      } else {
        animeList.value.push(...(response.data.results || response.data))
      }

      hasNextPage.value = !!response.data.next
      currentPage.value = page

    } catch (err: any) {
      error.value = err.message || 'Не удалось загрузить аниме'
      console.error('Ошибка загрузки аниме:', err)
    } finally {
      loading.value = false
      loadingMore.value = false
    }
  }

  // Загрузка следующей страницы
  const loadMoreAnime = async () => {
    if (hasNextPage.value && !loadingMore.value) {
      await fetchAnime(currentPage.value + 1)
    }
  }
  // Intersection Observer для infinite scroll
  const setupIntersectionObserver = () => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && hasNextPage.value && !loadingMore.value) {
            loadMoreAnime()
          }
        })
      },
      {
        rootMargin: '100px'
      }
    )

    nextTick(() => {
      const sentinel = document.querySelector('.loading-more') as Element
      if (sentinel) {
        observer.observe(sentinel)
      }
    })

    return observer
  }

  // Загрузка при монтировании
  onMounted(() => {
    fetchAnime()
    fetchGenres()
    setupIntersectionObserver()
  })
  </script>
  
  <style scoped>
  .anime-view {
    min-height: 100vh;
    background-color: #f9fafb;
  }
  .load-more-container {
    text-align: center;
    margin-top: 2rem;
  }

  .load-more-btn {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
  }
  .sort-box {
    margin-bottom: 1rem;
  }

  .sort-select {
    width: 100%;
    max-width: 300px;
    padding: 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    font-size: 1rem;
    outline: none;
    transition: border-color 0.2s;
  }

  .sort-select:focus {
    border-color: #3b82f6;
  }

  @media (max-width: 640px) {
    .sort-box {
      margin-bottom: 0.75rem;
    }

    .sort-select {
      max-width: 100%;
      padding: 0.625rem;
      font-size: 0.875rem;
    }
  }
  .loading-more {
    text-align: center;
    padding: 2rem;
    color: #6b7280;
  }

  @media (max-width: 640px) {
    .load-more-container {
      margin-top: 1.5rem;
    }

    .load-more-btn {
      padding: 0.625rem 1.25rem;
      font-size: 0.875rem;
    }
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

  .spinner.small {
    width: 24px;
    height: 24px;
    margin: 0 auto 0.5rem;
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
  
  /* Переключатель фильтров */
  .filters-toggle {
    margin-bottom: 1rem;
  }

  .toggle-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #f3f4f6;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    color: #4b5563;
    font-size: 0.875rem;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .toggle-btn:hover {
    background: #e5e7eb;
  }

  .toggle-icon {
    font-size: 0.75rem;
  }

  /* Фильтры */
  .filters {
    margin-bottom: 1.5rem;
  }

  .filter-group {
    margin-bottom: 1rem;
  }

  .filter-title {
    font-size: 1rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 0.5rem;
  }

  .filter-group .filters {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }

  .filter-actions {
    margin-top: 1rem;
    text-align: center;
  }

  .clear-btn {
    padding: 0.5rem 1rem;
    background: #dc2626;
    color: white;
    border: 1px solid #dc2626;
    border-radius: 0.375rem;
    font-size: 0.875rem;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .clear-btn:hover {
    background: #b91c1c;
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