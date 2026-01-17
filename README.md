# 🎌 AnimeCore

**Социальная сеть для анимешников** - платформа, объединяющая поиск аниме, создание плейлистов, озвучки и сообщество.

[![Django](https://img.shields.io/badge/Django-4.2.10-green.svg)](https://djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.3.8-green.svg)](https://vuejs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue.svg)](https://docker.com/)

---

## 📋 Оглавление
- [🎯 Идея проекта](#-идея-проекта)
- [✨ Возможности](#-возможности)
- [🏗️ Архитектура](#️-архитектура)
- [📊 Модели данных](#-модели-данных)
- [🔧 Установка и запуск](#-установка-и-запуск)
- [🚀 API документация](#-api-документация)
- [📱 Фронтенд структура](#-фронтенд-структура)
- [🎨 Дизайн и UX](#-дизайн-и-ux)
- [🔒 Безопасность](#-безопасность)
- [📈 Масштабируемость](#-масштабируемость)
- [🗺️ Roadmap](#️-roadmap)

---

## 🎯 Идея проекта

### Проблема
Русскоязычные анимешники разбрасаны по десяткам ресурсов:
- **Shikimori/MyAnimeList** - списки просмотренного
- **Jut.su/AnimeGo** - просмотр аниме
- **VK/Telegram** - озвучки и обсуждения
- **YouTube** - обзоры и Shorts

**Нет единой платформы**, где можно собрать всё в одном месте.

### Решение
**AnimeCore** - экосистема для анимешников, объединяющая:

🎬 **Просмотр аниме** - легальные и нелегальные источники
📋 **Плейлисты** - умные коллекции с живыми ссылками
🎙️ **Озвучки** - база групп и актёров
👥 **Сообщество** - группы, комментарии, Reactor
⚖️ **Модерация** - жалобы и верификация контента

### Целевая аудитория
- Анимешники 14-35 лет
- Озвучки и фан-субберы
- Российское и СНГ сообщество
- Энтузиасты аниме-культуры

---

## ✨ Возможности

### 🎬 Для зрителей
- **Поиск аниме** - по названию, жанрам, годам
- **Создание плейлистов** - личные коллекции с ссылками
- **Озвучки** - сравнение и выбор озвучек
- **Сообщество** - группы по интересам
- **Reactor** - Shorts видео об аниме

### 🎙️ Для озвучек
- **Профили групп** - портфолио и контакты
- **Верификация** - подтверждение официальности
- **Статистика** - просмотры и рейтинги
- **Монетизация** - премиум размещение

### 👥 Социальные фичи
- **Комментарии** - к аниме, плейлистам, видео
- **Группы** - сообщества по жанрам/студиям
- **Уведомления** - активность в сообществе
- **Репутация** - рейтинг пользователей

### ⚖️ Модерация
- **Жалобы** - система举报 нарушений
- **Верификация** - проверка контента
- **Автомодерация** - фильтры запрещённого контента
- **Админ-панель** - управление платформой

---

## 🏗️ Архитектура

### Backend Stack
```
🐍 Django 4.2.10 + Django REST Framework
🗄️ PostgreSQL 15 + Redis 7
🔄 Celery + RabbitMQ (фоновые задачи)
📁 MinIO (хранение медиа)
🚀 Gunicorn + Nginx (продакшен)
🐳 Docker + Docker Compose
```

### Frontend Stack
```
🎨 Vue.js 3 + TypeScript
🎭 Tailwind CSS + Headless UI
🔄 Pinia (стейт-менеджмент)
🛣️ Vue Router 4
📡 Axios (HTTP клиент)
🎬 HLS.js + Video.js (видео-плеер)
```

### Инфраструктура
```
🌐 Vercel (фронтенд + CDN)
🖥️ VPS Hetzner/Timeweb (бэкенд)
🗄️ PostgreSQL + Redis (данные)
📦 MinIO S3 (файлы)
🔐 Let's Encrypt (SSL)
📊 Sentry (мониторинг ошибок)
```

### Архитектурная диаграмма

```
┌─────────────────────────────────────┐
│              FRONTEND               │
│  ┌─────────────┬─────────────┐      │
│  │   Vue.js    │   Pinia     │      │
│  │   SPA       │   Store     │      │
│  └─────────────┴─────────────┘      │
│  ┌─────────────────────────────────┐ │
│  │         Vercel CDN              │ │
│  └─────────────────────────────────┘ │
└──────────────────▲───────────────────┘
                   │ HTTPS/API
┌──────────────────▼───────────────────┐
│              BACKEND                 │
│  ┌─────────────┬─────────────┐      │
│  │   Django    │   DRF       │      │
│  │   REST API  │   JWT Auth  │      │
│  └─────────────┴─────────────┘      │
│  ┌─────────────────────────────────┐ │
│  │     PostgreSQL + Redis          │ │
│  └─────────────────────────────────┘ │
│  ┌─────────────────────────────────┐ │
│  │     Celery + MinIO              │ │
│  └─────────────────────────────────┘ │
└─────────────────────────────────────┘
```

---

## 📊 Модели данных

### 🧑‍💼 User (Пользователь)
```python
class User(AbstractUser):
    avatar = models.ImageField()
    bio = models.TextField()
    email_verified = models.BooleanField()
    phone_number = models.CharField()
    reputation = models.IntegerField()
```

### 🎬 Anime (Аниме)
```python
class Anime(models.Model):
    title_ru = models.CharField()
    title_en = models.CharField()
    poster_url = models.URLField()
    description = models.TextField()
    year = models.IntegerField()
    status = models.CharField()  # ongoing, finished
    episodes = models.IntegerField()
    genres = models.ManyToManyField(Genre)
```

### 📋 Playlist (Плейлист)
```python
class Playlist(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField()
    description = models.TextField()
    is_public = models.BooleanField()
    created_at = models.DateTimeField()
```

### 🎙️ DubGroup (Группа озвучки)
```python
class DubGroup(models.Model):
    name = models.CharField()
    description = models.TextField()
    logo_url = models.URLField()
    is_verified = models.BooleanField()
    rating = models.FloatField()
    works_count = models.IntegerField()
```

### 👥 Group (Сообщество)
```python
class Group(models.Model):
    name = models.CharField()
    description = models.TextField()
    creator = models.ForeignKey(User)
    is_private = models.BooleanField()
    members_count = models.IntegerField()
    moderators = models.ManyToManyField(User)
```

### 📹 ReactorPost (Shorts видео)
```python
class ReactorPost(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField()
    video_file = models.FileField()
    thumbnail_file = models.ImageField()
    anime_tags = models.ManyToManyField(Anime)
    views_count = models.IntegerField()
    likes_count = models.IntegerField()
    comments_count = models.IntegerField()
```

### 💬 Comment (Комментарии - полиморфная)
```python
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    author = models.ForeignKey(User)
    text = models.TextField()
    parent = models.ForeignKey('self', null=True)  # replies
```

### ⚠️ Complaint (Жалобы)
```python
class Complaint(models.Model):
    content_type = models.ForeignKey(ContentType)  # polymorphic
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    complainant = models.ForeignKey(User)
    reason = models.CharField()  # spam, copyright, etc.
    status = models.CharField()  # pending, resolved
```

### 🔔 Notification (Уведомления)
```python
class Notification(models.Model):
    user = models.ForeignKey(User)
    type = models.CharField()  # comment, like, follow
    title = models.CharField()
    content = models.TextField()
    is_read = models.BooleanField()
```

---

## 🔧 Установка и запуск

### Требования
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL (или использовать Docker)

### Быстрый старт
```bash
# Клонирование
git clone https://github.com/yourusername/animecore.git
cd animecore

# Запуск через Docker
cd backend
docker-compose up -d

# Или ручной запуск
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Фронтенд
cd ../frontend
npm install
npm run dev
```

### Доступ
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000/api/
- **Admin:** http://localhost:8000/admin/
- **Статус:** http://localhost:8000/api/status/

### Переменные окружения
```bash
# backend/.env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost:5432/animecore
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-secret

# Email
EMAIL_HOST=smtp.yandex.ru
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=app-password
```

---

## 🚀 API документация

### Базовые endpoints
```
GET  /api/status/          # Статус системы
GET  /api/anime/           # Список аниме
POST /api/anime/           # Создать аниме (admin)
GET  /api/anime/{id}/      # Детали аниме

GET  /api/playlists/       # Плейлисты пользователя
POST /api/playlists/       # Создать плейлист
GET  /api/playlists/{id}/  # Детали плейлиста
PUT  /api/playlists/{id}/  # Обновить плейлист
DELETE /api/playlists/{id}/ # Удалить плейлист

GET  /api/dubs/            # Группы озвучек
GET  /api/dubs/{id}/       # Детали группы
```

### Аутентификация
```
POST /api/auth/login/      # Вход
POST /api/auth/register/   # Регистрация
POST /api/auth/refresh/    # Обновить токен
GET  /api/auth/user/       # Текущий пользователь
```

### Социальные фичи
```
GET  /api/social/comments/?content_type=anime&object_id=123
POST /api/social/comments/  # Создать комментарий

GET  /api/social/groups/   # Список групп
POST /api/social/groups/   # Создать группу
GET  /api/social/groups/{id}/members/  # Участники группы
```

### Reactor (Shorts)
```
GET  /api/reactor/posts/   # Список видео
POST /api/reactor/posts/   # Загрузить видео
GET  /api/reactor/posts/{id}/  # Детали видео
POST /api/reactor/posts/{id}/like/  # Лайк
```

### Модерация
```
GET  /api/notifications/complaints/  # Жалобы
POST /api/notifications/complaints/  # Создать жалобу
PUT  /api/notifications/complaints/{id}/  # Обновить статус

GET  /api/notifications/   # Уведомления пользователя
PUT  /api/notifications/{id}/read/  # Пометить как прочитанное
```

### Примеры запросов

#### Создание плейлиста
```bash
curl -X POST http://localhost:8000/api/playlists/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Мои любимые тайтлы",
    "description": "Коллекция лучших аниме",
    "is_public": true
  }'
```

#### Добавление аниме в плейлист
```bash
curl -X POST http://localhost:8000/api/playlists/1/add_item/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "anime": 123,
    "source_url": "https://jut.su/example/",
    "episode_number": 1,
    "dub_studio": 5
  }'
```

---

## 📱 Фронтенд структура

### Страницы (Views)
```
/ - Главная страница
/anime - Список аниме с фильтрами
/anime/:id - Детали аниме
/playlists - Мои плейлисты
/playlists/create - Создать плейлист
/playlists/:id - Просмотр плейлиста
/playlists/:id/edit - Редактировать плейлист
/groups - Список групп
/groups/create - Создать группу
/groups/:id - Страница группы
/reactor - Лента Shorts
/reactor/upload - Загрузить видео
/profile - Мой профиль
/profile/edit - Редактировать профиль
/login - Вход
/register - Регистрация
```

### Компоненты
```
NavBar.vue - Навигация
AnimeCard.vue - Карточка аниме
PlaylistCard.vue - Карточка плейлиста
CommentThread.vue - Дерево комментариев
VideoPlayer.vue - HLS плеер
SearchBar.vue - Поиск с автодополнением
GenreFilter.vue - Фильтр по жанрам
NotificationList.vue - Список уведомлений
ComplaintModal.vue - Форма жалобы
AddToPlaylistModal.vue - Быстрое добавление аниме
```

### Pinia Stores
```
auth.ts - Аутентификация пользователя
anime.ts - Управление аниме (кеш, поиск)
playlists.ts - Плейлисты и элементы
groups.ts - Группы и членство
reactor.ts - Shorts видео
notifications.ts - Уведомления
search.ts - Глобальный поиск
```

### Роутинг
```typescript
const routes = [
  { path: '/', component: HomeView },
  { path: '/anime', component: AnimeView },
  {
    path: '/anime/:id',
    component: AnimeDetailView,
    props: true
  },
  // ... другие маршруты
]
```

---

## 🎨 Дизайн и UX

### Цветовая схема
```css
/* Темная тема для ночных просмотров */
--primary: #0ea5e9;      /* Синий */
--secondary: #8b5cf6;    /* Фиолетовый */
--accent: #ff6bc9;       /* Розовый */
--background: #0f172a;   /* Тёмно-синий */
--surface: #1e293b;      /* Серый */
--text: #f8fafc;         /* Белый */
```

### Адаптивность
- **Мобильный first:** 320px - 768px
- **Планшет:** 768px - 1024px
- **Десктоп:** 1024px+

### Ключевые UX паттерны
- **Бесконечная прокрутка** в лентах
- **Pull-to-refresh** на мобильных
- **Swipe gestures** для навигации
- **Progressive disclosure** для форм
- **Skeleton loading** во время загрузки
- **Toast notifications** для фидбека

### Анимации
- **Fade-in** для новых элементов
- **Slide transitions** между страницами
- **Loading spinners** для асинхронных операций
- **Hover эффекты** на интерактивных элементах

---

## 🔒 Безопасность

### Аутентификация
- JWT токены с refresh механизмом
- CSRF защита для форм
- Rate limiting (100 req/min)
- Session management

### Авторизация
- Role-based access (User, Moderator, Admin)
- Object-level permissions
- API key для внешних интеграций
- CORS политика

### Данные
- Шифрование чувствительных данных
- SQL injection защита через ORM
- XSS фильтрация в контенте
- File upload validation

### Модерация
- Content filtering (запрещённые слова)
- Image moderation API
- User reputation system
- Automated spam detection

### Мониторинг
- Error tracking (Sentry)
- Performance monitoring
- Security audit logs
- Backup и recovery

---

## 📈 Масштабируемость

### Горизонтальное масштабирование
- **Load balancer** (Nginx)
- **Database sharding**
- **Redis clustering**
- **CDN** для медиа файлов

### Кэширование
- **Redis** для API responses
- **CDN** для статических файлов
- **Database query caching**
- **Page caching** для публичных страниц

### Оптимизации
- **Lazy loading** изображений
- **Code splitting** Vue.js
- **Database indexing**
- **API pagination**

### Производительность
- **Response time:** <200ms для API
- **Time to interactive:** <3s для страниц
- **Mobile score:** >90 в Lighthouse
- **SEO score:** >95 в Lighthouse

---

## 🗺️ Roadmap

### Фаза 1: MVP (1-2 месяца)
- ✅ **Базовая архитектура** (готово)
- ✅ **Аниме база и поиск**
- ✅ **Плейлисты с ссылками**
- ✅ **Базовая аутентификация**
- **Простые комментарии**
- **Группы сообществ**
- **Reactor (Shorts)**

### Фаза 2: Социальная сеть (3-4 месяца)
- **Продвинутая модерация**
- **Уведомления в реальном времени**
- **Мобильное приложение**
- **Интеграция с внешними API**
- **Платная подписка**

### Фаза 3: Масштаб (5-6 месяцев)
- **ИИ рекомендации**
- **Видео стримминг**
- **Многоязычность**
- **Аналитика и BI**
- **Партнёрства с озвучками**

### Фаза 4: Экосистема (7+ месяцев)
- **Маркетплейс мерча**
- **Кастинг для озвучек**
- **Виртуальные концерты**
- **NFT коллекции**
- **Образовательная платформа**

---

## 🤝 Содействие

### Как помочь проекту
1. **Fork** репозиторий
2. **Создай feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit изменения**: `git commit -m 'Add amazing feature'`
4. **Push branch**: `git push origin feature/amazing-feature`
5. **Создай Pull Request**

### Типы задач
- 🐛 **Bug fixes** - исправление ошибок
- ✨ **Features** - новая функциональность
- 📚 **Documentation** - улучшение документации
- 🎨 **UI/UX** - дизайн и интерфейс
- 🔧 **DevOps** - инфраструктура и деплой

---

## 📄 Лицензия

MIT License - см. [LICENSE](LICENSE) файл для деталей.

---

## 📞 Контакты

- **Email:** contact@animecore.app
- **Telegram:** @animecore_support
- **Discord:** AnimeCore Community
- **GitHub Issues:** для багов и фич

---

*🎌 AnimeCore - твой фэндом, твои правила! 🎌*