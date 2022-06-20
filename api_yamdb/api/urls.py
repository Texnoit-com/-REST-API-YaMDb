from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, TokenView, UserRegView,
                    UsersViewSet)

router1 = routers.DefaultRouter()
router1.register('users', UsersViewSet, basename='users')
router1.register('titles', TitleViewSet, basename='title')
router1.register('categories', CategoryViewSet, basename='category')
router1.register('genres', GenreViewSet, basename='genre')
router1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')
router1.register(r'titles/(?P<title_id>\d+)/reviews',
                 ReviewViewSet, basename='reviews')

urlpatterns = [
    path('v1/', include(router1.urls)),
    path('v1/auth/', include([
        path('signup/', UserRegView.as_view()),
        path('token/', TokenView.as_view())
    ])),
    path('token/', TokenObtainPairView.as_view())
]
