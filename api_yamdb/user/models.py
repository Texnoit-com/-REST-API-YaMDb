from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_user

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

USER_ROLE = (
    (USER, 'user'),
    (MODERATOR, 'moderator'),
    (ADMIN, 'admin'),
)


class User(AbstractUser):
    username = models.CharField(max_length=100,
                                verbose_name='Логин',
                                help_text='Укажите логин',
                                unique=True,
                                validators=[validate_user])
    email = models.EmailField(max_length=100,
                              verbose_name='Email',
                              help_text='Укажите email',
                              unique=True,
                              null=False)
    confirmation_code = models.CharField(max_length=40,
                                         blank=True,
                                         verbose_name='Проверочный код')
    first_name = models.CharField(max_length=100,
                                  verbose_name='Имя',
                                  help_text='Укажите Имя',
                                  blank=True)
    last_name = models.CharField(max_length=100,
                                 verbose_name='Фамилия',
                                 help_text='Укажите Фамилию',
                                 blank=True)
    bio = models.TextField(max_length=1000,
                           verbose_name='Биография',
                           help_text='Укажите Биографию',
                           blank=True,)
    role = models.CharField(max_length=100,
                            verbose_name='Роль',
                            choices=USER_ROLE,
                            default=USER,
                            help_text='Роль пользователя')

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_staff or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
