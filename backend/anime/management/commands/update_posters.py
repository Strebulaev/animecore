from django.core.management.base import BaseCommand
from anime.models import Anime
from anime.services import AnimeImportService

class Command(BaseCommand):
    help = 'Update posters for anime with missing images'

    def handle(self, *args, **options):
        service = AnimeImportService()

        anime_to_update = Anime.objects.filter(poster_url__contains='missing_original.jpg')

        self.stdout.write(f'Found {anime_to_update.count()} anime to update')

        for anime in anime_to_update:
            self.stdout.write(f'Updating {anime.title_ru} (ID: {anime.shikimori_id})')
            try:
                updated_anime = service.import_single_anime(anime.shikimori_id)
                if updated_anime and updated_anime.poster_url != anime.poster_url:
                    self.stdout.write(self.style.SUCCESS(f'Updated poster: {updated_anime.poster_url}'))
                else:
                    self.stdout.write(self.style.WARNING('No change or failed'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {e}'))