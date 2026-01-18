from django.core.management.base import BaseCommand
from anime.models import Anime
from parsers.anilist import AnilistParser

class Command(BaseCommand):
    help = 'Update posters from Anilist for anime with missing images'

    def _is_default_poster(self, poster_url):
        # Check for known default or duplicate posters
        bad_patterns = [
            'bx115853',  # Seems like a default
            'anilistcdn/media/anime/cover/medium/default',
        ]
        return any(pattern in poster_url for pattern in bad_patterns)

    def handle(self, *args, **options):
        parser = AnilistParser()

        anime_to_update = Anime.objects.filter(poster_url='/missing_original.jpg')

        self.stdout.write(f'Found {anime_to_update.count()} anime to update from Anilist')

        for anime in anime_to_update:
            # Try English, then Japanese, then Russian
            titles_to_try = [anime.title_en, anime.title_jp, anime.title_ru]
            titles_to_try = [t for t in titles_to_try if t]

            poster = None
            for title in titles_to_try:
                clean_title = title.strip('[]"\'')
                try:
                    poster = parser.get_poster_url(clean_title)
                    if poster and not self._is_default_poster(poster):
                        self.stdout.write(self.style.SUCCESS(f'Found poster for ID {anime.shikimori_id}'))
                        break
                    else:
                        poster = None
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error for ID {anime.shikimori_id}: {str(e)[:50]}'))
                import time
                time.sleep(0.2)

            if poster:
                anime.poster_url = poster
                anime.save()
                self.stdout.write(self.style.SUCCESS(f'Updated to {poster}'))
            else:
                self.stdout.write(self.style.WARNING('No valid poster found'))

            import time
            time.sleep(0.5)  # Rate limit