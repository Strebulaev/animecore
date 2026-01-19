from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentListCreateView, CommentDetailView, GroupViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
] + router.urls