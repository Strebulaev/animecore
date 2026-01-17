from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimeViewSet, GenreViewSet
from .views import import_anime_view

router = DefaultRouter()
router.register(r'anime', AnimeViewSet, basename='anime')
router.register(r'genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('', include(router.urls)),
    path('import/', import_anime_view, name='import-anime'),
]