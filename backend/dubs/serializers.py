from rest_framework import serializers
from .models import DubGroup, Dub, VoiceActor, DubRole, DubLink

class DubGroupSerializer(serializers.ModelSerializer):
    """Сериализатор группы озвучки"""
    
    class Meta:
        model = DubGroup
        fields = [
            'id', 'name', 'slug', 'description',
            'website', 'vk_url', 'telegram_url', 'discord_url',
            'logo_url', 'works_count', 'followers_count',
            'status', 'is_verified', 'created_at'
        ]


class VoiceActorSerializer(serializers.ModelSerializer):
    """Сериализатор актёра озвучки"""
    
    groups = DubGroupSerializer(many=True, read_only=True)
    
    class Meta:
        model = VoiceActor
        fields = [
            'id', 'name', 'slug', 'description',
            'photo_url', 'groups', 'roles_count',
            'created_at'
        ]


class DubLinkSerializer(serializers.ModelSerializer):
    """Сериализатор ссылки на озвучку"""
    
    class Meta:
        model = DubLink
        fields = ['id', 'source', 'url', 'episode', 'quality', 'is_active']


class DubRoleSerializer(serializers.ModelSerializer):
    """Сериализатор роли актёра"""
    
    actor = VoiceActorSerializer(read_only=True)
    
    class Meta:
        model = DubRole
        fields = ['id', 'actor', 'character_name', 'character_name_en', 'is_main']


class DubSerializer(serializers.ModelSerializer):
    """Сериализатор озвучки"""
    
    group = DubGroupSerializer(read_only=True)
    roles = DubRoleSerializer(many=True, read_only=True)
    links = DubLinkSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dub
        fields = [
            'id', 'group', 'dub_type', 'quality',
            'episodes_done', 'total_episodes', 'is_complete', 'is_abandoned',
            'external_url', 'average_rating', 'ratings_count',
            'started_at', 'finished_at', 'last_episode_at',
            'roles', 'links', 'created_at'
        ]


class AnimeDubSerializer(serializers.ModelSerializer):
    """Сериализатор озвучки для аниме (сокращённый)"""
    
    group = serializers.SerializerMethodField()
    dub_type_display = serializers.CharField(source='get_dub_type_display', read_only=True)
    
    class Meta:
        model = Dub
        fields = [
            'id', 'group', 'dub_type', 'dub_type_display', 'quality',
            'episodes_done', 'total_episodes', 'is_complete',
            'average_rating', 'ratings_count', 'external_url'
        ]
    
    def get_group(self, obj):
        return {
            'id': obj.group.id,
            'name': obj.group.name,
            'slug': obj.group.slug,
            'logo_url': obj.group.logo_url
        }