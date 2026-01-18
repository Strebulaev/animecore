import re
from django.core.management.base import BaseCommand
from anime.models import Anime

class Command(BaseCommand):
    help = 'Clean descriptions from BBCode tags'

    def _clean_description(self, description: str) -> str:
        """Очистка описания от BBCode тегов Shikimori"""
        if not description:
            return description

        # Удалить [tag=...] и [/tag]
        description = re.sub(r'\[/?\w+(=\w+)?[^\]]*\]', '', description)

        # Удалить лишние пробелы
        description = re.sub(r'\s+', ' ', description).strip()

        return description

    def handle(self, *args, **options):
        anime_with_tags = Anime.objects.filter(description__contains='[')

        self.stdout.write(f'Found {anime_with_tags.count()} anime with potential tags')

        cleaned_count = 0
        for anime in anime_with_tags:
            cleaned = self._clean_description(anime.description)
            if cleaned != anime.description:
                anime.description = cleaned
                anime.save()
                cleaned_count += 1

        self.stdout.write(f'Cleaned {cleaned_count} descriptions')

        self.stdout.write('Done')