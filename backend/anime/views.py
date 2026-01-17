from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Anime, Genre
from .serializers import AnimeSerializer, GenreSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from anime.services import AnimeImportService

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]

class AnimeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'year']
    search_fields = ['title_ru', 'title_en', 'title_jp']
    ordering_fields = ['title_ru', 'year', 'score']

@api_view(['POST'])
@permission_classes([IsAdminUser])
def import_anime_view(request):
    """API endpoint для импорта аниме"""
    external_id = request.data.get('external_id')
    source = request.data.get('source', 'shikimori')
    
    if not external_id:
        return Response(
            {'error': 'external_id обязателен'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    service = AnimeImportService()
    anime = service.import_anime_from_external(int(external_id), source)
    
    if anime:
        from .serializers import AnimeSerializer
        return Response({
            'success': True,
            'message': f'Аниме "{anime.display_title}" успешно импортировано',
            'anime': AnimeSerializer(anime).data
        })
    
    return Response(
        {'success': False, 'error': 'Не удалось импортировать аниме'},
        status=status.HTTP_400_BAD_REQUEST
    )