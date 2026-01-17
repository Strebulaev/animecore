from django.core.management.base import BaseCommand
from dubs.models import DubGroup, Dub
from anime.models import Anime
import random

class Command(BaseCommand):
    help = 'Создание тестовых озвучек для существующих аниме'

    def handle(self, *args, **options):
        # Получаем группы озвучки
        dub_groups = list(DubGroup.objects.filter(status='active'))
        if not dub_groups:
            self.stdout.write(self.style.WARNING('Нет активных групп озвучки'))
            return

        # Получаем аниме
        anime_list = list(Anime.objects.all())
        if not anime_list:
            self.stdout.write(self.style.WARNING('Нет аниме в базе данных'))
            return

        self.stdout.write(f'Найдено {len(dub_groups)} групп озвучки и {len(anime_list)} аниме')

        created_count = 0

        # Для каждого аниме создаем 1-2 озвучки
        for anime in anime_list[:5]:  # Только первые 5 для теста
            num_dubs = random.randint(1, min(2, len(dub_groups)))
            selected_groups = random.sample(dub_groups, num_dubs)

            for group in selected_groups:
                if not Dub.objects.filter(anime=anime, group=group).exists():
                    dub = Dub.objects.create(
                        anime=anime,
                        group=group,
                        dub_type=random.choice(['studio', 'independent']),
                        quality=random.choice(['720p', '1080p']),
                        episodes_done=random.randint(1, anime.episodes or 12),
                        total_episodes=anime.episodes,
                        is_complete=random.choice([True, False]),
                        average_rating=round(random.uniform(3.0, 5.0), 1),
                        ratings_count=random.randint(10, 500),
                        external_url=f'https://example.com/watch/{anime.id}/{group.slug}'
                    )
                    created_count += 1
                    self.stdout.write(f'✓ Создана озвучка: {group.name} для {anime.title_ru[:30]}...')

        self.stdout.write(self.style.SUCCESS(f'Создано {created_count} озвучек. Всего в базе: {Dub.objects.count()}'))