<template>
    <div class="dubs-section">
      <h3 class="section-title">
        Озвучки
        <span v-if="dubs.length > 0" class="count-badge">{{ dubs.length }}</span>
      </h3>
      
      <!-- Состояние загрузки -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Загрузка озвучек...</p>
      </div>
      
      <!-- Состояние ошибки -->
      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <button @click="fetchDubs" class="retry-btn">Повторить</button>
      </div>
      
      <!-- Нет озвучек -->
      <div v-else-if="dubs.length === 0" class="empty-state">
        <p>Пока нет информации об озвучках</p>
        <button v-if="isAuthenticated" @click="suggestDub" class="suggest-btn">
          Предложить озвучку
        </button>
      </div>
      
      <!-- Список озвучек -->
      <div v-else class="dubs-list">
        <div 
          v-for="dub in sortedDubs" 
          :key="dub.id" 
          class="dub-card"
          :class="{ 'complete': dub.is_complete, 'abandoned': dub.is_abandoned }"
        >
          <!-- Группа озвучки -->
          <div class="dub-group">
            <div class="group-logo">
              <img 
                v-if="dub.group.logo_url" 
                :src="dub.group.logo_url" 
                :alt="dub.group.name"
                @error="handleImageError"
              />
              <div v-else class="logo-placeholder">
                {{ dub.group.name.charAt(0) }}
              </div>
            </div>
            <div class="group-info">
              <h4 class="group-name">{{ dub.group.name }}</h4>
              <div class="dub-meta">
                <span class="dub-type">{{ getDubType(dub.dub_type) }}</span>
                <span class="quality" :class="getQualityClass(dub.quality)">
                  {{ getQualityText(dub.quality) }}
                </span>
              </div>
            </div>
          </div>
          
          <!-- Прогресс озвучки -->
          <div class="dub-progress">
            <div class="progress-info">
              <span class="episodes">
                {{ dub.episodes_done }} / {{ dub.total_episodes || '?' }} эп.
              </span>
              <span v-if="dub.is_complete" class="status-badge complete">Завершено</span>
              <span v-else-if="dub.is_abandoned" class="status-badge abandoned">Заброшено</span>
              <span v-else class="status-badge ongoing">В процессе</span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: getProgressPercent(dub) + '%' }"
                :class="getProgressClass(dub)"
              ></div>
            </div>
          </div>
          
          <!-- Рейтинг -->
          <div v-if="dub.average_rating > 0" class="dub-rating">
            <div class="stars">
              <span 
                v-for="n in 5" 
                :key="n"
                class="star"
                :class="{ filled: n <= Math.round(dub.average_rating / 2) }"
              >
                ★
              </span>
            </div>
            <span class="rating-value">{{ dub.average_rating.toFixed(1) }}</span>
            <span class="rating-count">({{ dub.ratings_count }})</span>
          </div>
          
          <!-- Действия -->
          <div class="dub-actions">
            <button 
              v-if="dub.external_url" 
              @click="openDub(dub.external_url)"
              class="watch-btn"
            >
              Смотреть
            </button>
            <button 
              @click="rateDub(dub)" 
              class="rate-btn"
              :disabled="!isAuthenticated"
            >
              Оценить
            </button>
            <button 
              @click="showDubDetails(dub)" 
              class="details-btn"
            >
              Подробнее
            </button>
          </div>
          
          <!-- Быстрые ссылки -->
          <div v-if="dub.links && dub.links.length > 0" class="quick-links">
            <button 
              v-for="link in dub.links.slice(0, 3)" 
              :key="link.id"
              @click="openLink(link.url)"
              class="link-btn"
              :title="`${link.source} - ${link.quality || 'качество'}`"
            >
              {{ getSourceIcon(link.source) }} 
              <span v-if="link.episode">{{ link.episode }} эп.</span>
              <span v-else>{{ getSourceName(link.source) }}</span>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Кнопка добавления -->
      <div v-if="isAuthenticated && dubs.length > 0" class="add-dub-section">
        <button @click="suggestDub" class="add-dub-btn">
          + Добавить другую озвучку
        </button>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, computed, onMounted } from 'vue'
  import apiClient from '@/api/client'
  import { useAuthStore } from '@/stores/auth'
  
  const props = defineProps<{
    animeId: number
  }>()
  
  const emit = defineEmits(['suggest-dub', 'rate-dub', 'show-details'])
  
  const authStore = useAuthStore()
  const dubs = ref<any[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  
  // Получение озвучек
  const fetchDubs = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await apiClient.get(`/dubs/anime/${props.animeId}/dubs/`)
      dubs.value = response.data
    } catch (err: any) {
      error.value = 'Не удалось загрузить озвучки'
      console.error('Ошибка загрузки озвучек:', err)
    } finally {
      loading.value = false
    }
  }
  
  // Сортировка озвучек
  const sortedDubs = computed(() => {
    return [...dubs.value].sort((a, b) => {
      // Сначала завершённые
      if (a.is_complete && !b.is_complete) return -1
      if (!a.is_complete && b.is_complete) return 1
      
      // Потом по рейтингу
      if (a.average_rating > b.average_rating) return -1
      if (a.average_rating < b.average_rating) return 1
      
      // Потом по количеству эпизодов
      if (a.episodes_done > b.episodes_done) return -1
      if (a.episodes_done < b.episodes_done) return 1
      
      return 0
    })
  })
  
  // Вспомогательные функции
  const getDubType = (type: string) => {
    const types: Record<string, string> = {
      'full': 'Полная озвучка',
      'subtitles': 'Субтитры',
      'partial': 'Частичная',
      'voiceover': 'Закадровый'
    }
    return types[type] || type
  }
  
  const getQualityText = (quality: string) => {
    const qualities: Record<string, string> = {
      'low': 'Низкое',
      'medium': 'Среднее',
      'high': 'Высокое',
      'excellent': 'Отличное',
      'unknown': 'Неизвестно'
    }
    return qualities[quality] || quality
  }
  
  const getQualityClass = (quality: string) => {
    const classes: Record<string, string> = {
      'low': 'quality-low',
      'medium': 'quality-medium',
      'high': 'quality-high',
      'excellent': 'quality-excellent'
    }
    return classes[quality] || ''
  }
  
  const getProgressPercent = (dub: any) => {
    if (!dub.total_episodes || dub.total_episodes === 0) return 0
    return Math.min(100, (dub.episodes_done / dub.total_episodes) * 100)
  }
  
  const getProgressClass = (dub: any) => {
    if (dub.is_complete) return 'progress-complete'
    if (dub.is_abandoned) return 'progress-abandoned'
    if (dub.episodes_done > 0) return 'progress-started'
    return 'progress-not-started'
  }
  
  const getSourceIcon = (source: string) => {
    const icons: Record<string, string> = {
      'jutsu': '🎬',
      'animego': '📺',
      'animedia': '🎙️',
      'anime365': '📱',
      'other': '🔗'
    }
    return icons[source] || '🔗'
  }
  
  const getSourceName = (source: string) => {
    const names: Record<string, string> = {
      'jutsu': 'Jut.su',
      'animego': 'AnimeGo',
      'animedia': 'Animedia',
      'anime365': 'Anime365',
      'other': 'Ссылка'
    }
    return names[source] || source
  }
  
  // Обработчики действий
  const openDub = (url: string) => {
    window.open(url, '_blank', 'noopener,noreferrer')
  }
  
  const openLink = (url: string) => {
    window.open(url, '_blank', 'noopener,noreferrer')
  }
  
  const rateDub = (dub: any) => {
    emit('rate-dub', dub)
  }
  
  const showDubDetails = (dub: any) => {
    emit('show-details', dub)
  }
  
  const suggestDub = () => {
    emit('suggest-dub', props.animeId)
  }
  
  const handleImageError = (event: Event) => {
    const img = event.target as HTMLImageElement
    img.style.display = 'none'
    const placeholder = img.parentElement?.querySelector('.logo-placeholder')
    if (placeholder) {
      placeholder.style.display = 'flex'
    }
  }
  
  // Загрузка при монтировании
  onMounted(() => {
    fetchDubs()
  })
  </script>
  
  <style scoped>
  .dubs-section {
    margin-top: 2rem;
    padding: 1.5rem;
    background: #ffffff;
    border-radius: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }
  
  .section-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1f2937;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .count-badge {
    background-color: #3b82f6;
    color: white;
    font-size: 0.75rem;
    padding: 0.125rem 0.5rem;
   