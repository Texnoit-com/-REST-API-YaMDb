from django.core.exceptions import ValidationError


def validate_user(value):
    """Проверка поля username."""
    if value == 'me':
        raise ValidationError('Использовать имя me запрещено.')
