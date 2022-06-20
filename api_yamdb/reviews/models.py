from api_yamdb.settings import LEN_OUTPUT
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from user.models import User


class Genre(models.Model):
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
    name = models.CharField(max_length=100,
                            verbose_name='Произведение',
                            help_text='Укажите название произведения')
    year = models.PositiveSmallIntegerField(
        db_index=True,
        verbose_name='Дата выхода произведения',
        help_text='Укажите дату выхода',
        validators=(MinValueValidator(0),
                    MaxValueValidator(timezone.now().year)))

    description = models.CharField(max_length=1000,
                                   verbose_name='Произведение',
                                   help_text='Укажите название произведения',
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
    author = models.ForeignKey(User,
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
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title'
            )
        ]

    def __str__(self):
        return self.text[:LEN_OUTPUT]


class Comment(models.Model):
    review = models.ForeignKey('Review',
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Комментарий к отзыву')
    text = models.TextField(max_length=1000,
                            verbose_name='Комментарий',
                            help_text='Укажите комментарий')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор комментария')
    pub_date = models.DateTimeField(verbose_name='Дата публикации',
                                    auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:LEN_OUTPUT]
