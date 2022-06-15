import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


USER_ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    username = models.CharField(max_length=100,
                                verbose_name='Логин',
                                help_text='Укажите логин',
                                unique=True)
    email = models.EmailField(max_length=100,
                              verbose_name='Email',
                              help_text='Укажите email',
                              unique=True,
                              blank=False,
                              null=False)
    confirmation_code = models.CharField(max_length=40,
                                         null=True,
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
                            default='user',
                            help_text='Роль пользователя')

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.is_staff or self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Genre (models.Model):
    "Модель для жанра"
    name = models.CharField(max_length=100,
                            verbose_name='Жанр',
                            help_text='Укажите жанр',
                            unique=True)
    slug = models.SlugField(verbose_name='Адрес',
                            help_text='Укажите адрес',
                            unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    "Модель для категории"
    name = models.CharField(max_length=100,
                            verbose_name='Жанр',
                            help_text='Укажите жанр',
                            unique=True)
    slug = models.SlugField(verbose_name='Адрес',
                            help_text='Укажите адрес',
                            unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    "Модель для заголовка"
    name = models.CharField(max_length=100,
                            verbose_name='Произведение',
                            help_text='Укажите название произведения')
    year = models.PositiveSmallIntegerField(
        db_index=True,
        verbose_name='Дата выхода произведения',
        help_text='Укажите дату выхода',
        validators=(MinValueValidator(0),
                    MaxValueValidator(datetime.date.today().year)))

    description = models.CharField(max_length=1000,
                                   verbose_name='Произведение',
                                   help_text='Укажите название произведения',
                                   null=True,
                                   blank=True,)
    genre = models.ManyToManyField('Genre',
                                   related_name='titles',
                                   verbose_name='Жанры произведения',
                                   help_text='Укажите жaнры')
    category = models.ForeignKey('Category',
                                 related_name='titles',
                                 verbose_name='Категория произведения',
                                 help_text='Укажите категорию',
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year',)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey('Title',
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Отзыв по произведению',
                              help_text='Укажите произведение')
    text = models.TextField(max_length=1000,
                            verbose_name='Отзыв',
                            help_text='Напишите Отзыв')
    author = models.ForeignKey('User',
                               on_delete=models.CASCADE,
                               related_name='reviews',
                               verbose_name='Автор отзыва')
    score = models.IntegerField(verbose_name='Оценка произведения',
                                help_text='Укажите рейтинг',
                                validators=(MinValueValidator(1),
                                            MaxValueValidator(10)))
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    help_text='Укажите дату',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[0:100]


class Comment(models.Model):
    review = models.ForeignKey('Review',
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Комментарий к отзыву')
    text = models.TextField(max_length=1000,
                            verbose_name='Комментарий',
                            help_text='Укажите комментарий')
    author = models.ForeignKey('User',
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор комментария')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:100]
