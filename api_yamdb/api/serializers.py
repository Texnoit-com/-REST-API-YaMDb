from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from review.models import Category, Comment, Genre, Review, Title, User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров"""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)

    def validate(self, data):
        if self.context.get('request').method != 'POST':
            return data
        reviewer = self.context.get('request').user
        title_id = self.context['view'].kwargs['title_id']
        if Review.objects.filter(author=reviewer, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Оставлять отзыв на одно произведение дважды запрещено!'
            )
        return data

    def check_score(self, value):
        if value in range(1, 11):
            return value
        raise serializers.ValidationError('Вне диапазона 0-10.')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для заголовков"""
    genre = GenreSerializer(
        many=True,
        required=True,
    )
    category = CategorySerializer(required=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre',
            'category',
        )


class TitleCreateSerialaizer(serializers.ModelSerializer):
    """Сериализатор для создания заголовков"""
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
        required=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True,
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
        read_only_fields = ('genre', 'category', )

        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year', 'category',)
            )
        ]


class UsersSerializer(serializers.ModelSerializer):
    pass
