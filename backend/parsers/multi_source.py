import time
import requests
import random
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from .base import BaseAnimeParser
from .shikimori import ShikimoriParser

class MultiSourceParser:
    """Парсер из нескольких источников"""
    
    def __init__(self, max_workers=10):
        self.max_workers = max_workers
        self.sources = {
            'shikimori': ShikimoriParser(),
            'anilist': AniListParser(),
            'jikan': JikanParser(),
        }
    
    def fetch_anime_batch(self, anime_ids: List[int]) -> List[Dict]:
        """Пакетная загрузка аниме"""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_id = {
                executor.submit(self._fetch_single_anime, anime_id): anime_id 
                for anime_id in anime_ids
            }
            
            for future in as_completed(future_to_id):
                anime_id = future_to_id[future]
                try:
                    data = future.result(timeout=30)
                    if data:
                        results.append(data)
                except Exception as e:
                    print(f"Ошибка ID {anime_id}: {e}")
        
        return results
    
    def _fetch_single_anime(self, anime_id: int, source: str = 'shikimori') -> Optional[Dict]:
        """Загрузка одного аниме с повторами"""
        parser = self.sources.get(source)
        if not parser:
            return None
        
        for attempt in range(3):
            try:
                data = parser.get_anime_by_id(anime_id)
                if data:
                    return parser.normalize_anime_data(data)
            except Exception as e:
                if attempt == 2:
                    print(f"Не удалось получить ID {anime_id}: {e}")
                time.sleep(2 ** attempt)  # Экспоненциальная задержка
        
        return None
    
    def generate_id_ranges(self, total: int = 100000) -> List[tuple]:
        """Генерация диапазонов ID для сбора"""
        # Shikimori: 1-50000 (популярные)
        # 50001-150000 (средние)
        # 150001-300000 (все остальные)
        
        ranges = []
        
        # Основной диапазон популярных
        ranges.append((1, 50000, int(total * 0.4)))  # 40%
        
        # Средний диапазон
        ranges.append((50001, 150000, int(total * 0.3)))  # 30%
        
        # Расширенный диапазон
        ranges.append((150001, 300000, int(total * 0.2)))  # 20%
        
        # Случайный разброс
        ranges.append((300001, 500000, int(total * 0.1)))  # 10%
        
        return ranges
    
    def get_random_ids_from_range(self, start: int, end: int, count: int) -> List[int]:
        """Генерация случайных ID из диапазона"""
        total_ids = end - start + 1
        if count > total_ids:
            count = total_ids
        
        # Используем разные стратегии выборки
        step = total_ids // count
        
        ids = []
        if step > 1:
            # Равномерная выборка
            ids = list(range(start, end, step))[:count]
        else:
            # Случайная выборка
            ids = random.sample(range(start, end + 1), count)
        
        return ids

# Создадим заглушки для других парсеров
class AniListParser(BaseAnimeParser):
    def search_anime(self, query: str, limit: int = 20) -> List[Dict]:
        return []
    
    def get_anime_by_id(self, external_id: int) -> Optional[Dict]:
        # TODO: Реализовать AniList API
        return None
    
    def get_popular_anime(self, page: int = 1, limit: int = 50) -> List[Dict]:
        return []

class JikanParser(BaseAnimeParser):
    def search_anime(self, query: str, limit: int = 20) -> List[Dict]:
        return []
    
    def get_anime_by_id(self, external_id: int) -> Optional[Dict]:
        # TODO: Реализовать Jikan API
        return None
    
    def get_popular_anime(self, page: int = 1, limit: int = 50) -> List[Dict]:
        return []