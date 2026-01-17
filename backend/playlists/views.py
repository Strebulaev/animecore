from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Playlist, PlaylistItem
from .serializers import PlaylistSerializer, PlaylistCreateSerializer, PlaylistItemSerializer, PlaylistItemCreateSerializer

class PlaylistViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления плейлистами
    """
    queryset = Playlist.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_public', 'user']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PlaylistCreateSerializer
        return PlaylistSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        queryset = Playlist.objects.all()
        if self.action == 'list':
            # Показывать публичные плейлисты и свои собственные
            if self.request.user.is_authenticated:
                queryset = queryset.filter(
                    is_public=True
                ) | queryset.filter(user=self.request.user)
            else:
                queryset = queryset.filter(is_public=True)
        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """Добавить элемент в плейлист"""
        playlist = self.get_object()

        # Проверяем права
        if playlist.user != request.user:
            return Response(
                {'error': 'У вас нет прав на изменение этого плейлиста'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = PlaylistItemCreateSerializer(data=request.data)
        if serializer.is_valid():
            # Проверяем уникальность аниме в плейлисте
            anime = serializer.validated_data['anime']
            if PlaylistItem.objects.filter(playlist=playlist, anime=anime).exists():
                return Response(
                    {'error': 'Это аниме уже есть в плейлисте'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.save(playlist=playlist)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        """Удалить элемент из плейлиста"""
        playlist = self.get_object()
        item_id = request.data.get('item_id')

        if not item_id:
            return Response(
                {'error': 'Не указан item_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            item = PlaylistItem.objects.get(id=item_id, playlist=playlist)
            if playlist.user != request.user:
                return Response(
                    {'error': 'У вас нет прав на изменение этого плейлиста'},
                    status=status.HTTP_403_FORBIDDEN
                )
            item.delete()
            return Response({'message': 'Элемент удалён'}, status=status.HTTP_204_NO_CONTENT)
        except PlaylistItem.DoesNotExist:
            return Response(
                {'error': 'Элемент не найден'},
                status=status.HTTP_404_NOT_FOUND
            )

class PlaylistItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления элементами плейлистов
    """
    queryset = PlaylistItem.objects.all()
    serializer_class = PlaylistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Показывать только свои элементы или из публичных плейлистов
        return PlaylistItem.objects.filter(
            playlist__user=self.request.user
        ) | PlaylistItem.objects.filter(
            playlist__is_public=True
        ).distinct()

    def perform_create(self, serializer):
        # Устанавливаем плейлист из URL или из данных
        playlist_id = self.kwargs.get('playlist_pk')
        if playlist_id:
            playlist = get_object_or_404(Playlist, id=playlist_id)
            if playlist.user != self.request.user:
                raise PermissionError("Не хватает прав")
            serializer.save(playlist=playlist)
        else:
            serializer.save()
