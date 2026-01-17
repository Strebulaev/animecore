from rest_framework import serializers
from .models import Playlist, PlaylistItem

class PlaylistItemSerializer(serializers.ModelSerializer):
    anime_title = serializers.CharField(source='anime.title_ru', read_only=True)
    anime_poster = serializers.CharField(source='anime.poster_url', read_only=True)
    dub_studio_name = serializers.CharField(source='dub_studio.name', read_only=True)

    class Meta:
        model = PlaylistItem
        fields = [
            'id', 'anime', 'anime_title', 'anime_poster',
            'episode_number', 'source_url', 'dub_studio', 'dub_studio_name',
            'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class PlaylistSerializer(serializers.ModelSerializer):
    items = PlaylistItemSerializer(many=True, read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = [
            'id', 'user', 'user_username', 'title', 'description',
            'is_public', 'created_at', 'items', 'items_count'
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def get_items_count(self, obj):
        return obj.items.count()

class PlaylistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['title', 'description', 'is_public']

class PlaylistItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistItem
        fields = ['anime', 'episode_number', 'source_url', 'dub_studio', 'notes']