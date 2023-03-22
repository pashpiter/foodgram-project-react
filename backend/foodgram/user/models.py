from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    USER_ROLE = 'user'
    MODERATOR_ROLE = 'moderator'
    ADMIN_ROLE = 'admin'

    CHOICES_ROLE = (
        (USER_ROLE, 'user'),
        (MODERATOR_ROLE, 'moderator'),
        (ADMIN_ROLE, 'admin')
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(UnicodeUsernameValidator(),),
        verbose_name='Уникальный юзернейм'
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        help_text='Например: Василий',
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        help_text='Например: Теркин',
        verbose_name='Фамилия'
    )
    role = models.CharField(
        'Роль',
        max_length=16,
        choices=CHOICES_ROLE,
        default=USER_ROLE,
        blank=True,
        null=True
    )
    password = models.CharField(
        'Пароль',
        max_length=255,
        blank=True,
        null=True
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN_ROLE

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR_ROLE

    @property
    def is_user(self):
        return self.role == self.USER_ROLE

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}'


class Subscribe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='author',
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
    )
    subscriber = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name='Сабскрайбер',
        on_delete=models.CASCADE,
    )
