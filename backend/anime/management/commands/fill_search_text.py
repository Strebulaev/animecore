from django.core.management.base import BaseCommand
from anime.models import Anime

class Command(BaseCommand):
    help = 'Fill search_text field for all anime'

    def handle(self, *args, **options):
        anime_list = Anime.objects.all()
        updated = 0

        for anime in anime_list:
            old_search_text = anime.search_text
            anime.save()  # This will trigger the save method to update search_text

            if anime.search_text != old_search_text:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated search_text for {updated} anime out of {anime_list.count()}'
            )
        )