<template>
    <div class="anime-detail">
      <!-- Modal for adding/editing dubs -->
      <AddDubModal
        :show="showAddDubModal"
        :anime-id="anime?.id || 0"
        :editing-dub="editingDub"
        @close="showAddDubModal = false"
        @dub-added="onDubAdded"
      />
      <NavBar />
  
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
              <img 
                v-if="anime.poster_url" 
                :src="anime.poster_url" 
                :alt="anime.title_ru || anime.title_en"
                class="poster-image"
              />
              <div v-else class="poster-placeholder-large">🎌</div>
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
  
              <!-- Рейтинг -->
              <div class="detail-row" v-if="anime.score">
                <span class="detail-label">Рейтинг:</span>
                <span class="detail-value rating-score">⭐ {{ anime.score }}</span>
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
            <!-- Где смотреть -->
            <div class="section">
              <h3>📺 Где смотреть?</h3>
              <p class="section-placeholder" v-if="!anime.playlists || anime.playlists.length === 0">
                Плейлисты с этим аниме появятся здесь
              </p>
              <div v-else class="playlists-list">
                <div 
                  v-for="playlist in anime.playlists" 
                  :key="playlist.id"
                  class="playlist-card"
                >
                  <span class="playlist-title">{{ playlist.title }}</span>
                  <span class="playlist-author">@{{ playlist.user?.username }}</span>
                </div>
              </div>
            </div>
            
            <!-- Озвучки -->
            <div class="section dubs-section">
              <DubsList
                :dubs="formattedDubs"
                :loading="loadingDubs"
                :can-add-dub="true"
                :anime-id="anime?.id"
                @add-dub="addDub"
                @select-dub="selectDub"
                @play-dub="playDub"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  // docker-compose up --build frontend
  import { ref, computed, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import apiClient from '@/api/client'
  import AddDubModal from '@/components/AddDubModal.vue'
  import DubsList from '@/components/DubsList.vue'
  import NavBar from '@/components/NavBar.vue'
  
  interface Dub {
    id: number
    group: {
      id: number
      name: string
      slug: string
      logo_url: string | null
    } | null
    dub_type: string
    dub_type_display?: string
    quality: string
    episodes_done: number
    total_episodes: number | null
    is_complete: boolean
    average_rating: number | null
    ratings_count: number
    external_url: string | null
    created_by?: {
      id: number
      username: string
    } | null
  }
  
  interface Playlist {
    id: number
    title: string
    user?: {
      username: string
    }
  }
  
  interface Genre {
    id: number
    name: string
    slug: string
  }
  
  interface Anime {
    id: number
    title_ru: string
    title_en: string
    title_jp: string
    description: string
    year: number | null
    status: string
    episodes: number | null
    score: number | null
    poster_url: string | null
    genres: Genre[]
    playlists?: Playlist[]
  }

  interface DubGroup {
    id: number
    name: string
    slug: string
    description: string
    logo_url: string | null
    works_count: number
    followers_count: number
    status: string
    is_verified: boolean
    has_dub: boolean
    dub_info: Dub
  }
  
  const route = useRoute()
  const anime = ref<Anime | null>(null)
  const dubs = ref<Dub[]>([])
  const dubGroups = ref<DubGroup[]>([])
  const showAddDubModal = ref(false)
  const editingDub = ref<Dub | null>(null)
  const currentUser = ref<{id: number, username: string} | null>(null) // In real app, get from auth store
  const loading = ref(true)
  const loadingDubs = ref(false)
  const error = ref<string | null>(null)
  const dubsError = ref<string | null>(null)

  // Преобразование данных для DubsList компонента
  const formattedDubs = computed(() => {
    return dubs.value.map(dub => ({
      id: dub.id,
      studio: dub.group?.name || 'Неизвестная студия',
      logo: dub.group?.logo_url || null,
      type: dub.dub_type,
      voiceActors: [], // Пока пустой массив, можем добавить позже если нужно
      verified: false, // Пока false, можем добавить позже
      is_official: dub.dub_type === 'official',
      latestEpisode: dub.episodes_done?.toString() || null,
      qualityRating: dub.average_rating || 0,
      external_url: dub.external_url,
      episodes_done: dub.episodes_done,
      total_episodes: dub.total_episodes,
      is_complete: dub.is_complete
    }))
  })
  
  const getStatusText = (status: string) => {
    const map: Record<string, string> = {
      'ongoing': 'Онгоинг',
      'finished': 'Завершён',
      'announced': 'Анонсирован',
      'released': 'Вышедший'
    }
    return map[status] || status
  }
  
  const getStatusClass = (status: string) => {
    const map: Record<string, string> = {
      'ongoing': 'status-ongoing',
      'finished': 'status-finished',
      'announced': 'status-announced',
      'released': 'status-released'
    }
    return map[status] || ''
  }
  
  const getInitials = (name: string | undefined | null) => {
    if (!name) return '?'
    return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2)
  }
  
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
  
  const fetchDubs = async () => {
    if (!anime.value) return

    loadingDubs.value = true
    try {
      const animeId = anime.value.id
      const response = await apiClient.get(`/dubs/anime/${animeId}/dubs/`)
      dubs.value = response.data
    } catch (err: any) {
      dubsError.value = 'Не удалось загрузить озвучки'
      console.error('Ошибка загрузки озвучек:', err)
    } finally {
      loadingDubs.value = false
    }
  }

  const fetchDubGroups = async () => {
    if (!anime.value) return

    loadingDubs.value = true
    try {
      const animeId = anime.value.id
      const response = await apiClient.get(`/dubs/anime/${animeId}/groups/`)
      dubGroups.value = response.data
    } catch (err: any) {
      dubsError.value = 'Не удалось загрузить группы озвучки'
      console.error('Ошибка загрузки групп озвучки:', err)
    } finally {
      loadingDubs.value = false
    }
  }
  
  const addDub = () => {
    showAddDubModal.value = true
  }

  const canEditDub = (dub: Dub) => {
    return currentUser.value && dub.created_by && dub.created_by.id === currentUser.value.id
  }

  const editDub = (dub: Dub) => {
    editingDub.value = dub
    showAddDubModal.value = true
  }

  const selectDub = (dub: Dub) => {
    // Обработка выбора озвучки (показать детали)
    console.log('Selected dub:', dub)
  }

  const playDub = (dub: Dub) => {
    // Обработка просмотра озвучки
    if (dub.external_url) {
      window.open(dub.external_url, '_blank')
    } else {
      console.log('No external URL for dub:', dub)
    }
  }

  const onDubAdded = () => {
    // Перезагрузить список озвучек
    fetchDubs()
    editingDub.value = null
  }
  
  onMounted(async () => {
    await fetchAnime()
    if (anime.value) {
      await fetchDubs()
    }
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
    .detail-content {
      padding: 1rem 0.5rem;
    }

    .detail-header {
      margin-bottom: 1.5rem;
    }

    .anime-title {
      font-size: 1.75rem;
    }

    .anime-title-en {
      font-size: 1rem;
    }

    .anime-main-info {
      grid-template-columns: 1fr;
      gap: 1.5rem;
      padding: 1rem;
      margin-bottom: 1.5rem;
    }

    .anime-poster-large {
      max-width: 250px;
      margin: 0 auto;
    }

    .anime-details {
      gap: 0.75rem;
    }

    .detail-row {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.25rem;
    }

    .detail-label {
      min-width: auto;
      font-weight: 600;
    }

    .genres-list {
      flex-wrap: wrap;
      gap: 0.5rem;
    }

    .genre-tag-large {
      padding: 0.25rem 0.5rem;
      font-size: 0.75rem;
    }

    .action-buttons {
      flex-direction: column;
      gap: 0.75rem;
    }

    .action-buttons .btn {
      width: 100%;
      text-align: center;
    }

    .anime-description-section {
      padding: 1rem;
    }

    .section {
      padding: 1rem;
    }
  }

  @media (max-width: 480px) {
    .detail-content {
      padding: 0.5rem 0.25rem;
    }

    .anime-title {
      font-size: 1.5rem;
    }

    .anime-main-info {
      padding: 0.75rem;
      border-radius: 0.75rem;
    }

    .anime-poster-large {
      height: 200px;
      max-width: 200px;
    }

    .poster-placeholder-large {
      font-size: 4rem;
    }

    .anime-details {
      gap: 0.75rem;
    }

    .anime-description-section,
    .section {
      padding: 0.75rem;
      border-radius: 0.75rem;
    }

    .section h3 {
      font-size: 1.125rem;
    }

    .btn {
      padding: 0.5rem 0.75rem;
      font-size: 0.75rem;
    }

    .playlists-list,
    .dub-groups-list {
      gap: 0.5rem;
    }

    .playlist-card,
    .dub-group-card {
      padding: 0.75rem;
    }
  }
  
  /* Постер */
  .anime-poster-large {
    width: 100%;
    aspect-ratio: 2/3;
    background: linear-gradient(135deg, #93c5fd 0%, #3b82f6 100%);
    border-radius: 0.75rem;
    overflow: hidden;
  }
  
  .poster-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .poster-placeholder-large {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
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
  
  .rating-score {
    color: #f59e0b;
    font-weight: 600;
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
  
  .status-released {
    background-color: #f3f4f6;
    color: #374151;
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
  
  @media (max-width: 1024px) {
    .anime-sections {
      grid-template-columns: 1fr;
      gap: 1rem;
    }
  }

  @media (min-width: 769px) and (max-width: 1024px) {
    .detail-content {
      padding: 1.5rem 1rem;
    }

    .anime-main-info {
      gap: 1.5rem;
      padding: 1.25rem;
    }

    .anime-poster-large {
      max-width: 300px;
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

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
  }

  .empty-subtitle {
    color: #6b7280;
    font-size: 0.875rem;
    margin-top: 0.5rem;
  }
  
  .section-placeholder {
    color: #9ca3af;
    font-style: italic;
  }
  
  /* Плейлисты */
  .playlists-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  
  .playlist-card {
    padding: 0.75rem;
    background: #f3f4f6;
    border-radius: 0.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .playlist-title {
    font-weight: 500;
    color: #1f2937;
  }
  
  .playlist-author {
    font-size: 0.875rem;
    color: #6b7280;
  }
  
  /* Состояния */
  .loading-inline, .error-inline, .empty-inline {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    padding: 1.5rem;
    color: #6b7280;
  }
  
  .spinner-small {
    width: 24px;
    height: 24px;
    border: 2px solid #e5e7eb;
    border-top-color: #3b82f6;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  .error-inline {
    color: #dc2626;
  }
  
  /* Группы озвучки */
  .dub-groups-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .dub-group-card {
    padding: 1rem;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    transition: all 0.2s;
  }

  .dub-group-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
  }

  .dub-group-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.75rem;
  }

  .dub-group-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }

  .dub-group-logo {
    width: 40px;
    height: 40px;
    border-radius: 0.5rem;
    object-fit: cover;
  }

  .dub-group-logo-placeholder {
    width: 40px;
    height: 40px;
    border-radius: 0.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.875rem;
  }

  .dub-group-details {
    display: flex;
    flex-direction: column;
  }

  .dub-group-name {
    font-weight: 600;
    color: #1f2937;
  }

  .dub-group-works {
    font-size: 0.75rem;
    color: #6b7280;
  }

  .dub-group-status .status-badge {
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
    font-size: 0.75rem;
    font-weight: 500;
  }

  .status-badge.available {
    background: #dcfce7;
    color: #166534;
  }

  .status-badge.unavailable {
    background: #f3f4f6;
    color: #374151;
  }

  .dub-info {
    border-top: 1px solid #e2e8f0;
    padding-top: 0.75rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  /* Озвучки */
  .dubs-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .dub-card {
    padding: 1rem;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    transition: all 0.2s;
  }
  
  .dub-card:hover {
    border-color: #3b82f6;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
  }
  
  .dub-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 0.75rem;
  }
  
  .dub-group-info {
    display: flex;
    align-items: center;
    gap: 0.75rem;
  }
  
  .dub-group-logo {
    width: 40px;
    height: 40px;
    border-radius: 0.5rem;
    object-fit: cover;
  }
  
  .dub-group-logo-placeholder {
    width: 40px;
    height: 40px;
    border-radius: 0.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.875rem;
  }
  
  .dub-group-details {
    display: flex;
    flex-direction: column;
  }
  
  .dub-group-name {
    font-weight: 600;
    color: #1f2937;
  }
  
  .dub-type {
    font-size: 0.75rem;
    color: #6b7280;
    text-transform: capitalize;
  }
  
  .dub-quality {
    display: flex;
    gap: 0.5rem;
  }
  
  .quality-badge {
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
    font-size: 0.75rem;
    font-weight: 500;
  }
  
  .quality-badge.complete {
    background: #dcfce7;
    color: #166534;
  }
  
  .quality-badge.ongoing {
    background: #fef3c7;
    color: #92400e;
  }
  
  .dub-stats {
    display: flex;
    gap: 1rem;
    margin-bottom: 0.75rem;
    font-size: 0.875rem;
    color: #6b7280;
  }
  
  .dub-rating {
    color: #f59e0b;
    font-weight: 500;
  }
  
  .dub-actions {
    display: flex;
    gap: 0.5rem;
  }
  
  .btn-sm {
    padding: 0.375rem 0.75rem;
    font-size: 0.875rem;
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
  
  /* Кнопки */
  .btn {
    padding: 0.625rem 1.25rem;
    border-radius: 0.5rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    font-size: 0.875rem;
  }
  
  .btn-primary {
    background: #3b82f6;
    color: white;
  }
  
  .btn-primary:hover {
    background: #2563eb;
  }
  
  .btn-outline {
    background: transparent;
    color: #3b82f6;
    border: 1px solid #3b82f6;
  }
  
  .btn-outline:hover {
    background: #eff6ff;
  }
  </style>