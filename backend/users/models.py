from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
# from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    # Дополнительные поля
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    # Поля для аутентификации
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone number'))
    email_verified = models.BooleanField(default=False, verbose_name=_('Email verified'))
    # phone_verified = models.BooleanField(default=False, verbose_name=_('Phone verified'))

    # OAuth поля
    google_id = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name=_('Google ID'))

    # Статус онлайн
    is_online = models.BooleanField(default=False, verbose_name=_('Is online'))

    # Для SMS верификации
    sms_code = models.CharField(max_length=6, blank=True, null=True, verbose_name=_('SMS verification code'))
    sms_code_expires = models.DateTimeField(blank=True, null=True, verbose_name=_('SMS code expiration'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username or self.email or str(self.phone_number) or f'User {self.id}'