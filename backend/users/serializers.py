from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'avatar', 'bio', 'email_verified',
            'phone_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации"""

    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'phone_number', 'first_name', 'last_name',
            'password', 'password_confirm'
        ]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")

        # Проверяем, что указан либо email, либо телефон
        if not data.get('email') and not data.get('phone_number'):
            raise serializers.ValidationError("Необходимо указать email или телефон")

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Сериализатор входа"""

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Неверные учетные данные")
        return data


class GoogleAuthSerializer(serializers.Serializer):
    """Сериализатор Google аутентификации"""

    id_token = serializers.CharField()


class PhoneVerificationSerializer(serializers.Serializer):
    """Сериализатор верификации телефона"""

    phone_number = serializers.CharField()
    action = serializers.ChoiceField(choices=['send', 'verify'])
    code = serializers.CharField(required=False, min_length=6, max_length=6)


class EmailVerificationSerializer(serializers.Serializer):
    """Сериализатор верификации email"""

    email = serializers.EmailField()
    action = serializers.ChoiceField(choices=['send', 'verify'])
    code = serializers.CharField(required=False, min_length=8, max_length=8)


class PasswordResetSerializer(serializers.Serializer):
    """Сериализатор сброса пароля"""

    email = serializers.EmailField()