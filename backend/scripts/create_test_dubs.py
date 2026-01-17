"""
Скрипт для создания тестовых озвучек для существующих аниме.
Запуск: python manage.py shell < create_test_dubs.py
"""

from dubs.models import DubGroup, Dub
from anime.models import Anime
import random

def run():
    """Создание тестовых озвучек для случайных аниме."""

    # Получаем все группы озвучки
    dub_groups = list(DubGroup.objects.filter(status='active'))
    print(f"Found {len(dub_groups)} active dub groups")
    if not dub_groups:
        print("❌ Нет активных групп озвучки. Сначала запустите скрипт fill_dubs.py")
        return

    # Получаем все аниме
    anime_list = list(Anime.objects.all())
    print(f"Found {len(anime_list)} anime")
    if not anime_list:
        print("❌ Нет аниме в базе данных.")
        return

    created_count = 0

    # Для каждого аниме создаем 1-3 случайные озвучки
    for anime in anime_list:
        # Выбираем случайное количество групп (1-3)
        num_dubs = random.randint(1, min(3, len(dub_groups)))
        selected_groups = random.sample(dub_groups, num_dubs)

        for group in selected_groups:
            # Проверяем, существует ли уже такая озвучка
            if not Dub.objects.filter(anime=anime, group=group).exists():
                # Создаем озвучку
                dub = Dub.objects.create(
                    anime=anime,
                    group=group,
                    dub_type=random.choice(['full', 'subtitles', 'partial', 'voiceover']),
                    quality=random.choice(['low', 'medium', 'high', 'excellent']),
                    episodes_done=random.randint(1, anime.episodes or 12),
                    total_episodes=anime.episodes,
                    is_complete=random.choice([True, False]),
                    average_rating=round(random.uniform(3.0, 5.0), 1),
                    ratings_count=random.randint(10, 500),
                    external_url=f"https://example.com/watch/{anime.id}/{group.slug}"
                )
                created_count += 1
                print(f"✅ Создана озвучка: {group.name} для {anime.title_ru}")

    print(f"\n🎉 Создано {created_count} тестовых озвучек!")
    print(f"Всего озвучек в базе: {Dub.objects.count()}")

if __name__ == '__main__':
    run()