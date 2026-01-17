# parsers/manager.py - упрощенная версия
import time
from .shikimori import ShikimoriParser

class AnimeParserManager:
    """Упрощенный менеджер парсеров"""
    
    def __init__(self):
        self.parser = ShikimoriParser()  # Только Shikimori для начала
    
    def import_popular(self, limit: int = 50) -> list:
        """Импорт популярных аниме"""
        print(f"Начинаю импорт {limit} популярных аниме...")
        popular = self.parser.get_popular_anime(limit=limit)
        
        imported = []
        for item in popular:
            try:
                normalized = self.parser.normalize_anime_data(item)
                imported.append(normalized)
                print(f"  ✓ {normalized['title_ru']}")
                time.sleep(0.1)  # Небольшая задержка
            except Exception as e:
                print(f"  ✗ Ошибка: {e}")
        
        return imported