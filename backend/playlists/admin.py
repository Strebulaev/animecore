from django.contrib import admin
from .models import Playlist, PlaylistItem

class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0
    readonly_fields = ['created_at']
    fields = ['anime', 'episode_number', 'source_url', 'dub_studio', 'notes']

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'is_public', 'items_count', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    readonly_fields = ['created_at', 'items_count']
    inlines = [PlaylistItemInline]

    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Количество элементов'

@admin.register(PlaylistItem)
class PlaylistItemAdmin(admin.ModelAdmin):
    list_display = ['playlist', 'anime', 'episode_number', 'source_url', 'dub_studio', 'created_at']
    list_filter = ['created_at', 'episode_number']
    search_fields = ['playlist__title', 'anime__title_ru', 'anime__title_en', 'source_url']
    readonly_fields = ['created_at']
    raw_id_fields = ['playlist', 'anime', 'dub_studio']
