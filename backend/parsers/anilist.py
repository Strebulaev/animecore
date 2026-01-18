import requests
from typing import Dict, List, Optional
from .base import BaseAnimeParser

class AnilistParser(BaseAnimeParser):
    """Парсер Anilist для получения постеров"""

    BASE_URL = "https://graphql.anilist.co"

    def search_anime(self, query: str, limit: int = 20) -> List[Dict]:
        """Поиск аниме по названию"""
        query_str = """
        query ($search: String, $limit: Int) {
          Page(page: 1, perPage: $limit) {
            media(search: $search, type: ANIME) {
              id
              title {
                romaji
                english
              }
              coverImage {
                large
                medium
              }
            }
          }
        }
        """
        variables = {"search": query, "limit": limit}
        response = self.session.post(self.BASE_URL, json={"query": query_str, "variables": variables})
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("Page", {}).get("media", [])

    def get_anime_by_id(self, anilist_id: int) -> Optional[Dict]:
        """Получение аниме по Anilist ID"""
        query_str = """
        query ($id: Int) {
          Media(id: $id, type: ANIME) {
            id
            title {
              romaji
              english
            }
            coverImage {
              large
              medium
            }
          }
        }
        """
        variables = {"id": anilist_id}
        response = self.session.post(self.BASE_URL, json={"query": query_str, "variables": variables})
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("Media")

    def get_popular_anime(self, page: int = 1, limit: int = 50) -> List[Dict]:
        """Получение популярных аниме"""
        query_str = """
        query ($page: Int, $limit: Int) {
          Page(page: $page, perPage: $limit) {
            media(type: ANIME, sort: POPULARITY_DESC) {
              id
              title {
                romaji
                english
              }
              coverImage {
                large
                medium
              }
            }
          }
        }
        """
        variables = {"page": page, "limit": limit}
        response = self.session.post(self.BASE_URL, json={"query": query_str, "variables": variables})
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("Page", {}).get("media", [])

    def get_poster_url(self, title: str) -> Optional[str]:
        """Получение постера по названию"""
        results = self.search_anime(title, limit=1)
        if results:
            return results[0].get("coverImage", {}).get("large") or results[0].get("coverImage", {}).get("medium")
        return None