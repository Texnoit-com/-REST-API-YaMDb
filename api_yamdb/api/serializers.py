from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from review.models import User


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email', )

    def validate_username(self, data):
        if data['username'] == 'me':
            raise ValidationError('Использовать me в качестве имени запрещено')
        return data

    def validate_exist(self, attrs):

        username = attrs.get('username')
        if_user = User.objects.filter(username=username)
        if if_user.exists():
            raise ValidationError('Пользователь с таким именем уже существует')

        email = attrs.get('email')
        if_email = User.objects.filter(email=email)
        if if_email.exists():
            raise ValidationError('Почта уже использовалась')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_role(self, attrs):
        user = get_object_or_404(User, id=id)
        if user.role == 'user' and 'role' in attrs and not user.is_superuser:
            attrs['role'] = 'user'
        return super().validate(attrs)


class CategorySerializer(serializers.ModelSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    pass


class ReviewSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    pass
