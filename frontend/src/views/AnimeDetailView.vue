<template>
    <div class="anime-detail">
      <nav class="navbar">
        <div class="container">
          <div class="nav-left">
            <router-link to="/" class="logo">🎌 AnimeCore</router-link>
            <div class="nav-links">
              <router-link to="/" class="nav-link">Главная</router-link>
              <router-link to="/anime" class="nav-link">Аниме</router-link>
            </div>
          </div>
          <div class="nav-right">
            <router-link to="/login" class="btn btn-outline">Войти</router-link>
          </div>
        </div>
      </nav>
  
      <div class="container detail-content">
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>Загрузка информации об аниме...</p>
        </div>
  
        <div v-else-if="error" class="error-state">
          <p>Ошибка: {{ error }}</p>
          <router-link to="/anime" class="btn btn-primary">← Назад к списку</router-link>
        </div>
  
        <div v-else-if="anime" class="anime-detail-card">
          <!-- Заголовок и навигация -->
          <div class="detail-header">
            <router-link to="/anime" class="back-link">← Все аниме</router-link>
            <h1 class="anime-title">{{ anime.title_ru || anime.title_en }}</h1>
            <p class="anime-title-en" v-if="anime.title_en && anime.title_en !== anime.title_ru">
              {{ anime.title_en }}
            </p>
          </div>
  
          <!-- Основная информация -->
          <div class="anime-main-info">
            <!-- Постер -->
            <div class="anime-poster-large">
              <div class="poster-placeholder-large">🎌</div>
            </div>
  
            <!-- Детали -->
            <div class="anime-details">
              <div class="detail-row">
                <span class="detail-label">Год:</span>
                <span class="detail-value">{{ anime.year || 'Не указан' }}</span>
              </div>
              
              <div class="detail-row">
                <span class="detail-label">Статус:</span>
                <span :class="['detail-value', 'status-badge', getStatusClass(anime.status)]">
                  {{ getStatusText(anime.status) }}
                </span>
              </div>
              
              <div class="detail-row">
                <span class="detail-label">Эпизодов:</span>
                <span class="detail-value">{{ anime.episodes || 'Не указано' }}</span>
              </div>
  
              <!-- Жанры -->
              <div class="detail-row">
                <span class="detail-label">Жанры:</span>
                <div class="genres-list">
                  <span
                    v-for="genre in anime.genres"
                    :key="genre.id"
                    class="genre-tag-large"
                  >
                    {{ genre.name }}
                  </span>
                </div>
              </div>
  
              <!-- Действия -->
              <div class="action-buttons">
                <button class="btn btn-primary">
                  <span>+</span> Добавить в плейлист
                </button>
                <button class="btn btn-outline">
                  💬 Обсудить
                </button>
              </div>
            </div>
          </div>
  
          <!-- Описание -->
          <div class="anime-description-section">
            <h3>Описание</h3>
            <p class="anime-description-full">
              {{ anime.description || 'Описание отсутствует' }}
            </p>
          </div>
  
          <!-- Разделы -->
          <div class="anime-sections">
            <div class="section">
              <h3>Где смотреть?</h3>
              <p class="section-placeholder">Ссылки на просмотр появятся здесь</p>
            </div>
            
            <div class="section">
              <h3>Озвучки</h3>
              <p class="section-placeholder">Информация об озвучках появится здесь</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import apiClient from '@/api/client'
  
  const route = useRoute()
  const anime = ref<any>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)
  
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
  
  // Загрузка аниме
  const fetchAnime = async () => {
    loading.value = true
    error.value = null
    
    try {
      const animeId = route.params.id
      const response = await apiClient.get(`/anime/anime/${animeId}/`)
      anime.value = response.data
    } catch (err: any) {
      error.value = 'Не удалось загрузить информацию об аниме'
      console.error('Ошибка загрузки аниме:', err)
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    fetchAnime()
  })
  </script>
  
  <style scoped>
  .anime-detail {
    min-height: 100vh;
    background-color: #f9fafb;
  }
  
  .detail-content {
    padding: 2rem 1rem;
  }
  
  /* Заголовок */
  .detail-header {
    margin-bottom: 2rem;
  }
  
  .back-link {
    display: inline-block;
    color: #6b7280;
    text-decoration: none;
    font-size: 0.875rem;
    margin-bottom: 1rem;
  }
  
  .back-link:hover {
    color: #3b82f6;
  }
  
  .anime-title {
    font-size: 2rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 0.5rem;
  }
  
  .anime-title-en {
    font-size: 1.125rem;
    color: #6b7280;
    font-style: italic;
  }
  
  /* Основная информация */
  .anime-main-info {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 2rem;
    margin-bottom: 2rem;
    background: white;
    padding: 1.5rem;
    border-radius: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }
  
  @media (max-width: 768px) {
    .anime-main-info {
      grid-template-columns: 1fr;
    }
  }
  
  /* Постер */
  .anime-poster-large {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #93c5fd 0%, #3b82f6 100%);
    border-radius: 0.75rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .poster-placeholder-large {
    font-size: 6rem;
    opacity: 0.8;
  }
  
  /* Детали */
  .anime-details {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .detail-row {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .detail-label {
    font-weight: 500;
    color: #374151;
    min-width: 100px;
  }
  
  .detail-value {
    color: #4b5563;
  }
  
  .status-badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.875rem;
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
  
  /* Жанры */
  .genres-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .genre-tag-large {
    padding: 0.375rem 0.75rem;
    background-color: #f3f4f6;
    color: #4b5563;
    border-radius: 0.5rem;
    font-size: 0.875rem;
  }
  
  /* Кнопки действий */
  .action-buttons {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }
  
  .action-buttons .btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  /* Описание */
  .anime-description-section {
    background: white;
    padding: 1.5rem;
    border-radius: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    margin-bottom: 1.5rem;
  }
  
  .anime-description-section h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 1rem;
  }
  
  .anime-description-full {
    color: #4b5563;
    line-height: 1.6;
    white-space: pre-line;
  }
  
  /* Разделы */
  .anime-sections {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
  }
  
  @media (max-width: 768px) {
    .anime-sections {
      grid-template-columns: 1fr;
    }
  }
  
  .section {
    background: white;
    padding: 1.5rem;
    border-radius: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }
  
  .section h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 1rem;
  }
  
  .section-placeholder {
    color: #9ca3af;
    font-style: italic;
  }
  
  /* Состояния (совпадают с AnimeView) */
  .loading-state, .error-state {
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
  
  .error-state p {
    color: #dc2626;
    margin-bottom: 1rem;
  }
  </style>