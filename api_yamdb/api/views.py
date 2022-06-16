from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from api_yamdb.settings import ADMIN_EMAIL
from rest_framework import viewsets, permissions, status, filters
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from review.models import Category, Genre, Review, Title, User
from ..review.filters import TitleFilterSet
from .serializers import (CommentSerializer, ReviewSerializer,
                          CategorySerializer, GenreSerializer,
                          TitleSerializer, TitleCreateSerialaizer)
from .permissions import IsAdminPermission
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
User = get_user_model()


class CreateDeleteListViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pass

class CategoryViewSet(CreateDeleteListViewSet):
    """Вьюсет для категорий."""

    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, pk=review_id, title__pk=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        new_review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=new_review)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого комментария запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if not (instance.author == self.request.user
                or self.request.user.is_moderator):
            raise PermissionDenied('Удаление чужого комментария запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)


class GenreViewSet(CreateDeleteListViewSet):
    """Вьюсет для жанров."""

    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого отзыва запрещено!')
        super(ReviewViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if not (instance.author == self.request.user
                or self.request.user.is_moderator):
            raise PermissionDenied('Удаление чужого отзыва запрещено!')
        super(ReviewViewSet, self).perform_destroy(instance)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для заголовков."""

    queryset = Title.objects.all().annotate(
        Avg('reviews__score')
    ).order_by('name')
    serializer_class = TitleSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    pagination_class = PageNumberPagination
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateSerialaizer
        return TitleSerializer


class ConfCodeView(APIView):
    """
    При получении POST-запроса с email и username отправляет
    письмо с confirmation_code на email.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email = serializer.validated_data.get('email')
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения регистрации',
            message='Вы зарегистрировались на YAMDB!'
                    f'Ваш код подтвержения: {confirmation_code}',
            from_email=ADMIN_EMAIL,
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
