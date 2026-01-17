from django.core.management.base import BaseCommand
from anime.mass_import import MassAnimeImporter

class Command(BaseCommand):
    help = 'Массовый импорт 100000+ аниме'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--target',
            type=int,
            default=100000,
            help='Целевое количество аниме'
        )
        parser.add_argument(
            '--workers',
            type=int,
            default=20,
            help='Количество потоков'
        )
        parser.add_argument(
            '--resume',
            action='store_true',
            help='Продолжить с места остановки'
        )
    
    def handle(self, *args, **options):
        importer = MassAnimeImporter(max_workers=options['workers'])
        
        print("⚠️  ВНИМАНИЕ: Импорт 100000+ аниме займет 10-48 часов!")
        print("Рекомендуется запускать на сервере с хорошим интернетом.")
        print("Для остановки нажмите Ctrl+C\n")
        
        confirm = input("Продолжить? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Отменено")
            return
        
        try:
            importer.import_100k()
        except KeyboardInterrupt:
            print("\nИмпорт прерван пользователем")
        except Exception as e:
            print(f"\nКритическая ошибка: {e}")
        
        print("\nИмпорт завершен (или прерван)")