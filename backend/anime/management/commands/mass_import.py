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
            '--ultra',
            action='store_true',
            help='Ультра-быстрый режим (200 потоков, без задержек, риск бана)'
        )
        parser.add_argument(
            '--resume',
            action='store_true',
            help='Продолжить с места остановки'
        )
    
    def handle(self, *args, **options):
        if options['ultra']:
            # Ultra mode: 200 workers, no delays, full speed
            options['workers'] = 200
            print("🚀 ULTRA MODE: 200 потоков, максимальная скорость!")
            print("⚠️  Риск бана IP, используйте VPN если нужно\n")

        importer = MassAnimeImporter(max_workers=options['workers'])

        if not options['ultra']:
            print("⚠️  ВНИМАНИЕ: Импорт 100000+ аниме займет 10-48 часов!")
            print("Рекомендуется запускать на сервере с хорошим интернетом.")
            print("Для остановки нажмите Ctrl+C\n")

            confirm = input("Продолжить? (yes/no): ")
            if confirm.lower() != 'yes':
                print("Отменено")
                return

        try:
            if options['ultra']:
                importer.import_ultra_fast()
            else:
                importer.import_100k()
        except KeyboardInterrupt:
            print("\nИмпорт прерван пользователем")
        except Exception as e:
            print(f"\nКритическая ошибка: {e}")

        print("\nИмпорт завершен (или прерван)")