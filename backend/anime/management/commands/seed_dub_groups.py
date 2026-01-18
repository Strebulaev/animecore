from django.core.management.base import BaseCommand
from dubs.models import DubGroup

class Command(BaseCommand):
    help = 'Заполнение базы известными группами озвучки'
    
    def handle(self, *args, **options):
        groups_data = [

        ]
        
        created = 0
        updated = 0
        
        for group_data in groups_data:
            name = group_data.pop('name')
            dub_group, created_flag = DubGroup.objects.update_or_create(
                name=name,
                defaults=group_data
            )
            
            if created_flag:
                created += 1
                self.stdout.write(f"✓ Создана: {name}")
            else:
                updated += 1
                self.stdout.write(f"✓ Обновлена: {name}")
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Готово! Создано: {created}, Обновлено: {updated}, Всего: {DubGroup.objects.count()}"
            )
        )