from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

from review.models import User
from .serializers import (SignUpSerializer, TokenSerializer, UserSerializer)
from .permissions import IsAdminPermission


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class CommentViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass


class ConfCodeView(APIView):
    """
    При получении POST-запроса с email и username отправляет
    письмо с confirmation_code на email.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения регистрации',
            message='Вы зарегистрировались на YAMDB!'
                    f'Ваш код подтвержения: {confirmation_code}',
            from_email=settings.ADMIN_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenView(APIView):
    """
    При получении POST-запроса с username и confirmation_code
    возвращает JWT-токен.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if ('username' not in request.data
                or 'confirmation_code' not in request.data):
            return Response(request.data, status=status.HTTP_400_BAD_REQUEST)
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            username=request.data.get('username')
        )
        confirmation_code = request.data.get('confirmation_code')
        if user.confirmation_code != confirmation_code:
            return Response(
                'Неверный код подтверждения',
                status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return Response({'token': token}, status=status.HTTP_201_CREATED)


class UsersViewSet(viewsets.ModelViewSet):
    """
    Управление пользователями:
    - получение списка всех пользователей
    - добавление пользователя
    - получение пользователя по username
    - изменение данных пользователя по username
    - удаление пользователя по username
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminPermission,)
    filter_backends = (filters.SearchFilter, )
    filterset_fields = ('=username',)
    lookup_url_kwarg = 'username'
    lookup_field = 'username'
    search_fields = ('username', 'email', 'role', 'bio', )

    @action(detail=False,
            url_path='me',
            methods=['get', 'patch'],
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            custom_user = get_object_or_404(
                User, username=request.user
            )
            serializer = self.get_serializer(custom_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
