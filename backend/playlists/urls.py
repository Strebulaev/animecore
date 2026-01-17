from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaylistViewSet, PlaylistItemViewSet

# Роутер для плейлистов
router = DefaultRouter()
router.register(r'playlists', PlaylistViewSet, basename='playlist')
router.register(r'playlist-items', PlaylistItemViewSet, basename='playlist-item')

urlpatterns = [
    path('', include(router.urls)),
]