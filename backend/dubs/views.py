from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import DubGroup, Dub, VoiceActor
from .serializers import (
    DubGroupSerializer, DubSerializer, 
    VoiceActorSerializer, AnimeDubSerializer
)
from anime.models import Anime

class DubGroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для групп озвучки"""
    
    queryset = DubGroup.objects.filter(status='active').order_by('name')
    serializer_class = DubGroupSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']
    
    @action(detail=True, methods=['get'])
    def dubs(self, request, pk=None):
        """Получить все озвучки группы"""
        group = self.get_object()
        dubs = group.dubs.all().select_related('anime')
        
        # Пагинация
        page = self.paginate_queryset(dubs)
        if page is not None:
            serializer = DubSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = DubSerializer(dubs, many=True)
        return Response(serializer.data)


class DubViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для озвучек"""
    
    queryset = Dub.objects.all().select_related('group', 'anime')
    serializer_class = DubSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['group', 'anime', 'dub_type', 'is_complete']
    
    @action(detail=False, methods=['get'])
    def by_anime(self, request):
        """Получить все озвучки для конкретного аниме"""
        anime_id = request.query_params.get('anime_id')
        if not anime_id:
            return Response({'error': 'anime_id parameter is required'}, status=400)
        
        anime = get_object_or_404(Anime, id=anime_id)
        dubs = self.queryset.filter(anime=anime)
        
        # Сортировка: сначала полные озвучки, потом по рейтингу
        dubs = dubs.order_by('-is_complete', '-average_rating')
        
        serializer = AnimeDubSerializer(dubs, many=True)
        return Response(serializer.data)


class VoiceActorViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для актёров озвучки"""
    
    queryset = VoiceActor.objects.all().order_by('name')
    serializer_class = VoiceActorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']


# API функции для получения озвучек аниме
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def anime_dubs(request, anime_id):
    """Получить все озвучки для аниме"""
    anime = get_object_or_404(Anime, id=anime_id)
    dubs = Dub.objects.filter(anime=anime).select_related('group').order_by('-average_rating')
    
    serializer = AnimeDubSerializer(dubs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def popular_dub_groups(request):
    """Получить популярные группы озвучки"""
    groups = DubGroup.objects.filter(status='active').order_by('-works_count')[:10]
    serializer = DubGroupSerializer(groups, many=True)
    return Response(serializer.data)