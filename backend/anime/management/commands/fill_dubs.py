from django.core.management.base import BaseCommand
from dubs.models import DubGroup

class Command(BaseCommand):
    help = 'Заполняет базу данных популярными группами озвучки'

    def handle(self, *args, **options):
        POPULAR_DUB_GROUPS = [
            {
                'name': 'Kubik&Cube',
                'slug': 'kubik-cube',
                'description': 'Качественная русская озвучка аниме-сериалов и фильмов.',
                'website': 'https://kubik-cube.com',
                'vk_url': 'https://vk.com/kubikcube',
                'telegram_url': 'https://t.me/kubikcube',
                'logo_url': '',
                'status': 'active',
                'is_verified': True,
                'works_count': 150,
                'followers_count': 50000,
            },
            {
                'name': 'AniLibria',
                'slug': 'anilirbia',
                'description': 'Одна из крупнейших студий озвучки аниме в России.',
                'website': 'https://www.anilibria.tv',
                'vk_url': 'https://vk.com/anilibria',
                'telegram_url': 'https://t.me/anilibria',
                'logo_url': None,
                'status': 'active',
                'is_verified': True,
                'works_count': 500,
                'followers_count': 200000,
            },
            {
                'name': 'Kanon',
                'slug': 'kanon',
                'description': 'Студия озвучки, известная качественной работой.',
                'website': 'https://kanon.ru',
                'vk_url': 'https://vk.com/kanon_voice',
                'telegram_url': 'https://t.me/kanon_official',
                'logo_url': None,
                'status': 'active',
                'is_verified': True,
                'works_count': 300,
                'followers_count': 100000,
            },
            {
                'name': '2x2',
                'slug': '2x2',
                'description': 'Озвучка от телеканала 2x2.',
                'website': 'https://2x2tv.ru',
                'vk_url': 'https://vk.com/2x2tv',
                'telegram_url': None,
                'logo_url': None,
                'status': 'active',
                'is_verified': True,
                'works_count': 100,
                'followers_count': 150000,
            },
            {
                'name': 'XDY',
                'slug': 'xdy',
                'description': 'Студия озвучки аниме.',
                'vk_url': 'https://vk.com/xdy_official',
                'telegram_url': 'https://t.me/xdy_official',
                'logo_url': None,
                'status': 'active',
                'is_verified': False,
                'works_count': 80,
                'followers_count': 30000,
            },
            {
                'name': 'JAM Club',
                'slug': 'jam-club',
                'description': 'Студия озвучки аниме и дорам.',
                'vk_url': 'https://vk.com/jamclub_voice',
                'telegram_url': 'https://t.me/jamclub',
                'logo_url': None,
                'status': 'active',
                'is_verified': False,
                'works_count': 120,
                'followers_count': 45000,
            },
            {
                'name': 'AniMedia',
                'slug': 'animedia',
                'description': 'Качественная озвучка аниме.',
                'vk_url': 'https://vk.com/animedia_official',
                'telegram_url': 'https://t.me/animedia_group',
                'logo_url': None,
                'status': 'active',
                'is_verified': True,
                'works_count': 200,
                'followers_count': 80000,
            },
            {
                'name': 'Victory-Films',
                'slug': 'victory-films',
                'description': 'Озвучка аниме-фильмов и сериалов.',
                'website': 'https://victoryfilms.ru',
                'vk_url': 'https://vk.com/victoryfilms',
                'telegram_url': 'https://t.me/victoryfilms',
                'logo_url': None,
                'status': 'active',
                'is_verified': True,
                'works_count': 250,
                'followers_count': 95000,
            },
            {
                'name': 'Crunchyroll',
                'slug': 'crunchyroll',
                'description': 'Официальная озвучка от стримингового сервиса Crunchyroll.',
                'website': 'https://crunchyroll.com',
                'vk_url': 'https://vk.com/crunchyroll_russia',
                'telegram_url': None,
                'logo_url': None,
                'status': 'active',
                'is_verified': True,
                'works_count': 300,
                'followers_count': 250000,
            },
            {
                'name': 'Netflix',
                'slug': 'netflix',
                'description': 'Официальная озвучка от Netflix.',
                'website': 'https://netflix.com',
                'vk_url': None,
                'telegram_url': None,
                'logo_url': None,
                'status': 'active',
                'is_verified': True,
                'works_count': 150,
                'followers_count': 300000,
            },
            {
                'name': 'Cuba77',
                'slug': 'cuba77',
                'description': 'Известная студия озвучки аниме.',
                'vk_url': 'https://vk.com/cuba77',
                'telegram_url': 'https://t.me/cuba77',
                'logo_url': None,
                'status': 'active',
                'is_verified': True,
                'works_count': 180,
                'followers_count': 65000,
            },
            {
                'name': 'Mioric',
                'slug': 'mioric',
                'description': 'Студия озвучки аниме.',
                'vk_url': 'https://vk.com/mioric',
                'telegram_url': 'https://t.me/mioric_voice',
                'logo_url': None,
                'status': 'active',
                'is_verified': False,
                'works_count': 90,
                'followers_count': 35000,
            },
        ]
        
        created = 0
        updated = 0
        
        for group_data in POPULAR_DUB_GROUPS:
            group, was_created = DubGroup.objects.update_or_create(
                slug=group_data['slug'],
                defaults=group_data
            )
            
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Создана группа: {group.name}'))
            else:
                updated += 1
                self.stdout.write(self.style.WARNING(f'- Обновлена группа: {group.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\nГотово! Создано: {created}, Обновлено: {updated}'))
        self.stdout.write(self.style.SUCCESS(f'Всего групп в базе: {DubGroup.objects.count()}'))