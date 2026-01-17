import time
import random
from datetime import datetime
from django.db import transaction
from parsers.shikimori import ShikimoriParser
from .models import Anime, Genre, Studio

class AnimeImportService:
    """Упрощенный сервис импорта"""
    
    def __init__(self):
        self.parser = ShikimoriParser()
    
    def import_single_anime(self, shikimori_id: int) -> Anime:
        """Импорт одного аниме"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ID: {shikimori_id}")
        
        # Получаем данные
        raw_data = self.parser.get_anime_by_id(shikimori_id)
        if not raw_data:
            print(f"  ✗ Не найдено")
            return None
        
        # Нормализуем
        data = self.parser.normalize_anime_data(raw_data)
        
        with transaction.atomic():
            # Создаем/обновляем аниме
            anime, created = Anime.objects.update_or_create(
                shikimori_id=shikimori_id,
                defaults={
                    'title_ru': data['title_ru'],
                    'title_en': data['title_en'],
                    'title_jp': data['title_jp'],
                    'description': data['description'],
                    'year': data['year'],
                    'status': data['status'],
                    'episodes': data['episodes'],
                    'score': data['score'],
                    'poster_url': data['poster_url'],
                    'data_source': 'shikimori'
                }
            )
            
            # Жанры
            if data['genres']:
                for genre_data in data['genres']:
                    genre_name = genre_data['name']
                    if genre_name:
                        genre, _ = Genre.objects.get_or_create(
                            name=genre_name,
                            defaults={'slug': genre_name.lower().replace(' ', '-')}
                        )
                        anime.genres.add(genre)
            
            # Студии (если есть в данных)
            if 'studios' in data and data['studios']:
                for studio_name in data['studios']:
                    if studio_name:
                        studio, _ = Studio.objects.get_or_create(
                            name=studio_name,
                            defaults={'slug': studio_name.lower().replace(' ', '-')}
                        )
                        anime.studios.add(studio)
            
            action = "Создано" if created else "Обновлено"
            print(f"  ✓ {action}: {anime.title_ru}")
            
            return anime
    
    def import_popular_by_pages(self, total_limit: int = 200) -> list:
        """Импорт популярных аниме по страницам"""
        print(f"Импорт {total_limit} популярных аниме...")
        
        imported = []
        page = 1
        limit_per_page = 50
        
        while len(imported) < total_limit:
            print(f"Страница {page}...")
            popular = self.parser.get_popular_anime(page=page, limit=limit_per_page)
            
            if not popular:
                print("Нет больше данных")
                break
            
            for item in popular:
                if len(imported) >= total_limit:
                    break
                
                shikimori_id = item.get('id')
                if shikimori_id:
                    exists = Anime.objects.filter(shikimori_id=shikimori_id).exists()
                    if not exists:
                        try:
                            anime = self.import_single_anime(shikimori_id)
                            if anime:
                                imported.append(anime)
                                print(f"  [{len(imported)}/{total_limit}]")
                        except Exception as e:
                            print(f"  ✗ Ошибка: {e}")
                        time.sleep(0.3)
                    else:
                        title = item.get('russian') or item.get('name')
                        print(f"  [{len(imported)}/{total_limit}] Уже есть: {title}")
            
            page += 1
            time.sleep(1)
        
        return imported
    
    def import_classics(self) -> list:
        """Импорт классических аниме"""
        classic_ids = [
            # Топ классики
            1,      # Cowboy Bebop
            20,     # Naruto
            1535,   # Death Note
            164,    # Bleach
            813,    # Dragon Ball Z
            6702,   # Fairy Tail
            11061,  # Hunter x Hunter (2011)
            9253,   # Steins;Gate
            6547,   # Angel Beats!
            20507,  # Haikyuu!!
            21881,  # Shingeki no Kyojin Season 2
            22319,  # Tokyo Ghoul
            23273,  # Shigatsu wa Kimi no Uso
            24701,  # Mob Psycho 100
            28223,  # Dr. Stone
            30276,  # One Punch Man
            31964,  # Boku no Hero Academia
            32935,  # Black Clover
            33352,  # Violet Evergarden
            34321,  # Made in Abyss
            34933,  # Kimetsu no Yaiba
            37491,  # Enen no Shouboutai
            38000,  # Kanata no Astra
            39486,  # Dr. Stone: Stone Wars
            40456,  # Kimetsu no Yaiba: Mugen Train
            40748,  # Jujutsu Kaisen
            41587,  # Tokyo Revengers
            42938,  # Fruits Basket: The Final
            44135,  # 86
            48561,  # Sonny Boy
            48607,  # Takt Op. Destiny
            48926,  # Blue Period
            49129,  # Komi-san wa, Komyushou desu.
            49596,  # Ousama Ranking
            # Еще классика
            5114,   # Fullmetal Alchemist: Brotherhood
            5081,   # Bakemonogatari
            47257,  # Spy x Family
            48583,  # Chainsaw Man
            47917,  # Bocchi the Rock!
            49762,  # Cyberpunk: Edgerunners
            50602,  # Bleach: Thousand-Year Blood War
            50631,  # Mob Psycho 100 III
            51179,  # Vinland Saga Season 2
            52034,  # Jujutsu Kaisen 2nd Season
        ]
        
        imported = []
        
        for idx, anime_id in enumerate(classic_ids):
            if Anime.objects.filter(shikimori_id=anime_id).exists():
                print(f"[{idx+1}/{len(classic_ids)}] Уже есть ID {anime_id}")
                continue
            
            try:
                anime = self.import_single_anime(anime_id)
                if anime:
                    imported.append(anime)
                    print(f"[{idx+1}/{len(classic_ids)}]")
                time.sleep(0.5)
            except Exception as e:
                print(f"[{idx+1}/{len(classic_ids)}] ✗ Ошибка ID {anime_id}: {e}")
        
        return imported
    
    def import_by_years(self, start_year: int = 2000, end_year: int = 2024, limit_per_year: int = 10) -> list:
        """Импорт по годам"""
        imported = []
        
        for year in range(end_year, start_year - 1, -1):
            print(f"Год {year}...")
            
            page = 1
            year_imported = 0
            
            while year_imported < limit_per_year:
                anime_list = self.parser.get_anime_by_year(year, page=page, limit=50)
                
                if not anime_list:
                    break
                
                for item in anime_list:
                    if year_imported >= limit_per_year:
                        break
                    
                    shikimori_id = item.get('id')
                    if shikimori_id and not Anime.objects.filter(shikimori_id=shikimori_id).exists():
                        try:
                            anime = self.import_single_anime(shikimori_id)
                            if anime:
                                imported.append(anime)
                                year_imported += 1
                                print(f"  [{year}] {year_imported}/{limit_per_year}")
                        except Exception as e:
                            print(f"  ✗ Ошибка: {e}")
                        time.sleep(0.3)
                
                page += 1
                time.sleep(1)
            
            print(f"Год {year}: импортировано {year_imported} аниме")
        
        return imported
    
    def import_random_by_id_range(self, start_id: int = 1000, end_id: int = 50000, limit: int = 50) -> list:
        """Импорт случайных аниме"""
        imported = []
        attempts = 0
        max_attempts = limit * 3
        
        while len(imported) < limit and attempts < max_attempts:
            random_id = random.randint(start_id, end_id)
            attempts += 1
            
            if Anime.objects.filter(shikimori_id=random_id).exists():
                continue
            
            try:
                anime = self.import_single_anime(random_id)
                if anime:
                    imported.append(anime)
                    print(f"[{len(imported)}/{limit}] Случайное ID {random_id}")
                time.sleep(0.5)
            except Exception as e:
                if "404" not in str(e):
                    print(f"ID {random_id}: {e}")
        
        return imported