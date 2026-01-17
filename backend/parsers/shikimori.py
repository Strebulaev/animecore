import time
import requests
from typing import Dict, List, Optional
from .base import BaseAnimeParser

class ShikimoriParser(BaseAnimeParser):
    """Улучшенный парсер Shikimori"""
    
    BASE_URL = "https://shikimori.one/api"
    
    def search_anime(self, query: str, limit: int = 20) -> List[Dict]:
        """Поиск аниме по названию"""
        try:
            url = f"{self.BASE_URL}/animes"
            params = {'search': query, 'limit': limit}
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Ошибка поиска: {e}")
            return []
    
    def get_anime_by_id(self, shikimori_id: int) -> Optional[Dict]:
        """Получение аниме по ID"""
        try:
            url = f"{self.BASE_URL}/animes/{shikimori_id}"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Ошибка получения аниме {shikimori_id}: {e}")
            return None
    
    def get_popular_anime(self, page: int = 1, limit: int = 50) -> List[Dict]:
        """Получение популярных аниме с пагинацией"""
        try:
            url = f"{self.BASE_URL}/animes"
            params = {
                'page': page,
                'limit': limit,
                'order': 'popularity',
                'status': 'released,ongoing,anons',
                'score': '7'
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Ошибка получения популярных: {e}")
            return []
    
    def get_anime_by_genre(self, genre_id: int, page: int = 1, limit: int = 50) -> List[Dict]:
        """Получение аниме по жанру"""
        try:
            url = f"{self.BASE_URL}/animes"
            params = {
                'page': page,
                'limit': limit,
                'genre': genre_id,
                'order': 'popularity'
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Ошибка получения по жанру {genre_id}: {e}")
            return []
    
    def get_anime_by_year(self, year: int, page: int = 1, limit: int = 50) -> List[Dict]:
        """Получение аниме по году"""
        try:
            url = f"{self.BASE_URL}/animes"
            params = {
                'page': page,
                'limit': limit,
                'season': 'summer,winter,spring,fall',
                'year': year,
                'order': 'popularity'
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Ошибка получения по году {year}: {e}")
            return []
    
    def get_all_genres(self) -> List[Dict]:
        """Получение всех жанров"""
        try:
            url = f"{self.BASE_URL}/genres"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Ошибка получения жанров: {e}")
            return []
    
    def normalize_anime_data(self, raw_data: Dict) -> Dict:
        """Нормализация данных Shikimori"""
        normalized = {
            'id': raw_data.get('id'),
            'title_ru': raw_data.get('russian') or raw_data.get('name'),
            'title_en': raw_data.get('english') or raw_data.get('name'),
            'title_jp': raw_data.get('japanese'),
            'description': raw_data.get('description', ''),
            'poster_url': f"https://shikimori.one{raw_data['image']['original']}" if raw_data.get('image') else '',
            'year': raw_data.get('aired_on', '').split('-')[0] if raw_data.get('aired_on') else None,
            'status': self._map_status(raw_data.get('status')),
            'episodes': raw_data.get('episodes'),
            'score': raw_data.get('score'),
            'genres': [{'name': g['russian'] or g['name']} for g in raw_data.get('genres', [])],
            'studios': [s['name'] for s in raw_data.get('studios', [])],
            'raw': raw_data
        }
        
        # Добавляем aired_from если есть
        if raw_data.get('aired_on'):
            normalized['aired_from'] = raw_data['aired_on']
        
        return normalized
    
    def _map_status(self, status: str) -> str:
        mapping = {'released': 'finished', 'ongoing': 'ongoing', 'anons': 'announced'}
        return mapping.get(status, 'finished')