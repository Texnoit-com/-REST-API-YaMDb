from api_yamdb.settings import EMPTY
from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User

admin.site.register(User)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year',
                    'description', 'category')
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = EMPTY


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author',
                    'score', 'pub_date', 'title')
    search_fields = ('text',)
    list_filter = ('author',)
    empty_value_display = EMPTY


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author',
                    'pub_date', 'review')
    search_fields = ('text',)
    list_filter = ('author',)
    empty_value_display = EMPTY
