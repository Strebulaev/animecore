from rest_framework import serializers
from .models import Comment, Group, GroupMembership


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_avatar = serializers.ImageField(source='author.avatar', read_only=True)
    replies_count = serializers.SerializerMethodField()
    is_reply = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'author_username', 'author_avatar',
            'text', 'parent', 'is_reply', 'replies_count',
            'created_at', 'updated_at', 'is_deleted'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_replies_count(self, obj):
        if hasattr(obj, 'replies'):
            return obj.replies.filter(is_deleted=False).count()
        return 0


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'parent', 'content_type', 'object_id']

    def validate(self, data):
        # Проверяем, что object_id существует для указанного content_type
        content_type = data.get('content_type')
        object_id = data.get('object_id')

        if content_type and object_id:
            try:
                model_class = content_type.model_class()
                model_class.objects.get(pk=object_id)
            except model_class.DoesNotExist:
                raise serializers.ValidationError("Object does not exist.")

        # Проверяем, что родительский комментарий существует и принадлежит тому же объекту
        parent = data.get('parent')
        if parent:
            if parent.content_type != content_type or parent.object_id != object_id:
                raise serializers.ValidationError("Parent comment must be on the same object.")
            if parent.is_reply:
                raise serializers.ValidationError("Cannot reply to a reply.")

        return data


class GroupSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    is_member = serializers.SerializerMethodField()
    is_moderator = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            'id', 'name', 'slug', 'description', 'avatar_url', 'avatar_file',
            'banner_url', 'banner_file', 'is_private', 'creator', 'creator_username',
            'moderators', 'members_count', 'posts_count', 'is_member', 'is_moderator',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'creator', 'members_count', 'posts_count', 'created_at', 'updated_at']

    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.memberships.filter(user=request.user).exists()
        return False

    def get_is_moderator(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.moderators.filter(pk=request.user.pk).exists() or obj.creator == request.user
        return False


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'description', 'avatar_url', 'banner_url', 'is_private']


class GroupMembershipSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = GroupMembership
        fields = ['id', 'user', 'user_username', 'group', 'group_name', 'role', 'joined_at']
        read_only_fields = ['id', 'joined_at']