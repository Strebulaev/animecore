from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Anime, Genre
from .serializers import AnimeSerializer, GenreSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from anime.services import AnimeImportService

class AnimePagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 2000

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]

class AnimeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    permission_classes = [AllowAny]
    pagination_class = AnimePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'year']
    search_fields = ['search_text']
    ordering_fields = ['title_ru', 'year', 'score', 'episodes']

    def paginate_queryset(self, queryset):
        if 'search' in self.request.query_params:
            # Для поиска отключаем пагинацию
            return None
        return super().paginate_queryset(queryset)

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