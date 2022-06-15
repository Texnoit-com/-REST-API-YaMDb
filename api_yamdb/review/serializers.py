from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, USER_ROLE


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email', )

    def validate(self, data):
        if data['username'] == 'me':
            raise ValidationError('Использовать me в качестве имени запрещено')
        return data


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=100)
    confirmation_code = serializers.CharField(required=True, max_length=9)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
            'token')

    def get_token(self, obj):
        user = get_object_or_404(
            User,
            username=self.initial_data.get('username')
        )
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class UsersSerializer(serializers.ModelSerializer):

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

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        check_user = User.objects.filter(username=username)
        check_email = User.objects.filter(email=email)
        if check_user.exists():
            raise ValidationError('Пользователь с таким именем уже существует')
        if check_email.exists():
            raise ValidationError('Почта уже использовалась')

        role = attrs.get('role')
        flag = True
        if role:
            flag = False
            for i in range(3):
                if USER_ROLE[i][0] == role:
                    flag = True
        if not flag:
            raise ValidationError('Неправильная роль')

        user = get_object_or_404(User, id=id)
        if user.role == 'user' and 'role' in attrs and not user.is_superuser:
            attrs['role'] = 'user'
        return super().validate(attrs)
