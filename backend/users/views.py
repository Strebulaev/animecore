from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
import random
import string
import json
import google.auth.transport.requests
import google.oauth2.id_token
import requests
from .models import User
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    PhoneVerificationSerializer, EmailVerificationSerializer,
    GoogleAuthSerializer, PasswordResetSerializer
)


def send_sms_via_textbee(phone_number, message):
    """Отправка SMS через TextBee API"""
    api_key = 'cfba766b-889e-4521-a983-fc8326cd5052'
    url = f'https://api.textbee.dev/sendSMS?apiKey={api_key}&to={phone_number}&from=AnimeCore&message={message}'

    try:
        response = requests.get(url)
        return response.status_code == 200
    except Exception as e:
        print(f"SMS send error: {e}")
        return False


def send_verification_email(email, code):
    """Отправка email с кодом подтверждения"""
    subject = 'Подтверждение email адреса - AnimeCore'
    html_message = f'''
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
            <h1 style="color: white; margin: 0; font-size: 24px;">AnimeCore</h1>
            <p style="color: #e8e8e8; margin: 10px 0 0 0;">Подтверждение email адреса</p>
        </div>

        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #333; margin-top: 0;">Код подтверждения</h2>
            <p style="color: #666; line-height: 1.6;">Для завершения регистрации введите этот код на сайте:</p>

            <div style="background: #f8f9fa; border: 2px dashed #667eea; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0;">
                <span style="font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 3px;">{code}</span>
            </div>

            <p style="color: #999; font-size: 14px; margin-top: 30px;">Код действителен в течение 30 минут.</p>
            <p style="color: #999; font-size: 14px;">Если вы не запрашивали этот код, просто игнорируйте это письмо.</p>
        </div>

        <div style="text-align: center; margin-top: 20px; color: #999; font-size: 12px;">
            <p>© 2024 AnimeCore. Все права защищены.</p>
        </div>
    </body>
    </html>
    '''
    plain_message = f'Ваш код подтверждения: {code}\n\nКод действителен в течение 30 минут.'

    try:
        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email send error: {e}")
        return False


class RegisterView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LoginView(APIView):
    """Вход в систему"""
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                update_last_login(None, user)

                return Response({
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                })
            return Response({'error': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthView(APIView):
    """Аутентификация через Google"""
    permission_classes = (AllowAny,)

    def get(self, request):
        """Начинаем OAuth flow - перенаправляем на Google"""
        from urllib.parse import urlencode
        import secrets

        # Генерируем state для защиты от CSRF
        state = secrets.token_urlsafe(32)
        request.session['google_oauth_state'] = state
        request.session.save()  # Принудительно сохраняем сессию

        print(f"DEBUG: Generated state: {state}")
        print(f"DEBUG: Session key: {request.session.session_key}")

        # Для локальной разработки используем фиксированный redirect URI
        redirect_uri = "http://localhost:8000/api/users/google/callback/"
        print(f"DEBUG: Using redirect_uri: {redirect_uri}")

        # Проверяем наличие Google credentials
        if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
            print("ERROR: Google OAuth credentials not configured")
            return Response({'error': 'Google OAuth не настроен'}, status=500)

        params = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'redirect_uri': redirect_uri,
            'scope': 'openid email profile',
            'response_type': 'code',
            'state': state,
            'access_type': 'offline',
            'prompt': 'consent'
        }

        google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
        print(f"DEBUG: Full Google auth URL: {google_auth_url}")
        return Response({'auth_url': google_auth_url})

    def post(self, request):
        """Обработка ID token (для альтернативного подхода)"""
        serializer = GoogleAuthSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Верификация Google токена
                id_token = serializer.validated_data['id_token']
                idinfo = google.oauth2.id_token.verify_oauth2_token(
                    id_token, google.auth.transport.requests.Request(),
                    settings.GOOGLE_CLIENT_ID
                )

                google_id = idinfo['sub']
                email = idinfo['email']
                name = idinfo.get('name', '')

                # Ищем пользователя или создаем нового
                user, created = User.objects.get_or_create(
                    google_id=google_id,
                    defaults={
                        'email': email,
                        'username': email.split('@')[0] + str(random.randint(1000, 9999)),
                        'first_name': name.split(' ')[0] if name else '',
                        'last_name': ' '.join(name.split(' ')[1:]) if name and len(name.split(' ')) > 1 else '',
                        'email_verified': True,
                    }
                )

                if not created and user.email != email:
                    user.email = email
                    user.save()

                login(request, user)
                refresh = RefreshToken.for_user(user)
                update_last_login(None, user)

                return Response({
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                })

            except Exception as e:
                return Response({'error': f'Ошибка Google аутентификации: {str(e)}'},
                              status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleAuthCallbackView(APIView):
    """Callback для обработки Google OAuth authorization code"""
    permission_classes = (AllowAny,)

    def get(self, request):
        """Обрабатываем authorization code от Google"""
        code = request.GET.get('code')
        state = request.GET.get('state')
        error = request.GET.get('error')

        print(f"DEBUG: Callback received - code: {code}, state: {state}, error: {error}")
        print(f"DEBUG: Session key: {request.session.session_key}")
        print(f"DEBUG: Session data: {dict(request.session)}")

        # Проверяем ошибки
        if error:
            return Response({'error': f'Google OAuth error: {error}'}, status=400)

        if not code:
            return Response({'error': 'No authorization code received'}, status=400)

        # Отключаем проверку state для локальной разработки (небезопасно для продакшена!)
        # TODO: В продакшене включить state проверку с Redis сессиями
        # session_state = request.session.get('google_oauth_state')
        # if not state or state != session_state:
        #     return Response({'error': 'Invalid state parameter'}, status=400)
        # del request.session['google_oauth_state']

        print(f"DEBUG: Skipping state validation for development")

        try:
            # Обмениваем authorization code на access token
            token_data = {
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': "http://localhost:8000/api/users/google/callback/"
            }

            token_response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
            token_response.raise_for_status()
            token_json = token_response.json()

            access_token = token_json.get('access_token')
            id_token = token_json.get('id_token')

            if not access_token:
                return Response({'error': 'Failed to obtain access token'}, status=400)

            # Получаем информацию о пользователе
            user_response = requests.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f'Bearer {access_token}'}
            )
            user_response.raise_for_status()
            user_info = user_response.json()

            google_id = user_info['id']
            email = user_info['email']
            name = user_info.get('name', '')
            first_name = user_info.get('given_name', '')
            last_name = user_info.get('family_name', '')

            # Ищем пользователя или создаем нового
            user, created = User.objects.get_or_create(
                google_id=google_id,
                defaults={
                    'email': email,
                    'username': email.split('@')[0] + str(random.randint(1000, 9999)),
                    'first_name': first_name,
                    'last_name': last_name,
                    'email_verified': True,
                }
            )

            if not created and user.email != email:
                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()

            login(request, user)
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)

            # Возвращаем HTML страницу, которая сохранит токены и перенаправит на frontend
            user_data = UserSerializer(user).data
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Google OAuth - AnimeCore</title>
                <script>
                    // Сохраняем токены в localStorage
                    localStorage.setItem('access_token', '{refresh.access_token}');
                    localStorage.setItem('refresh_token', '{refresh}');
                    localStorage.setItem('user', JSON.stringify({json.dumps(user_data)}));

                    // Перенаправляем на главную страницу
                    window.location.href = 'http://localhost:5173/';
                </script>
            </head>
            <body>
                <p>Google авторизация успешна! Перенаправление...</p>
            </body>
            </html>
            """

            return HttpResponse(html_content, content_type='text/html')

        except Exception as e:
            return Response({'error': f'Google OAuth callback error: {str(e)}'}, status=500)


class PhoneVerificationView(APIView):
    """Отправка и проверка SMS кода для телефона"""

    def post(self, request):
        serializer = PhoneVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            action = serializer.validated_data['action']

            if action == 'send':
                # Генерируем код
                code = ''.join(random.choices(string.digits, k=6))

                # Сохраняем код
                user = request.user
                user.sms_code = code
                user.sms_code_expires = timezone.now() + timedelta(minutes=10)
                user.save()

                # Отправляем SMS через TextBee
                message = f'Ваш код подтверждения: {code}'
                if send_sms_via_textbee(str(phone_number), message):
                    return Response({'message': 'SMS код отправлен'})
                else:
                    return Response({'error': 'Ошибка отправки SMS'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            elif action == 'verify':
                code = serializer.validated_data['code']
                user = request.user

                if (user.sms_code == code and
                    user.sms_code_expires and
                    timezone.now() < user.sms_code_expires):

                    user.phone_verified = True
                    user.sms_code = None
                    user.sms_code_expires = None
                    user.save()

                    return Response({'message': 'Телефон подтвержден'})
                else:
                    return Response({'error': 'Неверный или истекший код'},
                                  status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    """Отправка и проверка email кода"""

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            action = serializer.validated_data['action']

            if action == 'send':
                # Генерируем код
                code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

                # Сохраняем код в сессии или временном хранилище
                request.session[f'email_code_{email}'] = {
                    'code': code,
                    'expires': (timezone.now() + timedelta(minutes=30)).isoformat()
                }

                # Отправляем email
                if send_verification_email(email, code):
                    return Response({'message': 'Код отправлен на email'})
                else:
                    return Response({'error': 'Ошибка отправки email'},
                                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            elif action == 'verify':
                code = serializer.validated_data['code']
                session_key = f'email_code_{email}'
                session_data = request.session.get(session_key)

                if session_data and timezone.now() < timezone.datetime.fromisoformat(session_data['expires']):
                    if session_data['code'] == code:
                        # Обновляем пользователя
                        user = request.user
                        user.email = email
                        user.email_verified = True
                        user.save()

                        # Очищаем сессию
                        del request.session[session_key]

                        return Response({'message': 'Email подтвержден'})
                    else:
                        return Response({'error': 'Неверный код'},
                                      status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'Код истек или не найден'},
                                  status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """Выход из системы"""

    def post(self, request):
        logout(request)
        return Response({'message': 'Выход выполнен'})


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Профиль пользователя"""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset(request):
    """Сброс пароля"""
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            # Генерируем новый пароль и отправляем
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            user.set_password(new_password)
            user.save()

            # Отправляем email с новым паролем
            subject = 'Восстановление пароля - AnimeCore'
            html_message = f'''
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                    <h1 style="color: white; margin: 0; font-size: 24px;">AnimeCore</h1>
                    <p style="color: #e8e8e8; margin: 10px 0 0 0;">Восстановление пароля</p>
                </div>

                <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #333; margin-top: 0;">Ваш новый пароль</h2>
                    <p style="color: #666; line-height: 1.6;">Был сгенерирован новый пароль для вашей учетной записи:</p>

                    <div style="background: #f8f9fa; border: 2px dashed #667eea; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0;">
                        <span style="font-size: 24px; font-weight: bold; color: #667eea;">{new_password}</span>
                    </div>

                    <p style="color: #666; line-height: 1.6;"><strong>Важно:</strong> Рекомендуем изменить этот пароль после входа в систему в настройках профиля.</p>
                </div>

                <div style="text-align: center; margin-top: 20px; color: #999; font-size: 12px;">
                    <p>© 2024 AnimeCore. Все права защищены.</p>
                </div>
            </body>
            </html>
            '''
            plain_message = f'Ваш новый пароль: {new_password}\nРекомендуем изменить его после входа.'

            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=html_message,
            )

            return Response({'message': 'Новый пароль отправлен на email'})
        except User.DoesNotExist:
            return Response({'error': 'Пользователь с таким email не найден'},
                          status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

