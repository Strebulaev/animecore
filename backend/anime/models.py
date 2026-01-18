from multiprocessing import connection
from django.db import models
from django.utils.text import slugify
from django.db.models import Manager  # Добавляем импорт

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class BulkImportManager(Manager):
    """Менеджер для массовой вставки"""
    
    def bulk_create_fast(self, objs, batch_size=1000):
        """Быстрая массовая вставка с использованием RAW SQL"""
        if not objs:
            return
        
        model = self.model
        fields = [f for f in model._meta.fields if not f.auto_created]
        field_names = [f.column for f in fields]
        
        placeholders = ['%s'] * len(field_names)
        sql = f"""
            INSERT INTO {model._meta.db_table} ({','.join(field_names)})
            VALUES ({','.join(placeholders)})
            ON CONFLICT DO NOTHING
        """
        
        with connection.cursor() as cursor:
            for i in range(0, len(objs), batch_size):
                batch = objs[i:i+batch_size]
                values = []
                for obj in batch:
                    row = []
                    for field in fields:
                        value = getattr(obj, field.attname)
                        row.append(value)
                    values.append(row)
                
                cursor.executemany(sql, values)
                for obj in batch:
                    print(f"✅ Bulk imported: {obj.title_ru or obj.title_en or f'ID:{obj.shikimori_id}'}")
                print(f"Вставлено {i+len(batch)}/{len(objs)} записей")

                
class Studio(models.Model):
    """Студия-производитель аниме"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Anime(models.Model):

    objects = BulkImportManager() 
    
    class Meta:
        indexes = [
            models.Index(fields=['shikimori_id']),
            models.Index(fields=['mal_id']),
            models.Index(fields=['anilist_id']),
        ]

    STATUS_CHOICES = [
        ('ongoing', 'Онгоинг'),
        ('finished', 'Завершён'),
        ('announced', 'Анонсирован'),
    ]
    
    TYPE_CHOICES = [
        ('tv', 'TV Сериал'),
        ('movie', 'Фильм'),
        ('ova', 'OVA'),
        ('ona', 'ONA'),
        ('special', 'Спешл'),
    ]
    
    # Основные поля
    title_ru = models.CharField(max_length=500, blank=True, db_index=True)
    title_en = models.CharField(max_length=500, blank=True, db_index=True)
    title_jp = models.CharField(max_length=500, blank=True)
    
    # Внешние ID
    shikimori_id = models.IntegerField(null=True, blank=True, unique=True, db_index=True)
    anilist_id = models.IntegerField(null=True, blank=True)
    mal_id = models.IntegerField(null=True, blank=True)
    
    # Основная информация
    slug = models.SlugField(max_length=500, blank=True, db_index=True)
    anime_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='tv')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='finished')
    episodes = models.IntegerField(null=True, blank=True)
    
    # Даты
    aired_from = models.DateField(null=True, blank=True)
    aired_to = models.DateField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True, db_index=True)
    
    # Рейтинги
    score = models.FloatField(null=True, blank=True)
    scored_by = models.IntegerField(default=0)
    rank = models.IntegerField(null=True, blank=True)
    popularity = models.IntegerField(null=True, blank=True)
    
    # Контент
    description = models.TextField(blank=True)
    description_source = models.CharField(max_length=100, blank=True)
    
    # Изображения
    poster_url = models.URLField(max_length=1000, blank=True)
    poster_file = models.ImageField(upload_to='anime/posters/', null=True, blank=True)

    # Трейлер
    trailer_url = models.URLField(max_length=1000, blank=True)

    # Скриншоты
    screenshots = models.JSONField(null=True, blank=True)  # List of URLs
    
    # Связи
    genres = models.ManyToManyField(Genre, related_name='anime', blank=True)
    studios = models.ManyToManyField(Studio, related_name='anime', blank=True)
    
    # Поисковый текст
    search_text = models.TextField(blank=True, db_index=True)

    # Технические поля
    data_source = models.CharField(max_length=100, default='shikimori')
    approved = models.BooleanField(default=True)
    
    # Время
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_synced = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-popularity', '-score']
        indexes = [
            models.Index(fields=['title_ru']),
            models.Index(fields=['title_en']),
            models.Index(fields=['year']),
            models.Index(fields=['status']),
            models.Index(fields=['score']),
            models.Index(fields=['search_text']),
        ]
    
    def save(self, *args, **kwargs):
        # Генерируем slug
        if not self.slug:
            base = self.title_ru or self.title_en or str(self.shikimori_id)
            if base:
                self.slug = slugify(base)

        # Определяем год из даты
        if self.aired_from and not self.year:
            self.year = self.aired_from.year

        # Создаем поисковый текст
        self.search_text = f"{self.title_ru or ''} {self.title_en or ''} {self.title_jp or ''}".strip().lower()

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title_ru or self.title_en or f"Anime #{self.id}"
    
    @property
    def display_title(self):
        return self.title_ru or self.title_en or 'Без названия'
    
class VoiceActor(models.Model):
    """Актер озвучки"""
    name = models.CharField(max_length=200)
    name_original = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    photo_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    # Контакты
    vk_url = models.URLField(blank=True)
    telegram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Статистика
    is_verified = models.BooleanField(default=False)
    rating = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class DubStudio(models.Model):
    """Студия озвучки (AniMedia, AniLibria, SHIZA Project и т.д.)"""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    logo_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    
    # Контакты
    website_url = models.URLField(blank=True)
    vk_url = models.URLField(blank=True)
    telegram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    
    # Статус
    is_official = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Активна'),
            ('inactive', 'Неактивна'),
            ('closed', 'Закрыта'),
        ],
        default='active'
    )
    
    # Статистика
    rating = models.FloatField(default=0.0)
    works_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Студия озвучки'
        verbose_name_plural = 'Студии озвучки'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Dub(models.Model):
    """Озвучка конкретного аниме"""
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='anime_dubs')
    studio = models.ForeignKey(DubStudio, on_delete=models.CASCADE, related_name='studio_dubs')
    
    # Информация об озвучке
    title = models.CharField(max_length=500, blank=True)  # "Озвучка AniMedia"
    description = models.TextField(blank=True)
    quality = models.CharField(
        max_length=20,
        choices=[
            ('bd', 'Blu-ray'),
            ('dvd', 'DVD'),
            ('tv', 'TV'),
            ('web', 'Web'),
            ('unknown', 'Неизвестно'),
        ],
        default='unknown'
    )
    
    # Ссылки на просмотр
    player_url = models.URLField(blank=True)  # Ссылка на плеер с озвучкой
    download_url = models.URLField(blank=True)  # Ссылка на скачивание
    torrent_url = models.URLField(blank=True)  # Торрент-ссылка
    
    # Метаданные
    episodes_count = models.IntegerField(default=0)  # Сколько серий озвучено
    is_complete = models.BooleanField(default=False)  # Завершена ли озвучка полностью
    is_ongoing = models.BooleanField(default=True)    # Актуальна ли озвучка
    
    # Дата выпуска
    released_at = models.DateField(null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True)
    
    # Рейтинг пользователей
    rating = models.FloatField(default=0.0)
    votes_count = models.IntegerField(default=0)
    
    # Технические
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-rating', '-released_at']
        unique_together = ['anime', 'studio']
    
    def __str__(self):
        return f"{self.anime.title_ru} - {self.studio.name}"


class DubRole(models.Model):
    """Роль актера в озвучке"""
    dub = models.ForeignKey(Dub, on_delete=models.CASCADE, related_name='roles')
    actor = models.ForeignKey(VoiceActor, on_delete=models.CASCADE, related_name='roles')
    character_name = models.CharField(max_length=200)  # Имя персонажа
    character_name_original = models.CharField(max_length=200, blank=True)  # Оригинальное имя
    
    ROLE_TYPE_CHOICES = [
        ('main', 'Главная роль'),
        ('supporting', 'Второстепенная роль'),
        ('guest', 'Эпизодическая роль'),
        ('narrator', 'Рассказчик'),
    ]
    
    role_type = models.CharField(max_length=20, choices=ROLE_TYPE_CHOICES, default='supporting')
    order = models.IntegerField(default=0)  # Для сортировки
    
    class Meta:
        ordering = ['order', 'character_name']
    
    def __str__(self):
        return f"{self.character_name} - {self.actor.name}"


class UserDubRating(models.Model):
    """Оценка пользователем озвучки"""
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='dub_ratings')
    dub = models.ForeignKey(Dub, on_delete=models.CASCADE, related_name='user_ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])  # 1-10
    comment = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'dub']
    
    def __str__(self):
        return f"{self.user.username} - {self.dub} - {self.rating}"