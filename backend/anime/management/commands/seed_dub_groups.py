from django.core.management.base import BaseCommand
from dubs.models import DubGroup

class Command(BaseCommand):
    help = 'Заполнение базы известными группами озвучки'
    
    def handle(self, *args, **options):
        groups_data = [
            {
                'name': 'AniLibria',
                'description': 'Крупнейшее сообщество по озвучке аниме. Известны качественными работами и большим каталогом.',
                'website': 'https://www.anilibria.tv/',
                'vk_url': 'https://vk.com/anilibria',
                'telegram_url': 'https://t.me/anilibria_tv',
                'logo_url': 'https://anilibria.tv/upload/iblock/e5e/e5e5c00950831efdc7d66469f6478ae2.png',
            },
            {
                'name': 'AniMedia',
                'description': 'Популярная группа озвучки, известная работами над многими хитами.',
                'vk_url': 'https://vk.com/animedianews',
                'telegram_url': 'https://t.me/animediaofficial',
                'logo_url': 'https://sun9-10.userapi.com/impg/xZQmL5Nc1G5sUOqjqqGR9Yz_rry6NgyoKwA6qg/TYLQKY2ZRf8.jpg',
            },
            {
                'name': 'Kubik in Cube',
                'description': 'Известны нестандартным подходом к озвучке и авторским юмором.',
                'vk_url': 'https://vk.com/kubikrubika',
                'logo_url': 'https://sun9-73.userapi.com/impf/c841124/v841124490/7a20c/l68GtfTZHIY.jpg',
            },
            {
                'name': 'JAM',
                'description': 'Группа озвучки с акцентом на качество и внимание к деталям.',
                'vk_url': 'https://vk.com/jamanime',
            },
            {
                'name': 'Shiza Project',
                'description': 'Творческое объединение, известное необычными переводами.',
                'vk_url': 'https://vk.com/shizaproject',
            },
            {
                'name': 'AniDUB',
                'description': 'Одна из старейших групп озвучки в рунете.',
                'vk_url': 'https://vk.com/anidub_anime',
            },
            {
                'name': 'AnimeVost',
                'description': 'Группа, специализирующаяся на субтитрах и быстрых релизах.',
                'vk_url': 'https://vk.com/animevostorg',
            },
            {
                'name': 'ColdFilm',
                'description': 'Известны работами над популярными сериалами.',
                'vk_url': 'https://vk.com/coldfilm',
            },
            {
                'name': 'Studio Band',
                'description': 'Творческое объединение актёров озвучки.',
                'vk_url': 'https://vk.com/bandstudio',
            },
            {
                'name': 'AniPlay',
                'description': 'Молодая перспективная группа озвучки.',
                'vk_url': 'https://vk.com/aniplaytv',
            },
            {
                'name': 'AniMaunt',
                'description': 'Группа с акцентом на атмосферные произведения.',
                'vk_url': 'https://vk.com/animount',
            },
            {
                'name': 'AniRise',
                'description': 'Известны работами над сёнен-аниме.',
                'vk_url': 'https://vk.com/anirise',
            },
            {
                'name': 'AniSky',
                'description': 'Специализируются на романтических и драматических тайтлах.',
                'vk_url': 'https://vk.com/aniskylife',
            },
            {
                'name': 'SovetRomantica',
                'description': 'Группа, специализирующаяся на романтических аниме.',
                'vk_url': 'https://vk.com/sovetromantica',
            },
            {
                'name': 'AniMedia (UA)',
                'description': 'Украинская ветка AniMedia.',
                'vk_url': 'https://vk.com/animedianews',
            },
            {
                'name': 'AniStar',
                'description': 'Небольшая но качественная группа озвучки.',
                'vk_url': 'https://vk.com/anistar_tv',
            },
            {
                'name': 'AniRock',
                'description': 'Известны работами над музыкальными аниме.',
                'vk_url': 'https://vk.com/anirock_tv',
            },
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