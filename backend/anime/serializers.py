from rest_framework import serializers
from .models import Anime, Genre

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']

class AnimeSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Anime
        fields = [
            'id', 'title_ru', 'title_en', 'title_jp',
            'description', 'year', 'status', 'episodes',
            'score', 'poster_url', 'genres', 'created_at'
        ]