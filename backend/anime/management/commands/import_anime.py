from django.core.management.base import BaseCommand
from anime.services import AnimeImportService

class Command(BaseCommand):
    help = 'Импорт аниме из Shikimori'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--strategy',
            type=str,
            required=True,
            choices=['popular', 'years', 'classics', 'random'],
            help='Стратегия импорта'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Общий лимит импорта'
        )
        parser.add_argument(
            '--start-year',
            type=int,
            default=2010,
            help='Начальный год (для стратегии years)'
        )
        parser.add_argument(
            '--end-year',
            type=int,
            default=2024,
            help='Конечный год (для стратегии years)'
        )
        parser.add_argument(
            '--per-year',
            type=int,
            default=10,
            help='Аниме в год (для стратегии years)'
        )
    
    def handle(self, *args, **options):
        service = AnimeImportService()
        
        if options['strategy'] == 'popular':
            self.stdout.write(f"Импорт {options['limit']} популярных аниме...")
            imported = service.import_popular_by_pages(total_limit=options['limit'])
            
        elif options['strategy'] == 'years':
            self.stdout.write(f"Импорт по годам {options['start_year']}-{options['end_year']}...")
            imported = service.import_by_years(
                start_year=options['start_year'],
                end_year=options['end_year'],
                limit_per_year=options['per_year']
            )
            
        elif options['strategy'] == 'classics':
            self.stdout.write("Импорт классики...")
            imported = service.import_classics()
            
        elif options['strategy'] == 'random':
            self.stdout.write(f"Случайный импорт {options['limit']} аниме...")
            imported = service.import_random_by_id_range(limit=options['limit'])
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Импорт завершен! Добавлено {len(imported)} новых аниме."
            )
        )