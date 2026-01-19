from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import Comment, Group, GroupMembership
from .serializers import (
    CommentSerializer, CommentCreateSerializer,
    GroupSerializer, GroupCreateSerializer, GroupMembershipSerializer
)


class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def get_queryset(self):
        content_type_str = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')

        if not content_type_str or not object_id:
            return Comment.objects.none()

        try:
            content_type = ContentType.objects.get(model=content_type_str)
            return Comment.objects.filter(
                content_type=content_type,
                object_id=object_id,
                is_deleted=False
            ).select_related('author')
        except ContentType.DoesNotExist:
            return Comment.objects.none()

    def perform_create(self, serializer):
        content_type_str = self.request.data.get('content_type')
        object_id = self.request.data.get('object_id')

        try:
            content_type = ContentType.objects.get(model=content_type_str)
            serializer.save(
                author=self.request.user,
                content_type=content_type,
                object_id=object_id
            )
        except ContentType.DoesNotExist:
            raise serializer.ValidationError("Invalid content_type")


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.filter(is_deleted=False)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        # Только автор может редактировать
        if self.get_object().author != self.request.user:
            self.permission_denied(self.request, message="Cannot edit others' comments")
        serializer.save()

    def perform_destroy(self, instance):
        # Только автор или модератор может удалить
        if instance.author != self.request.user:
            # Проверяем модерацию - для простоты, пока только автор
            self.permission_denied(self.request, message="Cannot delete others' comments")
        instance.is_deleted = True
        instance.save()


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return GroupCreateSerializer
        return GroupSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        group = self.get_object()
        if group.memberships.filter(user=request.user).exists():
            return Response({"detail": "Already a member"}, status=status.HTTP_400_BAD_REQUEST)

        membership = GroupMembership.objects.create(user=request.user, group=group)
        group.update_members_count()
        return Response(GroupMembershipSerializer(membership).data)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        group = self.get_object()
        membership = group.memberships.filter(user=request.user).first()
        if not membership:
            return Response({"detail": "Not a member"}, status=status.HTTP_400_BAD_REQUEST)

        membership.delete()
        group.update_members_count()
        return Response({"detail": "Left group"})

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        group = self.get_object()
        memberships = group.memberships.all()
        serializer = GroupMembershipSerializer(memberships, many=True)
        return Response(serializer.data)
