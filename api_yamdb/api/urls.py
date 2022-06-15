from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UsersViewSet,
                    ConfCodeView, TokenView)

router = routers.DefaultRouter()
router.register('users', UsersViewSet, basename='users')
router.register('titles', TitleViewSet, basename='title')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='review')

urlpatterns = [
    path('v1/auth/signup/', ConfCodeView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
    path('v1/', include(router.urls)),
]
