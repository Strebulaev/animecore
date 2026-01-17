import os
import sys
import django

# Добавь путь к корню проекта
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Установи переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Настрой Django
django.setup()

from django.contrib.auth import get_user_model
from anime.models import Genre, Anime
import random

def main():
    User = get_user_model()
    
    print("🔄 Создание тестовых данных...")
    
    # Создай тестового пользователя
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'is_active': True
        }
    )
    if created:
        user.set_password('test123')
        user.save()
        print(f'✅ Создан пользователь: {user.username}')
    
    # Создай жанры
    genres_data = [
        'Экшен', 'Приключения', 'Комедия', 'Драма', 'Фэнтези',
        'Романтика', 'Сёнен', 'Сёдзё', 'Повседневность', 'Гарем'
    ]
    
    for genre_name in genres_data:
        genre, created = Genre.objects.get_or_create(
            name=genre_name,
            slug=genre_name.lower().replace(' ', '-')
        )
        if created:
            print(f'✅ Создан жанр: {genre_name}')
    
    # Создай тестовые аниме
    test_anime = [
        {
            'title_ru': 'Атака титанов',
            'title_en': 'Attack on Titan',
            'description': 'Человечество живет в городах, окруженных гигантскими стенами, защищающими от титанов.',
            'year': 2013,
            'status': 'finished',
            'episodes': 75,
        },
        {
            'title_ru': 'Стальной алхимик: Братство',
            'title_en': 'Fullmetal Alchemist: Brotherhood',
            'description': 'История двух братьев-алхимиков, ищущих философский камень.',
            'year': 2009,
            'status': 'finished',
            'episodes': 64,
        },
        {
            'title_ru': 'Ван Пис',
            'title_en': 'One Piece',
            'description': 'Монки Д. Луффи и его команда ищут сокровище Ван Пис.',
            'year': 1999,
            'status': 'ongoing',
            'episodes': 1100,
        },
    ]
    
    for anime_data in test_anime:
        anime, created = Anime.objects.get_or_create(
            title_ru=anime_data['title_ru'],
            defaults=anime_data
        )
        if created:
            # Добавляем случайные жанры
            all_genres = list(Genre.objects.all())
            random_genres = random.sample(all_genres, min(3, len(all_genres)))
            anime.genres.set(random_genres)
            print(f'✅ Создано аниме: {anime.title_ru}')
    
    print('🎉 Тестовые данные успешно созданы!')

if __name__ == '__main__':
    main()