<template>
  <div class="anime-card" @click="handleClick">
    <!-- Постер -->
    <div class="anime-poster">
      <img
        v-if="anime.poster_url"
        :src="anime.poster_url"
        :alt="anime.title_ru || anime.title_en"
        class="poster-image"
      />
      <div v-else class="poster-placeholder">🎌</div>
    </div>

    <!-- Информация -->
    <div class="anime-info">
      <h3 class="anime-title">{{ anime.title_ru || anime.title_en }}</h3>

      <div class="anime-meta">
        <span class="anime-year" v-if="anime.year">{{ anime.year }}</span>
        <span class="anime-episodes" v-if="anime.episodes">{{ anime.episodes }} эп.</span>
        <span :class="['anime-status', getStatusClass(anime.status)]">
          {{ getStatusText(anime.status) }}
        </span>
      </div>

      <p class="anime-description">{{ truncateDescription(anime.description) }}</p>

      <!-- Жанры -->
      <div class="anime-genres" v-if="anime.genres && anime.genres.length">
        <span
          v-for="genre in anime.genres.slice(0, 3)"
          :key="genre.id"
          class="genre-tag"
        >
          {{ genre.name }}
        </span>
        <span v-if="anime.genres.length > 3" class="genre-more">
          +{{ anime.genres.length - 3 }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
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
}

interface Props {
  anime: Anime
}

const props = defineProps<Props>()

const emit = defineEmits<{
  click: [anime: Anime]
}>()

// Обработчик клика
const handleClick = () => {
  emit('click', props.anime)
}

// Вспомогательные функции
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

const truncateDescription = (desc: string) => {
  if (!desc) return 'Описание отсутствует'
  return desc.length > 150 ? desc.substring(0, 150) + '...' : desc
}
</script>

<style scoped>
/* Карточка аниме */
.anime-card {
  background: white;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
  display: flex;
  flex-direction: column;
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
  overflow: hidden;
}

.poster-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.anime-card:hover .poster-image {
  transform: scale(1.05);
}

.poster-placeholder {
  font-size: 4rem;
  opacity: 0.8;
  color: white;
}

/* Информация об аниме */
.anime-info {
  padding: 1rem;
  flex: 1;
  display: flex;
  flex-direction: column;
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
  flex-wrap: wrap;
}

.anime-status {
  padding: 0.125rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
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
  background-color: #f0fdf4;
  color: #166534;
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
  flex: 1;
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
  white-space: nowrap;
}

.genre-more {
  font-size: 0.75rem;
  color: #9ca3af;
  align-self: center;
}

/* Responsive design */
@media (max-width: 640px) {
  .anime-card {
    margin-bottom: 1rem;
  }

  .anime-poster {
    height: 180px;
  }

  .anime-info {
    padding: 0.875rem;
  }

  .anime-title {
    font-size: 1rem;
  }

  .anime-meta {
    gap: 0.5rem;
    font-size: 0.8125rem;
  }

  .anime-description {
    font-size: 0.8125rem;
    -webkit-line-clamp: 2;
  }
}

@media (max-width: 480px) {
  .anime-poster {
    height: 160px;
  }

  .anime-info {
    padding: 0.75rem;
  }

  .anime-title {
    font-size: 0.95rem;
  }

  .anime-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.375rem;
  }

  .anime-status {
    align-self: flex-start;
  }
}

@media (min-width: 641px) and (max-width: 768px) {
  .anime-poster {
    height: 190px;
  }
}
</style>