from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    # JWT токены
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Аутентификация
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # Социальная аутентификация
    path('google/', views.GoogleAuthView.as_view(), name='google_auth'),
    path('google/callback/', views.GoogleAuthCallbackView.as_view(), name='google_auth_callback'),

    # Верификация
    path('verify/phone/', views.PhoneVerificationView.as_view(), name='phone_verification'),
    path('verify/email/', views.EmailVerificationView.as_view(), name='email_verification'),

    # Профиль
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),

    # Сброс пароля
    path('password-reset/', views.password_reset, name='password_reset'),
]